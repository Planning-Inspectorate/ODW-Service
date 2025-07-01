from pipelines.scripts.synapse_artifact.synapse_artifact_util_factory import SynapseArtifactUtilFactory
from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from pipelines.scripts.util import Util
from typing import Set, Tuple
import json
import logging
import os


logging.basicConfig(level=logging.INFO)


class ArtifactArchiver():
    def __init__(self):
        self.ARTIFACTS_TO_KEEP = {
            
        }
        """Artifacts that should not be marked for archival"""

        self.ROOT_ARTIFACTS = {
            "pipeline/pln_master.json"
        }
        """Artifacts to use as the base of the dependency analysis"""

        self.ALL_ARTIFACTS = {
            path for path in Util.get_all_artifact_paths("workspace")
        }
        """All json artifacts stored under the "./workspace" directory"""

        self.ALL_ARCHIVEABLE_ARTIFACTS = {
            artifact_path: json.load(open(artifact_path, "r"))
            for artifact_path in self.ALL_ARTIFACTS
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
        """All artifacts that can be archived. i.e. all artifacts that have a "folder" property"""

        self.ARTIFACTS_TO_IGNORE = {
            path
            for path in self.ALL_ARTIFACTS
            if path not in self.ALL_ARCHIVEABLE_ARTIFACTS.keys()
        }
        """Artifacts that cannot be archived. i.e. ALL_ARTIFACTS - ALL_ARCHIVEABLE_ARTIFACTS"""

        self.EXISTING_ARCHIVED_ARTIFACTS = {
            artifact_path
            for artifact_path, artifact in self.ALL_ARCHIVEABLE_ARTIFACTS.items()
            if SynapseArtifactUtil.is_archived(artifact)
        }
        """Artifacts that have already been marked as archived"""

    def get_artifact(self, artifact_path: str):
        return self.ALL_ARCHIVEABLE_ARTIFACTS.get(f"workspace/{artifact_path}")

    def get_dependencies(self) -> Set[str]:
        """
            Deeply return all dependencies of the root artifacts

            :return: The set of dependencies for the ROOT_ARTIFACTS
        """
        discovered_artifacts = set()
        undiscovered_artifacts = {x for x in self.ROOT_ARTIFACTS}

        while undiscovered_artifacts:
            next_artifact_name = undiscovered_artifacts.pop()
            next_artifact_path = f"workspace/{next_artifact_name}"
            if next_artifact_path not in self.ARTIFACTS_TO_IGNORE:
                if next_artifact_path not in self.ALL_ARCHIVEABLE_ARTIFACTS:
                    raise ValueError(f"Could not find artifact with path 'workspace/{next_artifact_name}'")
                logging.info(f"Analysing the dependencies of '{next_artifact_name}'")
                new_artifact = self.get_artifact(next_artifact_name)
                artifact_type = next_artifact_name.split("/")[0]
                artifact_dependencies = SynapseArtifactUtilFactory.get(artifact_type).dependent_artifacts(new_artifact)
                new_dependencies = {dependency for dependency in artifact_dependencies if dependency not in discovered_artifacts}
                undiscovered_artifacts.update(new_dependencies)
            discovered_artifacts.add(next_artifact_name)
        return discovered_artifacts

    def get_artifacts_to_archive(self, dependencies: Set[str]) -> Tuple[Set[str], Set[str]]:
        """
            Return all artifacts that can be archived

            :param dependencies: The set of dependencies identified by get_dependencies()
            :return: A set of all artifacts that can be archived, and a set of artifacts that can be archived but physically can't
        """
        return {
            artifact
            for artifact in self.ALL_ARCHIVEABLE_ARTIFACTS
            if not (artifact in dependencies or artifact in self.ARTIFACTS_TO_KEEP)
        }
    
    def get_artifacts_that_cannot_be_archived(self, artifacts_to_archive: Set[str]) -> Set[str]:
        """
            Filter out the given artifacts to archive by returning only the artifacts that can be archived.
            Only artifacts that have a "folder" property can be archived

            :return: The artifacts to be archived that cannot be archived due to their structure
        """
        return {
            artifact
            for artifact in artifacts_to_archive
            if not self.is_artifact_archiveable(artifact) 
        }

    def get_artifacts_to_delete(self, artifacts_to_archive: Set[str]):
        """
            Return all artifacts that have been marked for archival but are already archived, or physically cannot be archived
            These artifacts should theoretically be safe to delete
        """
        return {
            artifact
            for artifact in artifacts_to_archive
            if artifact in self.EXISTING_ARCHIVED_ARTIFACTS
        }
    
    def is_artifact_archiveable(self, artifact: str) -> bool:
        """
            Return true if the given artifact can be archived, false otherwise
        """
        artifact_type = artifact.split("/")[1]
        return SynapseArtifactUtilFactory.get(artifact_type).can_be_archived()
    
    def archive_artifacts(self, artifacts_to_archive: Set[str]):
        """
            Archive the given artifacts
        """
        artifact_util_instances = {
            artifact.split("/")[0]: SynapseArtifactUtilFactory.get(artifact.split("/")[0])
            for artifact in artifacts_to_archive
        }
        for artifact in artifacts_to_archive:
            artifact_util_instances[artifact.split("/")[0]].archive()
            artifact_json = self.get_artifact(artifact)
            artifact_json = SynapseArtifactUtilFactory.get(artifact_json).archive(artifact_json)
            with open(f"workspace/{artifact}", "w") as f:
                json.dump(artifact_json, f, indent="\t", ensure_ascii=False)

    def delete_artifacts(self, artifacts_to_delete: Set[str]):
        """
            Delete the given artifacts
        """
        for artifact in artifacts_to_delete:
            os.remove(f"workspace/{artifact}")

    def main(self):
        """
            Identify artifacts that can be archived or deleted, and then archive/delete them
        """
        logging.info(f"Identifying the dependencies of the root artifacts {self.ROOT_ARTIFACTS}")
        dependencies = self.get_dependencies()
        logging.info(f"A total of {len(dependencies)} artifacts have been identified as dependencies of the artifacts {self.ROOT_ARTIFACTS}")
        archive_candidates = self.get_artifacts_to_archive(dependencies)
        artifacts_that_cannot_be_archived = self.get_artifacts_that_cannot_be_archived(archive_candidates)
        artifacts_to_archived = {artifact for artifact in archive_candidates if artifact not in artifacts_that_cannot_be_archived}
        logging.info(f"A total of {len(artifacts_to_archived)} artifacts have been identified for archival")
        logging.info(f"Of the artifacts to be archived, {len(artifacts_that_cannot_be_archived)} cannot be archived and should be deleted instead")
        artifacts_to_delete = self.get_artifacts_to_delete(artifacts_to_archived)
        logging.info(f"A total of {len(artifacts_to_delete)} archived artifacts have been marked for archival again, and should be safe to delete")
        logging.info(f"The following artifacts have been identified as a dependency of one of the root artifacts {self.ROOT_ARTIFACTS}")
        logging.info(json.dumps(list(dependencies), indent=4))
        logging.info(f"The following artifacts can be archived")
        logging.info(json.dumps(list(artifacts_to_archived), indent=4))
        logging.info(f"The following artifacts have been marked for archival but cannot be archived due to their structure, so will be deleted")
        logging.info(json.dumps(list(artifacts_that_cannot_be_archived), indent=4))
        logging.info(f"The following archived artifacts have been marked for archival again, so will be deleted")
        logging.info(json.dumps(list(artifacts_to_delete), indent=4))
        logging.info("Archiving artifacts")
        # Archive the artifacts
        #self.archive_artifacts(artifacts_to_archived)
        # Delete the artifacts
        #self.delete_artifacts(artifacts_to_delete.union(artifacts_that_cannot_be_archived))


if __name__ == "__main__":
    ArtifactArchiver().main()
