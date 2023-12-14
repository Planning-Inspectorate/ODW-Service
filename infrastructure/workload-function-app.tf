resource "azurerm_resource_group" "function_app" {
  count = var.function_app_enabled ? 1 : 0

  name     = "pins-rg-function-app-${local.resource_suffix}"
  location = module.azure_region.location_cli

  tags = local.tags
}

resource "azurerm_resource_group" "function_app_failover" {
  count = var.function_app_enabled && var.failover_deployment ? 1 : 0

  name     = "pins-rg-function-app-${local.resource_suffix_failover}"
  location = module.azure_region.paired_location.location_cli

  tags = local.tags
}

module "service_plan" {
  count = var.function_app_enabled ? 1 : 0

  source = "./modules/service-plan"

  resource_group_name = azurerm_resource_group.function_app[0].name
  service_name        = local.service_name
  environment         = var.environment
  location            = module.azure_region.location_cli
  tags                = local.tags
}

module "service_plan_failover" {
  count = var.function_app_enabled && var.failover_deployment ? 1 : 0

  source = "./modules/service-plan"

  resource_group_name = azurerm_resource_group.function_app_failover[0].name
  service_name        = local.service_name
  environment         = var.environment
  location            = module.azure_region.paired_location.location_cli
  tags                = local.tags
}

module "storage_account" {
  count = var.function_app_enabled ? 1 : 0

  source = "./modules/storage-account"

  resource_group_name                     = azurerm_resource_group.function_app[0].name
  service_name                            = local.service_name
  environment                             = var.environment
  location                                = module.azure_region.location_cli
  tags                                    = local.tags
  network_rules_enabled                   = true
  network_rule_virtual_network_subnet_ids = concat([module.synapse_network.vnet_subnets[local.functionapp_subnet_name], module.synapse_network.vnet_subnets[local.compute_subnet_name]])
  shares = [
    {
      name  = "pins-${var.function_app_name}-${local.resource_suffix}"
      quota = 5120
    }
  ]
}

module "storage_account_failover" {
  count = var.function_app_enabled && var.failover_deployment ? 1 : 0

  source = "./modules/storage-account"

  resource_group_name                     = azurerm_resource_group.function_app_failover[0].name
  service_name                            = local.service_name
  environment                             = var.environment
  location                                = module.azure_region.paired_location.location_cli
  tags                                    = local.tags
  network_rules_enabled                   = true
  network_rule_virtual_network_subnet_ids = concat([module.synapse_network_failover.vnet_subnets[local.functionapp_subnet_name], module.synapse_network_failover.vnet_subnets[local.compute_subnet_name]])
  shares = [
    {
      name  = "pins-${var.function_app_name}-${local.resource_suffix_failover}"
      quota = 5120
    }
  ]
}

module "function_app" {
  count = var.function_app_enabled ? 1 : 0

  source = "./modules/function-app"

  resource_group_name        = azurerm_resource_group.function_app[0].name
  function_app_name          = var.function_app_name
  service_name               = local.service_name
  service_plan_id            = module.service_plan[0].id
  storage_account_name       = module.storage_account[0].storage_name
  storage_account_access_key = module.storage_account[0].primary_access_key
  environment                = var.environment
  location                   = module.azure_region.location_cli
  tags                       = local.tags
  synapse_vnet_subnet_names  = module.synapse_network.vnet_subnets
  app_settings               = var.function_app_settings
  site_config                = var.function_app_site_config
  file_share_name            = "pins-${var.function_app_name}-${local.resource_suffix}"
  servicebus_namespace       = var.odt_back_office_service_bus_name
}

module "function_app_failover" {
  count = var.function_app_enabled && var.failover_deployment ? 1 : 0

  source = "./modules/function-app"

  resource_group_name        = azurerm_resource_group.function_app_failover[0].name
  function_app_name          = var.function_app_name
  service_name               = local.service_name
  service_plan_id            = module.service_plan_failover[0].id
  storage_account_name       = module.storage_account_failover[0].storage_name
  storage_account_access_key = module.storage_account_failover[0].primary_access_key
  environment                = var.environment
  location                   = module.azure_region.paired_location.location_cli
  tags                       = local.tags
  synapse_vnet_subnet_names  = module.synapse_network_failover.vnet_subnets
  app_settings               = var.function_app_settings
  site_config                = var.function_app_site_config
  file_share_name            = "pins-${var.function_app_name}-${local.resource_suffix_failover}"
  servicebus_namespace       = var.odt_back_office_service_bus_name_failover
}

resource "azurerm_role_assignment" "servicebus_receiver" {
  for_each = var.odt_back_office_service_bus_enabled ? one(module.odt_backoffice_sb).subscription_ids : {}

  scope                = each.value
  role_definition_name = "Azure Service Bus Data Receiver"
  principal_id         = var.failover_deployment ? module.function_app_failover[0].identity[0].principal_id : module.function_app[0].identity[0].principal_id
}
output "functioan_app_idenitity" {
  description = "The identity of the Function App"
  value       = var.failover_deployment ? module.function_app_failover[0].identity[0].principal_id : module.function_app[0].identity[0].principal_id
}
