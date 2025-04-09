import shutil
import os
import argparse
from typing import List, Set


"""
    Script to detect which files have been modified by the current branch, and to remove unfiles from the local file system
    This is required so that the synapse artifact only contains new files so that the deployment is faster
"""


def get_all_synapse_files() -> List[str]:
    """
        Return all files under the current directory
    """
    return [
        os.path.join(path, name).replace("./", "")
        for path, subdirs, files in os.walk("./")
        for name in files
        if "workspace/" not in name
    ]


def get_modified_files(target_branch: str) -> Set[str]:
    """
        Return all files modified between the current branch and the target branch in the remote repo
    """
    return {x for x in os.popen(f"git diff --name-only origin/{target_branch}").read().split("\n") if x}


if __name__ == "__main__":
    # Load command line arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-tb", "--target_branch", help="Branch to compare the current branch against")
    parser.add_argument("-fd", "--full_deployment", help="Whether or not all files should be considered modified", default=False)
    args = parser.parse_args()
    target_branch = args.target_branch
    full_deployment = True if str(args.full_deployment).lower() == "true" else False

    # Collect the files modified between the current branch and the target branch
    if full_deployment:
        modified_files = []
    else:
        modified_files = get_modified_files(target_branch)
    
    # Delete all unmodified files
    all_files = get_all_synapse_files()
    for file in all_files:
        if file not in modified_files and file != "pipelines/scripts/delete_unmodified_files.py" and not file.startswith(".git"):
            print(f"Deleting file '{file}'")
            os.remove(file)
