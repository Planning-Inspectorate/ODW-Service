resource "azurerm_api_connection" "zendesk_api_connection" {
  name                = "zendesk"
  resource_group_name = var.resource_group_name
  managed_api_id      = data.azurerm_managed_api.zendesk_managed_api.id
  display_name        = "pinssupport"

  parameter_values = {
    "token:Subdomain" = "pinssupport"
  }

  lifecycle {
    ignore_changes = [
      parameter_values
    ]
  }
}

resource "azurerm_api_connection" "service_bus_api_connection" {
  name                = "servicebus"
  resource_group_name = var.resource_group_name
  managed_api_id      = data.azurerm_managed_api.service_bus_managed_api.id
  display_name        = "servicebus"

  parameter_values = {
    "name" : "managedIdentityAuth",
    "values" : {
      "namespaceEndpoint" : {
        "value" : "sb://pins-sb-odw-dev-uks-b9rt9m.servicebus.windows.net"
      }
    }
  }

  lifecycle {
    ignore_changes = [
      parameter_values
    ]
  }
}
