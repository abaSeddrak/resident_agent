import httpx
URL = "https://admin.cityeye.online/CityEye_API_Prod/api/Mobile/Configration/GetCompoundConfigration"
CONTENT_KEYS = ["aboutUs", "termsConditions", "faq", "communityRules", "bankInfo"]

def get_compound_content(
    appCode: str, compoundId: int, languageCode: str
) -> dict[str, str]:
    response = httpx.post(
        URL,
        json={
            "compoundId": compoundId,
            "languageCode": languageCode,
            "appCode": appCode,
        },
        timeout=50,
    )

    response.raise_for_status()
    compound = response.json()["result"]["compoundsetting"]
    return {key: compound.get(key) or "" for key in CONTENT_KEYS}

