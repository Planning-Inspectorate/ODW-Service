from pipelines.scripts.synapse_artifact.synapse_artifact_util_factory import SynapseArtifactUtilFactory
from pipelines.scripts.synapse_artifact.synapse_artifact_util import SynapseArtifactUtil
from pipelines.scripts.util import Util
from typing import Set, Dict, Any
import json
import logging
import os


logging.basicConfig(level=logging.INFO)


class ArtifactArchiver():
    def __init__(self):
        self.ARTIFACTS_TO_KEEP = {
            
        }
        """Artifacts that should not be marked for archival, even if they are identified as not being a dependency"""

        self.ROOT_ARTIFACTS = {
            "pipeline/pln_master.json"
        }
        """Artifacts to use as the base of the dependency analysis"""

        self.ARTIFACTS_TO_IGNORE = {
            "workspace/template-parameters-definition.json",
            "workspace/publish_config.json"
        }
        """Artifacts that should be skipped during all processing. i.e. artifacts that cannot be archived and should not affect processing"""

        self.ALL_ARTIFACT_NAMES = {
            path for path in Util.get_all_artifact_paths("workspace") if path not in self.ARTIFACTS_TO_IGNORE
        }
        """All json artifacts stored under the "./workspace" directory"""

        self.ALL_ARTIFACTS = {
            artifact_path: self._get_artifact_json(artifact_path)
            for artifact_path in self.ALL_ARTIFACT_NAMES
        }
        """All artifact json for the artifacts listed as part of ALL_ARTIFACT_NAMES"""

        self.ALL_ARCHIVEABLE_ARTIFACTS = {
            artifact_path
            for artifact_path in self.ALL_ARTIFACT_NAMES
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

        self.ALL_UNARCHIVEABLE_ARTIFACTS = {
            path
            for path in self.ALL_ARTIFACT_NAMES
            if path not in self.ALL_ARCHIVEABLE_ARTIFACTS
        }
        """Artifacts that cannot be archived. i.e. ALL_ARTIFACT_NAMES - ALL_ARCHIVEABLE_ARTIFACTS"""

        self.EXISTING_ARCHIVED_ARTIFACTS = {
            artifact_path
            for artifact_path in self.ALL_ARCHIVEABLE_ARTIFACTS
            if SynapseArtifactUtil.is_archived(self.ALL_ARTIFACTS.get(artifact_path))
        }
        """Artifacts that have already been marked as archived"""
    
    def _get_artifact_json(self, artifact_path: str) -> Dict[str, Any]:
        return json.load(open(artifact_path, "r"))

    def get_artifact(self, artifact_path: str) -> Dict[str, Any]:
        if f"workspace/{artifact_path}" not in self.ALL_ARTIFACTS:
            raise ValueError(f"No artifact json could be found for 'workspace/{artifact_path}'")
        return self.ALL_ARTIFACTS.get(f"workspace/{artifact_path}")

    def get_dependencies(self, artifact: str) -> Set[str]:
        """
            Deeply return all dependencies of the root artifacts

            :return: The set of dependencies for the the given artifact
        """
        discovered_artifacts = set()
        undiscovered_artifacts = {artifact}

        while undiscovered_artifacts:
            next_artifact_name = undiscovered_artifacts.pop()
            next_artifact_path = f"workspace/{next_artifact_name}"
            if next_artifact_path not in self.ALL_UNARCHIVEABLE_ARTIFACTS and next_artifact_path not in self.ALL_ARTIFACTS:
                raise ValueError(f"Could not find artifact with path 'workspace/{next_artifact_name}'")
            logging.info(f"Analysing the dependencies of '{next_artifact_name}'")
            new_artifact = self.get_artifact(next_artifact_name)
            artifact_type = next_artifact_name.split("/")[0]
            artifact_dependencies = SynapseArtifactUtilFactory.get(artifact_type).dependent_artifacts(new_artifact)
            new_dependencies = {
                dependency
                for dependency in artifact_dependencies
                if dependency not in discovered_artifacts and dependency != next_artifact_name
            }
            undiscovered_artifacts.update(new_dependencies)
            discovered_artifacts.add(next_artifact_name)
        return discovered_artifacts

    def get_artifacts_to_archive(self, dependencies: Set[str]) -> Set[str]:
        """
            Return all artifacts that can be archived

            :param dependencies: The set of dependencies identified by get_dependencies()
            :return: A set of all artifacts that can be archived, and a set of artifacts that can be archived but physically can't
        """
        return {
            artifact
            for artifact in self.ALL_ARTIFACT_NAMES
            if not (artifact in dependencies or artifact in self.ARTIFACTS_TO_KEEP or artifact in self.ROOT_ARTIFACTS)
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
            artifact.split("/")[1]: SynapseArtifactUtilFactory.get(artifact.split("/")[1])
            for artifact in artifacts_to_archive
        }
        for artifact in artifacts_to_archive:
            artifact_json = self.get_artifact(artifact)
            artifact_json = artifact_util_instances[artifact.split("/")[1]].archive(artifact_json)
            self._write_artifact(artifact, artifact_json)
    
    def _write_artifact(self, artifact_name: str, artifact_json: Dict[str, Any]):
        with open(f"workspace/{artifact_name}", "w") as f:
            json.dump(artifact_json, f, indent="\t", ensure_ascii=False)

    def delete_artifacts(self, artifacts_to_delete: Set[str]):
        """
            Delete the given artifacts
        """
        for artifact in artifacts_to_delete:
            os.remove(artifact)

    def main(self):
        """
            Identify artifacts that can be archived or deleted, and then archive/delete them
        """
        logging.info(f"Identifying the dependencies of the root artifacts {self.ROOT_ARTIFACTS}")
        # Get all artifacts that are essential for the ODW (i.e. all components related to the root artifacts)
        dependencies = set(self.ROOT_ARTIFACTS)
        for artifact in self.ROOT_ARTIFACTS:
            dependencies = dependencies.union(self.get_dependencies(artifact))
        logging.info(f"A total of {len(dependencies)} artifacts have been identified as dependencies of the artifacts {self.ROOT_ARTIFACTS}")
        # Get all artifacts that should not be archived (i.e. All components related to the ARTIFACTS_TO_KEEP)
        artifacts_to_keep = set(self.ARTIFACTS_TO_KEEP)
        for artifact in self.ARTIFACTS_TO_KEEP:
            artifacts_to_keep = artifacts_to_keep.union(self.get_dependencies(artifact))
        logging.info(f"A total of {len(artifacts_to_keep)} artifacts have been identified to be kept as dependencies of {self.ARTIFACTS_TO_KEEP}")
        # Get all artifacts that can be archived or deleted
        archive_candidates = self.get_artifacts_to_archive(dependencies.union(artifacts_to_keep))
        artifacts_that_cannot_be_archived = self.get_artifacts_that_cannot_be_archived(archive_candidates)
        artifacts_to_archived = archive_candidates.difference(artifacts_that_cannot_be_archived)
        logging.info(f"A total of {len(artifacts_to_archived)} artifacts have been identified for archival")
        logging.info(f"Of the artifacts to be archived, {len(artifacts_that_cannot_be_archived)} cannot be archived and should be deleted instead")
        artifacts_to_delete = self.get_artifacts_to_delete(artifacts_to_archived)
        artifacts_to_archived = artifacts_to_archived.difference(artifacts_to_delete)
        logging.info(f"A total of {len(artifacts_to_delete)} archived artifacts have been marked for archival again, and should be safe to delete")
        logging.info(f"The following artifacts have been identified as a dependency of one of the root artifacts {self.ROOT_ARTIFACTS}")
        logging.info(json.dumps(list(dependencies), indent=4))
        logging.info(f"The following artifacts have been identified as a dependency of one of the artifacts to keep {self.ARTIFACTS_TO_KEEP}")
        logging.info(json.dumps(list(artifacts_to_keep), indent=4))
        logging.info(f"The following artifacts can be archived")
        logging.info(json.dumps(list(artifacts_to_archived), indent=4))
        logging.info(f"The following artifacts have been marked for archival but cannot be archived due to their structure, so will be deleted")
        logging.info(json.dumps(list(artifacts_that_cannot_be_archived), indent=4))
        logging.info(f"The following archived artifacts have been marked for archival again, so will be deleted")
        logging.info(json.dumps(list(artifacts_to_delete), indent=4))
        logging.info("Archiving artifacts")
        # Archive the artifacts
        self.archive_artifacts(artifacts_to_archived)
        # Delete the artifacts
        self.delete_artifacts(artifacts_to_delete.union(artifacts_that_cannot_be_archived))


if __name__ == "__main__":
    ArtifactArchiver().main()
