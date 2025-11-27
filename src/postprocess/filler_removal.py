import re

# List of filler words (VERY POWERFUL)
FILLERS = [
    "um", "uh", "ah", "huh", "hmm", "erm", "mmm",
    "okay so", "you know", "i mean", "sort of", "kind of",
    "basically", "actually", "literally",
    "like", "right", "well", "so yeah",
    "kinda", "sorta", "etc"
]

# Create dynamic regex for smart matching
FILLER_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in FILLERS) + r")\b",
    flags=re.IGNORECASE
)

def remove_fillers(text: str) -> str:
    # Remove filler words safely
    cleaned = FILLER_PATTERN.sub("", text)

    # Remove repeated spaces
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Remove repeated words: like like → like (optional)
    cleaned = re.sub(r'\b(\w+)( \1\b)+', r'\1', cleaned, flags=re.IGNORECASE)

    return cleaned
