resource "azurerm_logic_app_workflow" "zendesk_created" {
  count = var.logic_app_enabled ? 1 : 0

  name                = "zendesk-created"
  location            = var.location
  resource_group_name = var.resource_group_name
  tags                = local.tags
}

# resource "azurerm_logic_app_action_custom" "action" {
#   count = var.logic_app_enabled ? 1 : 0

#   name         = "zendesk-action"
#   logic_app_id = azurerm_logic_app_workflow.zendesk_created[count.index].id

#   body = jsonencode({
#     "actions" : {
#       "Send_message" : {
#         "runAfter" : {},
#         "type" : "ApiConnection",
#         "inputs" : {
#           "body" : {
#             "ContentData" : "@{base64(triggerOutputs())}",
#             "Label" : "Created",
#             "MessageId" : "@{guid()}",
#             "SessionId" : "@{guid()}"
#           },
#           "host" : {
#             "connection" : {
#               "name" : "@parameters('$connections')['servicebus']['connectionId']"
#             }
#           },
#           "method" : "post",
#           "path" : "/@{encodeURIComponent(encodeURIComponent('zendesk'))}/messages",
#           "queries" : {
#             "systemProperties" : "None"
#           }
#         }
#       }
#     },
#     "outputs" : {}
#   })
# }

# resource "azurerm_logic_app_workflow" "zendesk_updated" {
#   count               = var.logic_app_enabled ? 1 : 0
#   name                = "zendesk-updated"
#   location            = var.location
#   resource_group_name = var.resource_group_name
#   tags                = local.tags
# }
