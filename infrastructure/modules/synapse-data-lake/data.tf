data "azurerm_client_config" "current" {}

data "azurerm_function_app" "function_app" {
  name                = var.function_app_name
  resource_group_name = var.function_app_resource_group_name
}
