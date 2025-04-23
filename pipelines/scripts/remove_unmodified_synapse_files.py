from pipelines.scripts.synapse_artifact.synapse_artifact_util_factory import SynapseArtifactUtilFactory
from pipelines.scripts.synapse_artifact.synapse_workspace_util import SynapseWorkspaceUtil
from typing import Set, Iterable, Dict, Any
import argparse
import json
import os
import logging


logging.basicConfig(level=logging.INFO)


class Util():
    def __init__(self, workspace_name: str):
        self.workspace_name = workspace_name
        self.local_workspace = "my_local_workspace"
    
    def remove_unmodified_files(self):
        SynapseWorkspaceUtil().download_workspace(synapse_workspace, self.local_workspace)
        modified_files = self._get_modified_files(self.local_workspace)
        logging.info(f"Total modified files: {len(modified_files)}")
        self._delete_modified_files(modified_files)
        #shutil.rmtree(local_workspace)

    def _get_all_files_under_folder(self, folder: str):
        """
            Return all leaf files in under the target folder

            :param folder: Folder to start from
        """
        return {
            os.path.join(path, name).replace(f"{folder}/", "", 1)
            for path, subdirs, files in os.walk(folder)
            for name in files
        }

    def _compare_live_and_local_artifacts(self, artifact_name: str):
        """
            Compare the local artifacts to the locally-downloaded live workspace

            :param artifact_name: Name of the artifact to compare
            :return: True if the artifacts match and both exist, False otherwise
        """
        local_artifact_name = f"workspace/{artifact_name}"
        live_artifact_name = f"{self.local_workspace}/{artifact_name}"
        if not os.path.exists(local_artifact_name):
            return False
        if not os.path.exists(live_artifact_name):
            return False
        local_workspace_file = json.load(open(local_artifact_name, "r"))
        live_workspace_file = json.load(open(live_artifact_name, "r"))
        artifact_type = artifact_name.replace("workspace/", "").split("/")[0]
        artifact_util = SynapseArtifactUtilFactory.get(artifact_type)(self.workspace_name)
        return artifact_util.compare(local_workspace_file, live_workspace_file)

    def _get_modified_files(self, live_workspace_local_download_folder: str) -> Set[str]:
        """
            Return all Synapse workspace files modified between the `workspace` folder and the `live_workspace_local_download_folder` folder

            :param live_workspace_local_download_folder: The folder where the live Synapse workspace was downloaded to locally
        """
        live_file_names = self._get_all_files_under_folder(live_workspace_local_download_folder)
        workspace_file_names = self._get_all_files_under_folder("workspace")

        new_files = workspace_file_names - live_file_names
        deleted_files = live_file_names - workspace_file_names
        common_files = (workspace_file_names - deleted_files) - new_files

        modified_files = {
            file
            for file in common_files
            if not self._compare_live_and_local_artifacts(file)
        }
        diff = modified_files.union(new_files)
        logging.info(f"Total files in local workspace: {len(workspace_file_names)}")
        logging.info(f"Total files in the live workspace {len(live_file_names)}")
        logging.info(f"Total files common between local and live workspace {len(common_files)}")
        logging.info(f"Total common files that have modifications: {len(modified_files)}")
        logging.info(f"Total number of files that have been modified or created: {len(diff)}")
        logging.info("The below files do not exist in the live workspace")
        logging.info(json.dumps(list(new_files), indent=4))
        logging.info("The below files exist in the live workspace but do not exist locally")
        logging.info(json.dumps(list(deleted_files), indent=4))
        logging.info("The below files have been modified in the local workspace")
        logging.info(json.dumps(list(modified_files), indent=4))
        return diff

    def _delete_modified_files(self, modified_files: Iterable[str]):
        """
            Delete all files under `workspace/` that have not been modified

            :param modified_files: The file names that have been modified
        """
        logging.info("Deleting unmodified files")
        all_files = self._get_all_files_under_folder("workspace")
        for file in all_files:
            if file not in modified_files:
                logging.info(f"    Deleting file '{file}'")
                #os.remove(f"workspace/{file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-sw", "--synapse_workspace", help="The synapse workspace to check against")
    parser.add_argument("-fd", "--full_deployment", default=False, action="store_true", help="Whether or not this should be a full deployment")
    parser.add_argument("--no_full_deployment", dest="full_deployment", action="store_false")
    args = parser.parse_args()
    synapse_workspace = args.synapse_workspace
    full_deployment = args.full_deployment
    if not full_deployment:
        Util(synapse_workspace).remove_unmodified_files()
