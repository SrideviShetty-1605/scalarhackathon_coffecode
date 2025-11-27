"""
Offline-safe 'grammar correction'.

No external API calls. Just tiny deterministic fixes:
- simple contractions
- collapse extra spaces
"""

import time
import re

_SIMPLE_CORRECTIONS = {
    r"\bi m\b": "I'm",
    r"\bi am\b": "I'm",
    r"\bcannot\b": "can't",
    r"\bdo not\b": "don't",
    r"\bdoes not\b": "doesn't",
}

_PATTERNS = [
    (re.compile(pattern, flags=re.IGNORECASE), repl)
    for pattern, repl in _SIMPLE_CORRECTIONS.items()
]

def apply_languagetool(text: str, lang: str = "en-US", timeout: float = 0.1):
    """
    Return (corrected_text, elapsed_ms)
    """
    if not text:
        return text, 0.0

    start = time.time()
    out = text

    for patt, repl in _PATTERNS:
        out = patt.sub(repl, out)

    out = re.sub(r"\s{2,}", " ", out).strip()
    elapsed_ms = (time.time() - start) * 1000.0
    return out, elapsed_ms
