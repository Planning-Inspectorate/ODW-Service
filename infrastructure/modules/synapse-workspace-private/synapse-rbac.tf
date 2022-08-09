resource "azurerm_synapse_role_assignment" "synapse" {
  for_each = var.synapse_role_assignments

  synapse_workspace_id = azurerm_synapse_workspace.synapse.id
  role_name            = each.key
  principal_id         = each.value

  depends_on = [
    azurerm_synapse_firewall_rule.allow_all,
    azurerm_synapse_firewall_rule.allow_all_azure
  ]
}

resource "azurerm_synapse_workspace_aad_admin" "synapse" {
  login                = var.synapse_aad_administrator.username
  object_id            = var.synapse_aad_administrator.object_id
  synapse_workspace_id = azurerm_synapse_workspace.synapse.id
  tenant_id            = data.azurerm_client_config.current.tenant_id

  depends_on = [
    azurerm_synapse_firewall_rule.allow_all,
    azurerm_synapse_firewall_rule.allow_all_azure
  ]
}
