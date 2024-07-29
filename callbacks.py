from dash import callback, Output, Input, State
import plotly.express as px
from plotly_football_pitch import make_pitch_figure, PitchDimensions, SingleColourBackground
from plotly.graph_objects import Figure

from db_util import get_teams_by_league_and_season, get_team_info, get_team_matches, get_players_names,\
    get_head_to_head, get_league_averages, get_team_fifa_attributes
from constants import TEAM_COLUMNS, SEASONS

@callback(
    Output('team', 'options'),
    Input('league', 'value'),
    Input('season', 'value'),
)
def update_team_dropdown(league, season):
    teams = get_teams_by_league_and_season(league, season)
    return [{'label': row['name'], 'value': row['team_api_id']} for _, row in teams.iterrows()]

@callback(
    Output('team', 'value'),
    Input('team', 'options')
)
def update_team_value(teams):
    return teams[0]['value'] if teams else None

@callback(
    Output('team-name', 'children'),
    Output('team-info-tbl', 'data'),
    Output('league-average-compare', 'figure'),
    Input('team', 'value'),
    Input('season', 'value'),
    State('league', 'value')
)
def update_team_info(team_api_id, season, league):
    if team_api_id is None or season is None:
        return "", []
    team_info = get_team_info(team_api_id, season)
    team_name = team_info['team_long_name']
    league_averages = get_league_averages(league, season)
    columns_to_remove = [col for col in team_info.index if col not in TEAM_COLUMNS.keys()]
    team_info = team_info.drop(columns_to_remove)
    
    for col_name, new_col_name in TEAM_COLUMNS.items():
        team_info[new_col_name] = team_info[col_name]
        team_info = team_info.drop(col_name)

    team_info = team_info.drop("Positioning").drop("Defence Line")
    fig = Figure()
    fig.add_bar(x=list(league_averages.index), y=league_averages.values, name='League Average')
    fig.add_bar(x=list(team_info.index), y=team_info.values, name=team_name)
    
    return team_name, team_info.to_frame().T.to_dict('records'), fig

@callback(
    Output('match-info-tbl', 'data'),
    Output('season-form', 'figure'),
    Input('team', 'value'),
    Input('season', 'value')
)
def update_team_matches(team, season):
    if team is None or season is None:
        return [], {}
    matches = get_team_matches(team, season)
    table_data = matches.to_dict('records')
    figure = px.bar(matches, x='date', y='goal_diff', color='result', hover_data=['home', 'away', 'score'], width=800, height=400,
                    color_discrete_map={'Win': 'blue', 'Loss': 'red', 'Draw': 'green'})
    for _, match in matches.iterrows():
        if match['result'] == 'Draw':
            figure.add_scatter(x=[match['date']], y=[match['goal_diff']], mode='markers', marker=dict(size=5, color='green'), showlegend=False)
        
    return table_data, figure

@callback(
    Output('football-pitch', 'figure'),
    Output('match-title', 'children'),
    Output('match-date', 'children'),
    Output('match-result', 'children'),
    Output('lineup-tbl', 'data'),
    Input('match-info-tbl', 'selected_rows'),
    Input('match-info-tbl', 'data')
)
def update_match_info(selected_rows, data):
    dim = PitchDimensions()
    fig = make_pitch_figure(dim, pitch_background=SingleColourBackground("#81B622"))
    width, height = fig.layout.xaxis.range[1], fig.layout.yaxis.range[1]
    if not selected_rows or not data:
        return fig, "", "", "", []
    row_num = selected_rows[0]
    if row_num >= len(data):
        return fig, "", "", "", []
    selected_row = data[row_num]
    home_players = [selected_row[f'home_player_{i}'] for i in range(1, 12)]
    away_players = [selected_row[f'away_player_{i}'] for i in range(1, 12)]
    all_players_id_name_mapping = get_players_names(home_players + away_players)
    all_players_location = {}
    
    for i in range(1, 12):
        player_id = selected_row[f'home_player_{i}']
        all_players_location[player_id] = (selected_row[f'home_player_X{i}'], selected_row[f'home_player_Y{i}'])
        
    for i in range(1, 12):
        player_id = selected_row[f'away_player_{i}']
        all_players_location[player_id] = (selected_row[f'away_player_X{i}'], selected_row[f'away_player_Y{i}'])
    
    for player_id in home_players:
        player_name = all_players_id_name_mapping[player_id]
        x, y = all_players_location[player_id]
        if x == 1 and y == 1:
            fig.add_scatter(x=[width/24], y=[height/2], mode='markers', marker=dict(size=20, color='blue'), text=player_name,
                            hovertext=player_name, hoverinfo='text')
        else:
            fig.add_scatter(x=[width*y/24], y=[height*x/10], mode='markers', marker=dict(size=20, color='blue'), text=player_name,
                            hovertext=player_name, hoverinfo='text')

    for player_id in away_players:
        player_name = all_players_id_name_mapping[player_id]
        x, y = all_players_location[player_id]
        if x == 1 and y == 1:
            fig.add_scatter(x=[width*23/24], y=[height/2], mode='markers', marker=dict(size=20, color='red'), text=player_name,
                            hovertext=player_name, hoverinfo='text')
        else:
            fig.add_scatter(x=[width-width*y/24], y=[height-height*x/10], mode='markers', marker=dict(size=20, color='red'), text=player_name,
                            hovertext=player_name, hoverinfo='text')

    fig.update_layout(showlegend=False)
    
    match_title = f"{selected_row['home']} vs {selected_row['away']}"
    match_result = f"{selected_row['home_team_goal']} - {selected_row['away_team_goal']}"
    lineup_data = [{'home': all_players_id_name_mapping[home_player_id], 'away': all_players_id_name_mapping[away_player_id]}
                   for home_player_id, away_player_id in zip(home_players, away_players)]
    
    return fig, match_title, selected_row['date'], match_result, lineup_data
    
