# ranked_MTG_draft_analysis

# Overview 
Homemade code that analyzes the results of best-of-one Magic the Gathering (MTG) Arena draft results to help reveal detailed win rate information and player tendencies. 

# What is a draft? 
A draft is a game mode where a circle of eight players each open a 15-card pack (so 120 total cards at the table), select one card from their pack, simultaneously pass the remaining 14 cards to their neighbor, then each make another pick, repeating the process of selecting and passing until the packs are depleted. This is repeated for two more packs (each) and players contruct minimum 40-card decks from their selections to battle against other drafters. This code is designed for best-of-one drafts on the MTG Arena client, where a draft run completes once the player reaches either 7 wins or 3 losses, whichever occurs first. Matches are created according to current win rate and the players' ranks. Thus, players' win rates are pushed towards 50% because you encounter stronger and stronger opponents on average the more you win (given enough time to reach equilibrium). This document will follow the convention of listing (wins-losses) when stating records. Also, the pool of draftable cards (referred to as "draft sets" or "MTG sets") changes every few months allowing the opportunity to compare results within draft sets and also collectively.

# Questions (for a given player and a given MTG set)
1. Which cards improve winrate the most?
   * Are certain cards being over or underplayed based on their contribution?
3. Which combinations of cards synergize the best?
4. Which color pairs are the best?

# Data Collection 
The input file is admittedly not as sophisticated as pulling results from MTG Arena output files, but I choose this approach because I had records from my entire usage across many iterations of the client and because old records are periodically discarded by the client. Typing up the input file is alleviated with text editors that feature autocomplete and by working on the task incrementally.

The input file follows the following format (csv) for each draft entry:

