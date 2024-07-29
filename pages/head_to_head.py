from dash import html, register_page

from components import create_league_filter, create_head_to_head_dropdowns, create_match_info,\
    create_all_match_info, create_team_attributes_compare
from callbacks import *

register_page(__name__, path='/head-to-head')

layout = html.Div(
        [
            html.H1("Head to Head records"),
            html.Div([
            html.Div(
                [
                    create_league_filter(),
                    create_head_to_head_dropdowns(),
                    create_match_info()
                ], style={'margin': '10px', 'border': '2px solid gray',
                            'padding': '10px', 'borderRadius': '5px'}
            ),
            html.Div(
                [
                    create_team_attributes_compare(),
                    create_all_match_info()
                ], style={'margin': '10px', 'border': '2px solid gray',
                            'padding': '10px', 'borderRadius': '5px'}
            )
        ], style={'display': 'flex'})
        ]
    )
