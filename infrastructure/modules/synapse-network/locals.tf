locals {
  module_name     = "synapse-network"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  devops_agent_subnet_service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.KeyVault"
  ]

  nsg_path = "providers/Microsoft.Network/networkSecurityGroups"

  subnets = flatten([for v in module.subnets.networks : [
    for subnet in v.subnets : {
      name = subnet.name
      cidr = subnet.cidr
    }
  ]])



  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )
}
