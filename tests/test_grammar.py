from src.processing.grammar_correction import apply_languagetool

def test_grammar_correction_runs():
    text = "i am happy"
    out, ms = apply_languagetool(text)
    assert isinstance(out, str)
    assert isinstance(ms, float)
