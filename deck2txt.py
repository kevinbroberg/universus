# coding=utf-8
import json
import argparse
from collections import Counter
from tkinter import filedialog

sauce = filedialog.askopenfilename()
deck_name = sauce.partition('.json')[0]

with open(sauce, "r") as read:
    data = json.load(read)

contained = data["ObjectStates"][0]
cards = [card["Nickname"].lower() for card in contained["ContainedObjects"]]
deck = ["{} {}".format(qty, name) for name, qty in Counter(cards).items()]

with open(deck_name + ".txt", "w") as outfile:
    outfile.write("\n".join(deck))
