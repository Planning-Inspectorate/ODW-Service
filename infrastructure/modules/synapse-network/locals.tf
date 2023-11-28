locals {
  module_name     = "synapse-network"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  devops_agent_subnet_service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.KeyVault"
  ]

  nsg_path = "providers/Microsoft.Network/networkSecurityGroups"

  subnets = { for v in module.subnets.networks : v.name => merge(var.vnet_subnets, v) }


  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )
}
