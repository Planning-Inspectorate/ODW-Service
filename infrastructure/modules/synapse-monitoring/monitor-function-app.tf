resource "azurerm_monitor_diagnostic_setting" "function_app" {
  for_each = {
    for function_app in var.function_app : function_app.name => function_app if var.function_app_enabled == true
  }

  name                       = "Function App Logs - ${each.key}"
  target_resource_id         = module.function_app[each.key].id
  log_analytics_workspace_id = azurerm_log_analytics_workspace.synapse.id


  enabled_log {
    category = "FunctionAppLogs"
  }

  metric {
    category = "AllMetrics"
  }
}
