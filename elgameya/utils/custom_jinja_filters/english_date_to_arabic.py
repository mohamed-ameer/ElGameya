from datetime import date, datetime
import re
import warnings

from elgameya.utils.custom_jinja_filters.english_to_arabic_numbers import english_to_arabic_numbers

with warnings.catch_warnings():
	warnings.filterwarnings("ignore", category=DeprecationWarning, module="hijri_converter")
	from hijri_converter import Gregorian

INVALID_DATE_MESSAGE = "تاريخ غير صحيح"

GREGORIAN_MONTHS = [
	"يناير",
	"فبراير",
	"مارس",
	"أبريل",
	"مايو",
	"يونيو",
	"يوليو",
	"أغسطس",
	"سبتمبر",
	"أكتوبر",
	"نوفمبر",
	"ديسمبر",
]

HIJRI_MONTHS = [
	"محرم",
	"صفر",
	"ربيع الأول",
	"ربيع الآخر",
	"جمادى الأولى",
	"جمادى الآخرة",
	"رجب",
	"شعبان",
	"رمضان",
	"شوال",
	"ذو القعدة",
	"ذو الحجة",
]

GREGORIAN_ALIASES = {"g", "geo", "gregorian", "gregory", "miladi", "ميلادي"}
HIJRI_ALIASES = {"h", "hijri", "هجري"}
WORD_FORMAT_ALIASES = {"word", "words", "text", "month", "month_name", "كتابة"}
NUMBER_FORMAT_ALIASES = {"number", "numbers", "numeric", "digits", "arabic_numbers", "أرقام"}
DATE_SEPARATORS = {"-", "/"}


def english_date_to_arabic(
	value,
	calendar="gregorian",
	output_format="words",
	separator="-",
	include_suffix=True,
):
	"""Convert an English Gregorian date to Arabic Gregorian or Hijri text."""
	try:
		parsed_date = _parse_gregorian_date(value)
		calendar = _normalize_calendar(calendar)
		output_format, include_suffix = _normalize_output_format(output_format, include_suffix)
		separator = _normalize_separator(separator)

		if calendar == "hijri":
			hijri_date = Gregorian(parsed_date.year, parsed_date.month, parsed_date.day).to_hijri()
			return _format_arabic_date(
				hijri_date.day,
				hijri_date.month,
				HIJRI_MONTHS[hijri_date.month - 1],
				hijri_date.year,
				"هـ" if include_suffix else "",
				output_format,
				separator,
			)

		return _format_arabic_date(
			parsed_date.day,
			parsed_date.month,
			GREGORIAN_MONTHS[parsed_date.month - 1],
			parsed_date.year,
			"م" if include_suffix else "",
			output_format,
			separator,
		)
	except (TypeError, ValueError):
		return INVALID_DATE_MESSAGE


def _parse_gregorian_date(value):
	if value is None:
		raise ValueError

	if isinstance(value, datetime):
		return value.date()

	if isinstance(value, date):
		return value

	date_text = str(value).strip()
	if not date_text:
		raise ValueError

	date_text = date_text.split("T", 1)[0].split(" ", 1)[0].replace("/", "-")
	match = re.fullmatch(r"(\d{1,4})-(\d{1,2})-(\d{1,4})", date_text)
	if not match:
		raise ValueError

	first, middle, last = [int(part) for part in match.groups()]
	if len(match.group(1)) == 4:
		year, month, day = first, middle, last
	elif len(match.group(3)) == 4:
		day, month, year = first, middle, last
	else:
		raise ValueError

	return date(year, month, day)


def _normalize_calendar(calendar):
	calendar = str(calendar or "gregorian").strip().lower()

	if calendar in GREGORIAN_ALIASES:
		return "gregorian"
	if calendar in HIJRI_ALIASES:
		return "hijri"

	raise ValueError


def _normalize_output_format(output_format, include_suffix):
	if isinstance(output_format, bool):
		return "words", output_format

	output_format = str(output_format or "words").strip().lower()

	if output_format in WORD_FORMAT_ALIASES:
		return "words", include_suffix
	if output_format in NUMBER_FORMAT_ALIASES:
		return "numbers", include_suffix

	raise ValueError


def _normalize_separator(separator):
	separator = str(separator or "-").strip()
	if separator not in DATE_SEPARATORS:
		raise ValueError

	return separator


def _format_arabic_date(day, month, month_name, year, suffix, output_format, separator):
	if output_format == "numbers":
		formatted_date = separator.join(
			[
				english_to_arabic_numbers(f"{day:02d}"),
				english_to_arabic_numbers(f"{month:02d}"),
				english_to_arabic_numbers(year),
			]
		)
	else:
		formatted_date = f"{english_to_arabic_numbers(day)} {month_name} {english_to_arabic_numbers(year)}"

	if suffix:
		return f"{formatted_date} {suffix}"

	return formatted_date
