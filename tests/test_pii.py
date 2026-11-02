from app.guardrails.pii import redact_pii

def test_redacts_egypt_phone():
    assert redact_pii("رقمي 01012345678") == "رقمي [EGYPT_PHONE]"