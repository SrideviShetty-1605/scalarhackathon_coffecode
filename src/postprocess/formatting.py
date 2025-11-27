import re

def format_text(text):
    text = text.strip()
    if not text:
        return text
    text = text[0].upper() + text[1:]
    if text[-1] not in ".!?":
        text += "."
    text = re.sub(r"\s+", " ", text)
    return text
