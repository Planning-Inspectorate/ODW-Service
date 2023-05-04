# resource "azurerm_api_connection" "servicebus" {
#   count               = var.api_connection_servicebus_enabled ? 1 : 0
#   name                = "servicebus"
#   resource_group_name = var.resource_group_name
#   managed_api_id      = data.azurerm_managed_api.servicebus.id
#   display_name        = "ESB"

#   parameter_values = {
#     connectionString = var.connection_string_servicebus
#   }

#   tags = local.tags

#   lifecycle {
#     # NOTE: since the connectionString is a secure value it's not returned from the API
#     ignore_changes = [parameter_values]
#   }
# }

# resource "azurerm_api_connection" "zendesk" {
#   count               = var.api_connection_zendesk_enabled ? 1 : 0
#   name                = "zendesk"
#   resource_group_name = var.resource_group_name
#   managed_api_id      = data.azurerm_managed_api.zendesk.id
#   display_name        = "pinssupport"

#   parameter_values = {
#     connectionString = var.connection_string_zendesk
#   }

#   tags = local.tags

#   lifecycle {
#     # NOTE: since the connectionString is a secure value it's not returned from the API
#     ignore_changes = [parameter_values]
#   }
# }
