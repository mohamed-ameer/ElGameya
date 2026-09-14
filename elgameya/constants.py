"""
ElGameya Constants Registry
------------------------
This module acts as a single source of truth for all fixed values,
error messages, and configuration keys used across the ElGameya application.

Usage:
    import frappe, elgameya

    # Use the .get() method to prevent KeyErrors
    frappe.throw(_(elgameya.ERRORS.get("no_permission")))
"""

# Error Messages
# Note: Do not wrap these strings in _() here.
# Use lowercase with underscores (snake_case) for keys.
# Wrap them at the call site to ensure they are picked up by the translation parser.
ERRORS = {"no_permission": "Insufficient permissions"}
