# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>, Rudy Lei <shlei@cisco.com>

import json
import os
import pathlib
import shutil
import importlib.util
import subprocess

from typing import Any, Dict, List
from ruamel import yaml
from jinja2 import ChainableUndefined, Environment, FileSystemLoader
from aac_init.log_utils import setup_logger


class VaultTag(yaml.YAMLObject):
    yaml_tag = "!vault"

    def __init__(self, v: str):
        self.value = v

    def __repr__(self) -> str:
        spec = importlib.util.find_spec("aac_validate.ansible_vault")
        if spec:
            if "ANSIBLE_VAULT_ID" in os.environ:
                vault_id = os.environ["ANSIBLE_VAULT_ID"] + "@" + str(spec.origin)
            else:
                vault_id = str(spec.origin)
            t = subprocess.check_output(
                [
                    "ansible-vault",
                    "decrypt",
                    "--vault-id",
                    vault_id,
                ],
                input=self.value.encode(),
            )
            return t.decode()
        return ""

    @classmethod
    def from_yaml(cls, loader: Any, node: Any) -> str:
        return str(cls(node.value))


class EnvTag(yaml.YAMLObject):
    yaml_tag = "!env"

    def __init__(self, v: str):
        self.value = v

    def __repr__(self) -> str:
        env = os.getenv(self.value)
        if env is None:
            return ""
        return env

    @classmethod
    def from_yaml(cls, loader: Any, node: Any) -> str:
        return str(cls(node.value))


def load_yaml_files(paths: List[str]) -> Dict[str, Any]:
    """Load all YAML files from a provided directory."""

    logger = setup_logger("aac_yaml.log")

    def _load_file(file_path: str, data: Dict[str, Any]) -> None:
        with open(file_path, "r") as file:
            if ".yaml" in file_path or ".yml" in file_path:
                logger.debug(f"Loading file: {file_path}")
                data_yaml = file.read()
                y = yaml.YAML()
                y.preserve_quotes = True  # type: ignore
                y.register_class(VaultTag)
                y.register_class(EnvTag)
                dict = y.load(data_yaml)
                logger.debug(f"Merging file: {file_path}")
                merge_dict(dict, data, logger)
                logger.debug(f"{file_path} merged successfully!")

    result: Dict[str, Any] = {}
    logger.debug("Loading yaml files...")
    for path in paths:
        if os.path.isfile(path):
            _load_file(path, result)
        else:
            for dir, subdir, files in os.walk(path):
                for filename in files:
                    try:
                        _load_file(dir + os.path.sep + filename, result)
                    except Exception as e:  # noqa: E722
                        logger.error(
                            f"Could not load file: {filename}, " f"reason: {e}"
                        )
    return result


def merge_list_item(
        source_item: Any, destination: List[Any], merge_list_items: bool = True
) -> None:
    """Merge items into list."""
    if isinstance(source_item, dict) and merge_list_items:
        # check if we have an item in destination with matching primitives
        for dest_item in destination:
            match = True
            comparison = False
            unique_source = False
            unique_dest = False
            for k, v in source_item.items():
                if isinstance(v, dict) or isinstance(v, list):
                    continue
                if k in dest_item and v == dest_item[k]:
                    comparison = True
                    continue
                if k not in dest_item:
                    unique_source = True
                    continue
                comparison = True
                match = False
            for k, v in dest_item.items():
                if isinstance(v, dict) or isinstance(v, list):
                    continue
                if k in source_item and v == source_item[k]:
                    comparison = True
                    continue
                if k not in source_item:
                    unique_dest = True
                    continue
                comparison = True
                match = False
            if comparison and match and not (unique_source and unique_dest):
                merge_dict(source_item, dest_item, merge_list_items)
                return
    elif source_item in destination:
        return
    destination.append(source_item)


def merge_dict(
        source: Dict[Any, Any],
        destination: Dict[Any, Any],
        logger,
        merge_list_items: bool = True,
) -> Dict[Any, Any]:
    """Merge two nested dict/list structures."""

    if not source:
        logger.warning(f"Empty source: {source}, skipped..")
        return destination
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            if node is None:
                destination[key] = value
            else:
                merge_dict(value, node, merge_list_items)
        elif isinstance(value, list):
            if key not in destination:
                destination[key] = value
            if isinstance(destination[key], list):
                for i in value:
                    merge_list_item(i, destination[key], merge_list_items)
        else:
            destination[key] = value
    return destination


