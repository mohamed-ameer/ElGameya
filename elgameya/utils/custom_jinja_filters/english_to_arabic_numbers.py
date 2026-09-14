def english_to_arabic_numbers(value):
    """
    Convert English numerals to Arabic-Indic numerals
    Works with integers, floats, and numeric strings
    
    Example:
    - english_to_arabic_numbers(1234.56)
    '١٢٣٤.٥٦'
    - english_to_arabic_numbers("7890")
    '٧٨٩٠'
    """
    if value is None:
        return ""

    arabic_digits = {
        '0': '٠',
        '1': '١',
        '2': '٢',
        '3': '٣',
        '4': '٤',
        '5': '٥',
        '6': '٦',
        '7': '٧',
        '8': '٨',
        '9': '٩'
    }

    return ''.join(arabic_digits.get(char, char) for char in str(value))