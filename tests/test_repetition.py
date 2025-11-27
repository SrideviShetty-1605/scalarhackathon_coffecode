from src.utils.text_cleaner import quick_clean

def test_repetition():
    s = "I think I think this is fine"
    out = quick_clean(s)
    assert "I think I think" not in out
