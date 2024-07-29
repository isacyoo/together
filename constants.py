PATH_TO_DB = 'database.sqlite'
SEASONS = [f"{year}/{year+1}" for year in range(2010, 2016)]
LEAGUES = [{'country': 'Belgium', 'league_id': 1}, {'country': 'England', 'league_id': 1729}, {'country': 'France', 'league_id': 4769},
           {'country': 'Germany', 'league_id': 7809}, {'country': 'Italy', 'league_id': 10257}, {'country': 'Netherlands', 'league_id': 13274},
           {'country': 'Portugal', 'league_id': 17642}, {'country': 'Scotland', 'league_id': 19694},
           {'country': 'Spain', 'league_id': 21518}, {'country': 'Switzerland', 'league_id': 24558}]
TEAM_COLUMNS = {'buildUpPlaySpeed': 'Play speed', 'buildUpPlayPassing': 'Build up', 'buildUpPlayPositioningClass': 'Positioning',
                'chanceCreationPassing': 'Passing', 'chanceCreationCrossing': 'Crossing', 'chanceCreationShooting': 'Shooting',
                'defencePressure': 'Pressure', 'defenceAggression': 'Aggression', 'defenceTeamWidth': 'Team width',
                'defenceDefenderLineClass': 'Defence Line'}