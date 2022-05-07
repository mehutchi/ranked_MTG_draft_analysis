# ranked_MTG_draft_analysis

# Overview 
Homemade code that analyzes the results of best-of-one Magic the Gathering (MTG) Arena draft results to help reveal best-performing cards by rarity, synergistic card combinations, and leading archetypes.

# What is a draft? 
A draft is a game mode where a circle of eight players each open a 15-card pack (so 120 total cards at the table), select one card from their pack, simultaneously pass the remaining 14 cards to their neighbor, then each make another pick, repeating the process of selecting and passing until the packs are depleted. This is repeated for two more packs (each) and players construct minimum 40-card decks from their selections to battle against other drafters. This code is designed for best-of-one drafts on the MTG Arena client, where a draft run completes once the player reaches either 7 wins or 3 losses, whichever occurs first. Matches are created according to current win rate and the players' ranks. Thus, players' win rates are pushed towards 50% because you encounter stronger and stronger opponents on average the more you win (given enough time to reach equilibrium). This document will follow the convention of listing (wins-losses) when stating records. Also, the pool of draftable cards (referred to as "draft sets" or "MTG sets") changes every few months allowing the opportunity to compare results within draft sets and also collectively.

# Questions (for a given player and a given MTG set)
1. Which cards improve win rate the most?
   * Are certain cards being over or underplayed based on their contribution?
3. Which combinations of cards synergize the best?
4. Which color pairs are the best?

# Data Collection 
The input file is admittedly not as sophisticated as pulling results from MTG Arena output files, but I choose this approach because I had records from my entire usage across many iterations of the client and because old records are periodically discarded by the client. Typing up the input file is alleviated with text editors that feature autocomplete and by working on the task incrementally.

The input file follows the following format (csv) for each draft entry:

