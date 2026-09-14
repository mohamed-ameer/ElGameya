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

# Egyptian Phone Number & Governorate Lookups
EGYPTIAN_MOBILE_PREFIXES = ("010", "011", "012", "015")
EGYPTIAN_GOVERNORATES = {
    "01": {"en": "Cairo", "ar": "القاهرة"},
    "02": {"en": "Alexandria", "ar": "الإسكندرية"},
    "03": {"en": "Port Said", "ar": "بورسعيد"},
    "04": {"en": "Suez", "ar": "السويس"},
    "11": {"en": "Damietta", "ar": "دمياط"},
    "12": {"en": "Dakahlia", "ar": "الدقهلية"},
    "13": {"en": "Sharqia", "ar": "الشرقية"},
    "14": {"en": "Qalyubia", "ar": "القليوبية"},
    "15": {"en": "Kafr El Sheikh", "ar": "كفر الشيخ"},
    "16": {"en": "Gharbia", "ar": "الغربية"},
    "17": {"en": "Monufia", "ar": "المنوفية"},
    "18": {"en": "Beheira", "ar": "البحيرة"},
    "19": {"en": "Ismailia", "ar": "الإسماعيلية"},
    "21": {"en": "Giza", "ar": "الجيزة"},
    "22": {"en": "Beni Suef", "ar": "بني سويف"},
    "23": {"en": "Fayoum", "ar": "الفيوم"},
    "24": {"en": "Minya", "ar": "المنيا"},
    "25": {"en": "Assiut", "ar": "أسيوط"},
    "26": {"en": "Sohag", "ar": "سوهاج"},
    "27": {"en": "Qena", "ar": "قنا"},
    "28": {"en": "Aswan", "ar": "أسوان"},
    "29": {"en": "Luxor", "ar": "الأقصر"},
    "31": {"en": "Red Sea", "ar": "البحر الأحمر"},
    "32": {"en": "New Valley", "ar": "الوادي الجديد"},
    "33": {"en": "Matrouh", "ar": "مطروح"},
    "34": {"en": "North Sinai", "ar": "شمال سيناء"},
    "35": {"en": "South Sinai", "ar": "جنوب سيناء"},
    "88": {"en": "Born Abroad", "ar": "خارج الجمهورية"},
}