# coding=utf-8
import re
import json
import argparse
from tkinter import filedialog

deck_spec = filedialog.askopenfilename()
deck_name = deck_spec.partition('.txt')[0]

with open(deck_spec, "r") as read:
    deck_in = read.readlines()


def tuples_to_deck(tuples):
    return [cards[name[1]] for name in tuples if name[1] in cards for _ in range(int(name[0]))]


stack = "2781_stack.json"

target_dir = ""


# TODO implement sideboard loading
sideboard = """
1 ninja outcast
1 superior technique
2x Power Struggles

1 undying rage
1 space land
"""
# deck_in = deck_in.replace('\xe2\x80\x99', "'")

# TODO modularize, use the thing i built for Tim
# TODO design script input / output

regex = re.compile(r'\s*(\d+)x?\)? (.*?)\s*$')  # TODO capture characters but not their "dots" (which are weird unicode shit)
deck = [(m.group(1), m.group(2).lower()) for l in deck_in for m in [regex.search(l)] if m]
# deckToMatch = [name[1] for name in deck for times in range(int(name[0]))]

with open(stack, "r") as read:
    data = json.load(read)

contained = data["ObjectStates"][0]
cards = {card["Nickname"].lower(): card for card in contained["ContainedObjects"]}

exact_matches = [what for what in deck if what[1] in cards]
deckToBuild = tuples_to_deck(deck)  # TODO append Levenshtein selections after this. if it worked

print(len(deckToBuild))
unmatched = [name[1] for name in deck if name[1] not in cards]

if unmatched:
    print(unmatched)
else:
    print("No missing cards")
ids = [card["CardID"] for card in deckToBuild]

contained["ContainedObjects"] = deckToBuild
contained["Nickname"] = deck_name
contained["DeckIDs"] = ids
dest = deck_name + ".json"

if target_dir:
    dest = target_dir + "/" + dest

with open(dest, "w") as write:
    json.dump(data, write, indent=2)


def search(name):
    return [card for card in cards if name in card]