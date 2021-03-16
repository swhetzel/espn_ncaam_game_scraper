import urllib.request
from datetime import datetime

def convert_html_roster(url, game_id):
    """converts raw html for box score url to a string"""
    if url == '':
        url = ('https://www.espn.com/mens-college-basketball/boxscore?gameId='
               + game_id)
    with urllib.request.urlopen(url) as response:
        html_roster = str(response.read())
        return html_roster

def roster_html_to_lists(game_id, teams_list):
    """converts html string to  list of relevant player names associated with
    a team"""
    url = ''
    html = convert_html_roster(url, game_id)
    string1 = '<article class="boxscore-tabs game-package-box-score"'
    
    raw_players = html.split(string1)
    raw_html_rosters = raw_players[1].split('>' + teams_list[1] + '</div></div><table')
    raw_away_players = raw_html_rosters[0].split('class="abbr">')   
    raw_home_players = raw_html_rosters[1].split('class="abbr">')
    away_players = []
    for raw_player in raw_away_players:
        player_string = ''
        if raw_player == raw_away_players[0]:
            continue
        for i in raw_player:
            if i == '<':
                break
            player_string += i
        away_players.append(player_string.strip())            
    home_players = []
    for raw_player in raw_home_players:
        player_string = ''
        if raw_player == raw_home_players[0]:
            continue
        for i in raw_player:
            if i == '<':
                break
            player_string += i
        home_players.append(player_string.strip())            
    roster_dicts = {}
    roster_dicts[teams_list[0]] = away_players
    roster_dicts[teams_list[1]] = home_players
    return roster_dicts
        

def convert_html_plays(url, game_id):
    """converts raw html to a string"""
    if url == '':
        url = ('https://www.espn.com/mens-college-basketball/playbyplay?gameId='
            + game_id)
    with urllib.request.urlopen(url) as response:
        html_plays = str(response.read())  
    return html_plays


def plays_html_to_list(url, game_id):
    """converts html string to a list of relevant play by play data"""
    html = convert_html_plays(url, game_id)
    raw_plays = []
    raw_plays = html.split('class="time-stamp"')
    return raw_plays    


def get_teams(url, game_id):
    """Defines and returns the home & away teams from the raw html string"""
    html = convert_html_plays(url, game_id)
    raw_list = html.split("<title>")
    teams_list_raw = raw_list[1].split(' - Play')
    teams_list = teams_list_raw[0].split(' vs. ')
    return(teams_list)


def get_time_stamp(play):
    """Returns the formatted time stamp for a given play"""
    time_stamp = ''
    for i in range(0,7):
        if play[i] == '<':
            break
        elif play[i] == '>':
            continue
        time_stamp += play[i]
    return(time_stamp)
    
    
def get_play_details(play):
    """Returns the formatted details of the play"""
    play_details = ''
    raw_play_details = play.split('class="game-details">')[1]
    count = 0
    while True:
        if raw_play_details[count] == '<':
            break
        play_details += raw_play_details[count]
        count += 1
    return(play_details)


def get_score(play):
    """return a list with [away_score, home_score] after the play"""
    scores = []
    away_score_str =''
    home_score_str = ''
    raw_score = play.split('class="combined-score">')[1]
    count = 0
    home_away_flag = 0
    while True:
        if raw_score[count] == '<':
            break
        elif raw_score[count] in [' ','-']:
            home_away_flag = 1
        elif home_away_flag == 0:
            away_score_str += raw_score[count]
        elif home_away_flag == 1:
            home_score_str += raw_score[count]
        count += 1
    
    scores.append(int(away_score_str))
    scores.append(int(home_score_str))
    return(scores)
    
    
def get_score_designation(plays, scores):
    """Return the score designation field, either '' or 'Scoring Play'"""
    scoring_play_flag = 0
    if len(plays) > 0:
        last_score = plays[-1][2]
        if scores == last_score:
            scoring_play_flag = 0
        if scores != last_score:
            scoring_play_flag = 1
    if scoring_play_flag == 0:
        return("")
    if scoring_play_flag == 1:
        return("Scoring Play") 
        
    
