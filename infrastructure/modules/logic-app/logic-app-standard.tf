resource "azurerm_logic_app_standard" "logic_app" {
  count = var.logic_app_standard_enabled ? 1 : 0

  name                       = "pins-logic-app-${local.resource_suffix}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  app_service_plan_id        = azurerm_service_plan.logic_app[count.index].id
  storage_account_name       = azurerm_storage_account.logic_app.name
  storage_account_access_key = azurerm_storage_account.logic_app.primary_access_key

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"     = "node"
    "WEBSITE_NODE_DEFAULT_VERSION" = "~18"
  }

  tags = local.tags
}
