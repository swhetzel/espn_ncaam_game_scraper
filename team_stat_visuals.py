# -*- coding: utf-8 -*-
"""This module takes team statistics and creates various visuals.

This gets data from the espn_team_stats, and espn_scraper module and
applies various libraries to visualize the data. Work on this module
is ongoing.

"""
import espn_scraper as espn
import espn_team_stats as espn_team
import pygal
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


game_id = "401300971"
plays = espn.play_by_play_builder(game_id)
shot_type_list = espn_team.get_team_shots(plays, game_id)
ft_list = espn_team.get_team_fts(plays, game_id)
team_fg_pcts = espn_team.get_team_fg_pcts(plays, game_id)
team_ft_pcts = espn_team.get_team_ft_pcts(plays, game_id)
teams = espn.get_teams("", game_id)
print(teams)

# print(team_ft_pcts)
# print(team_fg_pcts)

away_shot_pcts = team_fg_pcts[0]
away_shot_pcts.append(team_ft_pcts[0])
home_shot_pcts = team_fg_pcts[1]
home_shot_pcts.append(team_ft_pcts[1])

x_labels = ["3 pt Percentage", "2 pt Percentage", "Fg Percentage", "FT Percentage"]
team_shot_pcts_chart = pygal.Radar()
team_shot_pcts_chart.title = "Shooting Percentages by Team"
team_shot_pcts_chart.x_labels = x_labels
team_shot_pcts_chart.add(teams[0], away_shot_pcts)
team_shot_pcts_chart.add(teams[1], home_shot_pcts)
team_shot_pcts_chart.render_to_file("team_shot_pcts.svg")

# Split 1st half and 2nd half
period1 = [1]
period2 = [2]

half1_fg_pcts = espn_team.get_team_fg_pcts(plays, game_id, period1)
half2_fg_pcts = espn_team.get_team_fg_pcts(plays, game_id, period2)
half1_ft_pcts = espn_team.get_team_ft_pcts(plays, game_id, period1)
half2_ft_pcts = espn_team.get_team_ft_pcts(plays, game_id, period2)

h1_away_shot_pcts = half1_fg_pcts[0]
h1_away_shot_pcts.append(espn_team.get_team_ft_pcts(plays, game_id, period1)[0])
h1_home_shot_pcts = half1_fg_pcts[1]
h1_home_shot_pcts.append(espn_team.get_team_ft_pcts(plays, game_id, period1)[1])
h2_away_shot_pcts = half2_fg_pcts[0]
h2_away_shot_pcts.append(espn_team.get_team_ft_pcts(plays, game_id, period2)[0])
h2_home_shot_pcts = half2_fg_pcts[1]
h2_home_shot_pcts.append(espn_team.get_team_ft_pcts(plays, game_id, period2)[1])

h1_away_pcts_chart = pygal.Radar()
h1_away_pcts_chart.title = str(teams[0] + " Shooting pcts by Half")
h1_away_pcts_chart.x_labels = x_labels
h1_away_pcts_chart.add("1st Half", h1_away_shot_pcts)
h1_away_pcts_chart.add("2nd Half", h2_away_shot_pcts)
h1_away_pcts_chart.render_to_file("away_shots_by_half.svg")

h1_home_pcts_chart = pygal.Radar()
h1_home_pcts_chart.title = str(teams[1] + " Shooting pcts by Half")
h1_home_pcts_chart.x_labels = x_labels
h1_home_pcts_chart.add("1st Half", h1_home_shot_pcts)
h1_home_pcts_chart.add("2nd Half", h2_home_shot_pcts)
h1_home_pcts_chart.render_to_file("home_shots_by_half.svg")


# Trying to Create these same charts using Plotly Dash
fig = go.Figure()
fig.add_trace(
    go.Scatterpolar(
        r=h1_away_shot_pcts,
        theta=x_labels,
        fill="toself",
        name=teams[0] + " 1st half shot pcts",
    )
)
fig.add_trace(
    go.Scatterpolar(
        r=h2_away_shot_pcts,
        theta=x_labels,
        fill="toself",
        name=teams[0] + " 2nd half shot pcts",
    )
)

fig2 = go.Figure()
fig2.add_trace(
    go.Scatterpolar(
        r=h1_home_shot_pcts,
        theta=x_labels,
        fill="toself",
        name=teams[1] + " 1st half shot pcts",
    )
)
fig2.add_trace(
    go.Scatterpolar(
        r=h2_home_shot_pcts,
        theta=x_labels,
        fill="toself",
        name=teams[1] + " 2nd half shot pcts",
    )
)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children="Team Shooting Efficiency by Half"),
        html.Div(
            children="""Radar charts showing the shooting percentages by team by half"""
        ),
        html.Div(
            [
                dcc.Graph(id="away shooting pcts", figure=fig),
            ],
            style={"width": "49%", "display": "inline-block", "padding": "0 20"},
        ),
        html.Div(
            [
                dcc.Graph(id="home shooting pcts", figure=fig2),
            ],
            style={"width": "49%", "display": "inline-block", "padding": "0 20"},
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
