from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any


class SynapseNotebookUtil(SynapseArtifactUtil):
    def get(self, artifact_name: str) -> Dict[str, Any]:
        return self._web_request(
            f"{self.synapse_endpoint}/notebooks/{artifact_name}?api-version=2020-12-01",
        ).json()

    def get_all(self) -> List[Dict[str, Any]]:
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
            r"properties.cells.\d+.outputs",
            r"properties.metadata.kernelspec",
            r"properties.metadata.kernelspec.name",
            r"properties.metadata.kernelspec.display_name"
        ]

    def get_nullable_attributes(self) -> List[str]:
        return []
