resource "azurerm_synapse_spark_pool" "synapse" {
  count = var.spark_pool_enabled ? 1 : 0

  name                 = "pinssynspodw"
  synapse_workspace_id = azurerm_synapse_workspace.synapse.id
  node_size_family     = "MemoryOptimized"
  node_size            = var.spark_pool_node_size
  spark_version        = var.spark_pool_version

  auto_pause {
    delay_in_minutes = var.spark_pool_timeout_minutes
  }

  auto_scale {
    max_node_count = var.spark_pool_max_node_count
    min_node_count = var.spark_pool_min_node_count
  }

  dynamic "library_requirement" {
    for_each = var.spark_pool_requirements != null ? [1] : []

    content {
      content  = var.spark_pool_requirements
      filename = "requirements.txt"
    }
  }

  spark_config {
    content  = <<-EOT
      spark.executorEnv.dataLakeDfsEndpoint ${var.data_lake_dfs_endpoint}
      EOT
    filename = "configuration.txt"
  }

  tags = local.tags
}
