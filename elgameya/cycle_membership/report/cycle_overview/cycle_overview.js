// Copyright (c) 2026, ElGameya and contributors
// For license information, please see license.txt

frappe.query_reports["Cycle Overview"] = {
	filters: [
		{
			fieldname: "cycle",
			label: __("Cycle"),
			fieldtype: "Link",
			options: "Cycle",
		},
		{
			fieldname: "cycle_status",
			label: __("Cycle Status"),
			fieldtype: "Select",
			options: "\nDraft\nActive\nCompleted\nCancelled",
		},
		{
			fieldname: "member_status",
			label: __("Member Status"),
			fieldtype: "Select",
			options: "\nPending\nApproved\nRejected\nCancelled",
		},
	],
};
