import shutil
import os
import argparse
from typing import List


"""
    Script to detect which files have been modified by the current branch, and to copy these to a separate folder
"""


def get_all_files() -> List[str]:
    """
        Return all files under the current directory
    """
    return [
        os.path.join(path, name)
        for path, subdirs, files in os.walk("./")
        for name in files
    ]


def get_modified_files(target_branch: str) -> List[str]:
    """
        Return all files modified between the current branch and the target branch in the remote repo
    """
    return [x for x in os.popen(f"git diff --name-only origin/{target_branch}").read().split("\n") if x]


if __name__ == "__main__":
    # Load command line arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-tb", "--target_branch", help="Branch to compare the current branch against")
    parser.add_argument("-tf", "--target_folder", help="Where to copy the modified files")
    parser.add_argument("-fd", "--full_deployment", help="Whether or not all files should be considered modified", default=False)
    args = parser.parse_args()
    target_branch = args.target_branch
    target_folder = args.target_folder
    full_deployment = True if str(args.full_deployment).lower() == "true" else False

    # Collect the files modified between the current branch and the target branch
    if full_deployment:
        modified_files = get_all_files()
    else:
        modified_files = get_modified_files(target_branch)

    # Copy all modified files to the specified target folder
    print(f"Copying modified files to folder '{target_folder}'")
    os.mkdir(target_folder)
    for file_path in modified_files:
        print(f"    Copying '{file_path}'")
        file_path_split = file_path.split("/")[:-1]
        parent_folder = target_folder
        for subfolder in file_path_split:
            next_folder = f"{parent_folder}/{subfolder}"
            if not os.path.exists(next_folder):
                os.mkdir(next_folder)
            parent_folder = next_folder
        try:
            shutil.copy(file_path, f"{target_folder}/{file_path}")
        except FileNotFoundError as e:
            print(f"    Could not copy '{file_path}' - it has been deleted")
