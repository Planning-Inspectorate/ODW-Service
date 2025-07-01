from pipelines.scripts.synapse_artifact.synapse_artifact_util_factory import SynapseArtifactUtilFactory
from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from pipelines.scripts.util import Util
import json


# Artifacts that should not be marked for archival
ARTIFACTS_TO_KEEP = {
    
}

# Artifacts to use as the base of a dependency analysis
ROOT_ARTIFACTS = {
    "pipeline/pln_master.json"
}

ALL_ARTIFACTS = {
    path for path in Util.get_all_artifact_paths("workspace")
}

ALL_ARCHIVEABLE_ARTIFACTS = {
    artifact_path: json.load(open(artifact_path, "r"))
    for artifact_path in ALL_ARTIFACTS
    if any(
        artifact_path.startswith(x)
        for x in [  # Only the below artifacts types can be archived
            "workspace/dataset",
            "workspace/notebook",
            "workspace/pipeline",
            "workspace/sqlscript"
        ]
    )
}

# Artifacts that cannot be archived
ARTIFACTS_TO_IGNORE = {
    path
    for path in ALL_ARTIFACTS
    if path not in ALL_ARCHIVEABLE_ARTIFACTS.keys()
}

EXISTING_ARCHIVED_ARTIFACTS = {
    artifact_path
    for artifact_path, artifact in ALL_ARCHIVEABLE_ARTIFACTS.items()
    if SynapseArtifactUtil.is_archived(artifact)
}

discovered_artifacts = set()
undiscovered_artifacts = {x for x in ROOT_ARTIFACTS}

while undiscovered_artifacts:
    next_artifact_name = undiscovered_artifacts.pop()
    next_artifact_path = f"workspace/{next_artifact_name}"
    if next_artifact_path not in ARTIFACTS_TO_IGNORE:
        if next_artifact_path not in ALL_ARCHIVEABLE_ARTIFACTS:
            raise ValueError(f"Could not find artifact with path 'workspace/{next_artifact_name}'")
        print(f"analysing '{next_artifact_name}'")
        new_artifact = ALL_ARCHIVEABLE_ARTIFACTS.get(f"workspace/{next_artifact_name}")
        artifact_type = next_artifact_name.split("/")[0]
        artifact_dependencies = SynapseArtifactUtilFactory.get(artifact_type).dependent_artifacts(new_artifact)
        new_dependencies = {dependency for dependency in artifact_dependencies if dependency not in discovered_artifacts}
        undiscovered_artifacts.update(new_dependencies)
        discovered_artifacts.add(next_artifact_name)

print("The below artifacts can be archived")
print(json.dumps(list(discovered_artifacts), indent=4))