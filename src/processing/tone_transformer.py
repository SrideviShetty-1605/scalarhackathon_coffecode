import re

CONTRACTIONS = {
    "do not": "don't",
    "does not": "doesn't",
    "i would": "I'd",
    "i am": "I'm",
    "i will": "I'll",
    "cannot": "can't",
}

def tone_transform(text: str, mode: str = "neutral") -> str:
    """
    Very simple tone transform:
    - neutral: return as is
    - casual: expand contractions
    - formal: de-contract (don't -> do not)
    - concise: remove some weak words
    """
    if not text:
        return text
    out = text

    if mode == "neutral":
        return out

    if mode == "casual":
        for k, v in CONTRACTIONS.items():
            pattern = r"\b" + re.escape(k) + r"\b"
            out = re.sub(pattern, v, out, flags=re.IGNORECASE)
        return out

    if mode == "formal":
        for k, v in CONTRACTIONS.items():
            pattern = r"\b" + re.escape(v) + r"\b"
            out = re.sub(pattern, k, out, flags=re.IGNORECASE)
        return out

    if mode == "concise":
        out = re.sub(r"\b(very|actually|basically|quite|just)\b", "", out, flags=re.IGNORECASE)
        out = re.sub(r"\s{2,}", " ", out).strip()
        return out

    # unknown mode -> return unchanged
    return out
