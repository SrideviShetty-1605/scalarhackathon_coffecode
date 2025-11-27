def dedupe_repetition(text):
    if not text:
        return ""
    words = text.split()
    out = []
    for w in words:
        if not out or w != out[-1]:
            out.append(w)
    return " ".join(out)

