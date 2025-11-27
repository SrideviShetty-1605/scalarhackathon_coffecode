import re

FILLERS = [
    r"\bumm\b", r"\buh\b", r"\buhh\b", r"\bmmm\b", r"\bhmm\b",
    r"\byou know\b", r"\blike\b", r"\bi mean\b", r"\ber\b", r"\bmm\b"
]

FILLER_REGEX = re.compile("|".join(FILLERS), flags=re.IGNORECASE)

def remove_fillers(text: str) -> str:
    """
    Remove common speech fillers from text.
    """
    if not text:
        return text
    cleaned = FILLER_REGEX.sub("", text)
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
    return cleaned
