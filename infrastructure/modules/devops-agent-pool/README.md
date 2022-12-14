# Azure DevOps Agent Pool
This module provisions an Azure DevOps agent pool into the specified a specified subnet.

### Table of Contents
1. [Usage](#usage)
2. [Requirements](#requirements)
3. [Providers](#Providers)
4. [Inputs](#inputs)
5. [Outputs](#outputs)

## Usage
The below module definition provides an example of usage. This module is designed to depend on the outputs from the associated `synapse_network` module. This associated module provisions the Synapse virtual network resources. This module then deploys a Virtual Machine Scale Set which may be linked to Azure DevOps for the running of Pipelines internal to the Azure network. This arrangement allows for platform deployments for resources which are not publically accessible.
```
module "devops_agent_pool" {
  source = "./modules/devops-agent-pool"
  environment         = "dev"
  resource_group_name = azurerm_resource_group.example.name
  location            = "uks"
  service_name        = "odw"
  deploy_agent_pool         = true
  devops_agent_image_prefix = "devops-agents"
  devops_agent_instances    = 1
  devops_agent_subnet_name  = "ComputeSubnet"
  devops_agent_vm_sku       = "Standard_F2s_v2"
  vnet_subnet_ids           = module.synapse_network.vnet_subnets
  depends_on = [
    module.synapse_network
  ]
  tags = local.tags
}
```

| :scroll: Note |
|----------|
| This module is designed to work differently depending on whether the environment is being provisioned for the first time or not. A special Azure DevOps pipeline may be used to run a targetted Teraform deployment for this module with `deploy_agent_pool` set to `false` to first deploy network resources (dependencies) followed by a second deployment to provision the agent pool. |

<!-- BEGINNING OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 3.27.0 |
| <a name="provider_random"></a> [random](#provider\_random) | 3.4.3 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_azure_region"></a> [azure\_region](#module\_azure\_region) | claranet/regions/azurerm | 5.1.0 |

## Resources

| Name | Type |
|------|------|
| [azurerm_linux_virtual_machine_scale_set.devops_agent_pool](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_virtual_machine_scale_set) | resource |
| [azurerm_resource_group.devops_agents](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group) | resource |
| [random_password.devops_agent_password](https://registry.terraform.io/providers/hashicorp/random/latest/docs/resources/password) | resource |
| [azurerm_image.azure_agents](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/image) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_deploy_agent_pool"></a> [deploy\_agent\_pool](#input\_deploy\_agent\_pool) | A switch to determine whether the devops agent VM Scale Set should be deployed | `bool` | `true` | no |
| <a name="input_devops_agent_image_prefix"></a> [devops\_agent\_image\_prefix](#input\_devops\_agent\_image\_prefix) | The name prefix used to identify the devops agent image | `string` | `"devops-agents"` | no |
| <a name="input_devops_agent_instances"></a> [devops\_agent\_instances](#input\_devops\_agent\_instances) | The base number of devops agents in the VM Scale Set | `number` | `2` | no |
| <a name="input_devops_agent_subnet_name"></a> [devops\_agent\_subnet\_name](#input\_devops\_agent\_subnet\_name) | The name of the subnet into which the devops agent VM Scale Set will be deployed | `string` | n/a | yes |
| <a name="input_devops_agent_username"></a> [devops\_agent\_username](#input\_devops\_agent\_username) | The username of the devops agent local account | `string` | `"agent_user"` | no |
| <a name="input_devops_agent_vm_sku"></a> [devops\_agent\_vm\_sku](#input\_devops\_agent\_vm\_sku) | The size of the devops agent VMs to be deployed | `string` | `"Standard_F2s_v2"` | no |
| <a name="input_environment"></a> [environment](#input\_environment) | The name of the environment in which resources will be deployed | `string` | n/a | yes |
| <a name="input_location"></a> [location](#input\_location) | The short-format Azure region into which resources will be deployed | `string` | n/a | yes |
| <a name="input_resource_group_name"></a> [resource\_group\_name](#input\_resource\_group\_name) | The name of the resource group into which resources will be deployed | `string` | n/a | yes |
| <a name="input_service_name"></a> [service\_name](#input\_service\_name) | The short-format name of the overarching service being deployed | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | A collection of tags to assign to taggable resources | `map(string)` | `{}` | no |
| <a name="input_vnet_subnet_ids"></a> [vnet\_subnet\_ids](#input\_vnet\_subnet\_ids) | A map of subnet names and IDs comprising the linked Virtual Network | `map(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_resource_group_name"></a> [resource\_group\_name](#output\_resource\_group\_name) | The name of the resource group deployed in this module |
<!-- END OF PRE-COMMIT-TERRAFORM DOCS HOOK -->
