#!/usr/binenv python
from draft_class import draft
import datetime
import operator
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import numpy as np
from sklearn.linear_model import LinearRegression

import statistics
from statistics import mode

import scipy.cluster.hierarchy
from matplotlib.backends.backend_pdf import PdfPages
import collections

import itertools

import requests
from string import ascii_letters
import unicodedata
# import json

#from PyPDF2 import PdfFileReader, PdfFileWriter

# function for splitting raw line-lists
def list_splitter(raw_list, delimiter=","):
    """function for splitting raw line-list strings into lines of separate elements
    """
    split_list = []
    # split a list (by spaces) into separate elements 
    for i in range(len(raw_list)):
        split_list.append(raw_list[i].split(delimiter))
    return split_list

def print_list(list_file):
    '''Convert a list to a comma-separated string format, 
    so lists can be included in the output file
    '''
    list_len = len(list_file)
    list_str = '[ '
    for i in range(list_len):
        list_str += str(list_file[i])
        # only add a comma and a space if not the last entry
        if i < (len(list_file) - 1):
            list_str += ', '
        if i == (len(list_file) - 1):
            list_str += ' ]'
    return list_str

def list_similarity(list1, list2):
    '''' function for creating symmetric differences between lists 
    (can't use sets because of necessary repeat elements)
     
    This is the "distance" metric for comparing two drafts 
    (from the same set) to each other in order to cluster them
    '''
    l1 = [item for item in list1 if item not in list2]
    l2 = [item for item in list2 if item not in list1]
    lt = l1 + l2 # symmetric difference
    total_entries = len(list1)+len(list2)
    # similarity score for two lists (0-1)
    score = (total_entries-len(lt))/total_entries
    return score

def analyze_all(mains, all_drafts, output_filename):
    ''' analyze all drafts together (not by set)
    '''
    # color pairs, sticking with the alphebetical ordering convention
    color_pairs = [['B', 'G'], ['B', 'R'], ['B', 'U'], ['B', 'W'], ['G', 'R'], ['G', 'U'], ['G', 'W'], ['R', 'U'], ['R', 'W'], ['U', 'W']]
    # basic lands list for filtering their results out of the card counts
    basic_lands = ['swamp', 'forest', 'mountain', 'island', 'plains']
    num_total_wins = 0
    num_total_losses = 0
    num_7_wins = 0
    
    # indidual color variables
    B_wins = 0
    B_losses = 0
    num_B = 0
    G_wins = 0
    G_losses = 0
    num_G = 0
    R_wins = 0
    R_losses = 0
    num_R = 0
    U_wins = 0
    U_losses = 0
    num_U = 0
    W_wins = 0
    W_losses = 0
    num_W = 0
    # color pair variables
    BG_wins = 0
    BG_losses = 0
    num_BG = 0
    BR_wins = 0
    BR_losses = 0
    num_BR = 0
    BU_wins = 0
    BU_losses = 0
    num_BU = 0
    BW_wins = 0
    BW_losses = 0
    num_BW = 0
    GR_wins = 0
    GR_losses = 0
    num_GR = 0
    GU_wins = 0
    GU_losses = 0
    num_GU = 0
    GW_wins = 0
    GW_losses = 0
    num_GW = 0
    RU_wins = 0
    RU_losses = 0
    num_RU = 0
    RW_wins = 0
    RW_losses = 0
    num_RW = 0
    UW_wins = 0
    UW_losses = 0
    num_UW = 0

    
    num_drafts = 0
    for MTG_set_dictionary in all_drafts.items():
        mtg_set = MTG_set_dictionary[0]
        num_drafts += len(MTG_set_dictionary[1])
        
        # color pair variables
        for index, draft in MTG_set_dictionary[1].items():
            num_total_wins += draft.wins
            num_total_losses += draft.losses
            if draft.wins == 7:
                num_7_wins += 1
    #        for C in mains:
    #            if C in draft.main_colors:
    #                C_wins += draft.wins
    #                C_losses += draft.losses
    #                num_C +=1
            # wins/losses by individual colors
            if 'B' in draft.main_colors:
                B_wins += draft.wins
                B_losses += draft.losses
                num_B +=1
                if 'G' in draft.main_colors:
                    BG_wins += draft.wins
                    BG_losses += draft.losses
                    num_BG +=1
                if 'R' in draft.main_colors:
                    BR_wins += draft.wins
                    BR_losses += draft.losses
                    num_BR +=1
                if 'U' in draft.main_colors:
                    BU_wins += draft.wins
                    BU_losses += draft.losses
                    num_BU +=1
                if 'W' in draft.main_colors:
                    BW_wins += draft.wins
                    BW_losses += draft.losses
                    num_BW +=1
            if 'G' in draft.main_colors:
                G_wins += draft.wins
                G_losses += draft.losses
                num_G +=1
                if 'R' in draft.main_colors:
                    GR_wins += draft.wins
                    GR_losses += draft.losses
                    num_GR +=1
                if 'U' in draft.main_colors:
                    GU_wins += draft.wins
                    GU_losses += draft.losses
                    num_GU +=1
                if 'W' in draft.main_colors:
                    GW_wins += draft.wins
                    GW_losses += draft.losses
                    num_GW +=1
            if 'R' in draft.main_colors:
                R_wins += draft.wins
                R_losses += draft.losses
                num_R +=1
                if 'U' in draft.main_colors:
                    RU_wins += draft.wins
                    RU_losses += draft.losses
                    num_RU +=1
                if 'W' in draft.main_colors:
                    RW_wins += draft.wins
                    RW_losses += draft.losses
                    num_RW +=1
            if 'U' in draft.main_colors:
                U_wins += draft.wins
                U_losses += draft.losses
                num_U +=1
                if 'W' in draft.main_colors:
                    UW_wins += draft.wins
                    UW_losses += draft.losses
                    num_UW +=1
            if 'W' in draft.main_colors:
                W_wins += draft.wins
                W_losses += draft.losses
                num_W +=1
    num_total_games = num_total_wins+num_total_losses
    total_per_wins = num_total_wins/num_total_games
    
    def color_block(color, num_C, num_wins, num_losses):
        ''' function for color analysis of a given draft set
        output is a text block to be written to the output file
        '''
        # total number of games
        num_games = num_wins + num_losses
        if num_games != 0:
            # win percentage
            win_per = num_wins/num_games*100
            text_block = '\n\n%s'%color + '\ndrafts = %i, games = %i, wins = %i, losses = %i, win %% = %.f'%(num_C, num_games, num_wins, num_losses, win_per)
        elif num_games == 0:
            text_block = '\n\n%s'%color + '\nno data for this color(pair)'
