data "azurerm_key_vault_secret" "data_lake_storage_account_key" {
  count        = var.external_resource_links_enabled ? 1 : 0
  name         = "data-lake-storage-account-key"
  key_vault_id = var.key_vault_id
}
