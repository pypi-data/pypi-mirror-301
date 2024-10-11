from pyspark.sql.types import *

xero_bronze = StructType([
    StructField("type", StringType(), True),
    StructField("contact", StructType([
        StructField("contact_id", StringType(), True),
        StructField("merged_to_contact_id", StringType(), True),
        StructField("contact_number", StringType(), True),
        StructField("account_number", StringType(), True),
        StructField("contact_status", StringType(), True),
        StructField("name", StringType(), True),
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("company_number", StringType(), True),
        StructField("email_address", StringType(), True),
        StructField("contact_persons", ArrayType(StringType()), True),
        StructField("bank_account_details", StringType(), True),
        StructField("tax_number", StringType(), True),
        StructField("accounts_receivable_tax_type", StringType(), True),
        StructField("accounts_payable_tax_type", StringType(), True),
        StructField("addresses", ArrayType(StringType()), True),
        StructField("phones", ArrayType(StringType()), True),
        StructField("is_supplier", BooleanType(), True),
        StructField("is_customer", BooleanType(), True),
        StructField("sales_default_line_amount_type", StringType(), True),
        StructField("purchases_default_line_amount_type", StringType(), True),
        StructField("default_currency", StringType(), True),
        StructField("xero_network_key", StringType(), True),
        StructField("sales_default_account_code", StringType(), True),
        StructField("purchases_default_account_code", StringType(), True),
        StructField("sales_tracking_categories", StringType(), True),
        StructField("purchases_tracking_categories", StringType(), True),
        StructField("tracking_category_name", StringType(), True),
        StructField("tracking_category_option", StringType(), True),
        StructField("payment_terms", StringType(), True),
        StructField("updated_date_utc", StringType(), True),
        StructField("contact_groups", ArrayType(StringType()), True),
        StructField("website", StringType(), True),
        StructField("branding_theme", StringType(), True),
        StructField("batch_payments", StringType(), True),
        StructField("discount", StringType(), True),
        StructField("balances", StringType(), True),
        StructField("attachments", StringType(), True),
        StructField("has_attachments", BooleanType(), True),
        StructField("validation_errors", StringType(), True),
        StructField("has_validation_errors", BooleanType(), True),
        StructField("status_attribute_string", StringType(), True)
    ]), True),
    StructField("line_items", ArrayType(StructType([
        StructField("line_item_id", StringType(), True),
        StructField("description", StringType(), True),
        StructField("quantity", DecimalType(10, 4), True),
        StructField("unit_amount", DecimalType(10, 2), True),
        StructField("item_code", StringType(), True),
        StructField("account_code", StringType(), True),
        StructField("account_id", StringType(), True),
        StructField("tax_type", StringType(), True),
        StructField("tax_amount", DecimalType(10, 2), True),
        StructField("item", StringType(), True),
        StructField("line_amount", DecimalType(10, 2), True),
        StructField("tracking", ArrayType(StructType([
            StructField("tracking_category_id", StringType(), True),
            StructField("tracking_option_id", StringType(), True),
            StructField("name", StringType(), True),
            StructField("option", StringType(), True)
        ])), True),
        StructField("discount_rate", DecimalType(5, 2), True),
        StructField("discount_amount", DecimalType(10, 2), True),
        StructField("repeating_invoice_id", StringType(), True),
        StructField("taxability", StringType(), True),
        StructField("sales_tax_code_id", StringType(), True),
        StructField("tax_breakdown", StringType(), True)
    ])), True),
    StructField("date", DateType(), True),
    StructField("due_date", DateType(), True),
    StructField("line_amount_types", StringType(), True),
    StructField("invoice_number", StringType(), True),
    StructField("reference", StringType(), True),
    StructField("branding_theme_id", StringType(), True),
    StructField("url", StringType(), True),
    StructField("currency_code", StringType(), True),
    StructField("currency_rate", DecimalType(12, 10), True),
    StructField("status", StringType(), True),
    StructField("sent_to_contact", BooleanType(), True),
    StructField("expected_payment_date", StringType(), True),
    StructField("planned_payment_date", StringType(), True),
    StructField("cis_deduction", DecimalType(5, 2), True),
    StructField("cis_rate", DecimalType(5, 2), True),
    StructField("sub_total", DecimalType(10, 2), True),
    StructField("total_tax", DecimalType(10, 2), True),
    StructField("total", DecimalType(10, 2), True),
    StructField("total_discount", DecimalType(10, 2), True),
    StructField("invoice_id", StringType(), True),
    StructField("repeating_invoice_id", StringType(), True),
    StructField("has_attachments", BooleanType(), True),
    StructField("is_discounted", BooleanType(), True),
    StructField("payments", ArrayType(StructType([
        StructField("invoice", StringType(), True),
        StructField("credit_note", StringType(), True),
        StructField("prepayment", StringType(), True),
        StructField("overpayment", StringType(), True),
        StructField("invoice_number", StringType(), True),
        StructField("credit_note_number", StringType(), True),
        StructField("batch_payment", StringType(), True),
        StructField("account", StringType(), True),
        StructField("code", StringType(), True),
        StructField("date", DateType(), True),
        StructField("currency_rate", DecimalType(12, 10), True),
        StructField("amount", DecimalType(10, 2), True),
        StructField("bank_amount", DecimalType(10, 2), True),
        StructField("reference", StringType(), True),
        StructField("is_reconciled", BooleanType(), True),
        StructField("status", StringType(), True),
        StructField("payment_type", StringType(), True),
        StructField("updated_date_utc", StringType(), True),
        StructField("payment_id", StringType(), True),
        StructField("batch_payment_id", StringType(), True),
        StructField("bank_account_number", StringType(), True),
        StructField("particulars", StringType(), True),
        StructField("details", StringType(), True),
        StructField("has_account", BooleanType(), True),
        StructField("has_validation_errors", BooleanType(), True),
        StructField("status_attribute_string", StringType(), True),
        StructField("validation_errors", StringType(), True),
        StructField("warnings", StringType(), True)
    ])), True),
    StructField("prepayments", ArrayType(StringType()), True),
    StructField("overpayments", ArrayType(StringType()), True),
    StructField("amount_due", DecimalType(10, 2), True),
    StructField("amount_paid", DecimalType(10, 2), True),
    StructField("fully_paid_on_date", DateType(), True),
    StructField("amount_credited", DecimalType(10, 2), True),
    StructField("updated_date_utc", TimestampType(), True),
    StructField("credit_notes", ArrayType(StringType()), True),
    StructField("attachments", StringType(), True),
    StructField("has_errors", BooleanType(), True),
    StructField("status_attribute_string", StringType(), True),
    StructField("validation_errors", StringType(), True),
    StructField("warnings", StringType(), True),
    StructField("invoice_addresses", ArrayType(StringType()), True)
])

