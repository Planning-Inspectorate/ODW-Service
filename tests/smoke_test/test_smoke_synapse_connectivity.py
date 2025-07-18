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

        self.run_notebook(notebook_name, notebook_parameters)
