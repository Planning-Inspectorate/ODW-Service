"""
Unit tests for the workspace functions
"""

from aioresponses import aioresponses
import aiohttp
import pytest

NOTEBOOK_NAME = "test_notebook"

def test_get_notebook(requests_mock) -> None:
    """
    Tests the get_notebook function
    """
    url = f"https://pins-synw-odw-dev-uks.dev.azuresynapse.net/notebooks/{NOTEBOOK_NAME}?api-version=2020-12-01"
    requests_mock.get(url, json={"name": f"{NOTEBOOK_NAME}"}, status_code=200)
    from workspace_functions import get_notebook
    response = get_notebook(NOTEBOOK_NAME)
    assert response['name'] == NOTEBOOK_NAME
    assert isinstance(response, dict)


def test_delete_notebook_200(requests_mock) -> None:
    """
    Tests the delete_notebook function for a 200 status code
    """
    url = f"https://pins-synw-odw-dev-uks.dev.azuresynapse.net/notebooks/{NOTEBOOK_NAME}?api-version=2020-12-01"
    requests_mock.delete(url, json = {"message": "OK"}, status_code = 200)
    from workspace_functions import delete_notebook
    response = delete_notebook(NOTEBOOK_NAME)
    assert response["message"] == "OK"


def test_delete_notebook_201(requests_mock) -> None:
    """
    Tests the delete_notebook function for a 201 status code
    """
    url = f"https://pins-synw-odw-dev-uks.dev.azuresynapse.net/notebooks/{NOTEBOOK_NAME}?api-version=2020-12-01"
    requests_mock.delete(url, json = {"message": "Accepted"}, status_code = 201)
    from workspace_functions import delete_notebook
    response = delete_notebook(NOTEBOOK_NAME)
    assert response["message"] == "Accepted"


def test_delete_notebook_204(requests_mock) -> None:
    """
    Tests the delete_notebook function for a 204 status code
    """
    url = f"https://pins-synw-odw-dev-uks.dev.azuresynapse.net/notebooks/{NOTEBOOK_NAME}?api-version=2020-12-01"
    requests_mock.delete(url, status_code = 204)
    from workspace_functions import delete_notebook
    response = delete_notebook(NOTEBOOK_NAME)
    assert response is None


@pytest.mark.asyncio
async def test_fetch_objects():
    """
    Tests the fetch_objects function with paginated responses
    """
    from workspace_functions import fetch_objects

    workspace_url = "https://example-workspace-url"
    object_type = "datasets"
    first_url = f"{workspace_url}/{object_type}/?api-version=2020-12-01"
    next_url = f"{workspace_url}/{object_type}/page2?api-version=2020-12-01"

    # Define mock responses for the paginated API
    with aioresponses() as mock:
        # First page response
        mock.get(
            first_url,
            payload={
                "value": [{"name": "dataset1"}, {"name": "dataset2"}],
                "nextLink": next_url,
            },
        )
        # Second page response
        mock.get(
            next_url,
            payload={
                "value": [{"name": "dataset3"}],
                "nextLink": None,
            },
        )

        # Use an aiohttp client session for the test
        async with aiohttp.ClientSession() as session:
            # Call the function
            result = await fetch_objects(session, workspace_url, object_type)

    # Assertions
    assert result == ["dataset1", "dataset2", "dataset3"]


from workspace_functions import compare_json_files
import os

script_dir: str = os.path.dirname(__file__)
object_path: str = os.path.join(script_dir, "../workspace/notebook/")

file1= f"{object_path}/aie_document_data.json"
file2 = f"{object_path}/appeal_event.json"
compare_json_files(file1=file1, file2=file2)