everhour_time_entries_schema = StructType([
    StructField('id', LongType(), True),
    StructField('date', StringType(), True),
    StructField('createdAt', StringType(), True),
    StructField('user', LongType(), True),
    StructField('time', IntegerType(), True),
    StructField('comment', StringType(), True),
    StructField('task', StructType([
        StructField('id', StringType(), True),
        StructField('name', StringType(), True),
        StructField('type', StringType(), True),
        StructField('status', StringType(), True),
        StructField('url', StringType(), True),
        StructField('iteration', StringType(), True),
        StructField('projects', ArrayType(StringType()), True),
        StructField('createdAt', StringType(), True),
        StructField('labels', ArrayType(StringType()), True),
        StructField('time', StructType([
            StructField('total', LongType(), True),
            StructField('users', MapType(StringType(), IntegerType()), True),
            StructField('timerTime', IntegerType(), True)
        ]), True),
        StructField('completed', BooleanType(), True),
        StructField('assignees', ArrayType(StringType()), True)
    ]), True),
    StructField('history', ArrayType(StructType([
        StructField('id', LongType(), True),
        StructField('createdAt', StringType(), True),
        StructField('time', IntegerType(), True),
        StructField('action', StringType(), True),
        StructField('previousTime', IntegerType(), True),
        StructField('previousDate', StringType(), True),
        StructField('previousTask', StringType(), True),
        StructField('createdBy', LongType(), True),
        StructField('warning', StringType(), True)
    ])), True),
    StructField('lockReasons', ArrayType(StringType()), True),
    StructField('isLocked', BooleanType(), True),
    StructField('cost', IntegerType(), True),
    StructField('costRate', IntegerType(), True)
])

