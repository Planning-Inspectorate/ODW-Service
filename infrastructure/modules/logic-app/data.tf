data "azurerm_managed_api" "service_bus_managed_api" {
  location = var.location
  name     = "servicebus"
}

data "azurerm_key_vault_secret" "zendesk_username" {
  count        = var.external_resource_links_enabled ? 1 : 0
  name         = "zendesk-service-username"
  key_vault_id = var.key_vault_id
}

data "azurerm_key_vault_secret" "zendesk_password" {
  count        = var.external_resource_links_enabled ? 1 : 0
  name         = "zendesk-service-password"
  key_vault_id = var.key_vault_id
}
