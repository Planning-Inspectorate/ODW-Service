resource "azurerm_virtual_machine_extension" "custom_script" {
  name                 = "IntegrationRuntimeSetup"
  virtual_machine_id   = azurerm_windows_virtual_machine.synapse.id
  publisher            = "Microsoft.Compute"
  type                 = "CustomScriptExtension"
  type_handler_version = "1.9"

  protected_settings = <<PROTECTED_SETTINGS
    {
      "fileUris": ["${azurerm_storage_blob.install_shir.url}"],
      "commandToExecute": "powershell.exe -ExecutionPolicy Unrestricted -File Install-Shir.ps1 -authKey ${azurerm_synapse_integration_runtime_self_hosted.synapse.authorization_key_primary}",
      "managedIdentity": {}
    }
PROTECTED_SETTINGS

  #   protected_settings = <<PROTECTED_SETTINGS
  #     {
  #       "fileUris": ["${azurerm_storage_blob.install_shir.url}${data.azurerm_storage_account_sas.shir.sas}&sr=b"],
  #       "commandToExecute": "powershell.exe Install-Shir.ps1 -authKey ${azurerm_synapse_integration_runtime_self_hosted.synapse.authorization_key_primary}",
  #       "managedIdentity": {}
  #     }
  # PROTECTED_SETTINGS

  depends_on = [
    azurerm_private_endpoint.shir_blob,
    azurerm_role_assignment.shir_vm
  ]

  tags = local.tags
}
