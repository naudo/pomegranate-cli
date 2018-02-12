import argparse

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


def build_arg_parser():
    parser = argparse.ArgumentParser()
    # study = parser.add_mutually_exclusive_group()

    lists = parser.add_mutually_exclusive_group()
    lists.add_argument("--create", help="Create a new List")

    add_words = parser.add_mutually_exclusive_group()
    add_words.add_argument("--add", help="Add a word to a list")

    parser.add_argument("-l", "--list",
                        help="The list to add words to. If not provided, will use a list named default",
                        default="default")
    return parser.parse_args()
