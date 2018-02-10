
AFFIRMATIVE_CONFIRMATION = "y"
NEGATIVE_CONFIRMATION = "n"

def normalize_input_confirmations(input):
    lower = input.lower()
    if lower in ["yes", "y"]:
        return AFFIRMATIVE_CONFIRMATION
    elif lower in ["no", "n"]:
        return NEGATIVE_CONFIRMATION
    else:
        return False