def get_period(plays, play, period_count):
    """Return the period designation, 1 = 1st half, 2 = 2nd half, all else 
        denote overtime periods"""
    if len(plays) == 0:
        period_count = period_count
    elif "End of" in plays[-1][1]:
        period_count += 1
    return period_count
      
    
def get_formatted_time(time_stamp, period_count, date_time_flag):
    """Return the absolute formatted time based on the timestamp and period"""
    time_delt = (datetime.strptime("20:00", "%M:%S") - datetime.strptime(time_stamp, "%M:%S"))
    new_time = datetime(year=2020,month=1,day=1,hour=0,minute=0,second=0) + time_delt
    minutes = new_time.minute
    seconds = new_time.second
    form_time = datetime(year=2020, month=1, day=1, hour=0,minute=minutes,second=seconds)
    
    if period_count == 2:
        time_delt = time_delt + datetime.strptime("20:00", "%M:%S")
        minutes = time_delt.minute
        seconds = time_delt.second
        form_time = datetime(year=2020, month=1, day=1, hour=0,minute=minutes,second=seconds)
    
    if period_count > 2:
        overtime = period_count - 2
        minutes_added = 40 + overtime*5
        time_string = str(minutes_added) + ':00' 
        time_delt = (datetime.strptime(time_string, "%M:%S") - 
            datetime.strptime(time_stamp, "%M:%S"))
        new_time = datetime(year=2020,month=1,day=1,hour=0,minute=0,second=0) + time_delt
        minutes = new_time.minute
        seconds = new_time.second
        form_time = datetime(year=2020, month=1, day=1, hour=0,minute=minutes,second=seconds)
        return_time = datetime.time(form_time)
        
        #flag to determine if you want this as datetime or time
        if date_time_flag:
            return form_time
        else:
            return return_time
    
    
def get_player_name(play_details, teams_list):
    """Returns the name of the player"""
    #set a flag that will ignore plays that don't have associated 
        #players
    except_list = [
        'End of',
        'Jump Ball won by',
        'timeout'
        ]
    break_flag = 0
    for i in except_list:
        if i in play_details:
            break_flag = 1
    #return nothing if in exception list, otherwise return the name
    if break_flag == 1:
        return ''        
    else:    
        name_str = play_details.replace("\\'","'")
        name_str = name_str.replace('Foul on ','')
        name = ''
        name_exceptions = ['III','IV','Jr.']
        exception_flag = 0
        space_flag = 0
        for i in name_exceptions:
            if i in name_str:
                exception_flag = 1
                
        if exception_flag == 1:
            for i in name_str:
                if i == ' ':
                    space_flag += 1
                if space_flag == 3:
                    break
                name += i
        else:
            for i in name_str:
                if i == ' ':
                    space_flag += 1
                if space_flag == 2:
                    break
                name += i
        name = name.strip()
        name = name.replace(' made', '')
        if name not in teams_list:
            return name
        else:
            return ''


def get_player_abbr(player_name):
    """returns the abbreviated name of the player, useful for linking roster
    information/team information to the play"""
    flag = 0
    name_string = ''
    if player_name != '':
        name_string += player_name[0]
        while True:
            if player_name[1] == '.':
                name_string += '.'
                name_string += player_name[2]
                break
            else:
                break

        name_string += '.'
        for i in player_name:
            if i == ' ':
                flag = 1
            if flag == 1:
                name_string += i
        name_string = name_string.strip()
        if "Jr." not in name_string:
            name_string = name_string.strip('.')
        return name_string
    else: 
        return ''


