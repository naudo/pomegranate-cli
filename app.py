import argparse
import pprint


from core.input import normalize_input_confirmations, AFFIRMATIVE_CONFIRMATION, NEGATIVE_CONFIRMATION
from data.models import *

DEFAULT_LIST = "default"

# Used to track the starting point of this study session
START_POINT = None


def main():
    pp = pprint.PrettyPrinter(indent=4)

    # with db:
    create_tables()

    args = build_arg_parser()

    print("Initial State")
    wl = session.query(WordList).filter(WordList.name == args.list).all()
    if len(wl) == 0:
        wl = WordList(name=args.list)
        session.add(wl)
        session.commit()
        print(wl.id)
    elif len(wl) > 1:
        raise Exception("More than list found for {}".format(args.list))
    else:
        print("Found List with ID {}".format(wl))
    wl = wl[0]

    if args.add:
        # wl = WordList.query.filter(WordList.name == args.list).all()
        wl.entries.append(WordListEntry(word=args.add))
        session.add(wl)
        session.commit()
        # wl = WordList.select().where(WordList.name == args.list).get()
        print("adding {} to {}".format(args.add, wl))
        print("{} has a count of {} words".format(wl.name, len(wl.entries)))
    else:
        study(wl)


class Word:
    def __init__(self, word):
        self.word = word


def study(ls=DEFAULT_LIST):
    global START_POINT
    entry = ls.entries[0]
    while True:
        resp = normalize_input_confirmations(input("Do you know this: {}? (Y/N)".format(entry.word)))
        feedback = WordListEntryFeedback(word_list_entry_id=entry.id)

        if resp == AFFIRMATIVE_CONFIRMATION:
            feedback.feedback = True

            entry = ls.entries[1]

        elif resp == NEGATIVE_CONFIRMATION:
            feedback.feedback = False
            entry = ls.entries[2]

        session.add(feedback)
        session.commit()

        if not START_POINT:
            START_POINT = feedback.id


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


def add_words(db, word, ls=DEFAULT_LIST):
    found_lists = [l for l in db["lists"] if l["name"] == ls]

    if len(found_lists) != 1:
        raise Exception("Unable to continue. Found non-one number of lists for {}".format(list))

    found_lists[0]["entries"].append({"word": word})


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nThanks for playing!")
        study_session_results = session.query(WordListEntryFeedback).filter(WordListEntryFeedback.id >= START_POINT).all()
        print(study_session_results)
