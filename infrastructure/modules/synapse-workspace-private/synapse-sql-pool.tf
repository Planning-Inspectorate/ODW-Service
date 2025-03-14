resource "azurerm_synapse_sql_pool" "synapse" {
  count = var.sql_pool_enabled ? 1 : 0

  name                 = "pinssyndpodw"
  synapse_workspace_id = azurerm_synapse_workspace.synapse.id
  sku_name             = var.sql_pool_sku_name
  collation            = var.sql_pool_collation
  create_mode          = "Default"
  storage_account_type = "GRS"

  tags = local.tags
}
