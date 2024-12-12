# Synapse Data Lake

### Table of Contents
1. [Usage](#usage)
2. [Requirements](#requirements)
3. [Providers](#Providers)
4. [Inputs](#inputs)
5. [Outputs](#outputs)

## Usage

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.5.7, < 1.10.0 |
| <a name="requirement_azurerm"></a> [azurerm](#requirement\_azurerm) | >= 3.0, < 5.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 4.13.0 |
| <a name="provider_azurerm.horizon"></a> [azurerm.horizon](#provider\_azurerm.horizon) | 4.13.0 |
| <a name="provider_random"></a> [random](#provider\_random) | 3.6.3 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_azure_region"></a> [azure\_region](#module\_azure\_region) | claranet/regions/azurerm | 5.1.0 |

## Resources

| Name | Type |
|------|------|
| [azurerm_key_vault.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault) | resource |
| [azurerm_key_vault_secret.data_lake_storage_account_key](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault_secret) | resource |
| [azurerm_private_endpoint.data_lake](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/private_endpoint) | resource |
| [azurerm_role_assignment.data_lake](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_role_assignment.function_app](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_role_assignment.key_vault](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_role_assignment.key_vault_terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_role_assignment.terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_storage_account.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account) | resource |
| [azurerm_storage_account_network_rules.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account_network_rules) | resource |
| [azurerm_storage_account_queue_properties.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account_queue_properties) | resource |
| [azurerm_storage_container.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_container) | resource |
| [azurerm_storage_data_lake_gen2_filesystem.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_data_lake_gen2_filesystem) | resource |
| [azurerm_storage_management_policy.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_management_policy) | resource |
| [random_string.unique_id](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/string) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config) | data source |
| [azurerm_subnet.horizon_database](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/subnet) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_data_lake_account_tier"></a> [data\_lake\_account\_tier](#input\_data\_lake\_account\_tier) | The tier of the Synapse data lake Storage Account | `string` | `"Standard"` | no |
| <a name="input_data_lake_lifecycle_rules"></a> [data\_lake\_lifecycle\_rules](#input\_data\_lake\_lifecycle\_rules) | A list of objects describing data lifecycle rules for the Synapse data lake Storage Account | `list(any)` | `[]` | no |
| <a name="input_data_lake_private_endpoint_dns_zone_id"></a> [data\_lake\_private\_endpoint\_dns\_zone\_id](#input\_data\_lake\_private\_endpoint\_dns\_zone\_id) | The ID of the Private DNS Zone hosting privatelink.dfs.core.windows.net | `string` | n/a | yes |
| <a name="input_data_lake_replication_type"></a> [data\_lake\_replication\_type](#input\_data\_lake\_replication\_type) | The replication type for the Synapse data lake Storage Account | `string` | `"ZRS"` | no |
| <a name="input_data_lake_retention_days"></a> [data\_lake\_retention\_days](#input\_data\_lake\_retention\_days) | The number of days blob and queue data will be retained for upon deletion | `number` | `7` | no |
| <a name="input_data_lake_role_assignments"></a> [data\_lake\_role\_assignments](#input\_data\_lake\_role\_assignments) | An object mapping RBAC roles to principal IDs for the data lake Storage Account | `map(list(string))` | `{}` | no |
| <a name="input_data_lake_storage_containers"></a> [data\_lake\_storage\_containers](#input\_data\_lake\_storage\_containers) | A list of container names to be created in the Synapse data lake Storage Account | `list(string)` | <pre>[<br>  "default"<br>]</pre> | no |
| <a name="input_devops_agent_subnet_name"></a> [devops\_agent\_subnet\_name](#input\_devops\_agent\_subnet\_name) | The name of the subnet into which the devops agents will be deployed | `string` | `"ComputeSubnet"` | no |
| <a name="input_environment"></a> [environment](#input\_environment) | The name of the environment in which resources will be deployed | `string` | n/a | yes |
| <a name="input_firewall_allowed_ip_addresses"></a> [firewall\_allowed\_ip\_addresses](#input\_firewall\_allowed\_ip\_addresses) | A list of CIDR ranges to be permitted access to the data lake Storage Account | `list(string)` | `[]` | no |
| <a name="input_function_app_principal_ids"></a> [function\_app\_principal\_ids](#input\_function\_app\_principal\_ids) | The principal ID's of the function app identity | `any` | n/a | yes |
| <a name="input_function_app_subnet_name"></a> [function\_app\_subnet\_name](#input\_function\_app\_subnet\_name) | The name of the subnet into which the function apps will be deployed | `string` | `"FunctionAppSubnet"` | no |
| <a name="input_horizon_integration_config"></a> [horizon\_integration\_config](#input\_horizon\_integration\_config) | The configuration for integration with Horizon and associated systems | <pre>object({<br>    networking = object({<br>      resource_group_name  = string<br>      vnet_name            = string<br>      database_subnet_name = string<br>    })<br>  })</pre> | n/a | yes |
| <a name="input_key_vault_role_assignments"></a> [key\_vault\_role\_assignments](#input\_key\_vault\_role\_assignments) | An object mapping RBAC roles to principal IDs for Key Vault | `map(list(string))` | `{}` | no |
| <a name="input_location"></a> [location](#input\_location) | The short-format Azure region into which resources will be deployed | `string` | n/a | yes |
| <a name="input_network_resource_group_name"></a> [network\_resource\_group\_name](#input\_network\_resource\_group\_name) | The name of the resource group into which private endpoints will be deployed | `string` | n/a | yes |
| <a name="input_resource_group_name"></a> [resource\_group\_name](#input\_resource\_group\_name) | The name of the resource group into which resources will be deployed | `string` | n/a | yes |
| <a name="input_service_name"></a> [service\_name](#input\_service\_name) | The short-format name of the overarching service being deployed | `string` | n/a | yes |
| <a name="input_synapse_private_endpoint_subnet_name"></a> [synapse\_private\_endpoint\_subnet\_name](#input\_synapse\_private\_endpoint\_subnet\_name) | The name of the subnet into which Synapse private endpoints should be deployed | `string` | `"SynapseEndpointSubnet"` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | A collection of tags to assign to taggable resources | `map(string)` | `{}` | no |
| <a name="input_tenant_id"></a> [tenant\_id](#input\_tenant\_id) | The ID of the Azure AD tenant containing the identities used for RBAC assignments | `string` | n/a | yes |
| <a name="input_vnet_subnet_ids"></a> [vnet\_subnet\_ids](#input\_vnet\_subnet\_ids) | A map of subnet names and IDs comprising the linked Virtual Network | `map(string)` | n/a | yes |
| <a name="input_vnet_subnet_ids_failover"></a> [vnet\_subnet\_ids\_failover](#input\_vnet\_subnet\_ids\_failover) | A map of subnet names and IDs comprising the linked Virtual Network | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_data_lake_account_id"></a> [data\_lake\_account\_id](#output\_data\_lake\_account\_id) | The ID of the Data Lake Storage Account |
| <a name="output_data_lake_account_name"></a> [data\_lake\_account\_name](#output\_data\_lake\_account\_name) | The name of the Data Lake Storage Account |
| <a name="output_data_lake_dfs_endpoint"></a> [data\_lake\_dfs\_endpoint](#output\_data\_lake\_dfs\_endpoint) | The DFS endpoint URL of the Data Lake Storage Account |
| <a name="output_data_lake_filesystem_id"></a> [data\_lake\_filesystem\_id](#output\_data\_lake\_filesystem\_id) | The ID of the Data Lake Gen2 filesystem |
| <a name="output_key_vault_id"></a> [key\_vault\_id](#output\_key\_vault\_id) | The ID of the Key Vault |
| <a name="output_key_vault_name"></a> [key\_vault\_name](#output\_key\_vault\_name) | The name of the Key Vault |
| <a name="output_key_vault_uri"></a> [key\_vault\_uri](#output\_key\_vault\_uri) | The URI of the Key Vault |
<!-- END_TF_DOCS -->
