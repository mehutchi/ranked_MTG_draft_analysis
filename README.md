# ranked_MTG_draft_analysis

Homemade code that analyzes the results of best-of-one Magic the Gathering (MTG) Arena draft results. MTG Arena is the client and a draft is a game mode where a circle of eight players each select one card from a 15-card pack, pass the rest, then each make another pick until the pack is depleted. This is repeated for two more packs and players contruct minimum 40-card decks from their selections to battle against other drafters. This code is designed for best-of-one, where a draft run completes by reaching 7 wins or 3 losses, whichever occurs first. Matches are created according to current win rate and the players' ranks. Thus, the win rates are pushed towards 50% as you encounter stronger and stronger players on average the more you win. I'll follow the convention of listing (wins, losses) when stating records.

The input file is admittedly not as sophisticated as pulling results from MTG Arena output files, but I choose this approach because I had records from my entire usage for extra context. Typing up the input file is alleviated with text editors that feature autocomplete.

The input file follows the following form:



One of the output files produced is a pdf where each row represents a draft set (gameplay variant, described indicated with a 3-letter code) and where the left column is a histogram for that draft set according to the 10 possible outcomes (0-3 up to 7-0). Draft count and win rate by draft set is also posted in the left column in red font. The right column displays a time series of wins verses draft index (chronological order, not to scale). A linear trendline is also depicted with its corresponding equation in red for each time series. Given enough data points, the trendline can indicate the win rate trajectory of a given set (decreasing, neutral, or increasing).

![image](https://user-images.githubusercontent.com/20996215/127245189-b8ac76f9-adc3-40c6-a76c-16b24187c4e7.png)
