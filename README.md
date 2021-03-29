# espn_ncaam_game_scraper
Scrapes play by play data and roster data from individual games and processes the data

The goal of this project is to facilitate the creation of data sets and visual outputs from a single NCAA men's basketball game. Most online data sources do not let you segment by time within a game or even analyze statistical changes between periods. However, this project will eventually allow you to pull and visualize most basic statistics for a team or individual player by either period (first half, second half, overtime) or from a discrete period of time. 

This is very much a work in progress. Currently the team_stat_visuals.py module produces some svg files along with a plotly dash showing radar charts of team shooting percentages by half. This will continue to be built out. Right now, you can plug in any ESPN game id to the game_id variable in this module (found in the URL from an ESPN game summary page) to have the dashboard update for any NCAA men's basketball game. 

