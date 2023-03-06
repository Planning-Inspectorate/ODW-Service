resource "azurerm_servicebus_topic" "topics" {
  for_each = var.failover_namespace ? {} : {
    for topic in toset(local.service_bus_topics_and_subscriptions) : topic.topic_name => topic
  }

  name         = each.value.topic_name
  namespace_id = azurerm_servicebus_namespace.synapse.id

  auto_delete_on_idle                     = "P10675199DT2H48M5.4775807S"
  default_message_ttl                     = "P14D"
  duplicate_detection_history_time_window = "P7D"
  enable_batched_operations               = true
  enable_partitioning                     = false
  max_size_in_megabytes                   = 1024 # Attribute name incorrect: 1024 = 16GB
  requires_duplicate_detection            = true
}
