from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from typing import List, Dict, Any


class SynapseSparkConfigurationUtil(SynapseArtifactUtil):
    """
        Class for managing the retrieval and analysis of Synapse Spark Configuration artifacts
    """
    @classmethod
    def get_type_name(cls) -> str:
        return "sparkConfiguration"

    def get(self, artifact_name: str, **kwargs: Dict[str, Any]) -> Dict[str, Any]:
        # There doesn't seem to be a REST API endpoint for these, so leaving blank for now
        return dict()

    def get_all(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        # There doesn't seem to be a REST API endpoint for these, so leaving blank for now
        return []

    def get_uncomparable_attributes(self) -> List[str]:
        return []

    def get_nullable_attributes(self) -> List[str]:
        return []
    
    def get_attributes_that_can_be_missing(self) -> Dict[str, Any]:
        return dict()

    def get_env_attributes_to_replace(self) -> List[str]:
        return [
            "properties.configs.park.executorEnv.dataLakeAccountName",
            "properties.configs.spark.executorEnv.keyVaultName"
        ]
