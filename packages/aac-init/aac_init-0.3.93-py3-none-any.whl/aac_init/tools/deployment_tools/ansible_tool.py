# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>, Rudy Lei <shlei@cisco.com>

import os
import re

from typing import Any, Dict, List, Optional
from aac_init.log_utils import setup_logger
from aac_init.conf import settings
from aac_init.tools.file_tools.yaml_tool import load_yaml_files, YamlWriter
from ruamel import yaml
from ansible_runner import run


class Ansible_Tool:
    """Ansible Toolkits, include validation and deployment"""

    def __init__(self, output_path: str):
        self.logger = setup_logger("ansible_tool.log")

        self.data: Optional[Dict[str, Any]] = None
        self.output_path = output_path
        self.aac_inventory_path = None
        self.errors: List[str] = []

        self.logger.debug("Ansible Tool initialized successfully.")

    def ansible_runner(
        self, ansible_phase, playbook_dir, inventory_path=None, quiet=True
    ):
        """Ansible runner"""

        logger = setup_logger(f"ansible_tool_{ansible_phase}.log")

        def _callback(res):
            if not quiet and "stdout" in res:
                print(res["stdout"])
            output = re.compile(r"\x1b\[\[?(?:\d{1,2}(?:;\d{0,2})*)?[m|K]").sub(
                "", res["stdout"]
            )
            logger.debug(output)

        runner = run(
            playbook=playbook_dir,
            inventory=inventory_path,
            verbosity=5,
            quiet=True,
            event_handler=_callback,
        )

        if runner.status == "successful":
            logger.debug(
                f"Complete Network as Code Ansible phase: '{ansible_phase}' successfully."
            )
            return True

        else:
            msg = f"Error on Network as Code Ansible phase: '{ansible_phase}'!"
            logger.error(msg)
            self.errors.append(msg)
            return False
