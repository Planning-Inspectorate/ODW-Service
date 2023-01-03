resource "azurerm_role_assignment" "service_bus" {
  for_each = {
    for assignment in local.service_bus_role_assignments : "${assignment.role_definition_name}.${assignment.principal_id}" => assignment
  }

  scope                = azurerm_servicebus_namespace.synapse.id
  role_definition_name = each.value.role_definition_name
  principal_id         = each.value.principal_id
}