#        file.write('\n\nBlack')
#        file.write('\ndrafts = %i, games = %i, wins = %i, losses = %i, win %% = %.f'%(num_B, ))
        return text_block

    
    with open(output_filename, 'a+') as file:
        file.write('\n\n\n*****\t\t\t  *****')
        file.write('\n***** OVERALL INFORMATION *****')
        file.write('\n*****\t\t\t  *****')
        file.write('\nTotal number of drafts is %i'%num_drafts)
        file.write('\nTotal games = %i, total wins = %i, total losses = %i, win %% = %.2f'%(num_total_games, num_total_wins, num_total_losses, total_per_wins*100))
        file.write('\nSeven win drafts = %i, SWD %% = %.2f'%(num_7_wins, num_7_wins/num_drafts*100))
        file.write('\n\n** Overall information by main (not splashed) colors **')
        file.write(color_block('Black', num_B, B_wins, B_losses))
        file.write(color_block('Green', num_G, G_wins, G_losses))
        file.write(color_block('Red', num_R, R_wins, R_losses))
        file.write(color_block('Blue', num_U, U_wins, U_losses))
        file.write(color_block('White', num_W, W_wins, W_losses))
        file.write('\n\n** Overall information by main color pairs **')
        file.write(color_block('BG', num_BG, BG_wins, BG_losses))
        file.write(color_block('BR', num_BR, BR_wins, BR_losses))
        file.write(color_block('BU', num_BU, BU_wins, BU_losses))
        file.write(color_block('BW', num_BW, BW_wins, BW_losses))
        file.write(color_block('GR', num_GR, GR_wins, GR_losses))
        file.write(color_block('GU', num_GU, GU_wins, GU_losses))
        file.write(color_block('GW', num_GW, GW_wins, GW_losses))
        file.write(color_block('RU', num_RU, RU_wins, RU_losses))
        file.write(color_block('RW', num_RW, RW_wins, RW_losses))
        file.write(color_block('UW', num_UW, UW_wins, UW_losses))
        
def plot_histogram(win_list, mtg_set):
    # win_list contains 8's for 7-1 and 9's for 7-0 (7 is 7-2)
    # number of bins equal to the outcome possibilities
    fig, ax = plt.subplots()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
#    num_bins = 8
#    plt.hist(win_list, bins=num_bins)
    # hardcoded bin list for each possible outcome
    bins = [0,1,2,3,4,5,6,7,8,9,10]
    
    plt.hist(win_list, bins=bins) #color=['red', 'blue', 'green', 'yellow', 'black', 'orange', 'pink', 'violet']
    plt.text(0.07, 0.93, '%i total drafts'%len(win_list), color='red', transform=ax.transAxes)
    plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5], [0,1,2,3,4,5,6,'7-2','7-1','7-0'])
    plt.title(mtg_set)
    plt.xlabel('Number of Wins')
    plt.ylabel('Number of Drafts')
    plt.savefig('%s_%i.pdf'%(mtg_set, len(win_list)))
    plt.close()
    
def colored_bar_plot(win_list, mtg_set):
    num_bars = 8
    indices = np.range(num_bars)
    pb = plt.bar()
    pg = plt.bar()
    pr = plt.bar()
    pu = plt.bar()
    pw = plt.bar()
    
def plot_win_time_series(win_list_hist, mtg_set):
    # remove the 8's and 9's from the win_list (used for the histogram)
    win_list = [x if x != 8 and x != 9 else 7 for x in win_list_hist]
    fig, ax = plt.subplots()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    
    plt.plot(win_list)
    plt.title('%s Time Series'%mtg_set)
    
    x = np.array(range(len(win_list))).reshape((-1, 1))
    y = np.array(win_list)
    model = LinearRegression().fit(x,y)
    r_sq = model.score(x,y)
    y_pred = model.predict(x)
    m = model.coef_
    b = model.intercept_
    plt.plot(x, y_pred, 'r')
    plt.text(0.07, 0.93, 'y = %.2f*x + %.2f'%(m[0], b), color='red', transform=ax.transAxes)
    plt.xlabel('draft index (chronological order)')
    plt.ylabel('Number of Wins')

def find_max_mode(list1):
    list_table = statistics._counts(list1)
    len_table = len(list_table)

    if len_table == 1:
        max_mode = statistics.mode(list1)
    else:
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        max_mode = max(new_list) # use the max value here
    return max_mode

def column_plot(win_lists, mtg_sets, win_perc_list, num_all_drafts):
    ''' creates a "column plot" where each row is an MTG set, the left column
    is a histogram of record outcomes and the right column is a timeseries of
    record outcomes including a linear trendline
    '''
    num_sets = len(win_lists)
    # hardcoded bin list for each possible outcome (0-3 through 7-0)
    bins = [0,1,2,3,4,5,6,7,8,9,10]
    fig = plt.gcf()
    fig_len = 4 + num_sets
    fig.set_size_inches(8, fig_len)
    
    height = 0
    for wl in win_lists:
        common = find_max_mode(wl)
        tallest = wl.count(common)
        if tallest > height:
            height = tallest

    for i in range(num_sets):
        win_list_hist = win_lists[i]
        mtg_set = mtg_sets[i]
        ax1 = plt.subplot(num_sets, 2, 2*i+1)
        ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    #    num_bins = 8
    #    plt.hist(win_list, bins=num_bins)
        win_perc = win_perc_list[i]
        # create histogram
        plt.hist(win_list_hist, bins=bins) #color=['red', 'blue', 'green', 'yellow', 'black', 'orange', 'pink', 'violet']
        plt.text(0.07, 0.85, '%i total drafts, Win%% = %.2f'%(len(win_list_hist), win_perc), color='red', transform=ax1.transAxes)
        # specfied tick mark locations
        plt.xticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5], [0,1,2,3,4,5,6,'7-2','7-1','7-0'])
        if i == 0:
            plt.title('Histogram')
        if i == num_sets -1:
            plt.xlabel('Number of Wins')
        '''
        plt.yticks([])
        '''
