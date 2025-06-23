import subprocess
from typing import List, Dict, Any, Tuple, Union
import json
import os
import logging
import struct
import pyodbc
from azure.identity import AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential


SQL_COPT_SS_ACCESS_TOKEN = 1256
SQL_SERVER_VERSION = 17
class Util:
    """
        Class that has useful utility functions
    """
    @classmethod
    def run_az_cli_command(cls, args: List[str]):
        """
            Run an az cli command. Raises a `RuntimeException` if something goes wrong
        """
        logging.info(f"Running command {' '.join(args)}")
        try:
            return subprocess.check_output(args)
        except subprocess.CalledProcessError as e:
            exception = e
        raise RuntimeError(f"Exception raised when running the above command: {exception.output.decode('utf-8')}")

    @classmethod
    def get_current_subscription_details(cls) -> Dict[str, Any]:
        """
            Return the output of `az account show`
        """
        cmd = "az account show"
        exception = None
        try:
            return json.loads(os.popen(cmd).read())
        except json.JSONDecodeError as e:
            exception = e
        raise RuntimeError(f"Failed to decode output from `{cmd}` - please check you are signed in. Raised exception: {exception}")

    @classmethod
    def get_subscription(cls) -> str:
        return cls.get_current_subscription_details()["name"]

    @classmethod
    def set_subscription(cls, subscription_name: str):
        cmd = f'az account set --subscription {subscription_name}'
        logging.info(f"Switching subscription to '{subscription_name}' via command '{cmd}'")
        os.popen(cmd).read()
        logging.info(f"Current subscription is '{cls.get_subscription()}'")

    @classmethod
    def get_current_user(cls) -> str:
        """
            Return the name of the current user
        """
        return cls.get_current_subscription_details()["user"]["name"]

    @classmethod
    def get_subscription_id(cls, subscription_name: str) -> str:
        """
            Return the id of the current subscription
        """
        subscriptions = json.loads(cls.run_az_cli_command(["az", "account", "subscription", "list", "--output", "json"]))
        for subscription in subscriptions:
            if subscription["displayName"] == subscription_name:
                return subscription["id"].replace("/subscriptions/", "")
        raise ValueError(f"Could not find a subscription with name '{subscription_name}'")

    @classmethod
    def get_odw_storage_accounts(cls, env: str) -> Dict[str, Any]:
        """
            Return the details of all ODW storage accounts
        """
        resource_group = f"pins-rg-data-odw-{env}-uks"
        command = f"az storage account list -g {resource_group}"
        return json.loads(cls.run_az_cli_command(command.split(" ")))

    @classmethod
    def get_odw_storage_account_names(cls, env: str) -> List[str]:
        """
            Return the names of all ODW storage accounts
        """
        return [
            storage_account["name"]
            for storage_account in cls.get_odw_storage_accounts(env)
        ]
    
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

    @classmethod
    def get_synapse_sql_pool_connection(cls, env: str, database: str = "master"):
        """
            Get a connection to a dedicated SQL pool registered with synapse
        """
        server = f"pins-synw-odw-{env}-uks-ondemand.sql.azuresynapse.net"
        return cls._get_connection(server, database)

    @classmethod
    def _get_connection(cls, server: str, database: str) -> 'pyodbc.Connection':
        """
            Get a pyodbc.Connection to a Synapse endpoint
        """
        managed_identity = ManagedIdentityCredential()
        azure_cli = AzureCliCredential()
        credential_chain = ChainedTokenCredential(managed_identity, azure_cli)
        database_token = credential_chain.get_token('https://database.windows.net/.default')
        tokenb = bytes(database_token[0], "UTF-8")
        exptoken = b''
        for i in tokenb:
            exptoken += bytes({i})
            exptoken += bytes(1)
        token_struct = struct.pack("=i", len(exptoken)) + exptoken
        conn_string = "Driver={ODBC Driver " + str(SQL_SERVER_VERSION) + " for SQL Server};SERVER=" + server + ";DATABASE=" + database + ""
        return pyodbc.connect(conn_string, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})

    @classmethod
    def submit_sql(cls, connection: 'pyodbc.Connection', sql: str) -> Union[List[Tuple[Any]], None]:
        """
            Execute an SQL query against the specified pyodbc connection

            :param connection: An active pyodbc connection. Ensure the connection is pointing to the right database beforehand
            :param query: The query to execute

            Example usage

            ```
            SynapseUtil.submit_sql_query(
                SynapseUtil.get_pool_connection(),
                "SELECT * FROM MY_TABLE"
            )
            ```
        """
        # Execute Query
        result = None
        cursor = connection.cursor()
        execution_result = cursor.execute(sql)
        try:
            result = execution_result.fetchall()
        except pyodbc.ProgrammingError:
            result = None
        connection.close()
        return result
