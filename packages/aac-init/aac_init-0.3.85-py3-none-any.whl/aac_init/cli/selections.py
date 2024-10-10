# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

import os

from typing import Any, Dict, List, Optional
from aac_init.log_utils import setup_logger
from aac_init.conf import settings
from aac_init.tools.file_tools.yaml_tool import load_yaml_files
from ruamel import yaml
from aac_init.tools import (
    Thread_Tool,
    APIC_CIMC_Tool,
    ACI_Switch_Tool,
    APIC_Tool,
    Ansible_Tool,
)
from aac_init.tools.file_tools.yaml_tool import load_yaml_files, YamlWriter


class Selections:
    """
    Handle CLI selections
    """

    def __init__(self, data_path: str, output_path: str):
        self.logger = setup_logger("selections.log")

        self.logger.debug(
            f"Loaded selections with data_path: '{data_path}', "
            f"output_path: '{output_path}'"
        )

        self.data: Optional[Dict[str, Any]] = None
        self.data_path = data_path
        self.output_path = output_path
        self.fabric_mgmt = None
        self.global_policy = None
        self.errors: List[str] = []

        self._load_global_policy()

        if not self.global_policy:
            self.logger.error("Failed to load global policy!")
            exit(1)

        self.logger.debug("Selections initialized successfully!")

    def _load_global_policy(self):
        """Load global policy"""

        self.logger.debug("Loading global policy...")
        for dir, _, files in os.walk(self.data_path):
            for filename in files:
                if filename in settings.DEFAULT_DATA_PATH:
                    self.global_policy_path = os.path.join(dir, filename)
        if self.global_policy_path:
            self.global_policy = load_yaml_files([self.global_policy_path])
            self.logger.debug("'00-global_policy' loaded successfully.")
            return True
        else:
            msg = "'00-global_policy' is missing!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

    def _load_fabric_mgmt(self):
        """Load fabric mgmt"""

        self.logger.debug("Loading fabric mgmt...")
        for dir, _, files in os.walk(self.data_path):
            for filename in files:
                if filename in settings.DEFAULT_FABRIC_MGMT_PATH:
                    self.fabric_mgmt_path = os.path.join(dir, filename)
        if self.fabric_mgmt_path:
            self.fabric_mgmt = load_yaml_files([self.fabric_mgmt_path])
            self.logger.debug("'01-fabric-mgmt' loaded successfully.")
            return True
        else:
            msg = "'01-fabric-mgmt' is missing!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

    def fabric_bootstrap(self):
        """
        Method: 01-fabric_bootstrap
        Description: Wipe and boot APIC/switch to particular version
        """

        self.logger.debug("Start to bootstrap ACI fabric...")

        fabric_policy = self.global_policy.get("fabric", {})
        global_policies = fabric_policy.get("global_policies", {}) or {}
        apic_check = "apic_nodes_connection" in fabric_policy
        aci_switch_check = "switch_nodes_connection" in fabric_policy

        fabric_bootstrap_threads = []

        # Validate APICs if have
        if apic_check:
            apics = fabric_policy.get("apic_nodes_connection", []) or []

            for apic_cimc_connection in apics:
                apic = APIC_CIMC_Tool(global_policies, apic_cimc_connection)
                if not apic.api_validate_apic():
                    msg = f"Validate APIC '{apic.hostname}' failed!"
                    self.logger.error(msg)
                    self.errors.append(msg)
                    return False
                self.logger.info(f"Validate APIC '{apic.hostname}' successfully.")
                thread = Thread_Tool(target=apic.gen_install_apic)
                fabric_bootstrap_threads.append((apic.hostname, thread))

        # Validate ACI switches if have
        if aci_switch_check:
            aci_switches = fabric_policy.get("switch_nodes_connection", []) or []

            # Load fabric mgmt
            if self._load_fabric_mgmt():
                fabric_mgmt_policy_apic = self.fabric_mgmt.get("apic", {}) or {}
                fabric_mgmt_policy_apic_node_policies = (
                    fabric_mgmt_policy_apic.get("node_policies", {}) or {}
                )
                aci_switches_mgmt = (
                    fabric_mgmt_policy_apic_node_policies.get("nodes", []) or []
                )
            else:
                msg = "Unable to load fabric mgmt info!"
                self.logger.error(msg)
                self.errors.append(msg)
                return False

            for aci_switch_connection in aci_switches:
                aci_switch_mgmt = next(
                    (
                        node
                        for node in aci_switches_mgmt
                        if node["id"] == aci_switch_connection["id"]
                    ),
                    {},
                )

                aci_switch = ACI_Switch_Tool(
                    global_policies, aci_switch_connection, aci_switch_mgmt
                )
                if not aci_switch.validate_aci_switch():
                    msg = f"Validate ACI switch '{aci_switch.hostname}' failed!"
                    self.logger.error(msg)
                    self.errors.append(msg)
                    return False
                self.logger.info(
                    f"Validate ACI switch '{aci_switch.hostname}' successfully."
                )
                thread = Thread_Tool(target=aci_switch.install_aci_switch)
                fabric_bootstrap_threads.append((aci_switch.hostname, thread))

        for _, thread in fabric_bootstrap_threads:
            thread.start()

        for _, thread in fabric_bootstrap_threads:
            thread.join()

        install_errors = []
        for hostname, thread in fabric_bootstrap_threads:
            if thread.get_result():
                self.logger.info(f"Install '{hostname}' successfully.")
            else:
                msg = (
                    f"Install '{hostname}' failed. Check APIC/switch logs for details."
                )
                self.logger.error(msg)
                self.errors.append(msg)
                install_errors.append(hostname)

        if install_errors:
            msg = "ACI fabric bootstrap failed, check APIC/switch logs for details."
            self.logger.error(msg)
            self.errors.append(msg)
            return False
        return True

    def apic_init_setup(self):
        """
        Method: 02-apic_init_setup
        Description: APIC initial setup (Single Pod)
        """

        self.logger.debug("Start to initial setup APIC...")

        fabric_policy = self.global_policy.get("fabric", {})
        global_policies = fabric_policy.get("global_policies", {}) or {}
        apic_check = "apic_nodes_connection" in fabric_policy

        # Validate APIC exists
        if apic_check:
            apics = fabric_policy.get("apic_nodes_connection", []) or []

            for apic_cimc_connection in apics:
                apic = APIC_CIMC_Tool(global_policies, apic_cimc_connection)
                if not apic.api_validate_apic():
                    msg = f"Validate APIC CIMC'{apic.hostname}' failed!"
                    self.logger.error(msg)
                    self.errors.append(msg)
                    return False
                self.logger.info(f"Validate APIC CIMC {apic.hostname} successfully.")

            for apic_cimc_connection in apics:
                apic = APIC_CIMC_Tool(global_policies, apic_cimc_connection)
                if not apic.ssh_init_apic():
                    msg = f"Initial setup APIC '{apic.hostname}' failed!"
                    self.logger.error(msg)
                    self.errors.append(msg)
                    return False
                self.logger.info(f"Initial setup APIC {apic.hostname} successfully.")
        else:
            msg = "No APIC found!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        return True

    def _load_aac_data(self):
        """Load global policy and AAC data"""

        self.logger.debug("Loading global policy and AAC data...")

        try:
            global_policy_writer = YamlWriter([settings.DEFAULT_DATA_PATH])
            global_policy_writer.write_3(settings.TEMPLATE_DIR[0], self.output_path)
            self.logger.debug(
                f"Generate AAC working directory: '{self.output_path}' successfully."
            )

            aac_path = os.path.join(
                self.output_path,
                os.path.basename(settings.TEMPLATE_DIR[0]),
                "host_vars",
                "apic1",
            )
            aac_data_path = os.path.join(aac_path, "data.yaml")

            aac_data = load_yaml_files(settings.DATA_PATH)
            self.logger.debug("Load AAC data successfully.")

            with open(aac_data_path, "w") as aac:
                y = yaml.YAML()
                y.default_flow_style = False
                y.dump(aac_data, aac)

            self.logger.debug(
                f"Copy AAC data to working directory: '{self.output_path}' successfully."
            )

            self.aac_inventory_path = os.path.join(
                os.getcwd(),
                self.output_path,
                os.path.basename(settings.TEMPLATE_DIR[0]),
                "inventory.yaml",
            )

            self.logger.debug("Set AAC inventory successfully.")
            return True

        except Exception as e:
            msg = f"Exception occurred during loading AAC data: {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)

        return False

    def apic_nac_config(self):
        """
        Method: 03-apic_nac_config
        Description: Init ACI Fabric via NaC (Network as Code)
        """

        self.logger.debug("Start to configure ACI Fabric via NaC...")

        fabric_policy = self.global_policy.get("fabric", {})
        global_policies = fabric_policy.get("global_policies", {}) or {}
        apic_check = "apic_nodes_connection" in fabric_policy

        # Validate APIC exists
        if apic_check:
            apics = fabric_policy.get("apic_nodes_connection", []) or []
            apic1 = next((apic for apic in apics if apic.get("id") == 1), None)
            if not apic1:
                msg = "No APIC1 found!"
                self.logger.error(msg)
                self.errors.append(msg)
        else:
            msg = "No APIC found!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        apic = APIC_Tool(global_policies, apic1)
        if not apic.api_validate_apic():
            msg = f"Validate APIC '{apic.hostname}' failed!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False
        self.logger.info(f"Validate APIC {apic.hostname} successfully.")

        if not self._load_aac_data():
            msg = "Failed to load AAC data!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        aac_ansible = Ansible_Tool(self.output_path)

        playbook_dir_validate = os.path.join(
            os.getcwd(),
            self.output_path,
            os.path.basename(settings.TEMPLATE_DIR[0]),
            "aac_ansible",
            "apic_validate.yaml",
        )

        if not aac_ansible.ansible_runner("validate", playbook_dir_validate, self.aac_inventory_path):
            msg = "ACI as Code validation failed!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        playbook_dir_deploy = os.path.join(
            os.getcwd(),
            self.output_path,
            os.path.basename(settings.TEMPLATE_DIR[0]),
            "aac_ansible",
            "apic_deploy.yaml",
        )

        if not aac_ansible.ansible_runner("deploy", playbook_dir_deploy, self.aac_inventory_path):
            msg = "ACI as Code deploy failed!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        playbook_dir_test = os.path.join(
            os.getcwd(),
            self.output_path,
            os.path.basename(settings.TEMPLATE_DIR[0]),
            "aac_ansible",
            "apic_test.yaml",
        )

        if not aac_ansible.ansible_runner("test", playbook_dir_test, self.aac_inventory_path):
            msg = "ACI as Code test failed!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        self.logger.info(f"Configure APIC {apic.hostname} via AAC successfully.")
        return True