#        yticks[-1].set_visible(False)
        plt.ylim(0, height+1)
        plt.ylabel(mtg_set)
        yticks = ax1.yaxis.get_major_ticks()
        yticks[0].set_visible(False)
        yticks[-1].set_visible(False)

        ax1b = ax1.twinx()
        plt.yticks([])
#        ax1b.yaxis.set_major_locator(MaxNLocator(integer=True))

        plt.ylabel('Drafts')
        ax2 = plt.subplot(num_sets, 2, 2*i+2)
        # remove the 8's and 9's from the win_list (used for the histogram)
        win_list = [x if x != 8 and x != 9 else 7 for x in win_list_hist]
#        fig, ax = plt.subplots()
#        ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
        
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
        
        plt.plot(win_list)
        if i == 0:
            plt.title('Time Series')
        
        x = np.array(range(len(win_list))).reshape((-1, 1))
        y = np.array(win_list)
        model = LinearRegression().fit(x,y)
        r_sq = model.score(x,y)
        y_pred = model.predict(x)
        m = model.coef_
        b = model.intercept_
        plt.plot(x, y_pred, 'r')
        plt.text(0.07, 0.85, 'y = %.2f*x + %.2f'%(m[0], b), color='red', transform=ax2.transAxes)
        plt.xticks([])
        if i == num_sets -1:
            plt.xlabel('draft index (chronological order)')
#            ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
        else:
            plt.xticks([])
        tick_list = [1, 2, 3, 4, 5, 6, 7]
        plt.yticks(tick_list, tick_list)
        plt.ylim(0, 8)
        '''
        yticks2 = ax2.yaxis.get_major_ticks()
        yticks2[0].set_visible(False)
        yticks2[-1].set_visible(False)
        '''
        ax2b = ax2.twinx()
        plt.yticks([])
#        plt.xticks([])
        plt.ylabel('Wins')
#        if i == num_sets -1:
#            ax2b.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.subplots_adjust(hspace=0.000)
    plt.savefig('histogram_timeseries_%i.pdf'%num_all_drafts)
    plt.close()


def analyze_set(mains, MTG_set_dictionary, card_data, output_filename):
    ''' function that analyzes a single MTG set, icluding updating the output file
    and plotting the winshare plots
    '''
    color_pairs = [['B', 'G'], ['B', 'R'], ['B', 'U'], ['B', 'W'], ['G', 'R'], ['G', 'U'], ['G', 'W'], ['R', 'U'], ['R', 'W'], ['U', 'W']]
    basic_lands = ['swamp', 'forest', 'mountain', 'island', 'plains']
    num_total_wins = 0
    num_total_losses = 0
    # counting variables for splashes
    num_splash_wins = 0
    num_splash_losses = 0
    total_splashes = 0
    # seven wins
    num_7_wins = 0
    all_cards = {}
#    num_games = 0
    # obtain first saved key in dictionary
#    mtg_set = MTG_set_dictionary[1].set
#    num_drafts = len(MTG_set_dictionary)
    mtg_set = MTG_set_dictionary[0]
    num_drafts = len(MTG_set_dictionary[1])

    # indidual color variables
    B_wins = 0
    B_losses = 0
    num_B = 0
    G_wins = 0
    G_losses = 0
    num_G = 0
    R_wins = 0
    R_losses = 0
    num_R = 0
    U_wins = 0
    U_losses = 0
    num_U = 0
    W_wins = 0
    W_losses = 0
    num_W = 0
    # color pair variables
    BG_wins = 0
    BG_losses = 0
    num_BG = 0
    BR_wins = 0
    BR_losses = 0
    num_BR = 0
    BU_wins = 0
    BU_losses = 0
    num_BU = 0
    BW_wins = 0
    BW_losses = 0
    num_BW = 0
    GR_wins = 0
    GR_losses = 0
    num_GR = 0
    GU_wins = 0
    GU_losses = 0
    num_GU = 0
    GW_wins = 0
    GW_losses = 0
    num_GW = 0
    RU_wins = 0
    RU_losses = 0
    num_RU = 0
    RW_wins = 0
    RW_losses = 0
    num_RW = 0
    UW_wins = 0
    UW_losses = 0
    num_UW = 0
    
    # not currently in use, but set up for possible colorless emphasis in the future
    C_wins = 0
    C_losses = 0
    num_C = 0
    pair_wins = 0
    pair_losses = 0
    num_pair = 0
    
    win_list = []
    win_shares = {}
    # color pair variables
    for index, draft in MTG_set_dictionary[1].items():
        num_total_wins += draft.wins
        num_total_losses += draft.losses
        # collect information for winshares to be calculated later
        for card, num_card in draft.cards.items():
            # if card not yet in all_cards, create entry
            if card not in all_cards:
                all_cards.update({card : num_card})
                # win share is scaled by number of copies of each card
                # win_shares.update({card : win_share*num_card})
                win_shares.update({card : [num_card, num_total_wins, num_total_losses, 1]})
            # if card already in all_cards, update value
            elif card in all_cards:
                all_cards[card] += num_card
                win_shares[card][0] += num_card
                win_shares[card][1] += num_total_wins
                win_shares[card][2] += num_total_losses
                # increment the number of drafts
                win_shares[card][3] += 1
            # win_shares.update({card : win_share*num_card})
        # tracking winrate when decks "splash" color(s)
        if draft.splash_colors != "":
            num_splash_wins += draft.wins
            num_splash_losses += draft.losses
            total_splashes += 1
        # collect compete win list
        # distinguish 7-win records
        if draft.wins == 7:
            num_7_wins += 1
            if draft.losses == 2:
                win_list.append(7) # 7 = 7-2
            elif draft.losses == 1:
                win_list.append(8) # 8 = 7-1
            elif draft.losses == 0:
                win_list.append(9) # 9 = 7-0
        else:
            win_list.append(draft.wins)
        ### possible colorless archetypes in the future?
