from dash import html, dcc, dash_table
from plotly_football_pitch import make_pitch_figure, PitchDimensions, SingleColourBackground

from constants import TEAM_COLUMNS, SEASONS, LEAGUES

def create_global_filter():
    return html.Div(
        [
            html.Label("League", style={'marginTop': '10px'}),
            dcc.Dropdown(
                id='league',
                options=[{'label': row['country'], 'value': row['league_id']} for row in LEAGUES],
                value=LEAGUES[1]['league_id'],
                clearable=False,
                style={'marginBottom': '10px'}
            ),
            html.Label("Season", style={'marginTop': '10px'}),
            dcc.Dropdown(
                id='season',
                options=[{'label': season, 'value': season} for season in SEASONS],
                value=SEASONS[-1],
                clearable=False,
                style={'marginBottom': '10px'}
            ),
            html.Label("Team", style={'marginTop': '10px'}),
            dcc.Dropdown(id='team', clearable=False, style={'marginBottom': '10px'}),
        ], style={'width': '50%', 'display': 'inline-block', 'marginLeft': '5px'})
    
def create_match_info():
    dim = PitchDimensions()
    fig = make_pitch_figure(dim, pitch_background=SingleColourBackground("#81B622"))
    return html.Div(
        [
            html.H1("Match Info", style={'marginTop': '10px'}),
            dcc.Graph(figure=fig, id='football-pitch'),
            html.H2(id='match-title', style={'textAlign': 'center', 'marginTop': '10px'}),
            html.H3(id='match-date', style={'textAlign': 'center', 'marginTop': '10px'}),
            html.H3(id='match-result', style={'textAlign': 'center', 'marginTop': '10px'}),
            dash_table.DataTable(id='lineup-tbl', style_table={'width': '90%', 'marginLeft': 'auto', 'marginRight': 'auto'},
                                 columns=[{'name': 'home', 'id': 'home'}, {'name': 'away', 'id': 'away'}],
                                 cell_selectable=False, style_cell={'textAlign': 'center'})
            
        ]
    )
    
def create_team_info():        
    return html.Div(
        [
            html.H1("FIFA team attributes", style={"marginTop": "10px"}),
            dash_table.DataTable(id='team-info-tbl', style_table={'width': '90%'},
                                 cell_selectable=False,
                                 style_cell={'textAlign': 'center'}),
            dcc.Graph(id='league-average-compare')
        ]
    )
    
def create_all_match_info():
    columns = ["date", "home", "away", "score", "result"]
    return html.Div(
        [
            html.H1("All Matches", id='match-info', style={'margin': '10px'}),
            dash_table.DataTable(id='match-info-tbl', style_table={'width': '600px'},
                                 cell_selectable=False, row_selectable='single', columns=[{'name': col, 'id': col} for col in columns],
                                 style_cell={'textAlign': 'center'}, style_data_conditional=[
                                     {
                                         'if': {'filter_query': '{result} = "Win"'},
                                         'backgroundColor': '#3D9970',
                                         'color': 'white'
                                     },
                                    {
                                        'if': {'filter_query': '{result} = "Loss"'},
                                        'backgroundColor': '#FF4136',
                                        'color': 'white'
                                    },
                                    {
                                        'if': {'filter_query': '{result} = "Draw"'},
                                        'backgroundColor': '#FFDC00',
                                        'color': 'black'
                                    },
                                     {
                                         'if': {'filter_query': '{winner_team_api_id} = {team_1}'},
                                         'backgroundColor': '#3D9970',
                                         'color': 'white'
                                     },
                                    {
                                        'if': {'filter_query': '{winner_team_api_id} = {team_2}'},
                                        'backgroundColor': '#FF4136',
                                        'color': 'white'
                                    },
                                 ]
                                 )
        ]
    )
    
def create_season_form():
    return html.Div(
        [
            html.H1("Season Form"),
            dcc.Graph(id='season-form', style={'width': '70%', 'display': 'inline-block'}),
        ]
    )
    
def create_league_filter():
    return html.Div(
        [
            html.Label("League"),
            dcc.Dropdown(
                id='league',
                options=[{'label': row['country'], 'value': row['league_id']} for row in LEAGUES],
                value=LEAGUES[1]['league_id'],
                clearable=False
            )
        ], style={'width': '50%', 'display': 'inline-block',
                  'marginTop': '10px', 'marginBottom': '10px', 'marginLeft': '5px'}
    )

def create_head_to_head_dropdowns():
    return html.Div(
        [
            html.Label("Team 1"),
            dcc.Dropdown(id='hth-team-1', clearable=False,
                         style={'marginBottom': '10px'}),
            html.Label("Team 2"),
            dcc.Dropdown(id='hth-team-2', clearable=False,
                         style={'marginBottom': '10px'}),
        ], style={'width': '50%', 'display': 'inline-block',
                  'marginLeft': '5px'}
    )
    
def create_team_dropdown():
    return html.Div(
        [
            html.Label("Team"),
            dcc.Dropdown(id='history-team', clearable=False)
        ], style={'width': '50%', 'display': 'inline-block',
                  'marginLeft': '5px', 'marginBottom': '10px'}
    )
    
def create_match_type_dropdown():
    match_types = ['Home', 'Away', 'All']
    return html.Div(
        [
            html.Label("Match Type"),
            dcc.Dropdown(id='match-type', options=[{'label': match_type, 'value': match_type} for match_type in match_types],
                         value='All', clearable=False, style={'width': '40%', 'marginBottom': '10px'})
        ], style={'marginLeft': '5px'}
    )
    
def create_goals_trend():
    return html.Div(
        [
            html.H1("Goals Trend", style={'marginTop': '10px'}),
            dcc.Graph(id='goals-trend', style={'width': '70%', 'display': 'inline-block'})
        ]
    )
    
def create_team_fifa_attributes_history():
    attributes_columns = [{'label': attributes_name, 'value': attributes_name} for col_name, attributes_name in TEAM_COLUMNS.items()
                     if col_name not in ['buildUpPlayPositioningClass', 'defenceDefenderLineClass']]
    return html.Div(
        [
            html.H1("Team FIFA team attributes history", style={'padding': '10px'}),
            dcc.Dropdown(id='fifa-attributes', options=attributes_columns, multi=True),
            dcc.Graph(id='fifa-attributes-history', style={'width': '70%', 'display': 'inline-block'})
        ]
    )
    
def create_team_attributes_compare():
    return html.Div(
        [
            html.H1("Team Attributes Compare", style={'marginTop': '10px'}),
            dcc.Dropdown(id='season-select', options=[{'label': season, 'value': season} for season in SEASONS],
                         value=SEASONS[-1], clearable=False, style={'width': '50%'}),
            dcc.Graph(id='team-attributes-compare', style={'width': '100%', 'display': 'inline-block'})
        ]
    )