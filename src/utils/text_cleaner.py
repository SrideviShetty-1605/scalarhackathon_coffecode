from src.processing.filler_removal import remove_fillers
from src.processing.repetition_removal import remove_repetitions
from src.processing.formatter import format_text

def quick_clean(text: str) -> str:
    """
    Fast, lightweight cleaning only (no grammar / tone).
    """
    t = remove_fillers(text)
    t = remove_repetitions(t)
    t = format_text(t)
    return t