#        for C in mains:
#            if C in draft.main_colors:
#                C_wins += draft.wins
#                C_losses += draft.losses
#                num_C +=1
        # wins/losses by individual colors
        # and track color pair combos as well
        if 'B' in draft.main_colors:
            B_wins += draft.wins
            B_losses += draft.losses
            num_B +=1
            if 'G' in draft.main_colors:
                BG_wins += draft.wins
                BG_losses += draft.losses
                num_BG +=1
            if 'R' in draft.main_colors:
                BR_wins += draft.wins
                BR_losses += draft.losses
                num_BR +=1
            if 'U' in draft.main_colors:
                BU_wins += draft.wins
                BU_losses += draft.losses
                num_BU +=1
            if 'W' in draft.main_colors:
                BW_wins += draft.wins
                BW_losses += draft.losses
                num_BW +=1
        if 'G' in draft.main_colors:
            G_wins += draft.wins
            G_losses += draft.losses
            num_G +=1
            if 'R' in draft.main_colors:
                GR_wins += draft.wins
                GR_losses += draft.losses
                num_GR +=1
            if 'U' in draft.main_colors:
                GU_wins += draft.wins
                GU_losses += draft.losses
                num_GU +=1
            if 'W' in draft.main_colors:
                GW_wins += draft.wins
                GW_losses += draft.losses
                num_GW +=1
        if 'R' in draft.main_colors:
            R_wins += draft.wins
            R_losses += draft.losses
            num_R +=1
            if 'U' in draft.main_colors:
                RU_wins += draft.wins
                RU_losses += draft.losses
                num_RU +=1
            if 'W' in draft.main_colors:
                RW_wins += draft.wins
                RW_losses += draft.losses
                num_RW +=1
        if 'U' in draft.main_colors:
            U_wins += draft.wins
            U_losses += draft.losses
            num_U +=1
            if 'W' in draft.main_colors:
                UW_wins += draft.wins
                UW_losses += draft.losses
                num_UW +=1
        if 'W' in draft.main_colors:
            W_wins += draft.wins
            W_losses += draft.losses
            num_W +=1
    num_total_games = num_total_wins+num_total_losses
    # total win percent
    total_per_wins = num_total_wins/num_total_games
    
    def remove_accents(input_str):
        ''' function to remove accents from strings
        '''
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
    def plot_win_shares(mtg_set, win_shares, all_cards, basic_lands, WR, card_data, rarity):
        ''' function that creates winshare plots by rarity
        '''
        counts = []
        ws_value =[]
        card_list = []
        # separate lists for basic lands, since they are on a much different scale
        counts_bl = []
        ws_value_bl = []
        card_list_bl = []
        # iterate over the all_cards dict to obtain each card and the number of copies
        # of that card
        for card, count in all_cards.items():
            # a card's win share is total wins/(total games)*copies/(40*num_drafts)
            ws_val = win_shares[card][1]/(win_shares[card][2]+win_shares[card][1])*win_shares[card][0]/(40*win_shares[card][3])
            # filter out basic lands, which usually have a much higher winshare 
            # and inclusion
            if card not in basic_lands:
                counts.append(count)
                ws_value.append(ws_val)
                card_list.append(card)
            # build lists for basic lands
            else:
                counts_bl.append(count)
                ws_value_bl.append(ws_val)
                # ws_value_bl.append(win_shares[card])
                card_list_bl.append(card)    
        
        # use MTGJSON to look up colors and rarities
        print("plotting %s winshares for %s"%(rarity, mtg_set))
        ### TESTING OUT MTGJSON
        # get the json of the specific set
        response = requests.get('https://mtgjson.com/api/v5/%s.json'%mtg_set)
        # json -> dict
        set_dict = response.json()
        # account for mystical archives (STA) in STX
        if mtg_set == 'STX':
            # have to create a separate dict (ma_dict) to account for STA
            ma_response = requests.get('https://mtgjson.com/api/v5/STA.json')
            ma_dict = ma_response.json()
            ma_card_dict = {}
            for i in range(len(ma_dict['data']['cards'])):
                # workaround for adventure cards (and other multi-face cards like double-sided)
                if 'faceName' in ma_dict['data']['cards'][i]:
                    # name = set_dict['data']['cards'][i]['faceName']
                    name = remove_accents(ma_dict['data']['cards'][i]['faceName'])
                # otherwise get the name from the json
                else:
                    # name = set_dict['data']['cards'][i]['name']
                    name = remove_accents(ma_dict['data']['cards'][i]['name'])
                # remove capitalization and special characters from the name
                stripped_name = ''.join([letter.lower() for letter in ''.join(name) if letter.isalnum() or letter == ' '])
                # ma_card_dict is for looking up STA card indices within STX drafts
                ma_card_dict.update({stripped_name : i})
                
        # dict with punctuation/capitalization-stripped names and their indices
        # MTGJSON uses card indices which are not included in the input data
        # this next loop iterates over the JSON to match the card names to their index
        whole_card_dict = {}
        for i in range(len(set_dict['data']['cards'])):
            # workaround for adventure cards (and other multi-face cards like double-sided)
            if 'faceName' in set_dict['data']['cards'][i]:
                # name = set_dict['data']['cards'][i]['faceName']
                name = remove_accents(set_dict['data']['cards'][i]['faceName'])
            # otherwise get the name from the json
            else:
                # name = set_dict['data']['cards'][i]['name']
                name = remove_accents(set_dict['data']['cards'][i]['name'])
            # remove capitalization and special characters from the name
            stripped_name = ''.join([letter.lower() for letter in ''.join(name) if letter.isalnum() or letter == ' '])
            whole_card_dict.update({stripped_name : i})
            # print('name %s, index %i'%(stripped_name, i))

        # adjust based on rarity
        adj_card_list = []
        adj_counts = []
        adj_ws_value = []
        # when only including cards with certain rarities
        for i, label in enumerate(card_list):
            # workaround for mystical archives (STA) in STX
            # if set is STX AND the card not in STX (its in STA)
            if mtg_set == 'STX' and label not in whole_card_dict:
                use_dict = ma_card_dict[label]
            else:
                use_dict = whole_card_dict[label]
            # if common or uncommon
            if rarity == 'common' or rarity == 'uncommon':
                # print('card %s'%label)
                # print('rarity %s'%set_dict['data']['cards'][use_dict]['rarity'])
                if set_dict['data']['cards'][use_dict]['rarity'] == rarity:
                    adj_card_list.append(card_list[i])
                    adj_counts.append(counts[i])
                    adj_ws_value.append(ws_value[i])
            # when rarity == 'all', include every card
            else:
                adj_card_list = card_list
                adj_counts = counts
                adj_ws_value = ws_value

        # plot (custom) winshares vs count/inclusions
        plt.figure(figsize=(12,6))
        # plt.scatter(counts, ws_value)
        # ws_max = max(win_shares.values())
        ws_ave = sum(adj_ws_value)/len(adj_ws_value)
        count_max = max(adj_counts)
        # create a curve featuring win shares based on user's average for that set
        ave_counts = [i+1 for i in range(count_max)]
        
        # formula to get number of wins based on WR (winrate aka average) and l=3
        ave_ws09 = []
        ave_ws095 = []
        ave_ws_val = 0
        ylabel = r'Win Shares, for a given card: $(wins/games)*copies/(40*drafts)$'
        xlabel = "Number of Inclusions (copies)"
        for i in ave_counts:
            # for "all" or "common", drafts = copies^0.9
            # drafts copies increase compared to drafts over time
            # always at least one copy if included in the draft
            ave_ws_val = (WR)*i/(40*i**0.9) 
            ave_ws09.append(ave_ws_val)
            # for "uncommon", drafts = copies^0.95
            # drafts copies increase compared to drafts over time
            # but less than "common", because they're more uncommon
            ave_ws095.append(ave_ws_val*i**0.9/i**0.95)
        WP = WR*100 # win percentage
        # ave_ws = [i/40*(WR) for i in ave_counts]
        # plot win rate average WS, where drafts is scaled slightly differently 
        # for commons than uncommons
        if rarity == 'common' or rarity == 'all':
            plt.plot(ave_counts, ave_ws09, color='r', label='ws for %.1f ave win rate (drafts=counts^0.9)'%WP)
        elif rarity == 'uncommon':
            plt.plot(ave_counts, ave_ws095, color='r', label='ws for %.1f ave win rate (drafts=counts^0.95)'%WP)
        plt.legend()
        # iterate over cards to plot and annotate
        for i, label in enumerate(adj_card_list):
            # include all cards with winshares above 50 %
            # OR include if above 1/2 of the max count/inclusion rate
            if ws_value[i] > ws_ave*1.5 or all_cards[label] > count_max/2: 
                # workaround for mystical archives (STA) in STX
                # if set is STX AND the card not in STX (it's in STA)
                if mtg_set == 'STX' and label not in whole_card_dict:
                    use_dict = ma_card_dict[label]
                # if set is not STX, proceed as normal
                else:
                    use_dict = whole_card_dict[label]                
                # look up card color for annotation
                if len(set_dict['data']['cards'][use_dict]['colors']) == 0:
                    col = '#a8a495' # colorless, greyish
                elif len(set_dict['data']['cards'][use_dict]['colors']) > 1:
                    col = '#ffab0f' # multicolor "gold", yellowish-orange
                else:                    
                    # dot color where whole_card_dict gets the index needed for the json
                    if set_dict['data']['cards'][use_dict]['colors'][0] == 'B':
                        col = 'k' # black
                    elif set_dict['data']['cards'][use_dict]['colors'][0] == 'G':
                        col = 'g' # green
                    elif set_dict['data']['cards'][use_dict]['colors'][0] == 'R':
                        col = 'r' # red
                    elif set_dict['data']['cards'][use_dict]['colors'][0] == 'U':
                        col = 'b' # blue
                    elif set_dict['data']['cards'][use_dict]['colors'][0] == 'W':
                        col = '#e2ca76' # "sand" color (compensating for white background)
                plt.scatter(adj_counts[i], adj_ws_value[i], color=col)
                plt.annotate(label, (adj_counts[i], adj_ws_value[i]), color=col)
            # not sure if I should label the lower ones, the points are usually too crowded
            # elif ws_value[i] < 0.5: # label cards below a certain threshold in red
            #     plt.annotate(label, (counts[i], ws_value[i]), color='r')
        plt.title("%s Win Shares vs Inclusions for %s Set"%(rarity, mtg_set))
        # plt.ylabel(r'Win Shares, per card: $\sum_{n=1}^{drafts} (wins-losses)/40*copies_{n}$')
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.savefig('win_shares_%s_%s.pdf'%(mtg_set, rarity))
        plt.close()
        
        # only make basic lands plot if rarity == 'all'
        if rarity == 'all':
            # basic lands only plot
            for i, label in enumerate(card_list_bl):
                # color points and annotations to match basic land colors
                if label == "swamp":
                    col = 'k'
                elif label == "mountain":
                    col = 'r'
                elif label == "island":
                    col = 'b'
                elif label == "forest":
                    col = 'g'
                elif label == "plains":
                    col = '#e2ca76' # "sand" color
                plt.scatter(counts_bl[i], ws_value_bl[i], color=col)
                plt.annotate(label, (counts_bl[i], ws_value_bl[i]), color=col)
            plt.title("Win Shares vs Inclusions for basic lands in %s Set"%mtg_set)
            plt.ylabel(ylabel)
            plt.xlabel(xlabel)
            plt.savefig('win_shares_basics_%s.pdf'%mtg_set)
            plt.close()
    
    # filter out arena-exclusive sets from this analysis for now
    # also exclude two-set blocks for now (not much data anyway)
    arena_exclusive = ['AKR', 'CUB', 'KDR', 'RIX']
    # make winshare plots for each set, with the following groups
    rarity_list = ['common', 'uncommon', 'all']
    # iterate over each set
    if mtg_set not in arena_exclusive:
        # create a winshares plot for each rarity
        for rarity in rarity_list:
            plot_win_shares(mtg_set, win_shares, all_cards, basic_lands, total_per_wins, card_data, rarity)
        
    def color_block(color, num_C, num_wins, num_losses):
        ''' function that creates subsection reports for general results output file
        '''
        num_games = num_wins + num_losses
        if num_games != 0:
            win_per = num_wins/num_games*100
            text_block = '\n\n%s'%color + '\ndrafts = %i, games = %i, wins = %i, losses = %i, win %% = %.f'%(num_C, num_games, num_wins, num_losses, win_per)
        elif num_games == 0:
            text_block = '\n\n%s'%color + '\nno data for this color(pair)'
