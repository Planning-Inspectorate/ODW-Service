resource "azurerm_logic_app_workflow" "zendesk_created" {
  count               = var.logic_app_enabled ? 1 : 0
  name                = "zendesk-created"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
}

resource "azurerm_logic_app_action_custom" "zendesk_created" {
  count              = var.logic_app_enabled ? 1 : 0

  name               = "send-message"
  logic_app_id       = azurerm_logic_app_workflow.zendesk_created[count.index].id

  body = jsonencode(
        {
            "Send_message": {
                "inputs": {
                    "body": {
                        "ContentData": "@{base64(triggerOutputs())}",
                        "Label": "Created",
                        "MessageId": "@{guid()}",
                        "SessionId": "@{guid()}"
                    },
                    "host": {
                        "connection": {
                            "referenceName": "servicebus-2"
                        }
                    },
                    "method": "post",
                    "path": "/@{encodeURIComponent(encodeURIComponent('zendesk'))}/messages"
                },
                "runAfter": {},
                "type": "ApiConnection"
            }
        }
    )
}

resource "azurerm_logic_app_trigger_custom" "zendesk_created" {
    count = var.logic_app_enabled ? 1 : 0

    name = "When_an_item_is_created"
    logic_app_id = azurerm_logic_app_workflow.zendesk_created[count.index].id

    body = jsonencode(
        {
            "When_an_item_is_created": {
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
                },
                "type": "ApiConnection"
            }
        }
    )
}

# resource "azurerm_logic_app_workflow" "zendesk_updated" {
#   count               = var.logic_app_enabled ? 1 : 0
#   name                = "zendesk-updated"
#   location            = var.location
#   resource_group_name = var.resource_group_name
#   tags                = local.tags
# }
