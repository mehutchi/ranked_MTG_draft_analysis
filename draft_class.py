#!/usr/bin/env python

class draft:
    def __init__(self, mtg_set, wins, losses, draft_type, companion, sideboard, main_colors, splash_colors, cards):
        # the draft's set
        self.set = mtg_set
        # number of wins
        self.wins = wins
        #number of losses
        self.losses = losses
        # adding this with the advent of Quick and Premier drafts, default in main code is 'q'
        self.draft_type = draft_type
        # adding this with the advent of companions
        self.companion = companion
        # adding this with the advent of learn/lessons
        self.sideboard = []
        # main (capitalized) colors
        self.main_colors = main_colors
        # list of cards
        self.cards = cards
        # secondary (lower cased) colors
        self.splash_colors = splash_colors