#        file.write('\n\nBlack')
#        file.write('\ndrafts = %i, games = %i, wins = %i, losses = %i, win %% = %.f'%(num_B, ))
        return text_block

    # write general results output file
    with open(output_filename, 'a+') as file:
        file.write('\n\n\n*****\t\t\t *****')
        file.write('\n***** Draft info for %s *****'%mtg_set)
        file.write('\n*****\t\t\t *****')
        file.write('\nTotal number of drafts is %i'%num_drafts)
        file.write('\nTotal games = %i, total wins = %i, total losses = %i, win %% = %.2f'%(num_total_games, num_total_wins, num_total_losses, total_per_wins*100))
        file.write('\nSeven win drafts = %i, SWD %% = %.2f'%(num_7_wins, num_7_wins/num_drafts*100))
        counter = 0
        counter_stop = 20 # number of "most played cards" to show
        file.write('\n\nTop %i most played/drafted cards'%counter_stop)
        # sort cards by count
        sorted_cards = sorted(all_cards.items(), key=operator.itemgetter(1), reverse=True)
        # write the sorted cards list
        for i in range(len(sorted_cards)):
            if sorted_cards[i][0] not in basic_lands:
                if counter < counter_stop:
                    file.write('\n%i %s'%(sorted_cards[i][1], sorted_cards[i][0]))
                    counter += 1
        file.write('\n\n** Information by main (not splashed) colors for %s **'%mtg_set)
        file.write(color_block('Black', num_B, B_wins, B_losses))
        file.write(color_block('Green', num_G, G_wins, G_losses))
        file.write(color_block('Red', num_R, R_wins, R_losses))
        file.write(color_block('Blue', num_U, U_wins, U_losses))
        file.write(color_block('White', num_W, W_wins, W_losses))
        file.write(color_block('\'any splash\'', total_splashes, num_splash_wins, num_splash_losses))
        file.write('\n\n** Information by main color pairs for %s **'%mtg_set)
        file.write(color_block('BG', num_BG, BG_wins, BG_losses))
        file.write(color_block('BR', num_BR, BR_wins, BR_losses))
        file.write(color_block('BU', num_BU, BU_wins, BU_losses))
        file.write(color_block('BW', num_BW, BW_wins, BW_losses))
        file.write(color_block('GR', num_GR, GR_wins, GR_losses))
        file.write(color_block('GU', num_GU, GU_wins, GU_losses))
        file.write(color_block('GW', num_GW, GW_wins, GW_losses))
        file.write(color_block('RU', num_RU, RU_wins, RU_losses))
        file.write(color_block('RW', num_RW, RW_wins, RW_losses))
        file.write(color_block('UW', num_UW, UW_wins, UW_losses))

    return win_list, mtg_set, total_per_wins*100


    

