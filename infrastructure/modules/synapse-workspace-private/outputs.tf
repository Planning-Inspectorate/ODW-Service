output "key_vault_id" {
  description = "The ID of the Key Vault"
  value       = azurerm_key_vault.synapse.id
}

output "key_vault_uri" {
  description = "The URI of the Key Vault"
  value       = azurerm_key_vault.synapse.vault_uri
}

output "synapse_endpoints" {
  description = "A list of connectivity endpoints associated with the Synapse Workspace"
  value       = azurerm_synapse_workspace.synapse.connectivity_endpoints
}

output "synapse_spark_pool_id" {
  description = "The ID of the Synapse Spark Pool"
  value       = azurerm_synapse_spark_pool.synapse[0].id
}

output "synapse_sql_pool_id" {
  description = "The ID of the Synapse SQL Pool"
  value       = azurerm_synapse_sql_pool.synapse[0].id
}

output "synapse_workspace_id" {
  description = "The ID of the Synapse Workspace"
  value       = azurerm_synapse_workspace.synapse.id
}

output "synapse_workspace_name" {
  description = "The name of the Synapse Workspace"
  value       = azurerm_synapse_workspace.synapse.name
}
