frappe.provide("elgameya.ui");

elgameya.ui.LanguageSwitcher = class LanguageSwitcher {
	constructor() {
		this.languages = ["en", "ar"];
		this.current_language =
			frappe.boot.user.language || frappe.boot.lang || "en";
	}

	// Toggle language
	toggle() {
		const next_language = this.current_language === "en" ? "ar" : "en";
		this.set_language(next_language);
	}

	// Set language for current user
	set_language(lang) {
		frappe.call({
			method: "frappe.client.set_value",
			args: {
				doctype: "User",
				name: frappe.session.user,
				fieldname: "language",
				value: lang,
			},
			freeze: true,
			freeze_message: __("Refreshing..."),
			callback: () => {
				// frappe.ui.toolbar.clear_cache();
				// frappe.msgprint(__("Refreshing..."));
				// frappe.show_alert({ message: __("Toggle Language"), indicator: "blue" },3);
				window.location.reload();
			},
		});
	}
};