def main():
    # list of MTG Arena sets
    all_sets = ['RIX', 'DOM', 'M19', 'GRN', 'RNA', 'WAR', 'M20', 'ELD', 'THB', 'IKO', 'CUB', 'M21', 'AKR', 'ZNR', 'KDR', 'KHM', 'STX', 'AFR']
    # main colors are capitalized
    mains = ['B', 'G', 'R', 'U', 'W']
    # splash colors are lowercase
    splashes = ['b', 'g', 'r', 'u', 'w']
    # new field corresponding to draft type, since there's more options now
    # p = premier (best of one concluding at 7 wins or 3 losses, but draft process against humans)
    draft_types = ['p']
    # adding companion functionality, default is None
    companion = None
    # adding learn/lesson functionality, default is an empty list
    sideboard = []
    all_drafts = {}
    # splash/multicolor
    splash_wins = 0
    splash_losses = 0
    splash_count = 0
    num_all_drafts = 0
    # open entire raw file as lines
    with open('ranked_draft_analysis.csv') as raw:
        lines = raw.readlines()
    # split each line into its individual elements
    split_lines = list_splitter(lines, ",")
    # chronological list of draft win numbers
    win_list = []
    card_data = {} # placeholder for now

    
    # iterate over each line and save each draft as a draft object
    for line in range(len(split_lines)):
        # if the first element of that line is included in the all_sets list
        if split_lines[line][0] in all_sets:
            # find the line length, in order to catch all the inputs. This can vary depending on 
            # how many splash colors there are
            line_len = len(split_lines[line])
            mtg_set = split_lines[line][0]
            wins = int(split_lines[line][1])
            losses = int(split_lines[line][2])
            main_colors = []
            splash_colors = []
            # default draft type is 'q'
            draft_type = 'q'
            # add colors to the appropriate lists
            for i in range(3, line_len):
                if split_lines[line][i] in mains:
                    main_colors.append(split_lines[line][i])
                elif split_lines[line][i] in splashes:
                    splash_colors.append(split_lines[line][i])
                elif split_lines[line][i] in draft_types:
                    draft_type = split_lines[line][i]
            # counter tracks the place in the document
            counter = 1
            all_cards = {}
            last_line = False
            # continue iterating until a line is reached where the first element is contained in the set list
            while split_lines[line+counter][0] not in all_sets or last_line == True:
                # use a counter to advance iteration (through the individual draft's lines) until the 
                # while not condition is met
                line_check = line+counter
                raw_card = split_lines[line_check][1]
                # stripping the name of non-ascii letters and numbers to be concistent with the stripped database names
                card = ''.join([letter.lower() for letter in ''.join(raw_card) if letter.isalnum() or letter == ' '])
                # adding companion functionality
                if split_lines[line_check][0] == 'c':
                    num_cards = 1
                    # card = split_lines[line_check][1]
                    companion = card
                # adding learn/lesson functionality, but leaving it general for future sideboard mechanics
                elif split_lines[line_check][0] == 's':
                    # num_cards = 1
                    # card = split_lines[line_check][1]
                    sideboard.append(card)
                else:
                    num_cards = int(split_lines[line_check][0])
                    # card = split_lines[line_check][1]
                all_cards.update({card : num_cards})
                # exit loop if last line of the entire file
                if line_check == len(split_lines)-1:
                    last_line = True
                    break
                counter +=1
            # create a draft_object out of the collected information
            draft_object = draft(mtg_set=mtg_set, wins=wins, losses=losses, draft_type=draft_type, companion=companion, sideboard=sideboard, main_colors=main_colors, splash_colors=splash_colors, cards=all_cards)
            
            # multicolor/splash win rate
            if splash_colors != "":
                splash_wins += wins
                splash_losses += losses
                splash_count += 1
            
            # functionality for constructing histrograms for the three different 7-win outcomes
            if wins == 7:
                if losses == 2:
                    win_list.append(7) # 7-2 record
                elif losses == 1:
                    win_list.append(8) # 7-1 record
                elif losses == 0:
                    win_list.append(9) # 7-0 record
            else:
                win_list.append(wins)
            
            # if the MTG set is already a key in the dictionary, update the sub-dictionary for 
            # that MTG set
            if mtg_set in all_drafts:
                num_in_set = len(all_drafts[mtg_set])
                # all_drafts contains keys of MTG sets, the value for each MTG set is a sub-dictionary
                # containing the draft index as a key and the draft object as the value
    
                # update the dictionary and the sub-dictionary, increasing the index by one
                all_drafts[mtg_set].update({num_in_set+1 : draft_object})
