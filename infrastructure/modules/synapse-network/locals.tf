locals {
  module_name     = "synapse-network"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  devops_agent_subnet_service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.KeyVault"
  ]

  nsg_path = "providers/Microsoft.Network/networkSecurityGroups"

  subnets = { for k, v in var.vnet_subnets :
    k => {
      cidr_subnet_offset = v.new_bits
      name               = v.name
      service_delegation = v.service_delegation
    }
  }

  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )
}
