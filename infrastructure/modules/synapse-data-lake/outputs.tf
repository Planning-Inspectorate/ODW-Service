output "data_lake_account_id" {
  description = "The ID of the Data Lake Storage Account"
  value       = azurerm_storage_account.synapse.id
}

output "data_lake_account_name" {
  description = "The name of the Data Lake Storage Account"
  value       = azurerm_storage_account.synapse.name
}

output "data_lake_dfs_endpoint" {
  description = "The DFS endpoint URL of the Data Lake Storage Account"
  value       = azurerm_storage_account.synapse.primary_dfs_endpoint
}

output "data_lake_filesystem_id" {
  description = "The ID of the Data Lake Gen2 filesystem"
  value       = azurerm_storage_data_lake_gen2_filesystem.synapse.id
}

output "key_vault_id" {
  description = "The ID of the Key Vault"
  value       = var.external_resource_links_enabled ? azurerm_key_vault.synapse[0].id : null
}

output "key_vault_name" {
  description = "The name of the Key Vault"
  value       = var.external_resource_links_enabled ? azurerm_key_vault.synapse[0].name : null
}

output "key_vault_uri" {
  description = "The URI of the Key Vault"
  value       = var.external_resource_links_enabled ? azurerm_key_vault.synapse[0].vault_uri : null
}
