from app.cache.normalize import normalize_question


def test_hamza_becomes_alef():
    assert normalize_question("ما هي أوقات الهدوء") == "ما هي اوقات الهدوء"


def test_taa_marbuta_becomes_haa():
    assert normalize_question("كم رسوم الصيانة الشهرية") == "كم رسوم الصيانه الشهريه"


def test_question_mark_is_removed():
    assert normalize_question("ما هي اوقات الهدوء؟") == "ما هي اوقات الهدوء"


def test_extra_spaces_are_removed():
    assert normalize_question("  ما   هي اوقات الهدوء ") == "ما هي اوقات الهدوء"


def test_two_ways_of_writing_give_same_result():
    assert normalize_question("ما هي أوقات الهدوء؟") == normalize_question("ما هي اوقات الهدوء")