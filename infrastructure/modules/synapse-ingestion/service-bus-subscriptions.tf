resource "azurerm_servicebus_subscription" "topic_subscriptions" {
  for_each = var.failover_namespace ? {} : {
    for topic_name, subscription_name in local.service_bus_topics_and_subscriptions : "${topic_name}.${subscription_name}" => {
      topic_name        = topic_name
      subscription_name = subscription_name
    }
  }

  name               = each.value.subscription_name
  topic_id           = azurerm_servicebus_topic.topics[each.key].id
  max_delivery_count = 1
}
