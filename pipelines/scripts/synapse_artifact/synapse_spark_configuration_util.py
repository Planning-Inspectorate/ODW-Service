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
        return dict()

    def get_all(self, **kwargs: Dict[str, Any]) -> List[Dict[str, Any]]:
        return []

    def get_uncomparable_attributes(self) -> List[str]:
        return [
            r"^id$",
            r"^etag$",
            r"^type$"
        ]

    def get_nullable_attributes(self) -> List[str]:
        return []
