data "azurerm_managed_api" "servicebus" {
  name     = "servicebus"
  location = var.location
}

data "azurerm_managed_api" "zendesk" {
  name     = "zendesk"
  location = var.location
}
