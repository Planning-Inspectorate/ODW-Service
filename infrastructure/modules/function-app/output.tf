output "resource_group_name" {
  description = "Name of the resource group where resources have been deployed to"
  value       = azurerm_linux_function_app.function.resource_group_name
}

output "name" {
  description = "Name of the function app"
  value       = azurerm_linux_function_app.function.name
}

output "function_app_id" {
  description = "Id of the function app"
  value       = azurerm_linux_function_app.function.id
}

output "hostname" {
  description = "Id of the function app"
  value       = azurerm_linux_function_app.function.default_hostname
}

output "identity" {
  description = "Identity block function app managed identity"
  value       = azurerm_linux_function_app.function.identity
}

output "principal_ids" {
  value = {
    for key, function_app in azurerm_linux_function_app.function : function_app.name => function_app.identity[0].principal_id
  }
  description = "Principal ids of the function app"
}