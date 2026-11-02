import re
EGYPT_PHONE = re.compile(r"(?:\+20|0020|0)[\s-]?1[0125](?:[\s-]?\d){8}")

def redact_pii(text:str)->str:
    return EGYPT_PHONE.sub("[EGYPT_PHONE]", text)