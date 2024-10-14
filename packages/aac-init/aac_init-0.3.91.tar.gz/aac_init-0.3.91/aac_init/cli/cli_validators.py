# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>, Rudy Lei <shlei@cisco.com>

import os
import yamale

from typing import Any, Dict, List, Optional
from aac_init.log_utils import setup_logger
from aac_init.conf import settings
from aac_init.tools.file_tools.yaml_tool import load_yaml_files
from ruamel import yaml


class CLI_Validator:
    """
    Validators during CLI input stage.
    """

    def __init__(self, data_path: str, output_path: str):
        self.logger = setup_logger("cli_validator.log")

        self.logger.debug(
            f"CLI Validator initializing with data_path: '{data_path}', "
            f"output_path: '{output_path}'"
        )

        self.data: Optional[Dict[str, Any]] = None
        self.data_path = data_path
        self.output_path = output_path
        self.global_policy_path = None
        self.errors: List[str] = []

        self.logger.debug("CLI Validator initialized successfully.")

    def _validate_data_path(self):
        """Validate input data path"""

        self.logger.debug("Validating data path...")
        if not os.path.exists(self.data_path):
            msg = f"YAML Directory doesn't exist: {self.data_path}"
            self.logger.error(msg)
            self.errors.append(msg)
            return False
        if not os.path.isdir(self.data_path):
            msg = f"{self.data_path} is not a directory."
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        self.logger.debug(f"Validate YAML directory: '{self.data_path}' successfully!")
        return True

    def _validate_syntax_file(self, file_path: str):
        """Validate the syntax of a single YAML file."""

        filename = os.path.basename(file_path)
        self.logger.debug(f"Validating file: {filename}")

        if not all([os.path.isfile(file_path), filename.endswith((".yaml", ".yml"))]):
            msg = f"{filename} is not a yaml file!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        # YAML syntax validation
        try:
            load_yaml_files([file_path])
        except yaml.MarkedYAMLError as e:
            line = e.problem_mark.line + 1 if e.problem_mark else 0
            column = e.problem_mark.column + 1 if e.problem_mark else 0
            msg = (
                f"Syntax error in '{file_path}': "
                f"Line {line}, Column {column} - {e.problem}"
            )
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        return True

    def _validate_yaml(self):
        """Validate input yaml files"""

        self.logger.debug("Validating input yaml files...")
        data_path = os.path.abspath(self.data_path)
        global_policy_yaml_file_exist = False
        for dir, _, files in os.walk(data_path):
            for filename in files:
                self._validate_syntax_file(os.path.join(dir, filename))
                if filename in settings.DEFAULT_DATA_PATH:
                    if os.path.abspath(dir) != data_path:
                        msg = "'00-global_policy file cannot be in subdirectory"
                        self.logger.error(msg)
                        self.errors.append(msg)
                        return False

                    self.global_policy_path = os.path.join(dir, filename)

                    if global_policy_yaml_file_exist:
                        msg = "Duplicated 00-global_policy found"
                        self.logger.error(msg)
                        self.errors.append(msg)
                        return False

                    global_policy_yaml_file_exist = True

        if self.global_policy_path:
            self.global_policy = load_yaml_files([self.global_policy_path])
            self.logger.debug("00-global_policy loaded successfully.")
        else:
            self.global_policy = []
            msg = "00-global_policy is missing!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        self.logger.debug(f"Validate YAML files in: '{self.data_path}' successfully!")
        return True

    def validate_selections(self, value):
        """Validate CLI selections"""

        self.logger.debug("Validating CLI selections...")
        valid_selections = [
            str(i) for i in range(1, len(settings.DEFAULT_USER_SELECTIONS) + 1)
        ]

        if value == "*":
            selections = valid_selections
        else:
            selections = value.split(",")
            for selection in selections:
                if selection not in valid_selections:
                    msg = f"{selection} is not a valid selection!"
                    self.logger.error(msg)
                    self.errors.append(msg)
                    return False

        self.selections = sorted(selections, key=lambda x: int(x))

        self.logger.debug(f"Validate CLI selections: {self.selections} successfully!")
        return self.selections

    def _validate_global_policy(self):
        """Validate global policy per selection"""

        self.logger.debug("Validating global policy...")

        fabric_policy = self.global_policy.get("fabric", {})
        apic_check = "apic_nodes_connection" in fabric_policy
        aci_switch_check = "switch_nodes_connection" in fabric_policy

        def log_handle(selection_number, message):
            msg = f"Error Validate Selection {selection_number}: {message}"
            self.logger.error(msg)
            self.errors.append(msg)

        if "1" in self.selections and not any([apic_check, aci_switch_check]):
            log_handle(1, "No APIC/Switch configuration provided!")
            return False

        if "2" in self.selections and not apic_check:
            log_handle(2, "No APIC configuration provided!")
            return False

        if "3" in self.selections and not apic_check:
            log_handle(3, "No APIC configuration provided!")
            return False

        data = yamale.make_data(self.global_policy_path, parser="ruamel")
        schema_folder = os.path.join(settings.SCHEMA_DIR, "00-global_policy")

        # Need to pass at lease one schema
        for _, _, schema_files in os.walk(schema_folder):
            for schema_file in schema_files:
                self.logger.debug(
                    f"Validating schema: '{schema_file}' for global policy..."
                )
                schema_file_path = os.path.join(schema_folder, schema_file)
                try:
                    schema = yamale.make_schema(schema_file_path)
                    yamale.validate(schema, data)
                    self.logger.debug(f"Schema '{schema_file}' validated successfully.")
                    return True
                except ValueError as e:
                    self.logger.warning(f"Schema '{schema_file}' validated failed!")
                    self.logger.warning(e)

        text = """
            '00-global_policy' did not meet the requirements of any validation schema.
            This may be due to incorrect configuration in '00-global_policy',
            or it might be a new configuration scenario that is not supported by the current schema.
            If you confirm that your configuration is correct and represents a new scenario,
            please contact the shlei@cisco.com to update schema.
            """

        self.logger.error(text)
        self.errors.append(text)
        return False

    def _validate_fabric_mgmt(self):
        """Validate fabric_mgmt for selection1 - install ACI switch"""

        if "1" not in self.selections:
            return True

        self.logger.debug("Validating fabric management...")

        data_path = os.path.abspath(self.data_path)
        nac_data_path = os.path.join(data_path, settings.DATA_PATH)
        fabric_mgmt_file = None

        if not all([os.path.exists(nac_data_path), os.path.isdir(nac_data_path)]):
            msg = "NaC path doesn't exist or not a folder!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        for item in os.listdir(nac_data_path):
            item_path = os.path.join(nac_data_path, item)
            if os.path.isfile(item_path) and item in settings.DEFAULT_FABRIC_MGMT_PATH:
                if fabric_mgmt_file:
                    msg = "Duplicated 01-fabric_mgmt found."
                    self.logger.error(msg)
                    self.errors.append(msg)
                    return False
                fabric_mgmt_file = item_path

        if not fabric_mgmt_file:
            msg = "01-fabric_mgmt is missing!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        data = yamale.make_data(fabric_mgmt_file, parser="ruamel")
        schema_folder = os.path.join(settings.SCHEMA_DIR, "01-fabric_mgmt")

        for _, _, schema_files in os.walk(schema_folder):
            for schema_file in schema_files:
                self.logger.debug(
                    f"Validating schema: '{schema_file}' for fabric management..."
                )
                schema_file_path = os.path.join(schema_folder, schema_file)
                try:
                    schema = yamale.make_schema(schema_file_path)
                    yamale.validate(schema, data)
                    self.logger.debug(f"Schema '{schema_file}' validated successfully.")
                    return True

                except ValueError as e:
                    self.logger.warning(f"Schema '{schema_file}' validated failed!")
                    self.logger.warning(e)

            text = """
            '01-fabric_mgmt' did not meet the requirements of any validation schema.
            This may be due to incorrect configuration in '01-fabric_mgmt',
            or it might be a new configuration scenario that is not supported by the current schema.
            If you confirm that your configuration is correct and represents a new scenario,
            please contact the shlei@cisco.com to update schema.
            """

            self.logger.error(text)
            self.errors.append(text)
            return False

        # check fabric configuration
        # get fabric_mgmt_node_ids

        # TODO: need to validate duplicate id in each file..
        fabric_mgmt_policy = load_yaml_files([fabric_mgmt_file])
        self.logger.debug("01-fabric_mgmt loaded successfully.")
        fabric_mgmt_policy_apic = fabric_mgmt_policy.get("apic", {}) or {}
        fabric_mgmt_policy_apic_node_policies = (
            fabric_mgmt_policy_apic.get("node_policies", {}) or {}
        )
        fabric_mgmt_policy_apic_node_policies_nodes = (
            fabric_mgmt_policy_apic_node_policies.get("nodes", []) or []
        )
        fabric_mgmt_node_ids = set(
            i.get("id") for i in fabric_mgmt_policy_apic_node_policies_nodes
        )

        global_policy_fabric = self.global_policy.get("fabric", {}) or {}
        global_policy_switch_nodes_connection = (
            global_policy_fabric.get("switch_nodes_connection", []) or []
        )
        global_policy_switch_node_ids = set(
            i.get("id") for i in global_policy_switch_nodes_connection
        )

        if global_policy_switch_node_ids != fabric_mgmt_node_ids:
            msg = "Switch Nodes in global_policy and fabric_mgmt are not identical."
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        return True

    def _validate_nac_data(self):
        """Validate nac_data for selection3 - ACI as Code"""

        if "3" not in self.selections:
            return True

        self.logger.debug("Validating NaC Data...")

        # data_path = os.path.abspath(self.data_path)
        nac_data_path = os.path.join(self.data_path, settings.DATA_PATH)

        if not all([os.path.exists(nac_data_path), os.path.isdir(nac_data_path)]):
            msg = "NaC path doesn't exist or not a folder!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        nac_yaml_files = []
        for dir, _, files in os.walk(nac_data_path):
            for filename in files:
                nac_yaml_path = os.path.join(dir, filename)
                if nac_yaml_path:
                    nac_yaml_files.append(nac_yaml_path)

        if not nac_yaml_files:
            msg = f"No YAML file found in dir: {nac_data_path}"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        self.logger.debug("NaC Data validated successfully.")
        return True

    def validate_cli_input(self):
        """Validate CLI input data files and selections"""

        self.logger.debug("Validating CLI input data files and selections...")
        if all(
            [
                self._validate_data_path(),
                self._validate_yaml(),
                self._validate_global_policy(),
                self._validate_fabric_mgmt(),
                self._validate_nac_data(),
            ]
        ):
            self.logger.debug("CLI inputs validated successfully.")
            return True
        else:
            self.logger.error("CLI inputs validated failed!")

        return False
