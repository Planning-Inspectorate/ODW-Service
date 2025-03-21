resource "azurerm_monitor_activity_log_alert" "service_health" {
  name                = "Service Health"
  resource_group_name = var.resource_group_name
  scopes              = [var.alert_scope_service_health]
  description         = "Triggers an alert if the Azure Service Health changes"
  enabled             = var.alert_group_platform_enabled
  location            = "Global"

  criteria {
    category = "ServiceHealth"
    level    = "Informational"

    service_health {
      events = [
        "Incident",
        "Maintenance",
        "ActionRequired",
        "Security"
      ]
      locations = [
        module.azure_region.location
      ]
    }
  }

  action {
    action_group_id = azurerm_monitor_action_group.platform_alerts.id
  }

  tags = local.tags
}
