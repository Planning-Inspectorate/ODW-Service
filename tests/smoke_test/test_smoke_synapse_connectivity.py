from tests.util.notebook_run_test_case import NotebookRunTestCase
import tests.util.constants as constants
import json


class TestSmokeSynapseConnectivity(NotebookRunTestCase):
    """
        This test verifies that external connections from synapse are working properly
    """
    def test_synapse_connectivity(self):
        notebook_name = "test_smoke_py_connectivity"
        notebook_parameters = dict()

        notebook_run_result = self.run_notebook(notebook_name, notebook_parameters)
        error_message = (
            f"Expected the notebook's exit vallue to be '{constants.NOTEBOOK_EXIT_CODE_SUCCESS}', "
            f"but was '{notebook_run_result['result']['exitValue']}'"
        )
        assert notebook_run_result["result"]["exitValue"] == constants.NOTEBOOK_EXIT_CODE_SUCCESS, error_message
