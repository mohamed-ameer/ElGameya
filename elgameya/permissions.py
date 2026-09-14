"""
This module contains utility functions related to permissions in the ElGameya app.
For the hooks: has_permission, permission_query_conditions refer to apps/elgameya/elgameya/hooks.py

The naming rules for permissions related functions in this module are as follows:
- Functions that check if a user has permission to perform an action should be named `<doctype_name>_has_permission`, e.g. `ElGameyaSettings_has_permission`.
- Functions that return permission query conditions should be named `<doctype_name>_get_permission_query_conditions`, e.g. `ElGameyaSettings_get_permission_query_conditions`.
"""

import frappe
from frappe.utils.user import is_website_user

def check_app_permission():
	if frappe.session.user == "Administrator":
		return True

	if is_website_user():
		return False

	return True