from pipelines.scripts.synapse_artifact.synapse_artifact_util_factory import SynapseArtifactUtilFactory
from azure.identity import AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential
from itertools import repeat
from typing import Set, List, Iterable, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor
import argparse
import requests
import json
import os
import shutil
import logging


logging.basicConfig(level=logging.INFO)


class SynapseWorkspaceUtil:
    """
        Tool to handle using the Synapse REST API to query a Synapse workspace
    """
    def download_workspace(self, workspace_name: str, local_folder: str):
        """
            Download the full json content of the live Synapse workspace, and save it uner `local_folder/`
        """
        if os.path.exists(local_folder):
            shutil.rmtree(local_folder)
        synapse_artifact_names = [
            f
            for f in os.listdir("workspace")
            if os.path.isdir(os.path.join("workspace", f))
        ]
        artifact_util_classes = {
            type_name: SynapseArtifactUtilFactory.get(type_name)(workspace_name)
            for type_name in synapse_artifact_names
            if SynapseArtifactUtilFactory.is_valid_type_name(type_name)
        }
        # Filter out any artifacts that had no associated util class
        synapse_artifact_names = [x for x in synapse_artifact_names if x in artifact_util_classes]
        get_artifacts = lambda type_name: artifact_util_classes[type_name].download_live_workspace(local_folder)
        os.makedirs(local_folder)
        with ThreadPoolExecutor() as tpe:
            # Download all artifacts in parallel
            [
                thread_response
                for thread_response in tpe.map(get_artifacts, synapse_artifact_names)
                if thread_response
            ]


def get_all_files_under_folder(folder: str):
    """
        Return all leaf files in under the target folder

        Parameters
        - folder: Folder to start from
    """
    return {
        os.path.join(path, name).replace(f"{folder}/", "", 1)
        for path, subdirs, files in os.walk(folder)
        for name in files
    }


def get_modified_files(live_workspace_local_download_folder: str) -> Set[str]:
    """
        Return all Synapse workspace files modified between the `workspace` folder and the `live_workspace_local_download_folder` folder

        Parameters
        - live_workspace_local_download_folder: The folder where the live Synapse workspace was downloaded to locally
    """
    live_file_names = get_all_files_under_folder(live_workspace_local_download_folder)
    workspace_file_names = get_all_files_under_folder("workspace")

    new_files = workspace_file_names - live_file_names
    deleted_files = live_file_names - workspace_file_names
    common_files = (workspace_file_names - deleted_files) - new_files

    live_files = {
        file_name: json.dumps(json.load(open(f"{live_workspace_local_download_folder}/{file_name}", "r")), sort_keys=True)
        for file_name in common_files
    }
    workspace_files = {
        file_name: json.dumps(json.load(open(f"workspace/{file_name}", "r")), sort_keys=True)
        for file_name in common_files
    }
    modified_files = {
        file_name
        for file_name, file in workspace_files.items()
        if file != live_files[file_name]
    }
    diff = modified_files.union(new_files)
    logging.info("The below files have been added")
    logging.info(json.dumps(list(new_files), indent=4))
    logging.info("The below files have been deleted")
    logging.info(json.dumps(list(deleted_files), indent=4))
    logging.info("The below files have been modified")
    logging.info(json.dumps(list(modified_files), indent=4))
    return diff


def delete_modified_files(modified_files: Iterable[str]):
    """
        Delete all files under `workspace/` that have not been modified

        Parameters
        - modified_files: The file names that have been modified
    """
    logging.info("Deleting unmodified files")
    all_files = get_all_files_under_folder("workspace")
    for file in all_files:
        if file not in modified_files:
            logging.info(f"    Deleting file '{file}'")
            #os.remove(f"workspace/{file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-sw", "--synapse_workspace", help="The synapse workspace to check against")
    args = parser.parse_args()
    synapse_workspace = args.synapse_workspace
    local_workspace = "my_local_workspace"
    SynapseWorkspaceUtil().download_workspace(synapse_workspace, local_workspace)
    modified_files = get_modified_files(local_workspace)
    logging.info(f"Total modified files: {len(modified_files)}")
    delete_modified_files(modified_files)
    #shutil.rmtree(local_workspace)
