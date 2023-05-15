# resource "azurerm_role_assignment" "logic_app_standard" {
#   scope                = var.logic_app_id
#   role_definition_name = "Storage Blob Data Owner"
#   principal_id         = azurerm_logic_app_standard.logic_app.identity.principal_id
# }

# resource "azurerm_role_assignment" "logic_app_standard_failover" {
#   scope                = var.logic_app_id_failover
#   role_definition_name = "Storage Blob Data Owner"
#   principal_id         = azurerm_logic_app_standard.logic_app.identity.principal_id
# }
