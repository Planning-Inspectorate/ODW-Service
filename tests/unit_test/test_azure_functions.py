from tests.util.notebook_run_test_case import NotebookRunTestCase
import pytest


class TestAzureFunctions(NotebookRunTestCase):
    @pytest.mark.parametrize(
        "test_parameters",
        [
            {
                "function_name": "getDaRT",
                "url_parameters": "&caseReference=&applicationReference="
            },
            {
                "function_name": "gettimesheets",
                "url_parameters": "&searchCriteria="
            },
        ]
    )
    def test_azure_function_calls(self, test_parameters: str):
        self.run_notebook("py_unit_tests_azure_functions", test_parameters)
