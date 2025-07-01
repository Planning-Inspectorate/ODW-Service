from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any, Set
from pipelines.scripts.util import Util
import ast
from ast2json import ast2json
import re
import json


class SynapseNotebookUtil(SynapseArtifactUtil):
    """
        Class for managing the retrieval and analysis of Synapse Notebook artifacts
    """
    PYTHON_REFERENCE_PATTERNS = [
        r"%run",
        r"mssparkutils.notebook.run",
        r"mssparkutils.credentials.getFullConnectionString"
    ]

    @classmethod
    def get_type_name(cls) -> str:
        return "notebook"

    def get(self, artifact_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return self._web_request(
            f"{self.synapse_endpoint}/notebooks/{artifact_name}?api-version=2020-12-01",
        ).json()

    def get_all(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        response = self._web_request(
            f"{self.synapse_endpoint}/notebooks?api-version=2020-12-01",
        ).json()
        all_notebooks = response["value"]
        while "nextLink" in response:
            next_link = response["nextLink"]
            response = self._web_request(next_link,).json()
            all_notebooks.extend(response["value"])
        return all_notebooks

    def get_uncomparable_attributes(self) -> List[str]:
        return [
            r"id",
            r"type",
            r"etag",
            r"properties.entityState",
            r"properties.renameOperationDetails",
            r"properties.targetSparkConfiguration",
            r"properties.description",
            r"properties.sessionProperties.runAsWorkspaceSystemIdentity",
            r"properties.metadata.a365ComputeOptions.extraHeader",
            r"properties.metadata.a365ComputeOptions.auth.authHeader",
            r"properties.cells.\d+.execution_count",
            r"properties.cells.\d+.outputs",
            r"properties.metadata.kernelspec",
            r"properties.metadata.kernelspec.name",
            r"properties.metadata.kernelspec.display_name",
        ]

    def get_nullable_attributes(self) -> List[str]:
        return [
            r"properties.metadata.a365ComputeOptions.automaticScaleJobs",
            r"properties.cells.\d+.metadata",
            r"properties.folder",
            r"properties.bigDataPool",
            r"properties.metadata.a365ComputeOptions"
        ]
    
    def compare(self, artifact_a, artifact_b):
        def _add_missing_attributes(artifact: Dict[str, Any]) -> Dict[str, Any]:
            # Set default values for optional properties. This is the only artifact where this is required
            properties = artifact["properties"]
            metadata = properties["metadata"]
            if "a365ComputeOptions" not in metadata or metadata["a365ComputeOptions"] is None:
                metadata["a365ComputeOptions"] = {
                    "automaticScaleJobs": True
                }
            compute_options = metadata["a365ComputeOptions"]
            if "automaticScaleJobs" not in compute_options:
                compute_options["automaticScaleJobs"] = True
            return artifact
        artifact_a = _add_missing_attributes(artifact_a)
        artifact_b = _add_missing_attributes(artifact_b)
        return super().compare(artifact_a, artifact_b)

    def get_env_attributes_to_replace(self) -> List[str]:
        return [
            "properties.metadata.a365ComputeOptions.id",
            "properties.metadata.a365ComputeOptions.endpoint"
        ]

    @classmethod
    def convert_to_python(cls, artifact: Dict[str, Any]) -> str:
        python_lines = [
            line.rstrip()
            for cell in artifact["properties"]["cells"]
            for line in cell["source"]
            if cell["cell_type"] == "code"
        ]
        # All available magic commands: https://ipython.readthedocs.io/en/stable/interactive/magics.html
        magic_command_map = {
            "%run ": lambda x: x.replace("%run ", "mssparkutils.notebook.run(\"") + "\")",  # %run is equivalent to mssparkutils.notebook.run
            # Add any other special magic command cases here
            "%": lambda x: "#  " + x  # By default magic commands are turned into comments
        }
        # Replace magic command 
        python_line_magic_commands = {
            line: next((command for command in magic_command_map.keys() if line.startswith(command)), None)
            for line in python_lines
        }
        return "\n".join(
            [
                magic_command_map[magic_command](line) if magic_command else line
                for line, magic_command in python_line_magic_commands.items()
            ]

        )

    @classmethod
    def get_dependencies_in_notebook_code(cls, notebook_python: str):
        cls.PYTHON_REFERENCE_PATTERNS = [
            r"%run",
            r"mssparkutils.notebook.run",
            r"mssparkutils.credentials.getFullConnectionString"
        ]
        # Convert the python code into abstract syntax tree json that can be analysed
        abstract_syntax_tree = ast.parse(notebook_python)
        abstract_syntax_tree_json = ast2json(abstract_syntax_tree)
        abstract_syntax_tree_attributes = cls.get_all_attributes(abstract_syntax_tree_json)
        # Retrieve the list of attributes that correspond to function calls
        abstract_syntax_tree_funtion_attribute_names = [
            x[0:-10]
            for x in abstract_syntax_tree_attributes
            if ".func." in x and x.endswith("func.attr")
        ]
        # Retrives all function all objects from the AST
        abstract_syntax_tree_functions = [cls.get_by_attribute(abstract_syntax_tree_json, x) for x in abstract_syntax_tree_funtion_attribute_names]
        # Retrieve all notebook calls associated with the mssparkutils.run method
        notebook_dependencies = {
            f"notebook/{x['args'][0]['value'].split('/')[-1]}"
            for x in abstract_syntax_tree_functions
            if (
                x["func"]["attr"] == "run" and
                x["func"].get("value", dict()).get("attr", None) == "notebook" and
                x["func"].get("value", dict()).get("value", dict()).get("id", None) == "mssparkutils"
            )
        }
        # Retrieve all linked service references
        linked_service_dependencies = {
            f"linkedService/{x['args'][0]['value']}"
            for x in abstract_syntax_tree_functions
            if x["func"]["attr"] == "getFullConnectionString"
        }
        return notebook_dependencies | linked_service_dependencies

    @classmethod
    def _get_dependency_on_python_line(cls, python_line: str) -> str:
        # Validation and error handling
        pattern_matches = [pattern for pattern in cls.PYTHON_REFERENCE_PATTERNS if pattern in python_line]
        if len(pattern_matches) > 1:
            raise ValueError(
                "Multiple matches were found for SynapseNotebookUtil.PYTHON_REFERENCE_PATTERNS, when trying to extract the reference value, "
                "but we only expected one match. Please manually verify the dependencies for this notebook"
            )
        if not pattern_matches:
            raise ValueError("No matches found in SynapseNotebookUtil.PYTHON_REFERENCE_PATTERNS when trying to extract the reference value")
        matched_pattern = pattern_matches[0]
        if matched_pattern == r"%run":
            # The %run magic command is a special case
            reference_value = python_line.replace(matched_pattern, "")
            return reference_value.strip().split("/")[-1]
        else:
            abstract_syntax_tree = ast.parse(python_line)
            #  This is only being called for a 1-line python function, so
            target_function_args = abstract_syntax_tree.body[0].value.args
            print("args: ", function_args)
            c: ast.Constant = function_args[0]
            print(c.value)
            print(ast.dump(tree, indent=4))
            1 + "a"
            regex_pattern = fr"(?<={re.escape(matched_pattern)}\()(.*)(?=\))"
            print(f"checkig pattern: '{regex_pattern}' against '{python_line}'")
            reference_value_match = re.search(regex_pattern, python_line)
            if not reference_value_match:
                print("NO MATCH FOUND")
                return None
            # Remove trailing quote characters and whitespace
            return reference_value_match[0].strip()[1:-1].split("/")[-1]

    @classmethod
    def dependent_artifacts(cls, artifact: Dict[str, Any]) -> Set[str]:
        dependencies = super().dependent_artifacts(artifact)
        notebook_python = cls.convert_to_python(artifact)
        extra_dependencies = cls.get_dependencies_in_notebook_code(notebook_python)
        return dependencies | extra_dependencies

'''
import json
with open("workspace/notebook/py_utils_get_storage_account.json", "r") as f:
    nb_content = json.load(f)

tst = SynapseNotebookUtil.convert_to_python(nb_content)

with open("pipelines/scripts/synapse_artifact/synapse_notebook_util__output.py", "w") as f:
    f.write("\n".join(tst))
'''


#mssparkutils.notebook.run("utils/py_utils_get_storage_account")