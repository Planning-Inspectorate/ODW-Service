locals {
  module_name     = "synapse-data-lake"
  resource_suffix = "${var.service_name}-${var.environment}-${module.azure_region.location_short}"

  data_lake_role_assignments = flatten([
    for role, principals in var.data_lake_role_assignments : [
      for principal in principals : {
        role_definition_name = role
        principal_id         = principal
      }
    ]
  ])

  key_vault_role_assignments = flatten([
    for role, principals in var.key_vault_role_assignments : [
      for principal in principals : {
        role_definition_name = role
        principal_id         = principal
      }
    ]
  ])

  tags = merge(
    var.tags,
    {
      ModuleName = local.module_name
    }
  )

  azurerm_key_vault_synapse_vnet_subnet_ids = var.external_resource_links_enabled ? [
    var.vnet_subnet_ids[var.devops_agent_subnet_name],
    var.vnet_subnet_ids_failover[var.devops_agent_subnet_name],
    data.azurerm_subnet.horizon_database[0].id
    ] : [
    var.vnet_subnet_ids[var.devops_agent_subnet_name],
    var.vnet_subnet_ids_failover[var.devops_agent_subnet_name]
  ]
}
