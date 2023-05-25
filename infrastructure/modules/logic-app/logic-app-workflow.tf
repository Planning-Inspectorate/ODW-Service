resource "azurerm_logic_app_workflow" "zendesk_created" {
  count = var.logic_app_enabled ? 1 : 0

  name                = "pins-la-zendesk-created-${local.resource_suffix}"
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
        "connectionId" : azurerm_api_connection.zendesk_api_connection.id,
        "connectionName" : azurerm_api_connection.zendesk_api_connection.name,
        "id" : azurerm_api_connection.zendesk_api_connection.managed_api_id
      },
      "servicebus" : {
        "connectionId" : azurerm_api_connection.service_bus_api_connection.id,
        "connectionName" : azurerm_api_connection.service_bus_api_connection.name,
        "id" : azurerm_api_connection.service_bus_api_connection.managed_api_id
        "connectionProperties" : {
          "authenticationType" : "ManagedServiceIdentity"
        }
      }
    })
  }
  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_logic_app_trigger_custom" "zendesk_created_trigger" {
  count = var.logic_app_enabled ? 1 : 0

  logic_app_id = azurerm_logic_app_workflow.zendesk_created[count.index].id
  name         = "When_an_item_is_created"

  body = jsonencode({
    "triggers" : {
      "When_an_item_is_created" : {
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
          "path" : "/datasets/default/tables/@{encodeURIComponent(encodeURIComponent('tickets'))}/onnewitems"
        },
        "recurrence" : {
          "frequency" : "Minute",
          "interval" : 1
        },
        "splitOn" : "@triggerBody()?['value']",
        "type" : "ApiConnection"
      }
    }
  })
}

resource "azurerm_logic_app_action_custom" "zendesk_created_trigger" {
  count = var.logic_app_enabled ? 1 : 0

  logic_app_id = azurerm_logic_app_workflow.zendesk_created[count.index].id
  name         = "Send_message"

  body = jsonencode({
    "actions" : {
      "Send_message" : {
        "inputs" : {
          "body" : {
            "ContentData" : "@{base64(triggerOutputs())}",
            "Label" : "Created",
            "MessageId" : "@{guid()}",
            "SessionId" : "@{guid()}"
          },
          "host" : {
            "connection" : {
              "name" : "@parameters('$connections')['servicebus_1']['connectionId']"
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
      }
    },
    "contentVersion" : "1.0.0.0",
    "outputs" : {},
    "parameters" : {
      "$connections" : {
        "defaultValue" : {},
        "type" : "Object"
      }
    },
  })
}

# resource "azurerm_logic_app_workflow" "zendesk_updated" {
#   count               = var.logic_app_enabled ? 1 : 0
#   name                = "zendesk-updated"
#   location            = var.location
#   resource_group_name = var.resource_group_name
#   tags                = local.tags
# }
