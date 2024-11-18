"""
Unit tests for the workspace functions
"""

def test_get_notebook():
    """
    Tests the get_notebook function
    """

    from workspace_functions import get_notebook

    notebook_name = "py_retry_logic"

    result = get_notebook(notebook_name)

    # Assertions
    assert isinstance(result, dict), "The response does not match the expected type."
    assert result['name'] == notebook_name