class BaseYamlTool:
    def __init__(self, data_paths: List[str]) -> None:
        self.data = load_yaml_files(data_paths)

    def _fix_duplicate_path(self, *paths: str) -> str:
        directory = os.path.join(*paths[:-1])
        if os.path.exists(directory):
            entries = os.listdir(directory)
            lower_case_entries = [path.lower() for path in entries]
            if paths[-1].lower() in lower_case_entries and paths[-1] not in entries:
                return os.path.join(*paths[:-1], "_" + paths[-1])
        return os.path.join(*paths)


class YamlWriter(BaseYamlTool):
    def __init__(
        self,
        data_paths: List[str],
    ) -> None:
        super().__init__(data_paths)
        self.logger = setup_logger("yaml_writer.log")
        self.logger.debug("Loading YAML files from {}".format(data_paths[0]))
        self.filters: Dict[str, Any] = {}

    def render_template(
        self, template_path: str, output_path: str, env: Environment, **kwargs: Any
    ) -> None:
        """Render single robot jinja template"""
        self.logger.debug("Render Ansible playbook template: {}".format(template_path))
        # create output directory if it does not exist yet
        pathlib.Path(os.path.dirname(output_path)).mkdir(parents=True, exist_ok=True)

        template = env.get_template(template_path)
        # json roundtrip should be safe
        # as everything should be serializable
        data = json.loads(json.dumps(self.data))
        result = template.render(data, **kwargs)

        # remove extra empty lines
        lines = result.splitlines()
        cleaned_lines = []
        for index, line in enumerate(lines):
            if len(line.strip()):
                cleaned_lines.append(line)
            else:
                if index + 1 < len(lines):
                    next_line = lines[index + 1]
                    if len(next_line) and not next_line[0].isspace():
                        cleaned_lines.append(line)
        result = os.linesep.join(cleaned_lines)

        with open(output_path.replace(".j2", ""), "w") as file:
            file.write(result)

    def write_3(self, templates_path: str, output_path: str) -> None:
        env = Environment(
            loader=FileSystemLoader(templates_path),
            undefined=ChainableUndefined,
            lstrip_blocks=True,
            trim_blocks=True,
        )

        for dir, _, files in os.walk(templates_path):
            if files:
                try:
                    for filename in files:
                        if ".j2" not in filename:
                            self.logger.debug(
                                "Skip file with unknown file extension "
                                "(not.j2): {}".format(os.path.join(dir, filename))
                            )
                            out = os.path.join(
                                output_path,
                                os.path.basename(templates_path),
                                os.path.relpath(dir, templates_path),
                            )
                            pathlib.Path(out).mkdir(parents=True, exist_ok=True)
                            print(123, out)
                            shutil.copy(os.path.join(dir, filename), out)
                            continue

                        rel = os.path.relpath(dir, templates_path)
                        t_path = os.path.join(rel, filename)
                        t_path = t_path.replace("\\", "/")
                        o_dir = self._fix_duplicate_path(
                            output_path, os.path.basename(templates_path), rel
                        )

                        self.o_path = os.path.join(o_dir, filename)
                        self.render_template(t_path, self.o_path, env)
                        self.logger.debug(
                            "Generate working file successfully: {}".format(self.o_path)
                        )
                except Exception as e:
                    self.logger.error(
                        "Generate working file failed: {}".format(self.o_path)
                    )
                    self.logger.error("Error: {}".format(e))
                    exit()
            else:
                try:
                    rel = os.path.relpath(dir, templates_path)
                    rel = rel.replace("\\", "/")
                    self.o_dir = self._fix_duplicate_path(
                        output_path, os.path.basename(templates_path), rel
                    )
                    pathlib.Path(self.o_dir).mkdir(parents=True, exist_ok=True)
                    self.logger.debug(
                        "Generate working directory successfully: {}".format(self.o_dir)
                    )
                except Exception as e:
                    self.logger.error(
                        "Generate working directory failed: {}".format(self.o_dir)
                    )
                    self.logger.error("Error: {}".format(e))
                    exit()