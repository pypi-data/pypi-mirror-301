import json
import re

try:
    # For Python 3.9 and above
    import importlib.resources as pkg_resources
except ImportError:
    # For Python 3.7 - 3.8
    import importlib_resources as pkg_resources

def load_abbreviation_dict(filename):
    package_name = 'normalizer_usps.data'
    with pkg_resources.open_text(package_name, filename) as f:
        abbreviation_dict_raw = json.load(f)
    # Convert keys to uppercase
    abbreviation_dict = {k.upper(): v for k, v in abbreviation_dict_raw.items()}
    return abbreviation_dict

# Load dictionaries
street_type_abbreviations = load_abbreviation_dict('street_type_abbreviations.json')

def normalize_abbreviations(address_series, abbreviation_dict):
    # Compile regex pattern from uppercase dictionary keys
    keys = map(re.escape, abbreviation_dict.keys())
    pattern = r'\b(' + '|'.join(keys) + r')\b'
    compiled_pattern = re.compile(pattern, flags=re.IGNORECASE)

    # Define replacement function
    def replace_func(match):
        word = match.group(0)
        upper_word = word.upper()
        replacement = abbreviation_dict.get(upper_word, word)
        return replacement

    # Replace matches using the abbreviation dictionary
    return address_series.str.replace(compiled_pattern, replace_func, regex=True)
