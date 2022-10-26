resource "azurerm_storage_management_policy" "synapse" {
  count = length(var.data_lake_lifecycle_rules) == 0 ? 0 : 1

  storage_account_id = azurerm_storage_account.synapse.id

  dynamic "rule" {
    for_each = toset(var.data_lake_lifecycle_rules)

    content {
      name    = each.value.rule_name
      enabled = true

      filters {
        prefix_match = each.value.prefix_match
        blob_types   = ["blockBlob"]
      }

      actions {
        base_blob {
          tier_to_cool_after_days_since_modification_greater_than    = can(each.value.cool_tier_since_modified_days) ? each.value.cool_tier_since_modified_days : null
          tier_to_archive_after_days_since_modification_greater_than = can(each.value.archive_tier_since_modified_days) ? each.value.archive_tier_since_modified_days : null
          delete_after_days_since_modification_greater_than          = can(each.value.delete_since_modified_days) ? each.value.delete_since_modified_days : null
        }

        snapshot {
          change_tier_to_cool_after_days_since_creation    = can(each.value.cool_tier_since_created_days) ? each.value.cool_tier_since_created_days : null
          change_tier_to_archive_after_days_since_creation = can(each.value.archive_tier_since_created_days) ? each.value.archive_tier_since_created_days : null
          delete_after_days_since_creation_greater_than    = can(each.value.delete_since_created_days) ? each.value.delete_since_created_days : null
        }

        version {
          change_tier_to_cool_after_days_since_creation    = can(each.value.cool_tier_since_created_days) ? each.value.cool_tier_since_created_days : null
          change_tier_to_archive_after_days_since_creation = can(each.value.archive_tier_since_created_days) ? each.value.archive_tier_since_created_days : null
          delete_after_days_since_creation                 = can(each.value.delete_since_created_days) ? each.value.delete_since_created_days : null
        }
      }
    }
  }
}
