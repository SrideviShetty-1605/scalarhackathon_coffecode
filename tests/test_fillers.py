from src.utils.text_cleaner import quick_clean

def test_remove_fillers():
    s = "um I think um this is like a test"
    out = quick_clean(s)
    # 'um' and 'like' should be removed
    assert "um" not in out.lower()
    assert " like " not in out.lower()