def get_play_type(play_details):
    """Returns what kind of play occurred"""
    play_details = play_details.lower()
    play_type = ''
    if 'made' in play_details:
        play_type = 'make'
    elif 'missed' in play_details:
        play_type = 'miss'
    elif 'foul on' in play_details:
        play_type = 'foul'
    elif 'defensive rebound' in play_details:
        play_type = 'defensive rebound'
    elif 'offensive rebound' in play_details:
        play_type = 'offensive rebound'
    elif 'turnover' in play_details:
        play_type = 'turnover'
    elif 'block' in play_details:
        play_type = 'block'
    elif 'steal' in play_details:
        play_type = 'steal'  
    return play_type


def get_shot_type(play_type, play_details):
    """Returns what kind of shot occurred if there was one"""
    shot_bool = False
    for i in ['make','miss']:
        if i in play_type:
            shot_bool = True
    shot_type = ''
    if "Three Point" in play_details:
        shot_type = 'three'
    elif "Free Throw" in play_details:
        shot_type = 'free throw'
    else:
        shot_type = 'two'
    
    if shot_bool:
        return shot_type
    else:
        return ''
    
    
def get_team(player_abbr, roster_dicts):
    """Gets the team that the named player is on"""
    team = ''
    for dict_team, player_list in roster_dicts.items():
        if player_abbr in player_list:
            team = dict_team    
    return team


def play_by_play_builder(game_id='401123374', url='',
                         date_time_flag=True):
    """Builds a list of lists with play data in each of the 'rows'"""
    #play contents format:
    #0 - timestamp #:## or ##:##
    #1 - play details 
    #2 - list of scores [away, home]
    #3 - scoring play designation
    #4 - period number
    #5 - formatted time
    #6 - Player name
    #7 - Play type
    #8 - Shot type
    #9 - Player abbreviation
    #10 - Team
    
    #convert the html in the url to a raw list of unformatted play data
    raw_plays = plays_html_to_list(url, game_id)
    teams_list = get_teams(url, game_id)
    
    #Load the dictionaries of rosters
    roster_dicts = roster_html_to_lists(game_id, teams_list)
    
    #empty list to add individual pieces of formatted play data to
    plays = []
    
    #This will keep track of which period the play is in
    period_count = 1
    
    # Format raw_plays data and add data to plays list
    for play in raw_plays:
        
        #Skip the first row which is all the irrelevant data
        if play == raw_plays[0]:
            continue
        
        #temporary list to house an individual play's data
        play_data = []
        
        #Get Time Stamp and append to play_data
        time_stamp = get_time_stamp(play)
        play_data.append(time_stamp)
        
        #Get the text description of the play and append to play_data
        play_details = get_play_details(play)
        play_data.append(play_details)
    
        #Get the score that existed after the play was finished    
        scores = get_score(play)
        play_data.append(scores)
        
        #Get the scoring play designation, designates whether or not the play
        #resulted in a score
        scoring_designation = get_score_designation(plays, scores)
        play_data.append(scoring_designation)
        
        #Get the period number and append it to play_data
        period_count = get_period(plays, play, period_count)
        play_data.append(period_count)
        
        #Get the formatted datetime and append it to play_data
        formatted_time = get_formatted_time(time_stamp, 
                                            period_count, 
                                            date_time_flag)
        play_data.append(formatted_time)
        
        #Append name data to play_data
        player_name = get_player_name(play_details, teams_list)
        play_data.append(player_name)

        #Append play type data to play_data
        play_type = get_play_type(play_details)
        play_data.append(play_type)
        
        #Append shot type data to play_data
        shot_type = get_shot_type(play_type, play_details)
        play_data.append(shot_type)

        #Append the player name abbreviation to play_data
        player_abbr =get_player_abbr(player_name)
        play_data.append(player_abbr)
        
        #Append the team to play_data
        team = get_team(player_abbr, roster_dicts)
        play_data.append(team)

        #Append completed play_data list to the list of plays
        plays.append(play_data)
        
    return plays

