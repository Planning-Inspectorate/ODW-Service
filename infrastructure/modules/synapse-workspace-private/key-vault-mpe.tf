resource "azurerm_synapse_managed_private_endpoint" "key_vault" {
  name                 = "synapse-mpe-kv-${var.key_vault_name}"
  synapse_workspace_id = azurerm_synapse_workspace.synapse.id
  target_resource_id   = var.key_vault_id
  subresource_name     = "vault"
}
