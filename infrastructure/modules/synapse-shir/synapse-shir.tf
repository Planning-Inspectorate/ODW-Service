resource "azurerm_synapse_integration_runtime_self_hosted" "synapse" {
  name                 = "PinsIntegrationRuntime"
  synapse_workspace_id = var.synapse_workspace_id
}

resource "azurerm_synapse_integration_runtime_self_hosted" "purview" {
  name                 = "PinsPurviewIntergrationRuntime"
  synapse_workspace_id = var.synapse_workspace_id
}
