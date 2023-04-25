resource "azurerm_resource_group" "logic_app" {
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
  source = "./modules/logic-app"

  api_connection_servicebus2_enabled = var.api_connection_servicebus2_enabled
  api_connection_zendesk_enabled     = var.api_connection_zendesk_enabled
  environment                        = var.environment
  resource_group_name                = azurerm_resource_group.logic_app.name
  location                           = module.azure_region.location_cli
  service_name                       = local.service_name

  logic_app_service_plan_enabled = var.logic_app_service_plan_enabled
  logic_app_standard_enabled     = var.logic_app_standard_enabled
  workflow_names                 = var.workflow_names

  tags = local.tags
}

module "logic_app_failover" {
  count = var.failover_deployment ? 1 : 0

  source = "./modules/logic-app"

  api_connection_servicebus2_enabled = var.api_connection_servicebus2_enabled
  api_connection_zendesk_enabled     = var.api_connection_zendesk_enabled
  # api_connection_display_name        = var.api_connection_display_name
  # api_connection_name                = var.api_connection_name
  environment         = var.environment
  resource_group_name = azurerm_resource_group.logic_app_failover[0].name
  location            = module.azure_region.paired_location.location_cli
  service_name        = local.service_name

  logic_app_service_plan_enabled = var.logic_app_service_plan_enabled
  logic_app_standard_enabled     = var.logic_app_standard_enabled
  workflow_names                 = var.workflow_names

  tags = local.tags
}
