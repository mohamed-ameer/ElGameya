import frappe
from frappe.utils import strip_html_tags
from frappe.utils.html_utils import clean_html

no_cache = 1


def is_traceback_message(message):
	if not message:
		return False

	message = str(message)

	traceback_markers = [
		"Traceback (most recent call last)",
		"File \"apps/",
		"frappe/app.py",
		"frappe/handler.py",
		"frappe.utils",
		"frappe.core",
		"builtins.",
	]

	return any(marker in message for marker in traceback_markers)


def get_safe_error_message(message):
	if frappe.conf.get("developer_mode"):
		return message

	if is_traceback_message(message):
		return "Internal server error. Please contact support."

	return message


def get_context(context):
	message_context = frappe._dict()

	if hasattr(frappe.local, "message"):
		message_context["header"] = frappe.local.message_title
		message_context["title"] = strip_html_tags(frappe.local.message_title)

		raw_message = frappe.local.message
		message_context["message"] = get_safe_error_message(raw_message)

		if hasattr(frappe.local, "message_success"):
			message_context["success"] = frappe.local.message_success

	elif frappe.local.form_dict.id:
		message_id = frappe.local.form_dict.id
		key = f"message_id:{message_id}"
		message = frappe.cache.get_value(key, expires=True)

		if message:
			message_context.update(message.get("context", {}))

			if not frappe.conf.get("developer_mode"):
				message_context["message"] = get_safe_error_message(message_context.get("message"))

			if message.get("http_status_code"):
				frappe.local.response["http_status_code"] = message["http_status_code"]

	if not message_context.title:
		message_context.title = clean_html(frappe.form_dict.title)

	if not message_context.message:
		raw_message = clean_html(frappe.form_dict.message)
		message_context.message = get_safe_error_message(raw_message)

	return message_context