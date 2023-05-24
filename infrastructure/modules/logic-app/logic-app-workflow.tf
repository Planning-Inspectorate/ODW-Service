resource "azurerm_logic_app_workflow" "zendesk_created" {
  count = var.logic_app_enabled ? 1 : 0

  name                = "zendesk-created"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
}

data "azurerm_managed_api" "zendesk-managed-api" {
  location = var.location
  name     = "zendesk"
}

resource "azurerm_api_connection" "zendesk_api_connection" {
  name                = "zendesk"
  resource_group_name = var.resource_group_name
  managed_api_id      = data.azurerm_managed_api.zendesk-managed-api.id
  display_name        = "pinssupport"

  parameter_values = {
    "token:Subdomain" = "pinssupport"
    "token:Client_secret" = "C9yZPMVcE5UPPTiundacEJ0wHyNGsKJuELvP07tD"
  }

  # lifecycle {
  #   ignore_changes = [
  #     parameter_values
  #   ]
  # }
}

# resource "azurerm_logic_app_workflow" "zendesk_updated" {
#   count               = var.logic_app_enabled ? 1 : 0
#   name                = "zendesk-updated"
#   location            = var.location
#   resource_group_name = var.resource_group_name
#   tags                = local.tags
# }
