import sqlite3
from functools import lru_cache

import pandas as pd

from constants import TEAM_COLUMNS, PATH_TO_DB, SEASONS, LEAGUES

db_conn = sqlite3.connect(PATH_TO_DB, check_same_thread=False)
team_season_info_query = ("SELECT league_id, season, home_team_api_id AS team_api_id, t.team_long_name as name FROM Match m "
                          f"JOIN Team t on m.home_team_api_id = t.team_api_id WHERE m.season in {tuple(SEASONS)} "
                          f"AND m.league_id in {tuple(league['league_id'] for league in LEAGUES)} "
                          "group by m.season, m.home_team_api_id order by m.league_id, m.season, t.team_long_name")
team_season_info = pd.read_sql(team_season_info_query, db_conn)

def get_teams_by_league_and_season(league_id, season=None):
    if season is None:
        return team_season_info[team_season_info['league_id'] == league_id]
    return team_season_info[(team_season_info['season'] == season) & (team_season_info['league_id'] == league_id)]

def get_team_info(team_api_id, season):
    query = (f"SELECT * FROM Team t JOIN Team_Attributes ta ON t.team_api_id = ta.team_api_id WHERE t.team_api_id = {team_api_id} "
             f"AND STRFTIME('%Y', ta.date) = '{season[:4]}'")
    return pd.read_sql(query, db_conn).iloc[0]

@lru_cache
def get_league_averages(league_id, season):
    team_api_ids = get_teams_by_league_and_season(league_id, season)['team_api_id']
    query = " ".join([
        "SELECT",
        ', '.join([f'AVG({col}) as "{new_col}" ' for col, new_col in TEAM_COLUMNS.items()]),
        f"FROM Team_Attributes WHERE team_api_id in ({','.join(str(team_api_id) for team_api_id in team_api_ids)})",
        f"AND STRFTIME('%Y', date) = '{season[:4]}'"
    ])
    
    league_averages = pd.read_sql(query, db_conn).iloc[0]
    return league_averages.drop("Positioning").drop("Defence Line")

@lru_cache
def get_team_matches(team_id, season=None):
    if season is None:
        season_query = "WHERE season in {} ".format(tuple(SEASONS))
    else:
        season_query = f"WHERE season = '{season}' "
    query = ("SELECT m.*, ht.team_long_name as home, at.team_long_name as away FROM Match m JOIN Team ht on m.home_team_api_id = ht.team_api_id "
             "JOIN Team at on m.away_team_api_id = at.team_api_id "
             f"{season_query}"
             f"AND (home_team_api_id = {team_id} OR away_team_api_id = {team_id})"
             "ORDER BY m.date")
    matches = pd.read_sql(query, db_conn)
    matches["date"] = matches["date"].astype('datetime64[s]').dt.strftime('%Y-%m-%d')
    matches["score"] = matches.apply(lambda x: f"{x['home_team_goal']} - {x['away_team_goal']}", axis=1)
    
    def determine_winner(row):
        home = team_id == row['home_team_api_id']
        if row['home_team_goal'] == row['away_team_goal']:
            return 'Draw'
        elif (home and row['home_team_goal'] > row['away_team_goal']) or (not home and row['home_team_goal'] < row['away_team_goal']):
            return 'Win'
        else:
            return 'Loss'
        
    def determing_winner_team_api_id(row):
        if row['result'] == 'Draw':
            return 0
        return row['home_team_api_id'] if row['result'] == row['home'] else row['away_team_api_id']
        
    def calculate_goal_diff(row):
        home = team_id == row['home_team_api_id']
        return row['home_team_goal'] - row['away_team_goal'] if home else row['away_team_goal'] - row['home_team_goal']
    
    matches["result"] = matches.apply(determine_winner, axis=1)
    matches["goal_diff"] = matches.apply(calculate_goal_diff, axis=1)
    matches["winner_team_api_id"] = matches.apply(determing_winner_team_api_id, axis=1)
    matches["goals_scored"] = matches.apply(lambda x: x['home_team_goal'] if team_id == x['home_team_api_id'] else x['away_team_goal'], axis=1)
    matches["goals_conceded"] = matches.apply(lambda x: x['away_team_goal'] if team_id == x['home_team_api_id'] else x['home_team_goal'], axis=1)
    
    return matches

def get_players_names(player_ids):
    query = "SELECT player_api_id, player_name FROM Player WHERE player_api_id in ({})".format(','.join(str(player_id) for player_id in player_ids))
    df = pd.read_sql(query, db_conn)
    id_name_mapping = {row['player_api_id']: row['player_name'] for _, row in df.iterrows()}
    return id_name_mapping

def get_head_to_head(team_1, team_2):
    query = ("SELECT m.*, ht.team_long_name as home, at.team_long_name as away "
             "FROM Match m JOIN Team ht on m.home_team_api_id = ht.team_api_id "
             "JOIN Team at on m.away_team_api_id = at.team_api_id "
             f"WHERE (home_team_api_id = {team_1} AND away_team_api_id = {team_2}) OR (home_team_api_id = {team_2} AND away_team_api_id = {team_1})")
    matches = pd.read_sql(query, db_conn)
    matches["date"] = matches["date"].astype('datetime64[s]').dt.strftime('%Y-%m-%d')
    matches["score"] = matches.apply(lambda x: f"{x['home_team_goal']} - {x['away_team_goal']}", axis=1)
    matches["team_1"] = team_1
    matches["team_2"] = team_2
    
    def determine_winner(row):
        if row['home_team_goal'] == row['away_team_goal']:
            return 'Draw'
        elif row['home_team_goal'] > row['away_team_goal']:
            return row['home']
        else:
            return row['away']
        
    def determing_winner_team_api_id(row):
        if row['result'] == 'Draw':
            return 0
        return row['home_team_api_id'] if row['result'] == row['home'] else row['away_team_api_id']
        
    matches["result"] = matches.apply(determine_winner, axis=1)
    matches["winner_team_api_id"] = matches.apply(determing_winner_team_api_id, axis=1)        
    
    return matches

def get_team_fifa_attributes(team_id):
    query = f"SELECT * FROM Team_Attributes WHERE team_api_id = {team_id}"
    all_attributes = pd.read_sql(query, db_conn)
    all_attributes.rename(TEAM_COLUMNS, axis=1, inplace=True)
    all_attributes['season'] = all_attributes['date'].apply(lambda x: f'{x[:4]}/{int(x[:4])+1}')
    return all_attributes