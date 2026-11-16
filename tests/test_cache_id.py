from app.cache.answer_cache import make_cache_id


def test_same_question_gives_same_id():
    assert make_cache_id("cityeyeprod", "ar", "ما هي اوقات الهدوء") == make_cache_id("cityeyeprod", "ar", "ما هي اوقات الهدوء")


def test_different_compound_gives_different_id():
    assert make_cache_id("cityeyeprod", "ar", "ما هي اوقات الهدوء") != make_cache_id("greens", "ar", "ما هي اوقات الهدوء")


def test_different_language_gives_different_id():
    assert make_cache_id("cityeyeprod", "ar", "quiet hours") != make_cache_id("cityeyeprod", "en", "quiet hours")


def test_different_writing_of_same_question_gives_same_id():
    assert make_cache_id("cityeyeprod", "ar", "ما هي أوقات الهدوء؟") == make_cache_id("cityeyeprod", "ar", "ما هي اوقات الهدوء")