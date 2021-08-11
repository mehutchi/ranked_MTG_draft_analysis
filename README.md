# ranked_MTG_draft_analysis

**Overview** - Homemade code that analyzes the results of best-of-one Magic the Gathering (MTG) Arena draft results to help reveal detailed winrate information and player tendencies. 

**Explanation of Draft events** - A draft is a game mode where a circle of eight players each open a 15-card pack (so 120 total cards at the table), select one card from their pack, simultaneously pass the remaining 14 cards to their neighbor, then each make another pick, repeating the process of selecting and passing until the packs are depleted. This is repeated for two more packs (each) and players contruct minimum 40-card decks from their selections to battle against other drafters. This code is designed for best-of-one, where a draft run completes by reaching 7 wins or 3 losses, whichever occurs first. Matches are created according to current win rate and the players' ranks. Thus, players' win rates are pushed towards 50% because you encounter stronger and stronger opponents on average the more you win (given enough time to reach equilibrium). This document will follow the convention of listing (wins, losses) when stating records. Also, the pool of draftable cards (referred to as "draft sets") changes every few months allowing the opportunity to compare results within draft sets and also collectively.

The input file is admittedly not as sophisticated as pulling results from MTG Arena output files, but I choose this approach because I had records from my entire usage (I think MTG Arena records are discarded periodically, so one is limited to only recent data) for extra context. Typing up the input file is alleviated with text editors that feature autocomplete and by working on it incrementally.

The input file follows the following format (csv) for each draft entry:

![image](https://user-images.githubusercontent.com/20996215/127382097-bab2dee5-7f4a-4082-8b3e-4c1bb63697f6.png)

The first line contains: 3-letter set code, number of wins, number of losses, colors, premier or not.

Defining the colors of a given deck is definitely a judgement call and some decks are less straightforward than others. The pattern to follow, is to list included colors in alphabetical order where blue=u and is listed before "w" in this manner: b, g, r, u, w. Uppercase indicates a main color and lowercase indicates a splash color. Most of the analysis is centered around two-color pairs as that is historically the most prevalent outcome. There is opportunity for more targeted analysis of sets that deviate from this norm such as mono- or multicolored-focused enviroments. Immediately after the color entries, a single lowercase "p" indicates if the draft was "premier", drafted against humans as opposed to bots. A bot draft is assumed if "p" is left off.

Following the first descriptor line, the cards are listed, preceded by their count. Note that commas are left out of names as to not disrupt the csv format. Also, some decks/sets depend on sideboard cards and when that is relevant those cards are listed in the same manner, except with a lowercase "s" as the count. Duplicate sideboard cards are input using repeat "s"-count entries.

Each individual draft is stored as a draft object with the attributes made up of the input information.

One of the output files produced is a pdf where each row represents a draft set (gameplay variant, indicated with a 3-letter code) and where the left column is a histogram for that draft set with bins for the 10 possible outcomes (0-3 up to 7-0). Draft count and win rate by draft set is also posted in the left column in red font. The right column displays a time series of wins verses draft index (chronological order, not to scale). A linear trendline is also depicted with its corresponding equation in red for each time series. Given enough data points, the trendline can indicate the win rate trajectory of a given set (decreasing, neutral, or increasing).

![image](https://user-images.githubusercontent.com/20996215/127245189-b8ac76f9-adc3-40c6-a76c-16b24187c4e7.png)


