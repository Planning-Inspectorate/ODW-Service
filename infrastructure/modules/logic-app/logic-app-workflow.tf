resource "azurerm_logic_app_workflow" "zendesk_created" {
  count               = var.workflow_zendesk_created_enabled ? 1 : 0
  name                = "zendesk-created"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
}

resource "azurerm_logic_app_workflow" "zendesk_updated" {
  count               = var.workflow_zendesk_updated_enabled ? 1 : 0
  name                = "zendesk-created"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
}
