def remove_repetitions(text: str) -> str:
    """
    Remove immediate repeated words (e.g., 'I I' -> 'I').
    """
    if not text:
        return text
    tokens = text.split()
    out = []
    for tok in tokens:
        if not out:
            out.append(tok)
            continue
        if tok.lower() == out[-1].lower():
            continue
        out.append(tok)
    return " ".join(out)

