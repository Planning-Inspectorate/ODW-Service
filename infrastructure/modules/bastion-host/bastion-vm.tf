resource "azurerm_network_interface" "jumpbox" {
  name                = "bas-vm-nic-${local.resource_suffix}"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "ipconfig"
    subnet_id                     = var.synapse_vnet_subnet_names[var.synapse_compute_subnet_name]
    private_ip_address_allocation = "Dynamic"
  }

  tags = local.tags
}

resource "azurerm_windows_virtual_machine" "jumpbox" {
  #checkov:skip=CKV_AZURE_151: Host encryption is not supported
  #checkov:skip=CKV_AZURE_177: Automatic updates are only supported for Windows Server 2022
  name                       = "bas-vm-${local.resource_suffix}"
  location                   = var.location
  resource_group_name        = var.resource_group_name
  size                       = var.bastion_vm_size
  admin_username             = var.bastion_vm_username
  admin_password             = random_password.bastion_vm_admin_password.result
  allow_extension_operations = false
  computer_name              = "bastion-${random_string.unique_id.id}"
  network_interface_ids      = [azurerm_network_interface.jumpbox.id]
  provision_vm_agent         = true

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = var.bastion_vm_image["publisher"]
    offer     = var.bastion_vm_image["offer"]
    sku       = var.bastion_vm_image["sku"]
    version   = var.bastion_vm_image["version"]
  }

  tags = local.tags
}
