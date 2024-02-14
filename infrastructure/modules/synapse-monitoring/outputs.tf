output "instrumentation_key" {
  description = "Instrumentation key of the application insights"
  value       = azurerm_application_insights.function_app_insights[*].instrumentation_key
}
