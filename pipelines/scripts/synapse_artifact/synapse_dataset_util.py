from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any


class SynapseDatasetUtil(SynapseArtifactUtil):
    """
        Class for managing the retrieval and analysis of Synapse Dataset artifacts
    """
    @classmethod
    def get_type_name(cls) -> str:
        return "dataset"

    def get(self, artifact_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return self._web_request(
            f"{self.synapse_endpoint}/datasets/{artifact_name}?api-version=2020-12-01",
        ).json()

    def get_all(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        response = self._web_request(
            f"{self.synapse_endpoint}/datasets?api-version=2020-12-01",
        ).json()
        all_datasets = response["value"]
        while "nextLink" in response:
            next_link = response["nextLink"]
            response = self._web_request(next_link,).json()
            all_datasets.extend(response["value"])
        return all_datasets

    def get_uncomparable_attributes(self) -> List[str]:
        return [
            r"^id$",
            r"^etag$",
            r"^type$"
        ]

    def get_nullable_attributes(self) -> List[str]:
        return []
