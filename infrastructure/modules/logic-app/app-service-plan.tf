resource "azurerm_service_plan" "logic_app" {
  count               = var.logic_app_enabled ? 1 : 0
  name                = "pins-service-plan-${local.resource_suffix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  os_type             = "Windows"
  sku_name            = "WS1"
  tags                = local.tags
}