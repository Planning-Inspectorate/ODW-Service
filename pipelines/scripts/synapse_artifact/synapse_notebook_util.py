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
        def _process_cell(cell: Dict[str, Any]) -> List[str]:
            if cell["cell_type"] != "code":
                # If the cell is not a code cell, then it can be dropped to simplify processing
                return ""
            # If there are no non-whitespace lines in the cell, the just return an empty string and skip the rest of the processing
            first_meaningful_line = next((line for line in cell["source"] if line.strip()), None)
            if not first_meaningful_line:
                return ""
            is_magic_cell = first_meaningful_line.startswith("%")
            if is_magic_cell:
                # Merge magic cells into one line to simplify processing
                cleaned_cells = [line.strip() for line in cell["source"] if line.strip()]
                cleaned_cell_line = " ".join(cleaned_cells)
                # %run is a special magic command that can be converted to a real python command, which is important for detecting dependencies
                if cleaned_cell_line.startswith("%run "):
                    # Clean the arguments to be a single space between each arg, and convert to be a list of arguments
                    run_arguments = " ".join(cleaned_cell_line[cleaned_cell_line.rindex("%run ")+5:].split())
                    # The %run command either expects a quoted or unquoted path. The below logic only adds quotes if they are missing
                    quote = "\"" if not (run_arguments.startswith('"') or run_arguments.startswith("'") or run_arguments.startswith("`")) else ""
                    cleaned_line = f"mssparkutils.notebook.run({quote}{run_arguments}{quote})"
                    return cleaned_line
                else:
                    # Comment out all other magic commands, since their operation is not important in the grant scheme of things
                    return f"# {cleaned_cell_line}"   
            # Combine all lines into a single string, separated by the newline character
            return "\n".join([line.rstrip() for line in cell["source"]])

        cell_code = [
            _process_cell(cell)
            for cell in artifact["properties"]["cells"]
        ]
        return "\n".join([line for line in cell_code if line])

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
            f"notebook/{x['args'][0]['value'].split('/')[-1]}.json"
            for x in abstract_syntax_tree_functions
            if (
                x["func"]["attr"] == "run" and
                x["func"].get("value", dict()).get("attr", None) == "notebook" and
                x["func"].get("value", dict()).get("value", dict()).get("id", None) == "mssparkutils"
            )
        }
        # Retrieve all linked service references
        linked_service_dependencies = {
            f"linkedService/{x['args'][0]['value']}.json"
            for x in abstract_syntax_tree_functions
            if x["func"]["attr"] == "getFullConnectionString"
        }
        return notebook_dependencies | linked_service_dependencies

    @classmethod
    def dependent_artifacts(cls, artifact: Dict[str, Any]) -> Set[str]:
        dependencies = super().dependent_artifacts(artifact)
        notebook_python = cls.convert_to_python(artifact)
        extra_dependencies = cls.get_dependencies_in_notebook_code(notebook_python)
        return dependencies | extra_dependencies
    
    @classmethod
    def archive(cls, artifact: Dict[str, Any]) -> Dict[str, Any]:
        existing_folder = artifact["properties"].get("folder", dict())
        existing_folder_name = existing_folder.get("name", "")
        existing_folder.update(
            {
                "name": "/".join(["archive", existing_folder_name])
            }
        )
        artifact["properties"]["folder"] = existing_folder
        return artifact