![image](https://user-images.githubusercontent.com/20996215/127382097-bab2dee5-7f4a-4082-8b3e-4c1bb63697f6.png)

The first line contains: 3-letter set code, number of wins, number of losses, colors, premier or not.

Defining the colors of a given deck is definitely a judgement call and some decks are less straightforward than others. The pattern to follow, is to list included colors in alphabetical order where blue=u and is listed before "w" in this manner: b, g, r, u, w. Uppercase indicates a main color and lowercase indicates a splash color. Most of the analysis is centered around two-color pairs as that is historically the most prevalent outcome. There is opportunity for more targeted analysis of sets that deviate from this norm such as mono- or multicolored-focused environments. Immediately after the color entries, a single lowercase "p" indicates if the draft was "premier", drafted against humans as opposed to bots. A bot draft is assumed if "p" is left off.

Following the first descriptor line, the cards are listed, preceded by their count. Note that commas are left out of names as to not disrupt the csv format. Also, some decks/sets depend on sideboard cards and when that is relevant those cards are listed in the same manner, except with a lowercase "s" as the count. Duplicate sideboard cards are input using repeat "s"-count entries.

Each individual draft is stored as a draft object with the attributes made up of the input information.

Special thanks to https://mtgjson.com/ for their JSON which enabled me to analyze cards by color and rarity.

# Simple Win Shares
One of the questions when it comes to drafting is how strong cards are. I attempted to measure this for this data set by creating a simple win-share formula to assign fractions of each win to the cards contained in each draft deck. The formula for a given card in a given MTG set is:

win share = (wins/games)\*copies/(40\*drafts)

where: wins = total wins, games = total games, copies = every copy played across all drafts, drafts = total drafts card was used in

So if a card was used once as a single copy in a 3-3 draft. Its win share would be:

win share = (3/6)\*1/(40\*1) = 0.0125

The win rate (wins/games) is scaled by how many copies appeared across all 40-card drafts it was used in.

Here it is assumed that each draft has 40 cards (you can draft more, but I stick to 40, no Yorion Companion for me yet). 

The intent is to capture a sense of how much a card contributes to a winning draft, especially as the sample size increases. Some shortcomings include the fact that cards can be "carried" to a good win share when surrounded by a strong deck. This should correct given enough samples, but it is a concern for rares/mythics (which are not available as often) especially. The biggest shortcoming of this formula is the fact that this does not account for the card even being used in the games played. It is a common occurrence to play a few games and never even draw certain cards in your deck. Some games end before you even see 15/40 cards in your deck. I do not have real-time data to account for "when drawn", but a card's "real" contribution/win share should bear out with a large enough sample size. With enough drafts and enough games, if a card is truly damaging to your win rate it will be apparent. More on this later.

The code creates win shares plots for all cards together, commons, and uncommons where win share scores are plotted against copies. So that cards in the upper right quadrant are preforming well with high usage. Any high-usage data points are the most valuable for declaring cards "good" or "bad" on average. High win shares with low inclusions either means that that card is being "carried", or that it is being underdrafted.

Included on each plot is a reference line where wins/games is the drafter's average win rate for the set with increasing copies. For commons, the reference line uses drafts = copies^0.9 and uncommons use drafts = copies^0.95. This copies will always be at least equal to drafts and generally more over time, with commons appearing at a highest frequency. All in all, the reference line shows a very approximate average win shares for any given number of copies.

Another note, is that cards with win shares lower than 50% of the maximum are excluded unless they have a number of copies above 1/2 the maximum copies (of a single card). This is for plot clarity, since low usage and low win shares cards get clustered together. These data points are less valuable because they have low sample sizes.

The code creates many of these plots, but I review a handful of them here:

<img width="680" alt="image" src="https://user-images.githubusercontent.com/20996215/167018342-1ed8ced7-59c4-45fc-b4f0-a2941795b655.png">

Among AFR commons Sepulcher Ghoul and Vampire Spawn stand out with high usage and high win shares. This is consistent with popular draft stats website https://www.17lands.com/ where both of those cards are top 10 among AFR commons for GIH (games in hand) win rate. There are other high-usage standouts as well and notably Fates Reversal which is uncertain because of its small sample size. Notably absent from this plot are any blue cards. Blue was notoriously weak in this set and red and black were considered strong by the drafting community at large and that seems to bear out in the win shares.

I also made win share plots for basic lands, but had to include them on their own plots (they tend to have 6-10 copies per deck and dwarf the other cards with their inclusions/copies). These plots give an idea of the drafter's strength in certain colors:

<img width="589" alt="image" src="https://user-images.githubusercontent.com/20996215/167020598-d466041c-dc1b-4186-ac88-7cd1db07ddfe.png">

This is interesting because it appears that green was my strongest color and that I tended to do better with blue than white or red. This higher than expected win share for blue decks may be because I only "responsibly" drafted blue, which means that I avoided blue outside of when you lead off your draft with abnormally strong cards like Iymrith, Desert Doom which can carry weaker cards. Preliminary inspection of plots indicates that this phenomenon shows up in other sets as well, where a weaker color is avoided unless you draft some high rarity super-cards.

Here is the win shares plot for KHM:

<img width="679" alt="image" src="https://user-images.githubusercontent.com/20996215/167023386-fa08d6c1-afdb-4387-b726-785e2b4433a2.png">

Sarulf's Packmate and Struggle for Skemfar stand out here, with Berg Strider, Mistwalker, Shimmerdrift Vale, and Bound in Gold not far behind. 17lands also has Sarulf's Packmate as the #1 common with their GIH win rate metric. Interestingly Berg Strider and Struggle for Skemfar barely make it into their top 15 and Mistwalker and Bound in Gold into their top 20.

Any early debate early on in KHM's run was whether Sarulf's Packmate or Behold the Multiverse were the best commons. I played both about equally, but Sarulf's Packmate was much better on average (or at least was in better decks on average) than Behold the Multiverse, which hovered near my average performance threshold. This is also consistent with 17lands rankings as well. Although they both provide similar card advantage in game, it's clear that Packmate being a decent-sized creature mattered a lot.

A quick look at the basic lands information for KHM:

<img width="581" alt="image" src="https://user-images.githubusercontent.com/20996215/167025162-ccd11646-79ce-486e-8947-83a7f3f2e479.png">

Here we see another color-imbalanced format. The other data across almost all sets shows my tendency to draft black, but even I could not solve it for this set. The other four colors were about the same, but black lagged behind here and the lower usage reflects me avoiding it. More on this phenomenon under Output File Review.

# Clustering Analysis

In addition to win shares, I also wanted to see what clustering could tell me about the drafts. The distance metric I chose for comparing two drafts (in the same set) involved symmetric difference to find a union. This was modified to work with python lists (instead of sets, in math these would be multisets) because I wanted to account for repeating elements. Basic lands were excluded from this metric (because they would dominate over the actual drafted cards with their large inclusion rates). The formula is:

<img src="https://latex.codecogs.com/svg.image?distance(A,&space;B)&space;=&space;((|A|&space;&plus;&space;|B|)&space;-&space;(A&space;\Delta&space;B))&space;/&space;(|A|&space;&plus;&space;|B|)" />

Where A and B are card lists (multisets, but with strings). Now drafts (card lists) can be clustered using this distance metric, drafts can be fairly dissimilar, but this metric identifies what small similarities two drafts might have. This kind of analysis demands a large number of data points in order to have meaning, so the code only performs clustering if a given set has at least 40 drafts. Four sets (DOM, GRN, IKO, RNA) fit this criteria. I ended up using complete linkage agglomerative hierarchical clustering with a threshold cutoff of 1.35. The following plots explore that choice:

![method_comp](https://user-images.githubusercontent.com/20996215/167032629-e8904396-44d1-4a49-b07f-04f60ff15e8d.png)

The code creates these one of these plots for each set, but I have put them together for easier observation here. The method selection involved some intuition. Most draft environments are designed with 5-10 archetypes in mind, with some hidden ones that pop up time to time. Complete linkage was chosen because it was more-selective in combining clusters, which was important here because we know how dissimilar they (draft decks) tend to be, especially without really vast amounts of data. The threshold was selected in a attempt to region of where the dendrograms stabilized for a bit. Dendrograms here:

![dendrograms](https://user-images.githubusercontent.com/20996215/167033732-f26cfa79-5d45-4f3c-8b79-364756d22063.png)

Here we can see that the 5 color-pair sets RNA and GRN converge to fewer clusters and DOM and IKO end up with more. There might be a more optimal threshold choice, but this one has proved useful. Only draft contents was considered when clustering, win rate was not factored in. Here are the (abbreviated) cluster contents for GRN which had an average win rate of 57.5% across 46 drafts:

![Slide1](https://user-images.githubusercontent.com/20996215/167045485-57560545-1def-4019-a285-91fe0a3285f7.PNG)
![Slide2](https://user-images.githubusercontent.com/20996215/167045493-1b12dd3b-f410-4bf2-b4af-df1fd2a0dee0.PNG)
![Slide3](https://user-images.githubusercontent.com/20996215/167045501-10b42079-1d9c-468f-804e-02fbd9a63017.PNG)

Some additional context for GRN, I initially struggled a lot with drafting this set and had a win rate of about 52%, about 5% lower than my average across all sets. I eventually refined drafting the GB archetype and unlocked drafting UB, which I previously struggled with. These clusters help tell that story. My GB decks all essentially ended up in the same cluster (1 with one draft in 2), which makes some sense, because GB was considered somewhat under-supported which meant that GB-style cards were often not contested. GB ended up about 2% above my set average win rate. UB is the really interesting archetype in this clustering analysis and crystalized into three clusters: 3, 4, and 5. Cluster 3 (five drafts) is the "weak UB" cluster with a win rate of 50%, where the top cards consist mostly of GB cast-offs. The "weakness" of these cards is supported by the win shares plot. Cluster 4 (two drafts) is the "medium UB" cluster with a win rate of 61% and better card quality. Cluster 5 (ten drafts) is the "strong UB" cluster with  a win rate of 64% and with a higher density of removal in the top cards. The number of Passwall Adepts is an insane 2.6 per draft on average for cluster 5. It provided early necessary defense against a RW early onslaught and closed games against slow decks and board stalls. Even though RW was considered a strong archetype in GRN, I had a difficult time mastering it and therefore tended to avoid it so there was not a lot of differentiation. GW was considered a weak archetype and I rarely ended up in it, hence the single-draft clusters 9 and 10. 

It is important to note that the clusters are just indicating trends and those indications get stronger as the sample size increases.

# Bird's-Eye View
One of the output files produced is a pdf where each row represents a draft set (gameplay variant, indicated with a 3-letter code) and where the left column is a histogram for that draft set with bins for the 10 possible outcomes (0-3 up to 7-0). Draft count and win rate by draft set is also posted in the left column in red font. The right column displays a time series of wins verses draft index (chronological order, not to scale). A linear trendline is also depicted with its corresponding equation in red for each time series. Given enough data points, the trendline can indicate the win rate trajectory of a given set (decreasing, neutral, or increasing).

![histogram_timeseries_452_edit](https://user-images.githubusercontent.com/20996215/166829452-fb4ae7e7-2c79-48da-9364-301df6019f40.png)

One interesting observation from the time series in this set is that the win rate for some of the high-volume draft sets has a noticeable slope. GRN and DOM (near the top of the above diagram) have a noticeable positive trajectory where IKO (near the middle) has a negative trajectory. A major aspect of the drafts and the games themselves is a struggle between power and consistency. Generally, due to the nature of the resource system, a player tends to play two out of the five possible colors. Sometimes one can increase the power level by "splashing" other colors, but without enough ways to compensate for the additional color requirements your win rate could suffer despite the theoretical increase in power by sacrificing consistency. IKO was a set seeded with many cards to encourage "splashing" into more colors and it seems that over time the temptation to splash torpedoed the win rate. DOM was more straightforward and helped curb frequent extreme attempts at "splashing with its lack of enabling more colors per deck. GRN included many cards to enable splashing, but lacked many of the payoff incentive of IKO and was also unique in incentivizing just 5 two-color pairs instead of the typical 10.

![image](https://user-images.githubusercontent.com/20996215/133313617-e81848dc-2035-4558-ac3f-f10961c6c4a3.png)

# Analysis 
The above image is the unified histogram of the outcomes across all draft sets, accounting every draft event. It has largely normal Gaussian characteristics, but there is an inversion of expected bin height for the 6-3 and 7-2 outcomes. I estimate this is because of the 7-win-ceiling and the 3-loss-floor. Any start outside of an immediate 0-3 has the possibility of reaching a 7-win record. On the ends of the histogram, there is only one path to obtaining an 0-3 and also only one path to a 7-0. However, these bin heights are nowhere near the same, because 7 wins is much harder to obtain than 3 losses. To explore the disparity between expected and actual bin heights of the histogram, I made a short brute-force code to determine the number of total outcomes (win/loss sequences, ex. [w, l, w, l, w, w, l] is a sample 4-3 outcome). This code randomly builds outcomes according to the 7-win-ceiling and the 3-loss-floor rules, saving newly discovered outcomes to a list. After running the code a few times with different iteration counts (all the way up to 100,000 iterations) and the code converged at 120 total outcomes after about 2000 iterations. Here is the code:

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

It is important to recognize that we should not expect the bins of unified histogram to match these raw outcome counts. The outcomes do not have equal weights because of the difficulty of winning as opposed to losing. That being said, we can see that 6-3 and 7-2 both have 28 distinct outcomes. The relatively high outcome count for these two records helps explain the high bins we see in the unified histogram, but it does not explain the fact that the 7-2 bin is larger than the 6-3 bin. We would expect their bin heights to be inverted since the more win-dense outcomes of the 7-2 record should be harder to obtain. The only explanation I can think of is that there must be a psychological effect when sitting at 6 wins and shooting for the 7th win. Perhaps at that point, the player's play style subconsciously shifts to a more aggressive (or a more conservative) tactic when on the cusp of maxing out the wins and obtaining the larger prize payout. 

# Output File Overview

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

(End of output) The most drafted cards are listed in addition to win rate broken down by the five colors, then the ten color pairs. Especially for the color pairs, it is important to take into account the number of drafts/games played. For example, BU has a win rate of 67% which is quite good, but that is just from one draft. If we look at the data for all drafts that had black, the win rate was only 35%. KHM is a set where the community consensus was that black was a drastically weak color. This bears out in my data, and also helped me realize that I needed to try to avoid black when drafting. Here I have a high win rate with GW, but only across two drafts. This could mean that the color pair is strong, or it could just be two drafts carried by individually powerful card inclusions. With 10 drafts played, it seems safe to conclude that GU is one of my best (if not my best) color pair. The GU archetype was notable in KHM because of how easy it was to "splash" (play a few strong cards of other colors) without a major consistency hit. However, my win rate when splashing (in any combination) in KHM was only 58% across the board.
