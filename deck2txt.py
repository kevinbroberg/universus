# coding=utf-8
import json
import argparse
from collections import Counter

parser = argparse.ArgumentParser(description='Transforms a TTS object into a text deck.')
parser.add_argument('deck', metavar='deck', type=str,
                    help='deck json file to read. should end in .json')
args = parser.parse_args()
sauce = args.deck
deck_name = sauce.partition('.json')[0]

with open(sauce, "r") as read:
    data = json.load(read)

contained = data["ObjectStates"][0]
cards = [card["Nickname"].lower() for card in contained["ContainedObjects"]]
deck = ["{} {}".format(qty, name) for name, qty in Counter(cards).items()]

with open(deck_name + ".txt", "w") as outfile:
    outfile.write("\n".join(deck))
