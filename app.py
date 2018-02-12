import pprint

from tabulate import tabulate

from core.input import normalize_input_confirmations, AFFIRMATIVE_CONFIRMATION, NEGATIVE_CONFIRMATION, build_arg_parser
from data.models import *
import collections

DEFAULT_LIST = "default"

# Used to track the starting point of this study session
START_POINT = None


pp = pprint.PrettyPrinter(indent=4)


def main():

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


def study(ls=DEFAULT_LIST):
    global START_POINT
    if len(ls.entries) == 0:
        raise Exception("Nothing to study in this list")
    entries = ls.entries

    while len(entries) > 0:
        entry = entries[0]
        resp = normalize_input_confirmations(input("Do you know this: {}? (Y/N)".format(entry.word)))
        feedback = WordListEntryFeedback(word_list_entry_id=entry.id, feedback= True if resp == AFFIRMATIVE_CONFIRMATION else False)

        session.add(feedback)
        session.commit()
        del entries[0]

        if not START_POINT:
            START_POINT = feedback.id

    summary()


def add_words(db, word, ls=DEFAULT_LIST):
    found_lists = [l for l in db["lists"] if l["name"] == ls]

    if len(found_lists) != 1:
        raise Exception("Unable to continue. Found non-one number of lists for {}".format(list))

    found_lists[0]["entries"].append({"word": word})


def summary():
    print("\nThanks for playing!")
    study_session_results = session.query(WordListEntryFeedback) \
        .filter(WordListEntryFeedback.id >= START_POINT).all()

    print(study_session_results)

    results = [
        [x.entry.word for x in study_session_results if not x.feedback],
        [x.entry.word for x in study_session_results if x.feedback],
    ]

    print("Words you knew")
    print(tabulate(results[0]))

    print("Words to study for next time")
    print(tabulate(results[1]))

    pp.pprint(results)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        summary()

