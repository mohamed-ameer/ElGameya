import re

import frappe
from frappe import _


def normalize_egyptian_phone(phone_number):
	"""
	Normalize an Egyptian mobile number to local 11-digit format.

	Accepted examples:
		01012345678
		+201012345678
		00201012345678
		010 1234 5678
		+20 (101) 234-5678

	Returns:
		str: 11-digit local number, or None if the format is invalid.
	"""
	if not phone_number:
		return None

	phone = str(phone_number).strip()

	# Remove common formatting characters.
	phone = re.sub(r"[\s\-().]", "", phone)

	if phone.startswith("+20"):
		phone = "0" + phone[3:]
	elif phone.startswith("0020"):
		phone = "0" + phone[4:]

	# At this point we expect local Egyptian format.
	if not re.fullmatch(r"01[0125]\d{8}", phone):
		return None

	return phone


def validate_egyptian_phone(phone_number, throw=False):
	"""
	Validate the format of an Egyptian mobile phone number.

	Args:
		phone_number (str | int): Phone number to validate.
		throw (bool): Raise a translated ValidationError instead of
			returning False when the phone number is invalid.

	Returns:
		bool: True if the phone number is a valid Egyptian mobile number.
	"""
	is_valid = normalize_egyptian_phone(phone_number) is not None

	if not is_valid and throw:
		frappe.throw(
			_("{0} is not a valid Egyptian phone number.").format(phone_number),
			title=_("Invalid Phone Number"),
		)

	return is_valid
