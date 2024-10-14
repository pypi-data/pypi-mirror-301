# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

import re
import urllib3
import requests
import xml.etree.ElementTree as ET

from typing import List
from aac_init.log_utils import setup_logger, netmiko_session_logger
from netmiko import ConnectHandler
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def log_message(logger, level, msg):
    if level.lower() == 'debug':
        logger.debug(msg)
    elif level.lower() == 'info':
        logger.info(msg)
    elif level.lower() == 'warning':
        logger.warning(msg)
    elif level.lower() == 'error':
        logger.error(msg)
    elif level.lower() == 'critical':
        logger.critical(msg)
    else:
        logger.error(f"Unknown log level: {level} || {msg}")


def exec_step_chain(connection, step_chain, default_read_timeout=120, logger=None):
    for item in step_chain:
        start_log = item.get("start_log")
        if start_log and logger:
            log_message(logger, start_log.get("level"), start_log.get("msg"))

        read_timeout = item.get("read_timeout")
        if read_timeout is None:
            read_timeout = default_read_timeout

        connection.send_command(
            item.get("command"),
            item.get("expect"),
            read_timeout=read_timeout
        )

        end_log = item.get('end_log')
        if end_log and logger:
            log_message(logger, end_log.get("level"), end_log.get("msg"))


class APIC_CIMC_Tool:
    """APIC CIMC Toolkits, include API and SSH."""

    def __init__(self, global_policies: dict, apic_cimc_connection: dict):
        for k, v in global_policies.items():
            v = str(v) if isinstance(v, int) else v
            setattr(self, k, v)
        for k, v in apic_cimc_connection.items():
            v = str(v) if isinstance(v, int) else v
            setattr(self, k, v)
        self.logger = setup_logger(f"apiccimctool_{self.hostname}.log")
        self.device_ssh = {
            "host": self.cimc_address,
            "username": self.apic_cimc_username,
            "password": self.apic_cimc_password,
            "fast_cli": False,  # Disable fast CLI to mimic human-like sending
            "session_log": netmiko_session_logger(
                f"ssh_session_{self.hostname}_cimc.log"
            ),
        }
        self.token = None
        self.ssh_connection = None
        self.apic_workflow = (
            0  # APIC validate, api_install, ssh_install workflow protection
        )
        self.errors: List[str] = []

        self.logger.debug("APIC CIMC tool initialized successfully.")

    def _api_base_request(self, data):
        """Send POST request to the CIMC API."""

        try:
            cimc_url = f"https://{self.cimc_address}/nuova"
            headers = {
                "accept": "*/*",
                "Content-Type": "text/html",
            }

            response = requests.post(
                url=cimc_url, headers=headers, data=data, verify=False
            )

            if response.status_code == 200:
                return response
            else:
                msg = f"CIMC API request failed with status code {response.status_code}. Data sent: {data}"
                self.logger.error(msg)
                return None

        except Exception as e:
            msg = f"Exception occurred during CIMC API request. Error: {str(e)}, Data: {data}"
            self.logger.error(msg)
            return False

    def _api_login(self):
        """Login CIMC API and retrieve authentication token."""
        try:
            data = (
                f"<aaaLogin inName='{self.apic_cimc_username}' "
                f"inPassword='{self.apic_cimc_password}'>"
                f"</aaaLogin>"
            )

            for i in range(1, 4):
                response = self._api_base_request(data)
                if response:
                    self.token = ET.fromstring(response.text).attrib.get("outCookie")

                    if self.token:
                        self.logger.debug(
                            f"Login successfully to CIMC '{self.cimc_address}' via API. Token: {self.token}"
                        )
                        return self.token
                    else:
                        msg = f"Login failed to CIMC '{self.cimc_address}' via API: No token received. Retry = {i}"
                        self.logger.error(msg)
                        self.errors.append(msg)
                else:
                    msg = f"Login request to CIMC '{self.cimc_address}' failed: No response. Retry = {i}"
                    self.logger.error(msg)
                    self.errors.append(msg)
                time.sleep(3)

        except Exception as e:
            msg = f"Exception occurred during CIMC login for '{self.cimc_address}': {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)

        return None

    def _api_logout(self):
        try:
            data = (
                f"<aaaLogout cookie='{self.token}' inCookie='{self.token}'></aaaLogout>"
            )
            response = self._api_base_request(data)
            if response:
                self.logger.debug(
                    f"Successfully logged out from CIMC '{self.cimc_address}' with token {self.token}."
                )
                return True
            else:
                msg = f"Logout request to CIMC '{self.cimc_address}' failed!"
                self.logger.error(msg)
        except Exception as e:
            msg = f"Exception occurred during CIMC logout for '{self.cimc_address}': {str(e)}"
            self.logger.error(msg)

        return False

    def _api_health_check(self):
        """
        Perform health check on the CIMC by retrieving and logging key system information.
        """
        try:
            firmware_data = f"""
            <!-- Request firmware version -->
            <configResolveDn cookie="{self.token}" inHierarchical='false'
            dn="sys/rack-unit-1/mgmt/fw-system"/>
            """
            firmware_response = self._api_base_request(firmware_data)

            if firmware_response:
                firmware_version = (
                    ET.fromstring(firmware_response.text)
                    .find(".//firmwareRunning")
                    .attrib["version"]
                )
                self.logger.debug(f"Current Firmware version: {firmware_version}")
            else:
                self.logger.error(
                    f"Failed to retrieve firmware version from CIMC {self.cimc_address}."
                )
                return False

            # Retrieve fault information
            fault_data = f"""
            <!-- Request fault information -->
            <configResolveClass cookie="{self.token}" inHierarchical='false' classId='faultInst'/>
            """
            self.logger.debug(
                f"Retrieving fault information for CIMC {self.cimc_address}:"
            )
            fault_response = self._api_base_request(fault_data)

            if fault_response:
                self.logger.debug(f"Fault information: {fault_response.text}")
            else:
                self.logger.error(
                    f"Failed to retrieve fault information from CIMC {self.cimc_address}."
                )
                return False

            # Retrieve TPM status
            tpm_data = f"""
            <!-- Request TPM status -->
            <configResolveClass cookie="{self.token}" inHierarchical='false' classId='equipmentTpm'/>
            """
            tpm_response = self._api_base_request(tpm_data)

            if tpm_response:
                tpm_status = (
                    ET.fromstring(tpm_response.text)
                    .find(".//equipmentTpm")
                    .attrib["enabledStatus"]
                )
                self.logger.debug(f"Current TPM status: {tpm_status}")
            else:
                self.logger.error(
                    f"Failed to retrieve TPM status from CIMC {self.cimc_address}."
                )
                return False

            # Check if TPM is enabled
            if "enable" not in tpm_status:
                self.logger.error(f"CIMC {self.cimc_address}: TPM is not enabled!")
                return False

            return True

        except Exception as e:
            # Log any exceptions that occur during the health check
            msg = f"Exception occurred during CIMC health check for {self.cimc_address}: {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

    def _api_clear_mapping(self):
        """Clear existing CIMC virtual media mappings and boot order."""

        try:
            # Retrieve current CIMC media mappings
            cimc_mapping_data = f"""
            <!-- Request CIMC media mappings -->
            <configResolveClass cookie="{self.token}" inHierarchical='false' classId='commVMediaMap'/>
            """
            cimc_mapping_response = self._api_base_request(cimc_mapping_data)

            # Check if a virtual media mapping exists and remove it
            if cimc_mapping_response and re.search(
                r"commVMediaMap volumeName", cimc_mapping_response.text
            ):
                existing_mapping = (
                    ET.fromstring(cimc_mapping_response.text)
                    .find(".//commVMediaMap")
                    .attrib["volumeName"]
                )
                self.logger.debug(
                    f"Found existing virtual media mapping: {existing_mapping}. Removing it."
                )

                # Clear the existing virtual media mapping
                cimc_mapping_clear_data = f"""
                <!-- Clear CIMC media mapping -->
                <configConfMo cookie="{self.token}">
                    <inConfig>
                        <commVMediaMap
                        dn="sys/svc-ext/vmedia-svc/vmmap-{existing_mapping}"
                        volumeName="{existing_mapping}" status='removed'/>
                    </inConfig>
                </configConfMo>
                """
                cimc_mapping_clear_response = self._api_base_request(
                    cimc_mapping_clear_data
                )

                if cimc_mapping_clear_response:
                    self.logger.debug(
                        f"Successfully removed virtual media mapping: {existing_mapping}."
                    )
                else:
                    self.logger.error(
                        f"Failed to remove virtual media mapping: {existing_mapping}."
                    )
                    return False
            else:
                self.logger.debug("No existing virtual media mapping found.")

            # Retrieve current CIMC boot order
            cimc_boot_data = f"""
            <!-- Request CIMC boot order -->
            <configResolveClass cookie="{self.token}" inHierarchical='false' classId='lsbootVMedia'/>
            """
            cimc_boot_data_response = self._api_base_request(cimc_boot_data)

            # Check if a boot order exists and remove it
            if cimc_boot_data_response and re.search(
                r"lsbootVMedia name", cimc_boot_data_response.text
            ):
                existing_bootorder = (
                    ET.fromstring(cimc_boot_data_response.text)
                    .find(".//lsbootVMedia")
                    .attrib["name"]
                )
                self.logger.debug(
                    f"Found existing boot order: {existing_bootorder}. Removing it."
                )

                # Clear the existing boot order
                cimc_bootorder_clear_data = f"""
                <!-- Clear CIMC boot order -->
                <configConfMo cookie="{self.token}">
                    <inConfig>
                        <lsbootVMedia
                        dn="sys/rack-unit-1/boot-precision/vm-{existing_bootorder}"
                        name="{existing_bootorder}" status='removed'/>
                    </inConfig>
                </configConfMo>
                """
                cimc_bootorder_clear_response = self._api_base_request(
                    cimc_bootorder_clear_data
                )

                if cimc_bootorder_clear_response:
                    self.logger.debug(
                        f"Successfully removed boot order: {existing_bootorder}."
                    )
                else:
                    self.logger.error(
                        f"Failed to remove boot order: {existing_bootorder}."
                    )
                    return False
            else:
                self.logger.debug("No existing boot order found.")

            return True

        except Exception as e:
            # Log any exceptions that occur during the clearing process
            msg = f"Exception occurred during CIMC mapping/boot order clear for {self.cimc_address}: {str(e)}"
            self.logger.error(msg)
            return False

    def _api_power_on_cimc(self):
        """Power on CIMC."""
        try:
            cimc_power_on_data = f"""
            <!-- Request to power on CIMC -->
            <configConfMo cookie="{self.token}">
                <inConfig>
                    <computeRackUnit dn="sys/rack-unit-1" adminPower="up"/>
                </inConfig>
            </configConfMo>
            """

            cimc_power_on_response = self._api_base_request(cimc_power_on_data)

            if cimc_power_on_response:
                self.logger.debug(
                    f"CIMC '{self.cimc_address}' has been successfully powered on."
                )
                return True
            else:
                self.logger.error(f"Failed to power on CIMC {self.cimc_address}.")

        except Exception as e:
            # Log any exceptions that occur during the power on process
            msg = f"Exception occurred while powering on CIMC '{self.cimc_address}': {str(e)}"
            self.logger.error(msg)

        return False

    def _api_power_down_cimc(self):
        """Power down CIMC."""
        try:
            cimc_power_down_data = f"""
            <!-- Request to power down CIMC -->
            <configConfMo cookie="{self.token}">
                <inConfig>
                    <computeRackUnit dn="sys/rack-unit-1" adminPower="down" />
                </inConfig>
            </configConfMo>
            """

            cimc_power_down_response = self._api_base_request(cimc_power_down_data)

            if cimc_power_down_response:
                self.logger.debug(
                    f"CIMC '{self.cimc_address}' has been successfully powered down."
                )
                return True
            else:
                self.logger.error(f"Failed to power down CIMC: {self.cimc_address}!")

        except Exception as e:
            # Log any exceptions that occur during the power down process
            msg = f"Exception occurred while powering down CIMC '{self.cimc_address}': {str(e)}"
            self.logger.error(msg)

        return False

    def _validate_apic_image(self):
        """Validate APIC image"""
        self.logger.debug("Validating APIC image...")
        pattern = r"(?:aci-apic-dk9\.)(\d+\.\d+\.\d+[a-z])\.iso"
        version_match = re.search(pattern, self.apic_image)

        if version_match:
            self.logger.debug(
                f"Validate version: '{version_match.group(1)}' successfully."
            )
            return True
        else:
            self.logger.error(f"Invalid APIC image: {self.apic_image}")
            return False

    def api_validate_apic(self):
        """
        Validate CIMC for APIC installation by performing the following steps:
        1. Validate APIC image.
        2. Login CIMC via SSH.
        3. Login CIMC via API.
        4. Perform CIMC health check.
        5. Clear any existing virtual media mappings.
        6. Power down CIMC.
        """

        self.logger.debug("Validating APIC Image for APIC installation...")
        if not self._validate_apic_image():
            self.logger.error("Validate APIC Image failed.")
            return False

        self.logger.debug("Validating CIMC for APIC installation...")

        if not self._ssh_connect():
            self.logger.error("Validating CIMC failed due to SSH login failed.")
            return False
        else:
            self._ssh_disconnect()

        if not self._api_login():
            self.logger.error("Validating CIMC failed due to API login failed!")
            return False
        try:
            if not self._api_health_check():
                self.logger.error("CIMC health check failed!")
                return False
            self.logger.debug("CIMC health check passed.")

            if not self._api_clear_mapping():
                self.logger.error("CIMC mapping cleanup failed!")
                return False
            self.logger.debug("CIMC mapping cleanup successful.")

            self.logger.debug("Powering down CIMC...")
            if not self._api_power_down_cimc():
                self.logger.error("Failed to power down CIMC.")
                return False

            self.apic_workflow = 1
            self.logger.debug("CIMC for APIC installation validated successfully.")
            return True

        except Exception as e:
            # Log any exceptions that occur during the validation process
            msg = f"Exception occurred during CIMC validation for APIC: {str(e)}"
            self.logger.error(msg)

        finally:
            self._api_logout()

        return False

    def api_install_apic(self):
        """
        Configure installation parameters by performing the following steps:
        1. Login CIMC via API.
        2. Configure following configurations on CIMC:
            - hostname
            - description
            - DNS
            - timezone
            - NTP
            - Serial Over LAN(SOL)
            - CIMC mapping
            - boot order
        3. Power on CIMC.
        """

        # APIC validation is required before api installation
        if self.apic_workflow != 1:
            self.logger.error("APIC Validation is not performed, aborting...")
            return False

        self.logger.debug("Configure APIC installation via CIMC-MAP.")

        # Step 1: Login CIMC via api
        if not self._api_login():
            self.logger.error(
                "Configure APIC installation failed due to API login failed!"
            )
            return False
        try:
            # Define CIMC installation steps
            cimc_install_data = {
                "Configure hostname": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <mgmtIf dn="sys/rack-unit-1/mgmt/if-1" hostname="{self.hostname}"/>
                    </inConfig></configConfMo>
                """,
                "Configure description": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <computeRackUnit dn="sys/rack-unit-1" usrLbl="{self.description}"/>
                    </inConfig></configConfMo>
                """,
                # TODO: Add DNS Server Config
                "Configure timeZone": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <topSystem dn="sys" timeZone="{self.timezone}"/>
                    </inConfig></configConfMo>
                """,
                "Configure NTP": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <commNtpProvider dn="sys/svc-ext/ntp-svc" ntpServer1="{self.ntp_server}"/>
                    </inConfig></configConfMo>
                """,
                "Configure SOL (Serial Over LAN)": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <solIf dn="sys/rack-unit-1/sol-if" adminState="enable" speed="115200"
                            comport="com0" sshPort="2400"/>
                    </inConfig></configConfMo>
                """,
                "Configure CIMC mapping for APIC image": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <commVMediaMap volumeName="aci-automation" map="www"
                                    remoteShare="{self.aci_image_path}" remoteFile="{self.apic_image}"
                                    dn="sys/svc-ext/vmedia-svc/vmmap-aci-automation"/>
                    </inConfig></configConfMo>
                """,
                "Set CIMC boot order to CIMC-map": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <lsbootVMedia dn="sys/rack-unit-1/boot-precision/vm-cimc-map"
                                    name="cimc-map" type="VMEDIA" subtype="cimc-mapped-dvd"
                                    order="1" state="Enabled"/>
                    </inConfig></configConfMo>
                """,
            }

            # Step 2: Execute each configuration step in the CIMC installation process
            for step_name, config_data in cimc_install_data.items():
                cimc_install_response = self._api_base_request(config_data)
                if cimc_install_response:
                    self.logger.debug(f"{step_name} completed successfully.")
                else:
                    self.logger.error(f"{step_name} failed.")
                    return False  # Exit if any step fails

            # Step 3: All steps succeeded, power on CIMC
            self.logger.debug("Powering on CIMC...")
            if not self._api_power_on_cimc():
                self.logger.error("Failed to power on CIMC.")
                return False

            self.apic_workflow = 2
            self.logger.debug(
                "CIMC-MAP configured successfully, start to install APIC..."
            )
            return True

        except Exception as e:
            # Log any exceptions that occur during the installation process
            error_msg = f"Exception occurred during configure CIMC-MAP for {self.cimc_address}: {str(e)}"
            self.logger.error(error_msg)

        finally:
            self._api_logout()

        return False

    def _ssh_connect(self):
        """SSH Connector"""

        DEVICE_TYPES = [
            "linux",
            "generic",
        ]
        for i in range(1, 4):
            for device_type in DEVICE_TYPES:
                try:
                    self.logger.debug(
                        f"Attempting to connect '{self.cimc_address}' with '{device_type}'..."
                    )
                    self.device_ssh["device_type"] = device_type
                    self.ssh_connection = ConnectHandler(**self.device_ssh)
                    self.logger.debug(
                        f"Connected to '{self.cimc_address}': with '{device_type}' successfully!"
                    )
                    return True
                except Exception as e:
                    self.logger.debug(
                        f"Failed to connect to '{self.cimc_address}' with '{device_type}': {e}"
                    )
                    time.sleep(3)

            msg = f"Failed to connect to '{self.cimc_address}' with both methods! Retry = {i}"
            self.logger.warning(msg)
            #self.errors.append(msg)

        msg = f"Failed to connect to '{self.cimc_address}' with both methods after 3 attempts"
        self.logger.error(msg)
        self.errors.append(msg)
        return False

    def _ssh_disconnect(self):
        if self.ssh_connection:
            self.ssh_connection.disconnect()
            self.logger.debug(f"Disconnected SSH connection for: {self.cimc_address}")
            return True
        else:
            self.logger.error(f"No ssh connection found: {self.cimc_address}")
            return False

    def ssh_install_apic(self):
        """Monitor and accelerate APIC installation via CIMC SSH"""

        # API installation is required before ssh installation
        if self.apic_workflow != 2:
            self.logger.error("APIC API installation is not performed, aborting...")
            return False

        self.logger.debug(
            "Start APIC installation monitoring and acceleration via CIMC SSH..."
        )

        if not self._ssh_connect():
            self.logger.error(
                "APIC installation monitoring and acceleration failed due to SSH login failed."
            )
            return False

        iso_url = f"{self.aci_image_path}{self.apic_image}"
        step_chain = [
            {
                "command": "connect host",
                "expect": "To speed up the install, enter iso url",
                "read_timeout": 900,
            },
            {
                "command": iso_url,  # http://10.124.145.88/Images/ACI/4/4.2/aci-apic-dk9.4.2.7f.iso
                "expect": "type static, dhcp, bash for a shell to configure networking",
                "read_timeout": 90,
                "start_log": {
                    "level": "debug",
                    "msg": "Start to speed up APIC installation..."
                }
            },
            {
                "command": "bash",
                "expect": r"bash-4.2#|root@\(none\):/#",
                "read_timeout": 90
            },
        ]

        try:

            # TODO: update with bash config instead of static - need verify later
            exec_step_chain(self.ssh_connection, step_chain, logger=self.logger)
            # ls -l /sys/class/net
            # bash-4.2# ls -l /sys/class/net
            # total 0
            # lrwxrwxrwx. 1 root root 0 Sep 13 05:29 enp11s0 -> ../../devices/pci0000:00/0000:00:03.0/0000:06:00.0/0000:07:01.0/0000:09:00.0/0000:0a:00.0/0000:0b:00.0/net/enp11s0
            # lrwxrwxrwx. 1 root root 0 Sep 13 05:29 enp12s0 -> ../../devices/pci0000:00/0000:00:03.0/0000:06:00.0/0000:07:01.0/0000:09:00.0/0000:0a:01.0/0000:0c:00.0/net/enp12s0
            # lrwxrwxrwx. 1 root root 0 Sep 13 05:29 enp1s0f0 -> ../../devices/pci0000:00/0000:00:01.0/0000:01:00.0/net/enp1s0f0
            # lrwxrwxrwx. 1 root root 0 Sep 13 05:29 enp1s0f1 -> ../../devices/pci0000:00/0000:00:01.0/0000:01:00.1/net/enp1s0f1
            # lrwxrwxrwx. 1 root root 0 Sep 13 05:29 lo -> ../../devices/virtual/net/lo
            interfaces = self.ssh_connection.send_command_timing(
                "ls -l /sys/class/net",
                read_timeout=30,
            )
            oob_interface = "eno1" if "/net/eno1" in interfaces else "enp1s0f0"
            self.logger.debug(f"Configure interface: {oob_interface}")
            # + ip addr add 10.124.145.33/24 dev enp1s0f0
            # + ip link set enp1s0f0 up
            # + ip route add default via 10.124.145.1
            bash_cmd = [
                f"ip addr add {self.apic_address}/{self.apic_netmask} dev {oob_interface}",
                f"ip link set {oob_interface} up",
                f"ip route add default via {self.apic_gateway}",
            ]
            # bash-4.2# ip addr add 10.124.145.33/24 dev enp1s0f0
            # bash-4.2# ip link set enp1s0f0 up
            # bash-4.2# ip route add default via 10.124.145.1
            # bash-4.2# exit
            # exit
            # + echo 'Bash shell done, resuming install'
            # Bash shell done, resuming install
            # ++ seq 1 2
            # + for count in '$(seq 1 2)'
            # + ping -c 1 10.124.145.88
            # PING 10.124.145.88 (10.124.145.88) 56(84) bytes of data.
            # 64 bytes from 10.124.145.88: icmp_seq=1 ttl=64 time=0.254 ms
            self.ssh_connection.send_multiline_timing(bash_cmd)

            self.logger.debug("Interface configured, waiting for APIC installation...")

            # TODO: need to optimize in later version for apic version 5
            output = self.ssh_connection.send_command(
                "exit",
                r'Enter the artifact URL \(empty if done\):|atomix installation complete|atomix-installer returned 0',
                read_timeout=3600
            )
            if "Enter the artifact URL (empty if done):" in output:
                self.ssh_connection.send_multiline_timing("\n")

                self.ssh_connection.read_until_pattern(
                    pattern="atomix installation complete", read_timeout=3600
                )

            self.ssh_connection.read_until_pattern(
                pattern="reboot: Power down", read_timeout=120
            )

            self.logger.debug("APIC installation successfully.")

            return True

        except Exception as e:
            # Log any exceptions that occur during the installation process
            error_msg = f"Exception occurred during APIC install acceleration for {self.cimc_address}: {str(e)}"
            self.logger.error(error_msg)

        finally:
            self._ssh_disconnect()

        return False

    def ssh_init_apic(self):
        """Configure APIC initial setup parameters via CIMC SSH"""
        # TBD: Enhance more ACI fabric scenarios...

        self.logger.debug("Starting to initial setup APIC via CIMC SSH...")

        apic_config_dict = {
            "Enter the fabric name": self.fabric_name,
            "Enter the fabric ID": self.fabric_id,
            "Enter the number of active controllers in the fabric": self.fabric_active_controllers
            ,
            "Enter the POD ID": self.pod,
            "Is this a standby controller": self.standby_controller,
            "Enter the controller ID": self.id,
            "Enter the controller name": self.hostname,
            "Enter address pool for TEP addresses": self.tep_pool,
            "Enter the VLAN ID for infra network": self.infra_vlan,
            "Enter address pool for BD multicast addresses": self.gipo,
            "Enable IPv6 for Out of Band Mgmt": "N\n",  # Don't support IPv6 at this moment
            "Enter the IPv4 address of the default gateway": self.apic_gateway,
            "Enter the IPv4 address": f"{self.apic_address}/{self.apic_netmask}",            
            "Enter the interface speed": "\n",  # Don't support to change speed at this moment
            "Enable strong passwords": self.strong_password,
            "Enter the password for admin": self.aci_local_password,
            "Reenter the password for admin": self.aci_local_password,
            "Standalone APIC Cluster": "no\n",  # Don't support standalone controller at this moment
            "Welcome to APIC Setup Utility": "\n",
            "Enter the IP Address of default gateway": self.apic_gateway,
            "Enter the IP Address": f"{self.apic_address}/{self.apic_netmask}",
        }

        if not self._api_login():
            msg = "APIC initial setup failed due to API login failed!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        try:
            self.logger.debug("Powering on CIMC...")
            if not self._api_power_on_cimc():
                msg = "Failed to power on CIMC!"
                self.logger.error(msg)
                self.errors.append(msg)
                return False
        except Exception as e:
            # Log any exceptions that occur during the CIMC power on process
            msg = f"Exception occurred during powering on CIMC for {self.cimc_address}: {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)
            return False
        finally:
            self._api_logout()

        if not self._ssh_connect():
            msg = "APIC initial setup failed due to SSH login failed!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        try:
            self.ssh_connection.send_command(
                "connect host",
                "Press any key to continue...",
                read_timeout=900,
            )

            ###### Loop method

            # out_msg = self.ssh_connection.send_command_timing("\n", read_timeout=90)
            out_msg = self.ssh_connection.send_command(
                "\n", "Enter the fabric name", read_timeout=120
            )
            loop = True
            while loop:
                if "Would you like to edit the configuration?" in out_msg:
                    self.ssh_connection.send_command_timing("\n", read_timeout=15)
                    self.logger.debug("Complete APIC initial setup configuration.")
                    loop = False
                else:
                    matched = False
                    for key, value in apic_config_dict.items():
                        if key in out_msg:
                            out_msg = self.ssh_connection.send_command_timing(
                                value, read_timeout=15
                            )
                            matched = True
                            break
                    if not matched:
                        msg = f"APIC setup key/value match error, output msg: {out_msg}"
                        self.logger.error(msg)
                        self.errors.append(msg)
                        return False

            # Post Check
            pattern = r"(?:bootstrap:reboot_setup Setup done during reboot|bootstrap_config: Done|complete the bootstrapping)"
            self.ssh_connection.read_until_pattern(pattern=pattern, read_timeout=600)
            self.logger.debug("APIC initial setup successfully.")

            return True

            ###### Tree method
            # start_msg = self.ssh_connection.send_command_timing("\n", read_timeout=15)
            # # Version 4,5: Enter the fabric name
            # if "Enter the fabric name" in start_msg:
            #     self.ssh_connection.send_command(self.fabric_name, "Enter the fabric ID", read_timeout=15)
            #     self.ssh_connection.send_command(self.fabric_id, "Enter the number of active controllers in the fabric", read_timeout=15)
            #     output = self.ssh_connection.send_command_timing(self.fabric_active_controllers, read_timeout=15)
            #     # Version 4
            #     if "Enter the POD ID" in output:
            #         self.ssh_connection.send_command(self.pod)
            #     # Version 5
            #     elif "Is this a standby controller" in output:
            #         self.ssh_connection.send_command()
            #     # Unknown error
            #     else:
            #         msg = "Unknown popup, aborting..."
            #         self.logger.error(msg)
            #         self.errors.append(msg)
            #         return False

            #     self.ssh_connection.send_command()
            #     self.ssh_connection.send_command()
            #     self.ssh_connection.send_command()

            # # Version 6: Welcome to APIC Setup Utility
            # elif "Welcome to APIC Setup Utility" in start_msg:
            #     self.ssh_connection.send_command("\n", "Enter the password for admin", read_timeout=15)
            #     self.ssh_connection.send_command(self.aci_local_password, "Reenter the password for admin", read_timeout=15)
            #     self.ssh_connection.send_command(self.aci_local_password, "Enter the IP Address", read_timeout=15)
            #     self.ssh_connection.send_command(f"{self.apic_address}/{self.apic_netmask}", "Enter the IP Address of default gateway", read_timeout=15)
            #     self.ssh_connection.send_command(self.apic_gateway,"Would you like to edit the configuration?", read_timeout=15)
            #     self.ssh_connection.send_command_timing("\n")
            #     self.logger.debug("APIC initial configured, waiting for APIC ready...")
            #     self.ssh_connection.read_until_pattern(pattern="complete the bootstrapping", read_timeout=1200)
            #     self.logger.debug("APIC setup successfully.")
            #     return True
            # else:
            #     msg = "Unknown start message!"
            #     self.logger.error(msg)
            #     self.errors.append(msg)
            #     return False

        except Exception as e:
            # Log any exceptions that occur during the APIC initial setup process
            error_msg = f"Exception occurred during APIC initial setup for '{self.cimc_address}': {str(e)}"
            self.logger.error(error_msg)
        finally:
            self._ssh_disconnect()

        return False

    def gen_install_apic(self):
        """
        Complete APIC installation workflow:
        1. Configure installation parameters via CIMC API
        2. Monitor and accelerate APIC installation via CIMC SSH
        """
        self.logger.debug("Start to run APIC installation workflow...")
        if not self.api_install_apic():
            msg = f"APIC {self.hostname} API installation phase failed."
            self.logger.error(msg)
            self.errors.append(msg)
            return False
        self.logger.debug(
            f"APIC '{self.hostname}' API installation phase completed successfully."
        )

        if not self.ssh_install_apic():
            msg = f"APIC {self.hostname} SSH installation phase failed."
            self.logger.error(msg)
            self.errors.append(msg)
            return False
        self.logger.debug(
            f"APIC '{self.hostname}' SSH installation phase completed successfully."
        )

        self.logger.debug("APIC installation workflow has been successfully completed.")
        self.logger.info(
            f"APIC '{self.hostname}' had been successfully installed to '{self.apic_image}'."
        )
        return True

