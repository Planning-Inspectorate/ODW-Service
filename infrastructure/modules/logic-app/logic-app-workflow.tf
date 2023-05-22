resource "azurerm_logic_app_workflow" "zendesk_created" {
  count               = var.logic_app_enabled ? 1 : 0
  name                = "zendesk-created"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
}

resource "azurerm_logic_app_action_custom" "action" {
  count = var.logic_app_enabled ? 1 : 0

  name         = "zendesk-action"
  logic_app_id = azurerm_logic_app_workflow.zendesk_created[count.index].id

  body = <<BODY
    {
      "Send_message": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "referenceName": "servicebus-1"
            }
          },
          "method": "post",
          "body": {
            "SessionId": "@{guid()}",
            "MessageId": "@{guid()}",
            "Label": "Created",
            "ContentData": "@{base64(triggerOutputs())}"
          },
          "path": "/@{encodeURIComponent(encodeURIComponent('zendesk'))}/messages"
        },
        "runAfter": {}
      }
    }
BODY

}

resource "azurerm_logic_app_trigger_custom" "trigger" {
  count = var.logic_app_enabled ? 1 : 0

  name         = "zendesk-trigger"
  logic_app_id = azurerm_logic_app_workflow.zendesk_created[count.index].id

  body = <<BODY
    {
      "When_an_item_is_created": {
        "type": "ApiConnection",
        "inputs": {
          "host": {
            "connection": {
              "referenceName": "zendesk"
            }
          },
          "method": "get",
          "path": "/datasets/default/tables/@{encodeURIComponent(encodeURIComponent('tickets'))}/onnewitems"
        },
        "recurrence": {
          "frequency": "Minute",
          "interval": 1
        }
      }
    }
BODY

}

# resource "azurerm_logic_app_workflow" "zendesk_updated" {
#   count               = var.logic_app_enabled ? 1 : 0
#   name                = "zendesk-updated"
#   location            = var.location
#   resource_group_name = var.resource_group_name
#   tags                = local.tags
# }
