resource "azurerm_resource_group" "logic_app" {
  count = var.logic_app_enabled ? 1 : 0

  name     = "pins-rg-logic-app-${local.resource_suffix}"
  location = module.azure_region.location_cli

  tags = local.tags
}

resource "azurerm_resource_group" "logic_app_failover" {
  count = var.failover_deployment ? 1 : 0

  name     = "pins-rg-logic-app-${local.resource_suffix_failover}"
  location = module.azure_region.paired_location.location_cli

  tags = local.tags
}

module "logic_app" {
  count = var.logic_app_enabled ? 1 : 0

  source = "./modules/logic-app"

  environment         = var.environment
  resource_group_name = azurerm_resource_group.logic_app[0].name
  location            = module.azure_region.location_cli
  logic_app_enabled   = var.logic_app_enabled
  service_bus_id      = module.synapse_ingestion.service_bus_namespace_id
  service_name        = local.service_name

  tags = local.tags
}

module "logic_app_failover" {
  count = var.logic_app_enabled && var.failover_deployment ? 1 : 0

  source = "./modules/logic-app"

  environment         = var.environment
  resource_group_name = azurerm_resource_group.logic_app_failover[0].name
  location            = module.azure_region.paired_location.location_cli
  service_bus_id      = module.synapse_ingestion.service_bus_namespace_id
  logic_app_enabled   = var.logic_app_enabled
  service_name        = local.service_name

  tags = local.tags
}
