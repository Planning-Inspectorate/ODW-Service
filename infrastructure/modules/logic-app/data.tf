data "azurerm_managed_api" "zendesk-managed-api" {
  location = var.location
  name     = "zendesk"
}

data "azurerm_managed_api" "service-bus-managed-api" {
  location = var.location
  name     = "servicebus"
}