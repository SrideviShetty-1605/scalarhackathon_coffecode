import time
from src.processing.filler_removal import remove_fillers
from src.processing.repetition_removal import remove_repetitions
from src.processing.tone_transformer import tone_transform
from src.processing.grammar_correction import apply_languagetool
from src.processing.formatter import format_text

def full_pipeline(raw_text: str, mode: str = "neutral"):
    """
    Run all processing steps and measure simple timings.
    Returns: (final_text, timings_dict)
    """
    timings = {}
    t0 = time.time()

    t = time.time()
    s1 = remove_fillers(raw_text)
    timings["fillers_ms"] = (time.time() - t) * 1000

    t = time.time()
    s2 = remove_repetitions(s1)
    timings["repetition_ms"] = (time.time() - t) * 1000

    t = time.time()
    s3 = tone_transform(s2, mode=mode)
    timings["tone_ms"] = (time.time() - t) * 1000

    s4, lt_ms = apply_languagetool(s3)
    timings["languagetool_ms"] = lt_ms

    t = time.time()
    final = format_text(s4)
    timings["format_ms"] = (time.time() - t) * 1000

    timings["total_ms"] = (time.time() - t0) * 1000
    return final, timings

