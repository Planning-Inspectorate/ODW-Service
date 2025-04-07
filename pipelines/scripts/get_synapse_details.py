import os
import json
import argparse
from typing import List, Dict, Any, Callable


def get_storage_accounts(resource_group_name: str):
    args = [
        f'--resource-group "{resource_group_name}"',
    ]
    return json.loads(os.popen(f'az storage account list {" ".join(args)}').read())

def get_key_vaults(resource_group_name: str):
    args = [
        f'--resource-group "{resource_group_name}"',
    ]
    return json.loads(os.popen(f'az keyvault list {" ".join(args)}').read())


def get_services_buses(resource_group_name: str):
    args = [
        f'--resource-group "{resource_group_name}"',
    ]
    return json.loads(os.popen(f'az servicebus namespace list {" ".join(args)}').read())


def get_synapse_workspace(resource_group_name: str):
    args = [
        f'--resource-group "{resource_group_name}"',
    ]
    return json.loads(os.popen(f'az synapse workspace list {" ".join(args)}').read())


def get_resource(resource_type: str, resource_group_name: str, resource_name_prefix: str, optional: bool = False):
    resource_type_function_map = {
        "Blob Storage": get_storage_accounts,
        "Key Vault": get_key_vaults,
        "Service Bus": get_services_buses,
        "Synapse Workspace": get_synapse_workspace
    }
    if resource_type not in resource_type_function_map:
        raise ValueError(f"No resource getter defined for resource_type {resource_type}")
    all_resources = resource_type_function_map[resource_type](resource_group_name)
    print(json.dumps(all_resources, indent = 4))
    candidate_resources = [x for x in all_resources if x.startswith(resource_name_prefix)]
    if len(candidate_resources) != 1:
        if optional and not candidate_resources:
            return None
        raise ValueError(
            f"Expected only a single {resource_type} resource to match the prefix {resource_name_prefix}, but there were {len(candidate_resources)}"
        )
    return candidate_resources[0]


if __name__ == "__main__":
    # Load command line arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-e", "--env", help="Environment to run against")
    parser.add_argument("f", "--failover_deployment", help="If this is a backup deployment", default=False)
    args = parser.parse_args()
    env = args.env
    failover_deployment = bool(args.failover_deployment)

    # Set resource group during processing based on Terraform logic
    base_resource_group = f"pins-rg-data-odw-{env}-uks"
    base_backup_resource_group = ""

    if failover_deployment:
        resource_group = base_backup_resource_group
        backup_resource_group = base_resource_group
    else:
        resource_group = base_resource_group
        backup_resource_group = base_backup_resource_group

    # Extract relevant Azure resources
    main_datalake = get_resource("Blob Storage", resource_group, f"pinsrgdataodw{env}uks")
    backup_datalake = get_resource("Blob Storage", resource_group, f"pinsrgdataodw{env}uksbackup", optional=True)
    key_vault = get_resource("Key Vault", resource_group, f"")
    service_bus = get_resource("Service Bus", resource_group, f"")
    synapse_workspace = get_resource("Synapse Workspace", resource_group, f"")
    
    # Save variables to Azure Pipeline
    variables = {
        "data_lake_account_id": main_datalake["id"],
        "data_lake_account_id_failover": backup_datalake["id"],
        "data_lake_account_name": main_datalake["name"],
        "data_lake_dfs_endpoint": main_datalake["primaryEndpoints"]["blob"],
        "data_lake_dfs_endpoint_failover": backup_datalake["primaryEndpoints"]["blob"],
        "data_resource_group_name": f"pins-rg-data-odw-{env}-uks",
        "key_vault_uri": "",
        "service_bus_namespace_name": "",
        "synapse_dev_endpoint": "",
        "synapse_dsql_endpoint": "",
        "synapse_ssql_endpoint": "",
        "synapse_workspace_name": ""
    }
    for variable_name, variable_value in variables.items():
        print(f'##vso[task.setvariable variable=variable_name;]{variable_value}')
