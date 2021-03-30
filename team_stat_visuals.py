# -*- coding: utf-8 -*-
"""This module takes team statistics and creates various visuals.

This gets data from the espn_team_stats, and espn_scraper module and
applies various libraries to visualize the data in a dashboard using plotly
dash. 

game_id is set using the ESPN game ID in the URL from the game summary.
For example, the game summary for Syracuse v UVA on March 11th, 2021 has the
url: https://www.espn.com/mens-college-basketball/game?gameId=401300971
in this case game_id = '401300971'

"""
import espn_scraper as espn
import espn_team_stats as espn_team
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


def generate_pts_by_shot_fig(
    plays, game_id, teams, title, periods=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
):
    """Generate the figure for the point volume by shot type for each team/half"""
    # Points by shot type
    pts = espn_team.get_points_from_shot_type(plays, game_id, periods)

    pts_list = []
    for team in pts:
        for pts in team:
            pts_list.append(pts)
    away_team = teams[0]
    home_team = teams[1]
    teams_list = []
    for i in range(1, 9):
        if i < 5:
            teams_list.append(away_team)
        else:
            teams_list.append(home_team)
    shot_type = ["Two", "Three", "FT", "Total", "Two", "Three", "FT", "Total"]
    pts = pd.DataFrame(
        {"Points": pts_list, "Teams": teams_list, "Shot Type": shot_type}
    )
    pts_fig = px.bar(
        pts, x="Shot Type", y="Points", color="Teams", barmode="group", title=title
    )
    return pts_fig


def generate_shooting_pcts_radar(plays, game_id, team, periods=[1, 2]):
    """Generates radar charts displaying team shooting percents by half"""
    team_flag = 0
    if team == "home":
        team_flag = 1
    shot_pcts1 = espn_team.get_team_fg_pcts(plays, game_id, periods=[1])[team_flag]
    ft_pcts1 = espn_team.get_team_ft_pcts(plays, game_id, periods=[1])[team_flag]
    shot_pcts1.append(ft_pcts1)

    shot_pcts2 = espn_team.get_team_fg_pcts(plays, game_id, periods=[2])[team_flag]
    ft_pcts2 = espn_team.get_team_ft_pcts(plays, game_id, periods=[2])[team_flag]
    shot_pcts2.append(ft_pcts2)

    labels = ["2 pt Percentage", "3 pt Percentage", "Fg Percentage", "FT Percentage"]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=shot_pcts1,
            theta=labels,
            fill="toself",
            name=teams[team_flag] + " 1st half shot pcts",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=shot_pcts2,
            theta=labels,
            fill="toself",
            name=teams[team_flag] + " 2nd half shot pcts",
        )
    )
    fig.update_layout(title_text=teams[team_flag], title_xref="paper", title_x=0.5)
    return fig


game_id = "401300971"
plays = espn.play_by_play_builder(game_id)
teams = espn.get_teams("", game_id)

h1_pts_fig = generate_pts_by_shot_fig(plays, game_id, teams, "1st Half", [1])
h1_pts_fig.update_layout(title_xref="paper", title_x=0.5)

h2_pts_fig = generate_pts_by_shot_fig(plays, game_id, teams, "2nd Half", [2])
h2_pts_fig.update_layout(title_xref="paper", title_x=0.5)

game_pts_fig = generate_pts_by_shot_fig(plays, game_id, teams, "Entire Game")
game_pts_fig.update_layout(title_xref="paper", title_x=0.5)

away_shooting_radar_fig = generate_shooting_pcts_radar(plays, game_id, team="away")
home_shooting_radar_fig = generate_shooting_pcts_radar(plays, game_id, team="home")


flag = True
if flag == True:
    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    app.layout = html.Div(
        children=[
            html.H1(children="Team Shooting Statistics by Period"),
            html.Div(
                children="""Radar charts showing the shooting percentages by team by half"""
            ),
            html.Div(
                [
                    dcc.Graph(id="away shooting pcts", figure=away_shooting_radar_fig),
                ],
                style={"width": "49%", "display": "inline-block", "padding": "0 20"},
            ),
            html.Div(
                [
                    dcc.Graph(id="home shooting pcts", figure=home_shooting_radar_fig),
                ],
                style={"width": "49%", "display": "inline-block", "padding": "0 20"},
            ),
            html.Div(children="""Team Points by Shot Type and Period"""),
            html.Div(
                [dcc.Graph(id="h1 points by shot type", figure=h1_pts_fig)],
                style={"width": "32%", "display": "inline-block", "padding": "0 20"},
            ),
            html.Div(
                [dcc.Graph(id="h2 points by shot type", figure=h2_pts_fig)],
                style={"width": "32%", "display": "inline-block", "padding": "0 20"},
            ),
            html.Div(
                [dcc.Graph(id="game points by shot type", figure=game_pts_fig)],
                style={"width": "32%", "display": "inline-block", "padding": "0 20"},
            ),
        ]
    )

    if __name__ == "__main__":
        app.run_server(debug=True)
