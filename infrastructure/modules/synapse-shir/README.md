# Synapse Self-Hosted Integration Runtime
This module provisions an VM to work as a Self-Hosted Integration Runtime for Synapse.

### Table of Contents
- [Synapse Self-Hosted Integration Runtime](#synapse-self-hosted-integration-runtime)
    - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Requirements](#requirements)
  - [Providers](#providers)
  - [Modules](#modules)
  - [Resources](#resources)
  - [Inputs](#inputs)
  - [Outputs](#outputs)

## Usage

<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 4.14.0 |
| <a name="provider_random"></a> [random](#provider\_random) | 3.6.3 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_azure_region"></a> [azure\_region](#module\_azure\_region) | claranet/regions/azurerm | 5.1.0 |

## Resources

| Name | Type |
|------|------|
| [azurerm_network_interface.shir](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_interface) | resource |
| [azurerm_role_assignment.shir_vm](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_role_assignment.terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/role_assignment) | resource |
| [azurerm_storage_account.shir](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account) | resource |
| [azurerm_storage_account_queue_properties.shir](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account_queue_properties) | resource |
| [azurerm_storage_blob.deploy_script](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_blob) | resource |
| [azurerm_storage_blob.openjdk_script](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_blob) | resource |
| [azurerm_storage_blob.runtime_script](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_blob) | resource |
| [azurerm_storage_container.shir](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_container) | resource |
| [azurerm_synapse_integration_runtime_self_hosted.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/synapse_integration_runtime_self_hosted) | resource |
| [azurerm_windows_virtual_machine.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/windows_virtual_machine) | resource |
| [random_password.shir_vm_administrator_password](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password) | resource |
| [random_string.unique_id](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/string) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_devops_agent_subnet_name"></a> [devops\_agent\_subnet\_name](#input\_devops\_agent\_subnet\_name) | The name of the subnet into which the devops agent VM Scale Set will be deployed | `string` | n/a | yes |
| <a name="input_environment"></a> [environment](#input\_environment) | The name of the environment in which resources will be deployed | `string` | n/a | yes |
| <a name="input_location"></a> [location](#input\_location) | The short-format Azure region into which resources will be deployed | `string` | n/a | yes |
| <a name="input_resource_group_name"></a> [resource\_group\_name](#input\_resource\_group\_name) | The name of the resource group into which resources will be deployed | `string` | n/a | yes |
| <a name="input_runtime_vm_image"></a> [runtime\_vm\_image](#input\_runtime\_vm\_image) | An object describing the image specification to use for the self-hosted integration runtime VM | `map(string)` | <pre>{<br>  "offer": "WindowsServer",<br>  "publisher": "MicrosoftWindowsServer",<br>  "sku": "2022-datacenter-azure-edition-core",<br>  "version": "latest"<br>}</pre> | no |
| <a name="input_runtime_vm_size"></a> [runtime\_vm\_size](#input\_runtime\_vm\_size) | The size of the self-hosted integration runtime VM to be deployed | `string` | `"Standard_F2s_v2"` | no |
| <a name="input_runtime_vm_username"></a> [runtime\_vm\_username](#input\_runtime\_vm\_username) | The Windows administrator username for the self-hosted integration runtime VM | `string` | `"shiradmin"` | no |
| <a name="input_service_name"></a> [service\_name](#input\_service\_name) | The short-format name of the overarching service being deployed | `string` | n/a | yes |
| <a name="input_synapse_workspace_id"></a> [synapse\_workspace\_id](#input\_synapse\_workspace\_id) | The ID of the Synapse Workspace to register the self-hosted integration runtime with | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | A collection of tags to assign to taggable resources | `map(string)` | `{}` | no |
| <a name="input_vnet_subnet_ids"></a> [vnet\_subnet\_ids](#input\_vnet\_subnet\_ids) | A map of subnet names and IDs comprising the linked Virtual Network | `map(string)` | n/a | yes |
| <a name="input_run_shir_setup_script"></a> [run\_shir\_setup\_script](#input\_run\_shir\_setup\_script) | If the SHIR setup script should be triggered on start-up of the VM | `bool` | n/a | yes |

## Outputs

No outputs.
<!-- END_TF_DOCS -->
