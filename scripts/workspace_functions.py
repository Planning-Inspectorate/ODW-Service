"""
Functions to interact with Azure Synapse objects
"""
import os
import json
import asyncio
import timeit
import sys
import glob

# to track coroutine allocation for event loop handling
# an issue when running in Jupyter notebooks only
import tracemalloc
from azure.identity import DefaultAzureCredential
import requests
import aiohttp
import nest_asyncio

tracemalloc.start()

_CREDENTIAL: DefaultAzureCredential = DefaultAzureCredential()
_API_VERSION: str = "2020-12-01"
_SYNAPSE_ENDPOINT: str = "https://pins-synw-odw-dev-uks.dev.azuresynapse.net/"
_token: str = _CREDENTIAL.get_token("https://dev.azuresynapse.net/.default").token

_headers: dict = {
    "Authorization": f"Bearer {_token}",
    "Content-Type": "application/json",
}
_timeout: int = 5


def delete_notebook(notebook: str) -> dict:
    """
    Deletes a notebook from Synapse Live Mode in the target workspace
    """
    notebook_url = (
        f"{_SYNAPSE_ENDPOINT}/notebooks/{notebook}?api-version={_API_VERSION}"
    )
    response = requests.delete(notebook_url, headers=_headers, timeout=_timeout)
    return response.json()


def get_notebook(notebook: str) -> dict:
    """
    Gets a notebook from Synapse Live Mode in the target workspace
    """
    notebook_url = (
        f"{_SYNAPSE_ENDPOINT}/notebooks/{notebook}?api-version={_API_VERSION}"
    )
    response = requests.get(notebook_url, headers=_headers, timeout=_timeout)
    return response.json()


def create_or_update_notebook(notebook: str) -> dict:
    """
    This currently doesn't work.
    Error: Notebook cells must be defined in the payload
    """
    notebook_url = (
        f"{_SYNAPSE_ENDPOINT}/notebooks/{notebook}?api-version={_API_VERSION}"
    )
    script_dir = os.path.dirname(__file__)
    notebook_path = os.path.join(script_dir, f"../workspace/notebook/{notebook}.json")
    with open(notebook_path, "r", encoding="utf-8") as file:
        notebook_data = json.load(file)

    request_body = {"name": notebook, "properties": notebook_data}

    response = requests.put(
        notebook_url, headers=_headers, json=request_body, timeout=_timeout
    )
    return response.json()


async def list_json_files(object_type: str) -> list[str]:
    """
    List all JSON file names in the folder corresponding to the object_type asynchronously.
    """
    script_dir = os.path.dirname(__file__)
    object_path = os.path.join(script_dir, f"../workspace/{object_type}")

    if not os.path.exists(object_path):
        print(f"Error: The folder {object_path} does not exist.")
        return []

    # Use asyncio.to_thread to run the blocking operation in a separate thread
    json_files = await asyncio.to_thread(glob.glob, os.path.join(object_path, "*.json"))

    # Extract file names (just the name, not the full path, and remoe the .json extension to accurately compare with the workspace names)
    file_names = [os.path.splitext(os.path.basename(file))[0] for file in json_files]

    return file_names


async def fetch_objects(
    session: aiohttp.ClientSession, workspace_url: str, object_type: str
) -> list[str]:
    """
    Fetch all objects of a given type with pagination.
    """
    object_list = []
    url = f"{workspace_url}/{object_type}/?api-version={_API_VERSION}"

    while url:
        async with session.get(url, timeout=_timeout) as response:
            response_json = await response.json()
            object_list.extend(obj["name"] for obj in response_json.get("value", []))
            url = response_json.get("nextLink")

    return object_list


def compare_lists(fetched_objects: list, json_files: list) -> tuple:
    """
    Compare two lists (fetched_objects and json_files) and return the missing items from each list.
    """

    set_objects = set(fetched_objects)
    set_json_files = set(json_files)

    # Find items in fetched_objects but not in json_files
    missing_from_json_files = set_objects - set_json_files
    # Find items in json_files but not in fetched_objects
    missing_from_fetched_objects = set_json_files - set_objects

    return missing_from_json_files, missing_from_fetched_objects


async def main() -> None:
    """
    Main function to list all objects concurrently using asyncio.
    """
    object_types = [
        "notebooks",
        "datasets",
        "linkedservices",
        "pipelines",
        "sqlScripts",
        "triggers",
    ]

    object_data = {}

    async with aiohttp.ClientSession(headers=_headers) as session:
        tasks = [
            fetch_objects(session, _SYNAPSE_ENDPOINT, object_type)
            for object_type in object_types
        ]

        # remove the last letter 's' for the folder names
        json_folders = [folder[:-1] for folder in object_types]

        tasks += [list_json_files(folder) for folder in json_folders]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        fetched_objects = results[
            : len(object_types)
        ]  # First set of results: fetched objects
        json_files = results[len(object_types) :]  # Second set of results: JSON files

        for idx, object_type in enumerate(object_types):
            object_data[object_type] = {
                "fetched_objects": fetched_objects[idx],
                "json_files": json_files[idx],
            }

        for object_type in object_types:
            fetched = object_data[object_type]["fetched_objects"]
            files = object_data[object_type]["json_files"]
            missing_from_json, missing_from_objects = compare_lists(fetched, files)

            print(f"Comparing {object_type}:")

            if missing_from_json:
                print(f"In workspace but not in main branch: {missing_from_json}")
            else:
                print("No items missing from main branch.")

            if missing_from_objects:
                print(f"In main branch but not in workspace: {missing_from_objects}")
            else:
                print("No items missing from workspace.")

            print()


def run_main():
    """
    Function to call the async main function.
    Used for timeit to get the execution time.
    This is not possible with async functions.
    """
    asyncio.run(main())


if __name__ == "__main__":
    if sys.stdout.isatty():
        # For standard script execution, e.g. in terminal or DevOps pipeline
        NUMBER_OF_EXECUTIONS = 1
        total_time = timeit.timeit(run_main, number=NUMBER_OF_EXECUTIONS)
        average_time = total_time / NUMBER_OF_EXECUTIONS
        print(f"Average execution time: {average_time:.4f} seconds")
    else:
        try:
            asyncio.run(main())
        # Handle existing loop in Jupyter
        except RuntimeError:
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
