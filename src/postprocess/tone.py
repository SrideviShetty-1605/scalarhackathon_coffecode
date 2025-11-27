def apply_tone(text, mode="formal"):
    if mode == "formal":
        return text.replace("I'm", "I am").replace("can't", "cannot")
    if mode == "casual":
        return text.replace("do not", "don't")
    if mode == "concise":
        for w in ["basically", "actually", "very"]:
            text = text.replace(" " + w + " ", " ")
    return text
