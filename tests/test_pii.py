from app.guardrails.pii import redact_pii


def test_mobile_number_is_redacted():
    assert redact_pii("رقمي 01222295498") == "رقمي [EGYPT_PHONE]"


def test_international_format_is_redacted():
    assert redact_pii("رقمي +201222295498") == "رقمي [EGYPT_PHONE]"


def test_mobile_with_spaces_is_redacted():
    assert redact_pii("رقمي 012 2229 5498") == "رقمي [EGYPT_PHONE]"


def test_landline_is_not_redacted():
    assert redact_pii("رقمي 022111000122") == "رقمي 022111000122"


def test_text_without_numbers_is_unchanged():
    assert redact_pii("اوقات الهدوء ايه؟") == "اوقات الهدوء ايه؟"