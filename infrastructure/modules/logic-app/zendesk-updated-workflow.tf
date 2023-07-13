resource "azurerm_logic_app_workflow" "zendesk_updated" {
  count = var.logic_app_enabled ? 1 : 0

  name                = "pins-la-zendesk-updated-${local.resource_suffix}"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
  workflow_parameters = {
    "$connections" = jsonencode({
      "defaultValue" : {},
      "type" : "Object"
    })
  }

  parameters = {
    "$connections" = jsonencode({
      "zendesk" : {
        "connectionId" : azapi_resource.zendesk_custom_api[count.index].id,
        "connectionName" : azapi_resource.zendesk_custom_api[count.index].name,
        "id" : azapi_resource.zendesk_custom_api[count.index].id
      },
      "servicebus" : {
        "connectionId" : azurerm_api_connection.service_bus_api_connection[count.index].id,
        "connectionName" : azurerm_api_connection.service_bus_api_connection[count.index].name,
        "id" : azurerm_api_connection.service_bus_api_connection[count.index].managed_api_id
      }
    })
  }
  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_logic_app_trigger_custom" "zendesk_updated_trigger" {
  count = var.logic_app_enabled ? 1 : 0

  logic_app_id = azurerm_logic_app_workflow.zendesk_updated[count.index].id
  name         = "When_an_item_is_modified"

  body = jsonencode({
    "evaluatedRecurrence" : {
      "frequency" : "Minute",
      "interval" : 1
    },
    "inputs" : {
      "host" : {
        "connection" : {
          "name" : "@parameters('$connections')['zendesk']['connectionId']"
        }
      },
      "method" : "get",
      "path" : "/datasets/default/tables/@{encodeURIComponent(encodeURIComponent('tickets'))}/onupdateditems"
    },
    "recurrence" : {
      "frequency" : "Minute",
      "interval" : 1
    },
    "splitOn" : "@triggerBody()?['value']",
    "type" : "ApiConnection"
  })
}

resource "azurerm_logic_app_action_custom" "zendesk_updated_action" {
  count = var.logic_app_enabled ? 1 : 0

  logic_app_id = azurerm_logic_app_workflow.zendesk_updated[count.index].id
  name         = "Send_message"

  body = jsonencode({
    "inputs" : {
      "body" : {
        "ContentData" : "@{base64(triggerOutputs())}",
        "Label" : "Updated",
        "MessageId" : "@{guid()}",
        "SessionId" : "@{guid()}"
      },
      "host" : {
        "connection" : {
          "name" : "@parameters('$connections')['servicebus']['connectionId']"
        }
      },
      "method" : "post",
      "path" : "/@{encodeURIComponent(encodeURIComponent('zendesk'))}/messages",
      "queries" : {
        "systemProperties" : "None"
      }
    },
    "runAfter" : {},
    "type" : "ApiConnection"
  })
}
