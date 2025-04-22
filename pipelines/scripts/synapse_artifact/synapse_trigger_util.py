from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any


class SynapseTriggerUtil(SynapseArtifactUtil):
    """
        Class for managing the retrieval and analysis of Synapse Trigger artifacts
    """
    def get(self, artifact_name: str) -> Dict[str, Any]:
        return self._web_request(
            f"{self.synapse_endpoint}/triggers/{artifact_name}?api-version=2020-12-01",
        ).json()

    def get_all(self) -> List[Dict[str, Any]]:
        response = self._web_request(
            f"{self.synapse_endpoint}/triggers?api-version=2020-12-01",
        ).json()
        all_triggers = response["value"]
        while "nextLink" in response:
            next_link = response["nextLink"]
            response = self._web_request(next_link,).json()
            all_triggers.extend(response["value"])
        return all_triggers

    def get_uncomparable_attributes(self) -> List[str]:
        return [
            r"^id$",
            r"^etag$",
            r"^type$"
        ]

    def get_nullable_attributes(self) -> List[str]:
        return []
