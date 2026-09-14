from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from num2words import num2words
from num2words.lang_AR import Num2Word_AR

INVALID_AMOUNT_MESSAGE = "قيمة غير صحيحة"

RIYAL_FORMS = {
	"singular": "جنيه مصري",
	"dual": "جنيهان مصريان",
	"plural": "جنيهات مصرية",
	"accusative": "جنيهًا مصريًا",
}

HALALA_FORMS = {
	"singular": "قرش",
	"dual": "قرشان",
	"plural": "قروش",
	"accusative": "قرشًا",
}

LEGAL_AMOUNT_PREFIX = "فقط"
LEGAL_AMOUNT_SUFFIX = "لا غير"


def currency_to_arabic_words(number_str, include_only_text=True):
	"""Jinja filter function to convert EGP amounts to Arabic text."""
	try:
		return number_to_arabic_currency(number_str, include_only_text=include_only_text)
	except (InvalidOperation, TypeError, ValueError):
		return INVALID_AMOUNT_MESSAGE


def number_to_arabic_currency(number, include_only_text=True):
	"""Convert a decimal number to Arabic text using Egyptian Pound (EGP) currency units."""
	amount = _to_currency_decimal(number)
	riyals = int(amount)
	halalas = int((amount - Decimal(riyals)) * 100)

	result = []

	if riyals > 0:
		result.append(_format_currency_part(riyals, RIYAL_FORMS, feminine_number=False))

	if halalas > 0:
		if riyals > 0:
			result.append("و")
		result.append(_format_currency_part(halalas, HALALA_FORMS, feminine_number=True))

	amount_text = " ".join(result).strip() if result else f"صفر {RIYAL_FORMS['singular']}"
	if include_only_text:
		return f"{LEGAL_AMOUNT_PREFIX} {amount_text} {LEGAL_AMOUNT_SUFFIX}"

	return amount_text


def _to_currency_decimal(number):
	if number is None:
		raise ValueError

	normalized_number = str(number).strip().replace(",", "")
	if not normalized_number:
		raise ValueError

	amount = Decimal(normalized_number).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
	if amount < 0:
		raise ValueError

	return amount


def _format_currency_part(number, currency_forms, feminine_number=False):
	if number == 1:
		return f"{convert_to_arabic_text(number, feminine=feminine_number)} {currency_forms['singular']}"
	if number == 2:
		return currency_forms["dual"]

	return f"{convert_to_arabic_text(number, feminine=feminine_number)} {get_currency_name(number, currency_forms)}"


def convert_to_arabic_text(number, feminine=False):
	"""Convert number to Arabic text using num2words."""
	if not feminine:
		return num2words(number, lang="ar")

	converter = Num2Word_AR()
	converter.isCurrencyNameFeminine = True
	converter.currency_subunit = ("", "", "", "")
	converter.currency_unit = ("", "", "", "")
	converter.arabicPrefixText = ""
	converter.arabicSuffixText = ""
	converter.separator = ","
	return converter.convert(number).strip()


def get_currency_name(number, currency_forms):
	"""Get the appropriate currency name based on the number."""
	remaining_hundred = number % 100

	if 3 <= remaining_hundred <= 10:
		return currency_forms["plural"]
	if remaining_hundred in (0, 1, 2):
		return currency_forms["singular"]

	return currency_forms["accusative"]
