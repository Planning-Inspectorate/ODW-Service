from tests.util.config import TEST_CONFIG
from azure.identity import AzureCliCredential
from azure.keyvault.secrets import SecretClient
from tests.util.test_case import TestCase
import requests
import pytest
import json


class TestAzureFunctions(TestCase):
    KEY_VAULT_CLIENT = SecretClient(vault_url=f"https://pinskvsynwodw{TEST_CONFIG['ENV'].lower()}uks.vault.azure.net", credential=AzureCliCredential())

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
        function_name = test_parameters.get("function_name")
        url_parameters = test_parameters.get("url_parameters", dict())
        function_secret_name = f"function-url-{function_name.replace('-', '')}"
        function_url = f"{self.KEY_VAULT_CLIENT.get_secret(function_secret_name).value}{url_parameters}"
        response = requests.get(function_url)
        assert response.status_code == 200, f"Expected the status code to be 200, but was '{response.status_code}'"
        parsed_json = json.loads(response.text)
        assert len(parsed_json) > 0, "Expected the JSON response to have some content, but it was empty"
