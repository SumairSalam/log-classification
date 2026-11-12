import processor_regex as pr


def test_user_logged_in():
    assert pr.classify_with_regex("User User123 logged in") == "User Action"


def test_no_match():
    assert pr.classify_with_regex("something else") == "Other"
