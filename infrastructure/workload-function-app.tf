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

module "sp" {
  count = var.function_app_enabled ? 1 : 0

  source = "./modules/service-plan"

  resource_group_name = azurerm_resource_group.function_app[count.index].name
  service_name        = local.service_name
  environment         = var.environment
  location            = module.azure_region.location_cli
  tags                = local.tags
}

module "sp_failover" {
  count = var.function_app_enabled && var.failover_deployment ? 1 : 0

  source = "./modules/service-plan"

  resource_group_name = azurerm_resource_group.function_app_failover[count.index].name
  service_name        = local.service_name
  environment         = var.environment
  location            = module.azure_region.paired_location.location_cli
  tags                = local.tags
}

module "storage_account" {
  count = var.function_app_enabled ? 1 : 0

  source = "./modules/storage-account"

  resource_group_name = azurerm_resource_group.function_app[count.index].name
  service_name        = local.service_name
  environment         = var.environment
  location            = module.azure_region.location_cli
  tags                = local.tags
}

module "storage_account_failover" {
  count = var.function_app_enabled && var.failover_deployment ? 1 : 0

  source = "./modules/storage-account"

  resource_group_name = azurerm_resource_group.function_app_failover[count.index].name
  service_name        = local.service_name
  environment         = var.environment
  location            = module.azure_region.paired_location.location_cli
  tags                = local.tags
}

module "function_app" {
  count = var.function_app_enabled ? 1 : 0

  source = "./modules/function-app"

  resource_group_name        = azurerm_resource_group.function_app[count.index].name
  function_app_name          = var.function_app_name
  service_name               = local.service_name
  app_service_plan_id        = module.sp[0].id
  storage_account_name       = module.storage_account[0].storage_name
  storage_account_access_key = module.storage_account[0].primary_access_key
  environment                = var.environment
  location                   = module.azure_region.paired_location.location_cli
  tags                       = local.tags
  app_settings               = var.function_app_settings
  site_config                = var.function_app_site_config
}

module "function_app_failover" {
  count = var.function_app_enabled && var.failover_deployment ? 1 : 0

  source = "./modules/function-app"

  resource_group_name        = azurerm_resource_group.function_app_failover[count.index].name
  function_app_name          = var.function_app_name
  service_name               = local.service_name
  app_service_plan_id        = module.sp_failover[0].id
  storage_account_name       = module.storage_account_failover[0].storage_name
  storage_account_access_key = module.storage_account_failover[0].primary_access_key
  environment                = var.environment
  location                   = module.azure_region.paired_location.location_cli
  tags                       = local.tags
  app_settings               = var.function_app_settings
  site_config                = var.function_app_site_config
}
