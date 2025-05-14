import subprocess
from typing import List
import json
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
    def get_user(cls) -> str:
        """
            Return the name of the current user
        """
        exception = None
        try:
            return json.loads(os.popen('az account show').read())["user"]["name"]
        except json.JSONDecodeError as e:
            exception = e
        if exception:
            raise RuntimeError(f"Failed to decode output from `az account show` - please check you are signed in. Raised exception: {exception}")
