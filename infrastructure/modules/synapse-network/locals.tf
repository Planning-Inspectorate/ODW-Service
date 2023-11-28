locals {
  module_name     = "synapse-network"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  devops_agent_subnet_service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.KeyVault"
  ]

  nsg_path = "providers/Microsoft.Network/networkSecurityGroups"

  subnets = { for k, v in module.subnets.network_cidr_blocks : k => merge(var.var.vnet_subnets[k], { service_delegation = v.service_delegation }) }

  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )
}