![image](https://user-images.githubusercontent.com/20996215/127382097-bab2dee5-7f4a-4082-8b3e-4c1bb63697f6.png)

The first line contains: 3-letter set code, number of wins, number of losses, colors, premier or not.

Defining the colors of a given deck is definitely a judgement call and some decks are less straightforward than others. The pattern to follow, is to list included colors in alphabetical order where blue=u and is listed before "w" in this manner: b, g, r, u, w. Uppercase indicates a main color and lowercase indicates a splash color. Most of the analysis is centered around two-color pairs as that is historically the most prevalent outcome. There is opportunity for more targeted analysis of sets that deviate from this norm such as mono- or multicolored-focused enviroments. Immediately after the color entries, a single lowercase "p" indicates if the draft was "premier", drafted against humans as opposed to bots. A bot draft is assumed if "p" is left off.

Following the first descriptor line, the cards are listed, preceded by their count. Note that commas are left out of names as to not disrupt the csv format. Also, some decks/sets depend on sideboard cards and when that is relevant those cards are listed in the same manner, except with a lowercase "s" as the count. Duplicate sideboard cards are input using repeat "s"-count entries.

Each individual draft is stored as a draft object with the attributes made up of the input information.

# Code Output 
One of the output files produced is a pdf where each row represents a draft set (gameplay variant, indicated with a 3-letter code) and where the left column is a histogram for that draft set with bins for the 10 possible outcomes (0-3 up to 7-0). Draft count and win rate by draft set is also posted in the left column in red font. The right column displays a time series of wins verses draft index (chronological order, not to scale). A linear trendline is also depicted with its corresponding equation in red for each time series. Given enough data points, the trendline can indicate the win rate trajectory of a given set (decreasing, neutral, or increasing).

![image](https://user-images.githubusercontent.com/20996215/127245189-b8ac76f9-adc3-40c6-a76c-16b24187c4e7.png)

![image](https://github.com/mehutchi/ranked_MTG_draft_analysis/blob/main/histogram_timeseries_452.pdf)

One interesting observation from the time series in this set is that the win rate for some of the high-volume draft sets has a noticeable slope. GRN and DOM (near the top of the above diagram) have a noticable postive trajectory where IKO (near the middle) has a negative trajectory. A major aspect of the drafts and the games themselves is a struggle between power and concistancy. Generally, due to the nature of the resource system, a player tends to play two out of the five possible colors. Sometimes one can increase the power level by "splashing" other colors, but without enough ways to compensate for the additional color requirements your win rate could suffer despite the theoretical increase in power by sacrificing concistancy. IKO was a set seeded with many cards to encourage "splashing" into more colors and it seems that over time the temptation to splash torpedoed the win rate. DOM was more straighforward and helped curb frequent extreme attempts at "splashing with its lack of enabling more colors per deck. GRN included many cards to enable splasing, but lacked many of the payoff incentive of IKO and was also unique in incentivizing just 5 two-color pairs instead of the typical 10.

![image](https://user-images.githubusercontent.com/20996215/133313617-e81848dc-2035-4558-ac3f-f10961c6c4a3.png)

# Analysis 
The above image is the unified histogram of the outcomes across all draft sets, accounting every draft event. It has largely normal Gaussian characteristics, but there is an inversion of expected bin height for the 6-3 and 7-2 outcomes. I estimate this is because of the 7-win-ceiling and the 3-loss-floor. Any start outside of an immediate 0-3 has the possibility of reaching a 7-win record. On the ends of the histrogram, there is only one path to obtaining an 0-3 and also only one path to a 7-0. However, these bin heights are nowhere near the same, because 7 wins is much harder to obtain than 3 losses. To explore the disparity between expected and actual bin heights of the histogram, I made a short brute-force code to determine the number of total outcomes (win/loss sequences, ex. [w, l, w, l, w, w, l] is a sample 4-3 outcome). This code randomly builds outcomes according to the 7-win-ceiling and the 3-loss-floor rules, saving newly discovered outcomes to a list. After running the code a few times with different iteration counts (all the way up to 100,000 iterations) and the code converged at 120 total outcomes after about 2000 iterations. Here is the code:

```import random
from collections import Counter

# function to brute-force determine the number of outcomes for each record
def brute_force(count):
    ''' example outcome (w/l sequence) for 4-3 -> [w, l, w, l, w, w, l]
    '''
    # variables for counting the outcomes for the 10 possible records
    o1 = 0 #0-3
    o2 = 0 #1-3
    o3 = 0 #2-3
    o4 = 0 #3-3
    o5 = 0 #4-3
    o6 = 0 #5-3
    o7 = 0 #6-3
    o8 = 0 #7-2
    o9 = 0 #7-1
    o10 = 0 #7-0
    # list to hold each unique outcome
    holding_list = []
    # for each i in count, create a random outcome
    for i in range(count):
        # intialize outcome list
        rc = []
        # co = Counter(rc)
        # boolean to end outcome build loop
        build = True
        while build == True:
            # generate random float between 0 and 1
            rand = random.uniform(0, 1)
            # 50/50 chance for an "l" or a "w"
            if rand > 0.5:
                rc.append("l")
            else:
                rc.append("w")
            # create a Counter object to count occurances in outcome list
            co = Counter(rc)
            # as long as ending conditions are not yet met
            if co["l"] == 3 or co["w"] == 7:
                # if the outcome is not yet in the holding_list
                if rc not in holding_list:
                    holding_list.append(rc)
                    # increment the appropriate variable
                    if co["l"] == 3 and co["w"] == 0:
                        o1 += 1
                    elif co["l"] == 3 and co["w"] == 1:
                        o2 += 1
                    elif co["l"] == 3 and co["w"] == 2:
                        o3 += 1
                    elif co["l"] == 3 and co["w"] == 3:
                        o4 += 1
                    elif co["l"] == 3 and co["w"] == 4:
                        o5 += 1
                    elif co["l"] == 3 and co["w"] == 5:
                        o6 += 1
                    elif co["l"] == 3 and co["w"] == 6:
                        o7 += 1
                    elif co["l"] == 2 and co["w"] == 7:
                        o8 += 1
                    elif co["l"] == 1 and co["w"] == 7:
                        o9 += 1
                    elif co["l"] == 0 and co["w"] == 7:
                        o10 += 1
                    print("iteration %i total outcomes count: %i"%(i, len(holding_list)))
                build = False
    print("outcomes by record: 0-3 has %i"%o1)
    print("outcomes by record: 1-3 has %i"%o2)
    print("outcomes by record: 2-3 has %i"%o3)
    print("outcomes by record: 3-3 has %i"%o4)
    print("outcomes by record: 4-3 has %i"%o5)
    print("outcomes by record: 5-3 has %i"%o6)
    print("outcomes by record: 6-3 has %i"%o7)
    print("outcomes by record: 7-2 has %i"%o8)
    print("outcomes by record: 7-1 has %i"%o9)
    print("outcomes by record: 7-0 has %i"%o10)
    
    return holding_list
        
all_outcomes = brute_force(100000)
```

(End of code) Here is the outcomes broken down by each possible record as reported by the code:

outcomes by record: 0-3 has 1

outcomes by record: 1-3 has 3

outcomes by record: 2-3 has 6

outcomes by record: 3-3 has 10

outcomes by record: 4-3 has 15

outcomes by record: 5-3 has 21

outcomes by record: 6-3 has 28

outcomes by record: 7-2 has 28

outcomes by record: 7-1 has 7

outcomes by record: 7-0 has 1

It is important to recognize that we should not expect the bins of unified histogram to match these raw outcome counts. The outcomes do not have equal weights because of the difficulty of winning as opposed to losing. That being said, we can see that 6-3 and 7-2 both have 28 distinct outcomes. The relatively high outcome count for these two records helps explain the high bins we see in the unified histogram, but it does not explain the fact that the 7-2 bin is larger than the 6-3 bin. We would expect their bin heights to be inverted since the more win-dense outcomes of the 7-2 record should be harder to obtain. The only explanation I can think of is that there must be a pschological effect when sitting at 6 wins and shooting for the 7th win. Perhaps at that point, the player's play style subconciously shifts to a more aggressive (or a more conservative) tactic when on the cusp of maxing out the wins and obtaining the larger prize payout. 

In addition to the above plots, a detailed breakdown of each draft set is included in an output file. Below is sample output for one of the draft sets:

```
*****			               *****
***** Draft info for KHM       *****
*****			               *****
Total number of drafts is 38
Total games = 247, total wins = 146, total losses = 101, win % = 59.11
Seven win drafts = 10, SWD % = 26.32

Top 20 most played/drafted cards

26 sarulf's packmate
25 behold the multiverse
21 struggle for skemfar
20 mistwalker
20 berg strider
17 shimmerdrift vale
17 demon bolt
16 frost bite
16 snow-covered mountain
16 bound in gold
15 snow-covered plains
14 squash
14 glittering frost
13 highland forest
13 bind the monster
13 dwarven reinforcements
13 beskir shieldmate
13 sculptor of winter
12 ravenous lindwurm
12 gnottvold recluse

** Information by main (not splashed) colors for KHM **

Black
drafts = 8, games = 37, wins = 13, losses = 24, win % = 35

Green
drafts = 21, games = 148, wins = 95, losses = 53, win % = 64

Red
drafts = 17, games = 99, wins = 55, losses = 44, win % = 56

Blue
drafts = 21, games = 151, wins = 96, losses = 55, win % = 64

White
drafts = 10, games = 68, wins = 40, losses = 28, win % = 59

** Information by main color pairs for KHM **

BG
drafts = 2, games = 7, wins = 1, losses = 6, win % = 14

BR
drafts = 3, games = 13, wins = 4, losses = 9, win % = 31

BU
drafts = 1, games = 9, wins = 6, losses = 3, win % = 67

BW
drafts = 2, games = 8, wins = 2, losses = 6, win % = 25

GR
drafts = 8, games = 51, wins = 31, losses = 20, win % = 61

GU
drafts = 10, games = 81, wins = 56, losses = 25, win % = 69

GW
drafts = 2, games = 18, wins = 14, losses = 4, win % = 78

RU
drafts = 6, games = 36, wins = 22, losses = 14, win % = 61

RW
drafts = 1, games = 8, wins = 5, losses = 3, win % = 62

UW
drafts = 5, games = 34, wins = 19, losses = 15, win % = 56
```

(End of output) The most drafted cards are listed in addition to win rate broken down by the five colors, then the ten color pairs. Especially for the color pairs, it is important to take into account the number of drafts/games played. For example, BU has a winrate of 67% which is quite good, but that is just from one draft. If we look at the data for all drafts that had black, the winrate was only 35%. KHM is a set where the community concensus was that black was a drastically weak color. This bears out in my data, and also helped me realize that I needed to try to avoid black when drafting. Here I have a high win rate with GW, but only across two drafts. This could mean that the color pair is strong, or it could just be two drafts carried by individually powerful card inclusions. With 10 drafts played, it seems safe to conlcude that GU is one of my best (if not my best) color pair. The GU archetype was notable in KHM because of how easy it was to "splash" (play a few strong cards of other colors) without a major concistancy hit. However, my win rate when splashing (in any combination) in KHM was only 58% across the board. 