@callback(
    Output('hth-team-1', 'options'),
    Output('hth-team-2', 'options'),
    Input('league', 'value'),
)
def update_head_to_head_teams(league):
    teams = get_teams_by_league_and_season(league)
    league_teams = {}
    for _, row in teams.iterrows():
        league_teams[row['team_api_id']] = row['name']
    
    dropdown = [{'label': team_name, 'value': team_id} for team_id, team_name in league_teams.items()]
    dropdown.sort(key=lambda x: x['label'])
    return dropdown, dropdown

@callback(
    Output('hth-team-1', 'value'),
    Output('hth-team-2', 'value'),
    Input('hth-team-1', 'options'),
    Input('hth-team-2', 'options')
)
def update_head_to_head_teams_value(team_1, team_2):
    return team_1[0]['value'], team_2[1]['value']

@callback(
    Output('match-info-tbl', 'data', allow_duplicate=True),
    Input('hth-team-1', 'value'),
    Input('hth-team-2', 'value'),
    prevent_initial_call=True
)
def update_head_to_head_matches(team_1, team_2):
    if team_1 is None or team_2 is None:
        return []
    matches = get_head_to_head(team_1, team_2)
    table_data = matches.to_dict('records')
        
    return table_data

@callback(
    Output('team-attributes-compare', 'figure'),
    Input('season-select', 'value'),
    Input('hth-team-1', 'value'),
    Input('hth-team-2', 'value')
)
def update_team_attributes_compare(season, team_1, team_2):
    if season is None or team_1 is None or team_2 is None:
        return {}
    team_1_info, team_2_info = get_team_info(team_1, season), get_team_info(team_2, season)
    team_1_name, team_2_name = team_1_info['team_long_name'], team_2_info['team_long_name']
    columns_to_remove = [col for col in team_1_info.index if col not in TEAM_COLUMNS.keys()]
    team_1_info, team_2_info = team_1_info.drop(columns_to_remove), team_2_info.drop(columns_to_remove)
    
    for col_name, new_col_name in TEAM_COLUMNS.items():
        team_1_info[new_col_name], team_2_info[new_col_name] = team_1_info[col_name], team_2_info[col_name]
        team_1_info, team_2_info = team_1_info.drop(col_name), team_2_info.drop(col_name)

    team_1_info = team_1_info.drop("Positioning").drop("Defence Line")
    team_2_info = team_2_info.drop("Positioning").drop("Defence Line")
    fig = Figure()
    fig.add_bar(x=list(team_1_info.index), y=team_1_info.values, name=team_1_name)
    fig.add_bar(x=list(team_2_info.index), y=team_2_info.values, name=team_2_name)
    
    return fig

@callback(
    Output('season-select', 'value'),
    Input('match-info-tbl', 'selected_rows'),
    State('match-info-tbl', 'data'),
    State('url', 'pathname'),
    State('season-select', 'value')
)
def update_season_for_hth(selected_rows, all_matches, pathname, current_season_value):
    if pathname != "/head-to-head":
        return {}
    if selected_rows is None:
        return current_season_value
    season = all_matches[selected_rows[0]]['season']
    
    return season if season in SEASONS else current_season_value
    


@callback(
    Output('history-team', 'options'),
    Input('league', 'value')
)
def update_history_team(league):
    return update_head_to_head_teams(league)[0]

@callback(
    Output('history-team', 'value'),
    Input('history-team', 'options')
)
def update_history_team_value(teams):
    return teams[0]['value'] if teams else None

@callback(
    Output('season-form', 'figure', allow_duplicate=True),
    Output('goals-trend', 'figure'),
    Input('history-team', 'value'),
    Input('match-type', 'value'),
    prevent_initial_call=True
)
def update_history_form(team, match_type):
    if team is None:
        return {}
    team_matches = get_team_matches(team)
    if match_type == 'Home':
        team_matches = team_matches[team_matches['home_team_api_id'] == team]
    elif match_type == 'Away':
        team_matches = team_matches[team_matches['away_team_api_id'] == team]
    
    goals_per_season = team_matches.groupby('season').agg({'goals_scored': 'sum', 'goals_conceded': 'sum'}).reset_index()
    figure = px.histogram(team_matches, x='season', color='result', width=800, height=400,
                          color_discrete_map={'Win': 'blue', 'Loss': 'red', 'Draw': 'green'},
                          labels={'result': 'Result', 'season': 'Season', 'count': 'Matches'})
    goals = px.line(goals_per_season, x='season', y=['goals_scored', 'goals_conceded'], width=800, height=400,
                    labels={'value': 'Goals', 'variable': 'Goals'})
    return figure, goals

@callback(
    Output('fifa-attributes-history', 'figure'),
    Input('history-team', 'value'),
    Input('fifa-attributes', 'value')
)
def update_attributes_graph(team, attributes):
    if not attributes or team is None:
        return {}
    all_attributes = get_team_fifa_attributes(team)
    return px.line(all_attributes, x='season', y=attributes, width=800, height=400, labels={'value': 'Value', 'variable': 'Attribute'})