# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 15:15:44 2021

@author: swhetzel
"""

import espn_scraper as espn

def get_team_shots(plays, game_id, periods=[1,2,3,4,5,6,7,8,9,10]):
    """Gets the number of shots attempted by each team and their types
    returned as a list of lists"""
    #[[[away 2 atts, away 2s made], 
    #[away 3 atts, away 3s made], 
    #[total away atts, total away made]],
    #[[home 2 atts, home 2s made], 
    #[home 3 atts, home 3s made],
    #[total home atts, total home made]]]
    
    teams = espn.get_teams('',game_id)
    away_two_atts, away_three_atts, away_shot_atts = 0, 0, 0
    home_two_atts, home_three_atts, home_shot_atts = 0, 0, 0
    
    away_twos_made, away_threes_made, away_shots_made = 0, 0, 0
    home_twos_made, home_threes_made, home_shots_made = 0, 0, 0
    
    for play in plays:
        if (('miss' in play[7] or 'make' in play[7]) 
            and 'free throw' not in play[8] and play[4] in periods ):
            if play[8] == 'two':
                if play[10] == teams[0]:
                    away_two_atts += 1
                    if play[7] == 'make':
                        away_twos_made += 1
                if play[10] == teams[1]:
                    home_two_atts += 1
                    if play[7] == 'make':
                        home_twos_made += 1
            if play[8] == 'three':
                if play[10] == teams[0]:
                    away_three_atts += 1
                    if play[7] == 'make':
                        away_threes_made += 1
                if play[10] == teams[1]:
                    home_three_atts += 1
                    if play[7] == 'make':
                        home_threes_made += 1
    away_shot_atts = away_two_atts + away_three_atts
    home_shot_atts = home_two_atts + home_three_atts
    away_shots_made = away_twos_made + away_threes_made
    home_shots_made = home_twos_made + home_threes_made
    shot_list = [[[away_two_atts, away_twos_made],
                   [away_three_atts,away_threes_made],
                   [away_shot_atts,away_shots_made]],
                  [[home_two_atts,home_twos_made],
                  [home_three_atts,home_threes_made],
                  [home_shot_atts,home_shots_made]]]
    return shot_list


def get_team_fg_pcts(plays, game_id):
    """Gets the field goal percentages of each team and returns them 
    as a list"""
    #[[away 2 pct, away 3 pct, away fg pct], 
    #[home 2 pct, home 3 pct, home fg pct]]
    
    away_2_pct, away_3_pct, away_fg_pct = float(0), float(0), float(0),
    home_2_pct, home_3_pct, home_fg_pct = float(0), float(0), float(0),    
    team_shots = get_team_shots(plays, game_id)
    
    try:
        away_2_pct = round(team_shots[0][0][1]/team_shots[0][0][0],3)
    except ZeroDivisionError:
        away_2_pct = 0
    try:
        away_3_pct = round(team_shots[0][1][1]/team_shots[0][1][0],3)
    except ZeroDivisionError:
        away_3_pct = 0
    try:
        away_fg_pct = round(team_shots[0][2][1]/team_shots[0][2][0],3)
    except ZeroDivisionError:
        away_fg_pct = 0
    try:
        home_2_pct = round(team_shots[1][0][1]/team_shots[1][0][0],3)
    except ZeroDivisionError:
        home_2_pct = 0
    try:
        home_3_pct = round(team_shots[1][1][1]/team_shots[1][1][0],3)
    except ZeroDivisionError:
        home_3_pct = 0
    try:
        home_fg_pct = round(team_shots[1][2][1]/team_shots[1][2][0],3)
    except ZeroDivisionError:
        home_fg_pct = 0    
    fg_pcts = [[away_2_pct,away_3_pct,away_fg_pct],
               [home_2_pct,home_3_pct,home_fg_pct]]
    return fg_pcts


def get_team_fts(plays, game_id, periods=[1,2,3,4,5,6,7,8,9,10]):
    """Gets the free throws taken and made by each team"""
    teams = espn.get_teams('',game_id)
    away_ft_atts, away_fts_made = 0, 0
    home_ft_atts, home_fts_made = 0, 0
        
    for play in plays:
        if (('miss' in play[7] or 'make' in play[7]) 
            and 'free throw' in play[8] and play[4] in periods ):
            if play[10] == teams[0]:
                away_ft_atts += 1
                if play[7] == 'make':
                    away_fts_made += 1
            if play[10] == teams[1]:
                home_ft_atts += 1
                if play[7] == 'make':
                    home_fts_made += 1
    ft_shot_list = [
        [away_ft_atts, away_fts_made],
        [home_ft_atts, home_fts_made]]
    return ft_shot_list


def get_team_ft_pcts(plays, game_id, periods=[1,2,3,4,5,6,7,8,9,10]):
    """Gets the ft percentages for both teams for a given period"""
    ft_shot_list = get_team_fts(plays, game_id, periods)
    try:
        away_ft_pct = round(ft_shot_list[0][1]/ft_shot_list[0][0],3)
    except ZeroDivisionError:
        away_ft_pct = 0
    try:    
        home_ft_pct = round(ft_shot_list[1][1]/ft_shot_list[1][0],3)
    except ZeroDivisionError:
        home_ft_pct = 0
    team_ft_pcts = [away_ft_pct, home_ft_pct]
    return team_ft_pcts



 
