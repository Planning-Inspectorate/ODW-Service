# Synapse Network
This module deploys a virtual network and private DNS zone to enable the Synapse Workspace and associated resources to be deployed privately.

### Table of Contents
1. [Usage](#usage)
2. [Requirements](#requirements)
3. [Providers](#Providers)
4. [Inputs](#inputs)
5. [Outputs](#outputs)

## Usage
The below module definition provides an example of usage.

```
module "synapse_network" {
  source = "./modules/synapse-network"

  environment         = var.environment
  resource_group_name = azurerm_resource_group.network.name
  location            = module.azure_region.location_cli
  service_name        = local.service_name

  network_watcher_enabled = true
  vnet_base_cidr_block    = "10.10.0.0/24"
  vnet_subnets            = [
    {
      name     = "ManagementSubnet"
      new_bits = 2
    },
    {
      name     = "SynapseEndpointSubnet"
      new_bits = 2
    },
    {
      name     = null
      new_bits = 2
    },
    {
      name     = null
      new_bits = 2
    }
  ]

  tags = local.tags
}
```

| :scroll: Note |
|----------|
| This module uses the HashiCorp `subnets` module to determine the subnet size CIDR ranges. |

<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_azurerm"></a> [azurerm](#provider\_azurerm) | 4.14.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_azure_region"></a> [azure\_region](#module\_azure\_region) | claranet/regions/azurerm | 5.1.0 |
| <a name="module_subnets"></a> [subnets](#module\_subnets) | hashicorp/subnets/cidr | 1.0.0 |

## Resources

| Name | Type |
|------|------|
| [azurerm_network_security_group.nsg](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_group) | resource |
| [azurerm_network_watcher.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_watcher) | resource |
| [azurerm_subnet.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet) | resource |
| [azurerm_subnet_network_security_group_association.nsg](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/subnet_network_security_group_association) | resource |
| [azurerm_virtual_network.synapse](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_network) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_devops_agent_subnet_name"></a> [devops\_agent\_subnet\_name](#input\_devops\_agent\_subnet\_name) | The name of the subnet into which the devops agents will be deployed | `string` | `"ComputeSubnet"` | no |
| <a name="input_environment"></a> [environment](#input\_environment) | The name of the environment in which resources will be deployed | `string` | n/a | yes |
| <a name="input_location"></a> [location](#input\_location) | The short-format Azure region into which resources will be deployed | `string` | n/a | yes |
| <a name="input_network_watcher_enabled"></a> [network\_watcher\_enabled](#input\_network\_watcher\_enabled) | Determines whether a Network Watcher resource will be deployed | `bool` | `false` | no |
| <a name="input_resource_group_id"></a> [resource\_group\_id](#input\_resource\_group\_id) | The ID of the resource group into which resources will be deployed | `string` | n/a | yes |
| <a name="input_resource_group_name"></a> [resource\_group\_name](#input\_resource\_group\_name) | The name of the resource group into which resources will be deployed | `string` | n/a | yes |
| <a name="input_service_name"></a> [service\_name](#input\_service\_name) | The short-format name of the overarching service being deployed | `string` | n/a | yes |
| <a name="input_synapse_private_endpoint_subnet_name"></a> [synapse\_private\_endpoint\_subnet\_name](#input\_synapse\_private\_endpoint\_subnet\_name) | The name of the subnet into which Synapse private endpoints should be deployed | `string` | `"SynapseEndpointSubnet"` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | A collection of tags to assign to taggable resources | `map(string)` | `{}` | no |
| <a name="input_vnet_base_cidr_block"></a> [vnet\_base\_cidr\_block](#input\_vnet\_base\_cidr\_block) | The base IPv4 range for the Virtual Network in CIDR notation | `string` | `"10.90.0.0/24"` | no |
| <a name="input_vnet_subnets"></a> [vnet\_subnets](#input\_vnet\_subnets) | A collection of subnet definitions used to logically partition the Virtual Network | <pre>list(object({<br>    name              = string<br>    new_bits          = number<br>    service_endpoints = list(string)<br>    service_delegation = list(object({<br>      delegation_name = string<br>      actions         = list(string)<br>    }))<br>  }))</pre> | <pre>[<br>  {<br>    "name": "AzureBastionSubnet",<br>    "new_bits": 4,<br>    "service_delegation": [],<br>    "service_endpoints": []<br>  },<br>  {<br>    "name": "FunctionAppSubnet",<br>    "new_bits": 4,<br>    "service_delegation": [<br>      {<br>        "actions": [<br>          "Microsoft.Network/virtualNetworks/subnets/action"<br>        ],<br>        "delegation_name": "Microsoft.Web/serverFarms"<br>      }<br>    ],<br>    "service_endpoints": [<br>      "Microsoft.Storage",<br>      "Microsoft.KeyVault"<br>    ]<br>  },<br>  {<br>    "name": "SynapseEndpointSubnet",<br>    "new_bits": 2,<br>    "service_delegation": [],<br>    "service_endpoints": []<br>  },<br>  {<br>    "name": "ComputeSubnet",<br>    "new_bits": 2,<br>    "service_delegation": [],<br>    "service_endpoints": [<br>      "Microsoft.Storage",<br>      "Microsoft.KeyVault"<br>    ]<br>  },<br>  {<br>    "name": "ApimSubnet",<br>    "new_bits": 2,<br>    "service_delegation": [],<br>    "service_endpoints": []<br>  }<br>]</pre> | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_devops_agent_subnet_name"></a> [devops\_agent\_subnet\_name](#output\_devops\_agent\_subnet\_name) | The name of the subnet into which the devops agents will be deployed |
| <a name="output_synapse_private_endpoint_subnet_name"></a> [synapse\_private\_endpoint\_subnet\_name](#output\_synapse\_private\_endpoint\_subnet\_name) | The name of the subnet into which Synapse private endpoints should be deployed |
| <a name="output_vnet_id"></a> [vnet\_id](#output\_vnet\_id) | The ID of the Virtual Network deployed in this module |
| <a name="output_vnet_name"></a> [vnet\_name](#output\_vnet\_name) | The name of the Virtual Network deployed in this module |
| <a name="output_vnet_security_groups"></a> [vnet\_security\_groups](#output\_vnet\_security\_groups) | A map of subnet names to network security group names deployed in this module |
| <a name="output_vnet_subnet_ids"></a> [vnet\_subnet\_ids](#output\_vnet\_subnet\_ids) | A list of subnet IDs deployed in this module |
| <a name="output_vnet_subnet_prefixes"></a> [vnet\_subnet\_prefixes](#output\_vnet\_subnet\_prefixes) | A map of subnet names to CIDR ranges deployed in this module |
| <a name="output_vnet_subnets"></a> [vnet\_subnets](#output\_vnet\_subnets) | A map of subnet names to IDs deployed in this module |
<!-- END_TF_DOCS -->
