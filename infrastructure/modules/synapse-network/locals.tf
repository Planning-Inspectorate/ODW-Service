locals {
  module_name     = "synapse-network"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  devops_agent_subnet_service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.KeyVault"
  ]

  nsg_path = "providers/Microsoft.Network/networkSecurityGroups"

  networks_delegation = {
    for k, v in module.subnets.networks : k => {
      name    = v.name
      address = v.address_prefixes[0]
    }
  }

  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )
}