#                .update({mtg_set : {num_in_set +1 : draft_object}})
            elif mtg_set not in all_drafts:
                num_in_set = 1
                # all_drafts contains keys of MTG sets, the value for each MTG set is a sub-dictionary
                # containing the draft index as a key and the draft object as the value
                
                # initialize the dictionary and sub-dictionary, starting index is one
                all_drafts.update({mtg_set : {num_in_set : draft_object}})
                
    # draft scores
    
    def card_dict_to_list(cdict):
        ''' function to convert card dictionaries where each element is [card, count] 
        into lists
        '''
        basic_lands = ['swamp', 'forest', 'mountain', 'island', 'plains']
        clist = []
        for card, count in cdict.items():
            # exclude (non-snow) basic lands for this comparison
            if card not in basic_lands:
                # append card i times, where i is the count
                for i in range(count):
                    clist.append(card)
        return clist
    
    def cluster_results(fcluster, threshold):
        ''' function that takes a cluster result and changes the index
        '''
        result = collections.defaultdict(list)
        for i, c in enumerate(fcluster):
            # make it so indexing begins from 1 (for concistency)
            result[c].append(i+1)
            # print("cluster %i draft %i")
        # result = {}
        return result
    
    def analyze_clusters(result, MTG_set_dictionary, mtg_set):
        ''' function that takes a cluster and prints the results and saves
        findings to cluster_results_%s.txt where %s is the MTG set
        '''
        print("clustering %s"%mtg_set)
        cluster_wins = []
        cluster_losses = []
        with open('cluster_results_%s.txt'%mtg_set, 'w') as out:
            out.write('%i drafts among %i clusters in %s\n\n'%(len(MTG_set_dictionary), len(result), mtg_set))
            for c, drafts in sorted(result.items()):
                cluster_cards = {}
                # total wins and losses for a given cluster
                num_wins = 0
                num_losses = 0
                # iterate over drafts contained in cluster c and update win totals and card dictionaries
                for d in drafts:
                    # indexing of 
                    cluster_wins.append(MTG_set_dictionary[d].wins)
                    num_wins += MTG_set_dictionary[d].wins
                    cluster_losses.append(MTG_set_dictionary[d].losses)
                    num_losses += MTG_set_dictionary[d].losses
                    for card in MTG_set_dictionary[d].cards:
                        if card in cluster_cards:
                            cluster_cards[card] = cluster_cards[card] + MTG_set_dictionary[d].cards[card]
                        else:
                            cluster_cards.update({card : MTG_set_dictionary[d].cards[card]})
                    # cluster_cards.update(MTG_set_dictionary[d].cards)
                # print("cluster %i "%c)
                out.write("*** cluster %i"%c)
                ave_wins = num_wins/(num_wins+num_losses)*100
                # print("count: %i ave win %.2f"%(len(drafts), ave_wins))
                num_games = num_wins+num_losses
                # print('num wins %i, num games %i'%(num_wins, num_games))
                out.write(" (count: %i ave win %.2f) ***\n"%(len(drafts), ave_wins))
                sorted_cards = sorted(cluster_cards.items(), key=lambda x: x[1], reverse=True)
                # print sorted list of cards among drafts in cluster (most to least)
                # print(sorted_cards)
                for i in range(len(sorted_cards)):
                    out.write(sorted_cards[i][0] + " %i\n"%sorted_cards[i][1])
                out.write("\n\n")
            
    # clustering steps
    for MTG_set_dictionary in all_drafts.items():
        # create (difference) score matrix (for clustering)
        score_matrix = []
        mtg_set = MTG_set_dictionary[0]
        # if mtg_set == "DOM":
        # print("right before the clustering portion")
        print("%s has "%mtg_set + str(len(MTG_set_dictionary[1])) + " drafts")
        # exclude sets from clustering with fewer than 40 total drafts
        ### this could possibly be reduced to 30 total drafts
        if len(MTG_set_dictionary[1]) > 40:            
            # color pair variables
            for index1, draft1 in MTG_set_dictionary[1].items():
                #num_total_wins += draft1.wins
                #num_total_losses += draft1.losses
                # convert card dictionary to list
                list1 = card_dict_to_list(draft1.cards)   
                row_scores = []
                # iterate over drafts without double-counting
                for index2, draft2 in MTG_set_dictionary[1].items():
                    # print("index1, index2 -> (%i, %i)"%(index1, index2))
                    # convert card dictionary to list
                    list2 = card_dict_to_list(draft2.cards)
                    # use symmetric difference as a "distance" metric between drafts
                    score = list_similarity(list1, list2)
                    # update row_scores list
                    row_scores.append(score)
                # append completed row_scores list
                score_matrix.append(row_scores)
            # clustering
            method = "complete" #"complete"
            linkage = scipy.cluster.hierarchy.linkage(score_matrix, method=method)
            # based on comparison plots accross sets, 
            # average linkage with a threshold of 1.35 was chosen
            thresh = 1.35
            with PdfPages('%s_linkage_%s.pdf'%(method, mtg_set), 'w') as pp:
                fig, ax = plt.subplots()
                plt.title('%s linkage hierarchical clustering dendrogram for %s'%(method, mtg_set))
                scipy.cluster.hierarchy.dendrogram(linkage, no_labels=True, count_sort='descendent')
                plt.axhline(thresh, color='k')
                ymin, ymax = plt.gca().get_ylim()
                plt.ylabel('cluster threshold')
                axb = ax.twinx()
                plt.ylim(ymin, ymax)
                plt.yticks([thresh])
                pp.savefig()
                plt.close()
            # cluster comparison of num_clusters vs threshold (across methods)
            average_linkage = scipy.cluster.hierarchy.linkage(score_matrix, method="average")
            complete_linkage = scipy.cluster.hierarchy.linkage(score_matrix, method="complete")
            single_linkage = scipy.cluster.hierarchy.linkage(score_matrix, method="single")
            ward_linkage = scipy.cluster.hierarchy.linkage(score_matrix, method="ward")
            plot_thresh_list = np.arange(0, 1.9, 0.01)
            a_list = []
            c_list = []
            s_list = []
            w_list = []
            for i in plot_thresh_list:
                a = scipy.cluster.hierarchy.fcluster(average_linkage, t=i, criterion='distance')
                c = scipy.cluster.hierarchy.fcluster(complete_linkage, t=i, criterion='distance')
                s = scipy.cluster.hierarchy.fcluster(single_linkage, t=i, criterion='distance')
                w = scipy.cluster.hierarchy.fcluster(ward_linkage, t=i, criterion='distance')
                a_list.append(max(a))
                c_list.append(max(c))
                s_list.append(max(s))
                w_list.append(max(w))
        
            plt.figure()
            plt.title('Hierarchical Cluster Method Comparison for %s'%mtg_set)
            plt.plot(plot_thresh_list, a_list, label="average")
            plt.plot(plot_thresh_list, c_list, label="complete")
            plt.plot(plot_thresh_list, s_list, label="single")
            plt.plot(plot_thresh_list, w_list, label="ward")
            plt.axvline(thresh, color='k')
            plt.ylabel("Number of Clusters")
            plt.ylim(0, 50)
            #plt.yscale("log")
            plt.xlabel("Threshold")
            #plt.legend([a_list, c_list, s_list], ["average", "complete", "single"], prop={'size':100})
            plt.legend()
            plt.savefig("method_comp_%s.pdf"%mtg_set)
            plt.close()
            
            # using selected threshold mentioned earlier
            results_1_35 = scipy.cluster.hierarchy.fcluster(linkage, t=thresh, criterion='distance')
            result = cluster_results(results_1_35, thresh)
            analyze_clusters(result, MTG_set_dictionary[1], mtg_set)
            
    # complete histogram (of every draft from every set)
    plot_histogram(win_list, 'All Sets')
    # iterate over all sets and drafts to count the total number of drafts
    for set_key, drafts in all_drafts.items():
        dl = len(drafts)
        num_all_drafts += len(drafts)
