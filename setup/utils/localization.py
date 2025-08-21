import json
import os
from typing import Dict, Optional

_translations: Dict[str, str] = {}
_language: str = "en"

def set_language(language: str = "en"):
    """
    Sets the language for the application.

    Args:
        language: The language code (e.g., "en", "ja").
    """
    global _language, _translations
    _language = language

    # Construct the path to the locale file
    current_dir = os.path.dirname(__file__)
    locale_file = os.path.join(current_dir, "locales", f"{language}.json")

    if os.path.exists(locale_file):
        with open(locale_file, "r", encoding="utf-8") as f:
            _translations = json.load(f)
    else:
        # Fallback to English if the language file is not found
        en_locale_file = os.path.join(current_dir, "locales", "en.json")
        if os.path.exists(en_locale_file):
            with open(en_locale_file, "r", encoding="utf-8") as f:
                _translations = json.load(f)
        else:
            _translations = {}

def get_string(key: str, *args) -> str:
    """
    Gets a translated string by its key.

    Args:
        key: The key of the string to retrieve.
        *args: Optional arguments to format the string.

    Returns:
        The translated and formatted string, or the key itself if not found.
    """
    message = _translations.get(key)
    if message is None:
        # Return a user-friendly fallback: try to join args into a readable form
        if args:
            return f"{key}: " + ", ".join(str(a) for a in args)
        return key

    try:
        if args:
            return message.format(*args)
        return message
    except Exception:
        # If formatting fails, return message with args appended
        if args:
            return message + " " + ", ".join(str(a) for a in args)
        return message

# Initialize with default language
set_language()
