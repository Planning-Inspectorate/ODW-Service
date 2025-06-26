from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any, Set
import re


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
    def convert_to_python(cls, artifact: Dict[str, Any]) -> List[str]:
        pass

    @classmethod
    def get_dependencies_in_notebook_code(cls, notebook_python: Set[str]):
        cls.PYTHON_REFERENCE_PATTERNS = [
            r"%run",
            r"mssparkutils.notebook.run",
            r"mssparkutils.credentials.getFullConnectionString"
        ]
        lines_with_external_references = [line for line in notebook_python if any(pattern in line for pattern in cls.PYTHON_REFERENCE_PATTERNS)]
        dependency_names = {
            cls._get_dependency_on_python_line(line)
            for line in lines_with_external_references
        }
        

        # Need to extract the dependency
    
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
            return reference_value.strip()
        else:
            regex_pattern = fr"(?<={re.escape(matched_pattern)}\()(.*)(?=\))"
            reference_value_match = re.match(regex_pattern, python_line)
            if not reference_value_match:
                return None
            # Remove trailing quote characters and whitespace
            return reference_value_match[0].strip()[1:-1]

    @classmethod
    def dependent_artifacts(cls, artifact: Dict[str, Any]) -> Set[str]:
        dependencies = super().dependent_artifacts(artifact)
        notebook_python = cls.convert_to_python(artifact)
        extra_dependencies = cls.get_dependencies_in_notebook_code(notebook_python)
        return dependencies | extra_dependencies
