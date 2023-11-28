locals {
  module_name     = "synapse-network"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  devops_agent_subnet_service_endpoints = [
    "Microsoft.Storage",
    "Microsoft.KeyVault"
  ]

  nsg_path = "providers/Microsoft.Network/networkSecurityGroups"

  subnets = flatten([
    for subnet in var.vnet_subnets : [
      {
        name               = subnet.name
        new_bits           = subnet.new_bits
        cidr_block         = module.subnets.network_cidr_blocks[subnet.name]
        service_delegation = subnet.service_delegation
      }
    ]
  ])

  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )
}
