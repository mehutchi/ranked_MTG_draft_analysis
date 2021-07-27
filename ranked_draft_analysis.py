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
    '''Convert a list to a comma-separated string format, so lists can be included in the output file
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

def analyze_all(mains, all_drafts, output_filename):
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
        """ function for color analysis of a given draft set
        output is a text block to be written to the output file
        """
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
    num_sets = len(win_lists)
    # hardcoded bin list for each possible outcome
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
        plt.hist(win_list_hist, bins=bins) #color=['red', 'blue', 'green', 'yellow', 'black', 'orange', 'pink', 'violet']
        plt.text(0.07, 0.85, '%i total drafts, Win%% = %.2f'%(len(win_list_hist), win_perc), color='red', transform=ax1.transAxes)
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


def analyze_set(mains, MTG_set_dictionary, output_filename):
    color_pairs = [['B', 'G'], ['B', 'R'], ['B', 'U'], ['B', 'W'], ['G', 'R'], ['G', 'U'], ['G', 'W'], ['R', 'U'], ['R', 'W'], ['U', 'W']]
    basic_lands = ['swamp', 'forest', 'mountain', 'island', 'plains']
    num_total_wins = 0
    num_total_losses = 0
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
    # color pair variables
    for index, draft in MTG_set_dictionary[1].items():
        for card, num_card in draft.cards.items():
            if card not in all_cards:
                all_cards.update({card : num_card})
            elif card in all_cards:
                all_cards[card] += num_card
        num_total_wins += draft.wins
        num_total_losses += draft.losses
        # collect compete win list
        # 
        if draft.wins == 7:
            num_7_wins += 1
            if draft.losses == 2:
                win_list.append(7)
            elif draft.losses == 1:
                win_list.append(8)
            elif draft.losses == 0:
                win_list.append(9)
        else:
            win_list.append(draft.wins)
#        if draft.wins == 7:
#            num_7_wins += 1
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
    
#    plot_histogram(win_list, mtg_set)
#    plot_win_time_series(win_list, mtg_set)
    
#    if B_wins+B_losses != 0:
#        per_B_wins = B_wins/(B_wins+B_losses)
#    if G_wins+G_losses != 0:
#        per_G_wins = G_wins/(G_wins+G_losses)
#    if R_wins+R_losses != 0:
#        per_R_wins = R_wins/(R_wins+R_losses)
#    if U_wins+U_losses != 0:
#        per_U_wins = U_wins/(U_wins+U_losses)
#    if W_wins+W_losses != 0:
#        per_W_wins = W_wins/(W_wins+W_losses)
#    
#    if BG_wins+BG_losses != 0:
#        per_BG_wins = BG_wins/(BG_wins+BG_losses)
#    if BR_wins+BR_losses != 0:
#        per_BR_wins = BR_wins/(BR_wins+BR_losses)
#    if BU_wins+BU_losses != 0:
#        per_BU_wins = BU_wins/(BU_wins+BU_losses)
#    if BW_wins+BW_losses != 0:
#        per_BW_wins = BW_wins/(BW_wins+BW_losses)
#    if GR_wins+GR_losses != 0:
#        per_GR_wins = GR_wins/(GR_wins+GR_losses)
#    if GU_wins+GU_losses != 0:
#        per_GU_wins = GU_wins/(GU_wins+GU_losses)
#    if GW_wins+GW_losses != 0:
#        per_GW_wins = GW_wins/(GW_wins+GW_losses)
#    if RU_wins+RU_losses != 0:
#        per_RU_wins = RU_wins/(RU_wins+RU_losses)
#    if RW_wins+RW_losses != 0:
#        per_RW_wins = RW_wins/(RW_wins+RW_losses)
#    if UW_wins+UW_losses != 0:
#        per_UW_wins = UW_wins/(UW_wins+UW_losses)
    

#    return 
        
    def color_block(color, num_C, num_wins, num_losses):
        num_games = num_wins + num_losses
        if num_games != 0:
            win_per = num_wins/num_games*100
            text_block = '\n\n%s'%color + '\ndrafts = %i, games = %i, wins = %i, losses = %i, win %% = %.f'%(num_C, num_games, num_wins, num_losses, win_per)
        elif num_games == 0:
            text_block = '\n\n%s'%color + '\nno data for this color(pair)'
#        file.write('\n\nBlack')
#        file.write('\ndrafts = %i, games = %i, wins = %i, losses = %i, win %% = %.f'%(num_B, ))
        return text_block

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
    num_all_drafts = 0
    # open entire raw file as lines
    with open('ranked_draft_analysis.csv') as raw:
        lines = raw.readlines()
    # split each line into its individual elements
    split_lines = list_splitter(lines, ",")
    # chronological list of draft win numbers
    win_list = []
    # iterate over each line
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
            counter = 1
            all_cards = {}
            last_line = False
            # continue iterating until a line is reached where the first element is contained in the set list
            while split_lines[line+counter][0] not in all_sets or last_line == True:
                # use a counter to advance iteration (through the individual draft's lines) until the 
                # while not condition is met
                line_check = line+counter
                # adding companion functionality
                if split_lines[line_check][0] == 'c':
                    num_cards = 1
                    card = split_lines[line_check][1]
                    companion = card
                # adding learn/lesson functionality, but leaving it general for future sideboard mechanics
                elif split_lines[line_check][0] == 's':
                    # num_cards = 1
                    card = split_lines[line_check][1]
                    sideboard.append(card)
                else:
                    num_cards = int(split_lines[line_check][0])
                    card = split_lines[line_check][1]
                all_cards.update({card : num_cards})
                # exit loop if last line of the entire file
                if line_check == len(split_lines)-1:
                    last_line = True
                    break
                counter +=1
            # create a draft_object out of the collected information
            draft_object = draft(mtg_set=mtg_set, wins=wins, losses=losses, draft_type=draft_type, companion=companion, sideboard=sideboard, main_colors=main_colors, splash_colors=splash_colors, cards=all_cards)
            
            
#            win_list.append(wins)
            # functionality for constructing histrograms for the three different 7-win outcomes
            if wins == 7:
                if losses == 2:
                    win_list.append(7)
                elif losses == 1:
                    win_list.append(8)
                elif losses == 0:
                    win_list.append(9)
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
    # complete histogram
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
    # iterate over each set and obtain analysis
    for mtg_set_dict in all_drafts.items():
        win_list, mtg_set, win_perc = analyze_set(mains=mains, MTG_set_dictionary=mtg_set_dict, output_filename=output_filename)
        win_lists.append(win_list)
        mtg_sets.append(mtg_set)
        win_perc_list.append(win_perc)
    column_plot(win_lists, mtg_sets, win_perc_list, num_all_drafts)
    return

if __name__ == '__main__':
    main()
