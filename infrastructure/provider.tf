terraform {
  backend "azurerm" {
    # Per-environment key specified in ./environments/*.tfbackend
    container_name       = "terraformstate-odw"
    resource_group_name  = "pins-rg-shared-terraform-uks"
    subscription_id      = "edb1ff78-90da-4901-a497-7e79f966f8e2"
    storage_account_name = "pinsstsharedtfstateuks"
  }

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "= 4.28.0"
    }
  }
  required_version = ">= 1.1.6, <= 1.12.1"
}

provider "azurerm" {
  resource_provider_registrations = "none"

  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
  }
}

provider "azurerm" {
  subscription_id                 = var.environment == "build" ? null : var.odt_subscription_id
  alias                           = "odt"
  resource_provider_registrations = "none"

  features {}
}

provider "azurerm" {
  subscription_id                 = var.environment == "build" ? null : var.horizon_subscription_id
  alias                           = "horizon"
  resource_provider_registrations = "none"

  features {}
}

provider "azurerm" {
  subscription_id                 = var.tooling_config.subscription_id
  alias                           = "tooling"
  resource_provider_registrations = "none"

  features {}
}
