# espn_ncaam_game_scraper
Scrapes play by play data and roster data from individual games and processes the data

The goal of this project is to facilitate the creation of data sets and visual outputs from a single NCAA men's basketball game that will provide some additional insight about how a game progressed from period to period. Most online data sources do not let you segment by time within a game or even analyze statistical changes between periods. However, this project will eventually allow you to pull and visualize most basic statistics for a team or individual player by either period (first half, second half, overtime) or from a discrete period of time. 

This is very much a work in progress. Currently the team_stat_visuals.py module produces a plotly dash displaying various team shooting statistics by half. This will continue to be built out. Right now, you can plug in any ESPN game id to the game_id variable in this module (found in the URL from an ESPN game summary page) to have the dashboard update for any NCAA men's basketball game. 

ESPN Game IDs can be found in the URL for an ESPN game summary such as the one below:

https://www.espn.com/mens-college-basketball/game?gameId=401300971

This particular URL leads to the game summary for Syracuse at Virginia from March 11, 2021 and the game_id here is '401300971'. Plug in an ESPN game id from any NCAA men's basketball game into that field in the team_stat_visuals.py module after downloading the repository to produce a unique dashboard. 

![image](https://user-images.githubusercontent.com/79474788/113053682-8f395600-9176-11eb-85e9-7838f1c283d4.png)

Here's an example of some of the dashboard visuals that are produced so far:

![image](https://user-images.githubusercontent.com/79474788/113053831-bdb73100-9176-11eb-81ca-11637f6ff88d.png)

