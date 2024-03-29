resource "azapi_resource" "zendesk_custom_api" {
  count = var.logic_app_enabled ? 1 : 0

  type      = "Microsoft.Web/customApis@2016-06-01"
  name      = "zendesk-custom-api"
  location  = var.location
  parent_id = var.resource_group_id
  tags      = local.tags

  body = jsonencode(
    {
      "properties" : {
        "connectionParameters" : {
          "username" : {
            "type" : "securestring",
          },
          "password" : {
            "type" : "securestring",
          }
        },
        "backendService" : {
          "serviceUrl" : "https://pinssupport.zendesk.com",
        },
        "capabilities" : [],
        "description" : "Custom API for Zendesk",
        "displayName" : "zensdesk-custom-api",
        "iconUri" : "https://content.powerapps.com/resource/makerx/static/media/default-connection-icon.00d06b6e.svg",
        "swagger" : jsondecode(file("${path.module}/zendesk-swagger.json")),
        "apiType" : "Rest",
      }
  })
}
