resource "azurerm_app_service_plan" "logic_app" {
  count               = var.logic_app_enabled ? 1 : 0
  name                = "pins-logic-app-${local.resource_suffix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags

  sku {
    tier = "Standard"
    size = "WS1"
  }
}