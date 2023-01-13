resource "azurerm_storage_blob" "test" {
  for_each = toset(var.data_lake_configuration_files)

  name                   = each.key
  storage_account_name   = azurerm_storage_account.synapse.name
  storage_container_name = "odw-config"
  type                   = "Block"
  source                 = each.key
}
