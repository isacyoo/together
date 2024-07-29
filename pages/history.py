from dash import html, register_page

from components import create_league_filter, create_match_type_dropdown, create_season_form,\
    create_team_dropdown, create_goals_trend, create_team_fifa_attributes_history

register_page(__name__, path='/history')

layout = html.Div(
    [
        html.H1("Team History"),
        html.Div([
        html.Div(
            [
                create_league_filter(),
                create_team_dropdown(),
                create_match_type_dropdown(),
                create_team_fifa_attributes_history()
            ], style={'margin': '10px', 'border': '2px solid gray',
                        'padding': '10px', 'borderRadius': '5px'}
        ),
        html.Div(
            [
                create_season_form(),
                create_goals_trend()
            ], style={'margin': '10px', 'border': '2px solid gray',
                        'padding': '10px', 'borderRadius': '5px'}
        )
    ], style={'display': 'flex'})
    ]
)
