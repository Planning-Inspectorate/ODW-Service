from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any
import json
import re


class SynapseNotebookUtil(SynapseArtifactUtil):
    def get(self, artifact_name: str) -> Dict[str, Any]:
        """
            Return the json for the specified notebook
        """
        return self._web_request(
            f"{self.synapse_endpoint}/notebooks/{artifact_name}?api-version=2020-12-01",
        ).json()

    def get_all(self) -> List[Dict[str, Any]]:
        """
            Return the json for all Synapse notebooks
        """
        response = self._web_request(
            f"{self.synapse_endpoint}/notebooks?api-version=2020-12-01",
        ).json()
        all_notebooks = response["value"]
        while "nextLink" in response:
            next_link = response["nextLink"]
            response = self._web_request(next_link,).json()
            all_notebooks.extend(response["value"])
        return all_notebooks

    def compare(self, artifact_a, artifact_b) -> bool:
        uncomparable_properties = [
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
            r"properties.cells.\d+.outputs",
            r"properties.metadata.kernelspec",
            r"properties.metadata.kernelspec.name",
            r"properties.metadata.kernelspec.display_name"
        ]
        artifact_a_properties = self._extract_dict_keys(artifact_a)
        artifact_b_properties = self._extract_dict_keys(artifact_b)
        artifact_a_properties_cleaned = {
            key: val
            for key, val in artifact_a_properties.items()
            if not any(re.match(pattern, key) for pattern in uncomparable_properties)
        }
        artifact_b_properties_cleaned = {
            key: val
            for key, val in artifact_b_properties.items()
            if not any(re.match(pattern, key) for pattern in uncomparable_properties)
        }
        artifact_a_string = json.dumps(artifact_a_properties_cleaned, sort_keys=True)
        artifact_b_string = json.dumps(artifact_b_properties_cleaned, sort_keys=True)
        return artifact_a_string == artifact_b_string
