"""
Functions to interact with Azure Synapse
"""
import os
import json
import asyncio
import timeit
import sys

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


def get_objects_from_branch(object_type: str) -> list | str:
    """
    Function to get all objects from the main branch.
    Fetches the names of all the json files from the folders in the workspace folder.
    """

    json_files = []

    script_dir = os.path.dirname(__file__)
    object_path = os.path.join(script_dir, f"../workspace/{object_type}")

    if not os.path.exists(object_path):
        print(f"Error: The folder {object_path} does not exist.")
        return []

    json_files.extend([file for file in os.listdir(object_path)])

    return f"{len(json_files)} {object_type}"


async def fetch_objects(
    session: aiohttp.ClientSession, workspace_url: str, object_type: str
) -> str:
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

    return f"{len(object_list)} {object_type}"


async def main():
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

    async with aiohttp.ClientSession(headers=_headers) as session:
        tasks = [
            fetch_objects(session, _SYNAPSE_ENDPOINT, object_type)
            for object_type in object_types
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        for object_type, result in zip(object_types, results):
            if isinstance(result, Exception):
                print(f"Error fetching {object_type}: {result}")
            else:
                print(result)


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

# def main():
#     """
#     Main function for fetching folder contents
#     """
#     object_types = ['dataset',
#                'linkedService',
#                'notebook',
#                'pipeline',
#                'sqlScript',
#                'trigger']

#     for object_type in object_types:
#         pprint.pprint(get_objects_from_branch(object_type))

# if __name__ == "__main__":
#     main()
