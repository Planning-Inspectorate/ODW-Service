from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any
import json


class SynapseDatabaseUtil(SynapseArtifactUtil):
    """
        Class for managing the retrieval and analysis of Synapse Database artifacts
    """
    @classmethod
    def get_type_name(cls) -> str:
        return "database"

    def get(self, artifact_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        return self._web_request(
            f"{self.synapse_endpoint}/databases/{artifact_name}?api-version=2020-12-01",
        ).json()

    def get_all(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        response = self._web_request(
            f"{self.synapse_endpoint}/databases?api-version=2020-12-01",
        ).json()
        all_triggers = response["items"]
        while "nextLink" in response:
            next_link = response["nextLink"]
            response = self._web_request(next_link,).json()
            all_triggers.extend(response["value"])
        return all_triggers

    def get_uncomparable_attributes(self) -> List[str]:
        return []

    def get_nullable_attributes(self) -> List[str]:
        return []

    def get_env_attributes_to_replace(self) -> List[str]:
        return []


dbs = SynapseDatabaseUtil("pins-synw-odw-dev-uks").get_all()
print(json.dumps(dbs, indent=4))