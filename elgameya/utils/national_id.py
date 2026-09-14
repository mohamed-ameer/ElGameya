"""
Egyptian National ID structure
------------------------------
C YY MM DD GG SSSS X
│ │  │  │  │    │   │
│ │  │  │  │    │   └── final digit
│ │  │  │  │    └────── serial
│ │  │  │  └─────────── governorate registration
│ │  │  └────────────── day
│ │  └───────────────── month
│ └──────────────────── year
└────────────────────── century
"""

import re
from datetime import date

import frappe
from frappe import _
from frappe.utils import getdate

from elgameya.constants import EGYPTIAN_GOVERNORATES

CENTURY_BASE_YEARS = {"2": 1900, "3": 2000}
CHECKSUM_WEIGHTS = (2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2)


def normalize_national_id(national_id):
	"""
	Normalize an Egyptian National ID.

	Returns:
		str: 14-digit National ID, or None if malformed.
	"""
	if national_id is None:
		return None

	value = str(national_id).strip()

	if not re.fullmatch(r"\d{14}", value):
		return None

	return value


def validate_egyptian_national_id(national_id, throw=False):
	"""
	Validate the structural format of an Egyptian National ID: century,
	birth date, governorate code, serial number and checksum digit.

	Args:
		national_id (str | int): National ID to validate.
		throw (bool): Raise a translated ValidationError instead of
			returning False when the National ID is invalid.

	Returns:
		bool: True if the National ID is structurally valid.
	"""
	normalized_id = normalize_national_id(national_id)

	is_valid = (
		normalized_id is not None
		and _get_birth_date(normalized_id) is not None
		and normalized_id[7:9] in EGYPTIAN_GOVERNORATES
		and normalized_id[9:12] != "000"
		and int(normalized_id[13]) == _get_checksum_digit(normalized_id)
	)

	if not is_valid and throw:
		frappe.throw(
			_("{0} is not a valid Egyptian National ID.").format(national_id),
			title=_("Invalid National ID"),
		)

	return is_valid


@frappe.whitelist()
def parse_egyptian_national_id(national_id):
	"""
	Parse an Egyptian National ID and extract the information encoded in
	it: birth date, age, governorate, gender and serial number.

	Does not perform any government/database verification.

	Whitelisted so client scripts can call it directly, e.g. to
	auto-fill birth date / gender / governorate fields from a National
	ID field.

	Returns:
		dict: `is_valid` plus the decoded fields, or `is_valid` and
			`error` when the National ID is malformed.
	"""
	normalized_id = normalize_national_id(national_id)

	if normalized_id is None:
		return {
			"is_valid": False,
			"error": _("National ID must contain exactly 14 digits."),
		}

	if not validate_egyptian_national_id(normalized_id):
		return {
			"is_valid": False,
			"national_id": normalized_id,
			"error": _("Invalid National ID structure."),
		}

	century_digit = normalized_id[0]
	birth_date = _get_birth_date(normalized_id)
	governorate_code = normalized_id[7:9]
	governorate = EGYPTIAN_GOVERNORATES[governorate_code]
	gender_digit = int(normalized_id[12])

	today = getdate()
	age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

	return {
		"is_valid": True,
		"national_id": normalized_id,
		"century_digit": int(century_digit),
		"century_range": "1900-1999" if century_digit == "2" else "2000-2099",
		"birth_date": birth_date.isoformat(),
		"birth_year": birth_date.year,
		"birth_month": birth_date.month,
		"birth_day": birth_date.day,
		"age": age,
		"governorate_code": governorate_code,
		"governorate": governorate["en"],
		"governorate_ar": governorate["ar"],
		"serial_number": normalized_id[9:13],
		"gender_digit": gender_digit,
		"gender": "Male" if gender_digit % 2 else "Female",
		"final_digit": int(normalized_id[13]),
	}


# Internal helpers


def _get_birth_date(normalized_id):
	"""Return the birth date encoded in a normalized National ID, or None if out of range."""
	century_digit = normalized_id[0]

	if century_digit not in CENTURY_BASE_YEARS:
		return None

	year = CENTURY_BASE_YEARS[century_digit] + int(normalized_id[1:3])
	month = int(normalized_id[3:5])
	day = int(normalized_id[5:7])

	try:
		return date(year, month, day)
	except ValueError:
		return None


def _get_checksum_digit(normalized_id):
	"""Compute the expected checksum (14th) digit for a normalized National ID."""
	total = sum(int(digit) * weight for digit, weight in zip(normalized_id, CHECKSUM_WEIGHTS, strict=False))
	remainder = 11 - total % 11

	return 0 if remainder == 10 else (1 if remainder == 11 else remainder)
