resource "azurerm_logic_app_workflow" "zendesk_created" {
  count               = var.logic_app_enabled ? 1 : 0
  name                = "zendesk-created"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags

  workflow_parameters = jsondecode(
    {
      "definition" : {
        "$schema" : "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
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
                  "referenceName" : "servicebus-2"
                }
              },
              "method" : "post",
              "path" : "/@{encodeURIComponent(encodeURIComponent('zendesk'))}/messages"
            },
            "runAfter" : {},
            "type" : "ApiConnection"
          }
        },
        "contentVersion" : "1.0.0.0",
        "outputs" : {},
        "triggers" : {
          "When_an_item_is_created" : {
            "inputs" : {
              "host" : {
                "connection" : {
                  "referenceName" : "zendesk"
                }
              },
              "method" : "get",
              "path" : "/datasets/default/tables/@{encodeURIComponent(encodeURIComponent('tickets'))}/onnewitems"
            },
            "recurrence" : {
              "frequency" : "Minute",
              "interval" : 1
            },
            "type" : "ApiConnection"
          }
        }
      },
      "kind" : "Stateful"
  })
}

# resource "azurerm_logic_app_workflow" "zendesk_updated" {
#   count               = var.logic_app_enabled ? 1 : 0
#   name                = "zendesk-updated"
#   location            = var.location
#   resource_group_name = var.resource_group_name
#   tags                = local.tags
# }
