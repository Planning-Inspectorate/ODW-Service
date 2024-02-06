resource "azurerm_application_insights" "synapse" {
  name                = "pins-appi-${local.resource_suffix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "other"
  retention_in_days   = var.log_retention_days
  workspace_id        = azurerm_log_analytics_workspace.synapse.id

  tags = local.tags
}

resource "azurerm_application_insights" "function_app_insights {
  for_each = {
    for function_app in var.function_app : function_app.name => function_app if var.function_app_enabled == true
  }

resource "azurerm_application_insights" "function_app_insights" {
  name                = pins-appi-[each.key]-${local.resource_suffix}
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
}
  tags = local.tags
}