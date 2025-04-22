from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any
import json
import re


class SynapsePipelineUtil(SynapseArtifactUtil):
    def get(self, artifact_name: str) -> Dict[str, Any]:
        """
            Return the json for the specified pipeline
        """
        return self._web_request(
            f"{self.synapse_endpoint}/pipelines/{artifact_name}?api-version=2020-12-01",
        ).json()

    def get_all(self) -> List[Dict[str, Any]]:
        """
            Return the json for all Synapse pipelines
        """
        response = self._web_request(
            f"{self.synapse_endpoint}/pipelines?api-version=2020-12-01",
        ).json()
        all_pipelines = response["value"]
        while "nextLink" in response:
            next_link = response["nextLink"]
            response = self._web_request(next_link,).json()
            all_pipelines.extend(response["value"])
        return all_pipelines

    def compare(self, artifact_a, artifact_b) -> bool:
        uncomparable_properties = [
            r"^id$",
            r"^etag$",
            r"^properties.lastPublishTime"
        ]
        nullable_properties = [
            r"^properties.activities.\d+.inputs.\d+.parameters$",
            r"^properties.activities.\d+.outputs.\d+.parameters$",
            r"^properties.activities.\d+.policy$",
            r"^properties.activities.\d+.policy.secureInput$",
            r"^properties.activities.\d+.typeProperties.parameters$",
            r"^properties.policy$",
            r"^properties.policy.elapsedTimeMetric$"
        ]
        artifact_a_properties = self._extract_dict_keys(artifact_a)
        artifact_b_properties = self._extract_dict_keys(artifact_b)
        artifact_a_properties_cleaned = self.clean_json_properties(
            artifact_a,
            artifact_a_properties,
            uncomparable_properties,
            nullable_properties
        )
        artifact_b_properties_cleaned = self.clean_json_properties(
            artifact_b,
            artifact_b_properties,
            uncomparable_properties,
            nullable_properties
        )
        if artifact_a_properties_cleaned != artifact_b_properties_cleaned:
            return False
        return self._compare_properties(artifact_a_properties_cleaned, artifact_a, artifact_b)
