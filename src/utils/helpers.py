def safe_text(s: str) -> str:
    """
    Trim and make sure we never explode on None.
    """
    return (s or "").strip()
