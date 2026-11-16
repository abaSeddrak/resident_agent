import re

ALEF_VARIANTS = re.compile("[أإآ]")
DIACRITICS = re.compile("[\u064B-\u0652\u0640]")
PUNCTUATION = re.compile(r"[^\w\s]")


def normalize_question(text: str) -> str:
    text = DIACRITICS.sub("", text)
    text = ALEF_VARIANTS.sub("ا", text)
    text = text.replace("ة", "ه").replace("ى", "ي")
    text = PUNCTUATION.sub(" ", text)
    text = " ".join(text.split())
    return text.lower()