from transliterate import translit
from langdetect import detect


def from_cyrillic_to_eng(cyrillic_text):
    language_code = detect(cyrillic_text)
    english_text = translit(cyrillic_text, language_code, reversed=True)
    return english_text