#    num_all_drafts = sum([len(draft_set) for draft_set in all_drafts])
        output_filename = 'draft_stats_%i.txt'%num_all_drafts
    # write the opening text block of the output file
    with open(output_filename, 'w') as text_block:
        text_block.write('Ranked Magic: The Gathering Arena Draft Analysis')
        text_block.write('\nCreated on %s'%datetime.datetime.now())
        text_block.write('\nSets analyzed: %s'%print_list(all_sets))
        count_list = []
        for i in all_sets:
            count_list.append(len(all_drafts[i]))
        text_block.write('\nDraft Count: %s'%print_list(count_list))
#        text_block.write('\nGames played %i, Games won %i, Games lost %i, win\% %.1f'%())
#        text_block.write('\n\nSET INFORMATION')
    analyze_all(mains=mains, all_drafts=all_drafts, output_filename=output_filename)
    with open(output_filename, 'a+') as text_block:
        text_block.write('\n\nSET INFORMATION')
#    for mtg_set in all_sets:
#        analyze_set(mains=mains, MTG_set_dictionary=all_drafts[mtg_set], output_filename=output_filename)
    # returning win_list and mtg_set from analyze set to create column plot
    win_lists = []
    mtg_sets = []
    win_perc_list = []
    # win_shares = {}
    # iterate over each set and obtain analysis
    for mtg_set_dict in all_drafts.items():
        win_list, mtg_set, win_perc = analyze_set(mains=mains, MTG_set_dictionary=mtg_set_dict, card_data=card_data, output_filename=output_filename)
        win_lists.append(win_list)
        mtg_sets.append(mtg_set)
        win_perc_list.append(win_perc)
    column_plot(win_lists, mtg_sets, win_perc_list, num_all_drafts)
    return

if __name__ == '__main__':
    main()
