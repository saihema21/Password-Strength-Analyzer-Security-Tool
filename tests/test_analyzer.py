from utils.analyzer import analyze_password


def test_common_password():
    result = analyze_password("123456")
    assert result["classification"] == "VERY WEAK"
    assert result["metrics"]["common_password"] is True


def test_strong_password():
    result = analyze_password("River!Cloud#92Moon$Tree")
    assert result["score"] >= 61
    assert result["classification"] in ["STRONG", "VERY STRONG"]


def test_length_detection():
    result = analyze_password("abc123")
    assert result["metrics"]["length"] == 6


def test_sequence_detection():
    result = analyze_password("abcd1234")
    assert result["metrics"]["sequence_detected"] is True


def test_repeated_character_detection():
    result = analyze_password("aaaaBBBB1111")
    assert result["metrics"]["repeated_characters"] is True