everhour_projects_schema = StructType([
    StructField("attributes", StringType(), True),
    StructField("billing", StructType([
        StructField("fee", LongType(), True),
        StructField("type", StringType(), True)
    ]), True),
    StructField("budget", StructType([
        StructField("budget", LongType(), True),
        StructField("disallowOverbudget", BooleanType(), True),
        StructField("excludeExpenses", BooleanType(), True),
        StructField("excludeUnbillableTime", BooleanType(), True),
        StructField("expenseProgress", LongType(), True),
        StructField("period", StringType(), True),
        StructField("progress", LongType(), True),
        StructField("showToUsers", BooleanType(), True),
        StructField("threshold", LongType(), True),
        StructField("thresholdNotificationUsers", ArrayType(LongType()), True),
        StructField("timeProgress", LongType(), True),
        StructField("type", StringType(), True)
    ]), True),
    StructField("canSyncTasks", BooleanType(), True),
    StructField("changeProtected", BooleanType(), True),
    StructField("client", LongType(), True),
    StructField("connectionStatus", StringType(), True),
    StructField("createdAt", StringType(), True),  # Could be TimestampType
    StructField("editable", BooleanType(), True),
    StructField("enableResourcePlanner", BooleanType(), True),
    StructField("estimatesType", StringType(), True),
    StructField("favorite", BooleanType(), True),
    StructField("foreign", BooleanType(), True),
    StructField("hasWebhook", BooleanType(), True),
    StructField("id", StringType(), True),
    StructField("isTemplate", BooleanType(), True),
    StructField("metadata", StructType([
        StructField("type", StringType(), True),
        StructField("url", StringType(), True)
    ]), True),
    StructField("name", StringType(), True),
    StructField("platform", StringType(), True),
    StructField("privacy", StringType(), True),
    StructField("rate", StructType([
        StructField("rate", LongType(), True),
        StructField("type", StringType(), True),
        StructField("userRateOverrides", MapType(StringType(), LongType()), True)
    ]), True),
    StructField("status", StringType(), True),
    StructField("type", StringType(), True),
    StructField("unarchiveDisabledBy", StringType(), True),
    StructField("users", ArrayType(LongType()), True),
    StructField("workspaceId", StringType(), True),
    StructField("workspaceName", StringType(), True)
])

everhour_users_schema = StructType([
    StructField("avatarUrl", StringType(), True),
    StructField("avatarUrlLarge", StringType(), True),
    StructField("budget", StructType([
        StructField("budget", LongType(), True),
        StructField("disallowOverbudget", BooleanType(), True),
        StructField("excludeExpenses", BooleanType(), True),
        StructField("excludeUnbillableTime", BooleanType(), True),
        StructField("expenseProgress", LongType(), True),
        StructField("period", StringType(), True),
        StructField("progress", LongType(), True),
        StructField("showToUsers", BooleanType(), True),
        StructField("timeProgress", LongType(), True),
        StructField("type", StringType(), True)
    ]), True),
    StructField("capacity", LongType(), True),
    StructField("cost", LongType(), True),
    StructField("costHistory", ArrayType(StructType([
        StructField("appliedFrom", StringType(), True),
        StructField("cost", LongType(), True),
        StructField("createdAt", StringType(), True),
        StructField("id", LongType(), True)
    ]), True), True),
    StructField("email", StringType(), True),
    StructField("enableResourcePlanner", BooleanType(), True),
    StructField("groups", ArrayType(StructType([
        StructField("id", LongType(), True),
        StructField("name", StringType(), True),
        StructField("headline", StringType(), True)
    ]), True), True),
    StructField("isEmailVerified", BooleanType(), True),
    StructField("id", StringType(), True),
    StructField("name", StringType(), True),
    StructField("headline", StringType(), True),
    StructField("createdAt", StringType(), True),
    StructField("permissions", StructType([
        StructField("billingBudgets", BooleanType(), True),
        StructField("costs", BooleanType(), True),
        StructField("expenses", BooleanType(), True),
        StructField("invoices", BooleanType(), True),
        StructField("userLimits", BooleanType(), True),
        StructField("rate", LongType(), True)
    ]), True),
    StructField("resourcePlannerAccess", StructType([
        StructField("editAll", BooleanType(), True),
        StructField("editMine", BooleanType(), True),
        StructField("viewAll", BooleanType(), True),
        StructField("viewMine", BooleanType(), True)
    ]), True),
    StructField("role", StringType(), True),
    StructField("status", StringType(), True),
    StructField("timeTrackingPolicy", StructType([
        StructField("allowCompletedTaskTime", BooleanType(), True),
        StructField("allowExceedEstimate", BooleanType(), True),
        StructField("allowFutureTime", BooleanType(), True),
        StructField("allowManageEstimates", BooleanType(), True),
        StructField("allowManualTimeInput", BooleanType(), True),
        StructField("allowTimeWithoutEstimate", BooleanType(), True),
        StructField("allowTimeWithoutTask", BooleanType(), True)
    ]), True),
    StructField("type", StringType(), True)
])

