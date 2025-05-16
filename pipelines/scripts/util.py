import subprocess
from typing import List
import os


class Util:
    """
        Class that has useful utility functions
    """
    @classmethod
    def run_az_cli_command(cls, args: List[str]):
        """
            Run an az cli command. Raises a `RuntimeException` if something goes wrong
        """
        print(f"Running command: '{' '.join(args)}'")
        try:
            return subprocess.check_output(args)
        except subprocess.CalledProcessError as e:
            exception = e
        raise RuntimeError(f"Exception raised when running the above command: {exception.output.decode('utf-8')}")
    
    @classmethod
    def get_all_artifact_paths(cls, artifact_paths: List[str]) -> List[str]:
        """
            Return the paths to all artifacts under the given paths

            :param artifact_paths: Local artifact folder to include. e.g: `workspace/notebook`
        """
        return [
            os.path.join(path, name)
            for path, subdirs, files in os.walk("workspace")
            for name in files
            if any(
                os.path.join(path, name).startswith(x)
                for x in artifact_paths
            ) and name.endswith(".json")
        ]
