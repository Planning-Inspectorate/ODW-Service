data "azurerm_image" "azure_agents" {
  count = var.deploy_agent_pool ? 1 : 0

  name_regex          = "devops-agents-20241114120119"
  sort_descending     = true
  resource_group_name = azurerm_resource_group.devops_agents.name
}