everhour_assignments_schema = StructType([
    StructField("color", StringType(), True),
    StructField("createdAt", StringType(), True),
    StructField("createdBy", LongType(), True),
    StructField("days", LongType(), True),
    StructField("endDate", StringType(), True),
    StructField("id", LongType(), True),
    StructField("includeWeekends", BooleanType(), True),
    StructField("note", StringType(), True),
    StructField("project", StringType(), True),
    StructField("startDate", StringType(), True),
    StructField("task", StructType([
        StructField("assignees", ArrayType(StructType([
            StructField("accountId", StringType(), True),
            StructField("accountName", StringType(), True),
            StructField("userId", LongType(), True)
        ])), True),
        StructField("completed", BooleanType(), True),
        StructField("createdAt", StringType(), True),
        StructField("id", StringType(), True),
        StructField("iteration", StringType(), True),
        StructField("labels", ArrayType(StringType(), True), True),
        StructField("name", StringType(), True),
        StructField("projects", ArrayType(StringType(), True), True),
        StructField("status", StringType(), True),
        StructField("time", StructType([
            StructField("timerTime", LongType(), True),
            StructField("total", LongType(), True),
            StructField("users", MapType(StringType(), LongType()), True)  # Changed to MapType
        ]), True),
        StructField("url", StringType(), True)
    ]), True),
    StructField("time", LongType(), True),
    StructField("timeSpend", StructType([
        StructField("timePerWeek", MapType(StringType(), LongType()), True),  # Changed to MapType
        StructField("totalTime", LongType(), True),
        StructField("type", StringType(), True)
    ]), True),
    StructField("updatedAt", StringType(), True),
    StructField("updatedBy", LongType(), True),
    StructField("user", StructType([
        StructField("avatarUrl", StringType(), True),
        StructField("avatarUrlLarge", StringType(), True),
        StructField("capacity", LongType(), True),
        StructField("email", StringType(), True),
        StructField("headline", StringType(), True),
        StructField("id", LongType(), True),
        StructField("name", StringType(), True)
    ]), True)
])

asana_projects_schema = StructType([
    StructField("gid", StringType(), True),
    StructField("archived", BooleanType(), True),
    StructField("color", StringType(), True),
    StructField("created_at", StringType(), True),
    StructField("current_status", StringType(), True),
    StructField("custom_fields", ArrayType(StringType()), True),
    StructField("custom_field_settings", ArrayType(StructType([StructField("gid", StringType(), True), StructField("resource_type", StringType(), True)])), True),
    StructField("due_on", StringType(), True),
    StructField("followers", ArrayType(StructType([StructField("gid", StringType(), True), StructField("resource_type", StringType(), True)])), True),
    StructField("html_notes", StringType(), True),
    StructField("members", ArrayType(StructType([StructField("gid", StringType(), True), StructField("resource_type", StringType(), True)])), True),
    StructField("modified_at", StringType(), True),
    StructField("name", StringType(), True),
    StructField("notes", StringType(), True),
    StructField("owner", StructType([StructField("gid", StringType(), True), StructField("resource_type", StringType(), True)]), True),
    StructField("public", BooleanType(), True),
    StructField("resource_type", StringType(), True),
    StructField("start_on", StringType(), True),
    StructField("team", StructType([StructField("gid", StringType(), True), StructField("resource_type", StringType(), True)]), True),
    StructField("workspace", StructType([StructField("gid", StringType(), True), StructField("resource_type", StringType(), True)]), True),
])

asana_tasks_schema = StructType([
    StructField("gid", StringType(), True),
    StructField("assignee", StructType([
        StructField("gid", StringType(), True),
        StructField("resource_type", StringType(), True),
    ])),
    StructField("completed", BooleanType(), True),
    StructField("completed_at", StringType(), True),
    StructField("created_at", StringType(), True),
    StructField("custom_fields", ArrayType(
        StructType([
            StructField("gid", StringType(), True),
            StructField("enabled", BooleanType(), True),
            StructField("name", StringType(), True),
            StructField("description", StringType(), True),
            StructField("number_value", StringType(), True),
            StructField("precision", StringType(), True),
            StructField("created_by", StructType([
                StructField("gid", StringType(), True),
                StructField("name", StringType(), True),
                StructField("resource_type", StringType(), True),
            ])),
            StructField("display_value", StringType(), True),
            StructField("resource_subtype", StringType(), True),
            StructField("resource_type", StringType(), True),
            StructField("is_formula_field", BooleanType(), True),
            StructField("is_value_read_only", BooleanType(), True),
            StructField("type", StringType(), True),
            StructField("date_value", StructType([
                StructField("date", StringType(), True),
                StructField("date_time", StringType(), True),
            ]))
        ])
    )),
    StructField("dependencies", ArrayType(StringType()), True),
    StructField("dependents", ArrayType(StringType()), True),
    StructField("due_at", StringType(), True),
    StructField("due_on", StringType(), True),
    StructField("modified_at", StringType(), True),
    StructField("name", StringType(), True),
    StructField("notes", StringType(), True),
    StructField("projects", ArrayType(
        StructType([
            StructField("gid", StringType(), True),
            StructField("name", StringType(), True)
        ])
    ), True)
])