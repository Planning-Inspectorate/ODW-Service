resource "azurerm_api_connection" "api" {
  name                = var.name
  resource_group_name = var.resource_group_name
  managed_api_id      = data.azurerm_managed_api.example.id
  display_name        = var.display_name

  parameter_values = {
    connectionString = azurerm_servicebus_namespace.synapse.default_primary_connection_string
  }

  tags = {
    local.tags
  }

  lifecycle {
    # NOTE: since the connectionString is a secure value it's not returned from the API
    ignore_changes = ["parameter_values"]
  }
}