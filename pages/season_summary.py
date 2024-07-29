from dash import html, register_page

from components import create_global_filter, create_all_match_info,\
    create_team_info, create_match_info, create_season_form
from callbacks import *

register_page(__name__, path='/season-summary')

layout = html.Div(
        [
            html.Div(
                [
                    html.H1("Team Season Summary:"),
                    html.H1(id='team-name', style={'marginLeft': '20px', 'fontWeight': 'bold'})
                ], style={'display': 'flex'}
            ),
            html.Div(
                [
                    html.Div(
                        [
                            create_global_filter(),
                            create_team_info(),
                            create_match_info()
                        ], style={'margin': '10px', 'border': '2px solid gray',
                                'padding': '10px', 'borderRadius': '5px'}
                    ),
                    html.Div(
                        [
                            create_season_form(),
                            create_all_match_info(),
                        ], style={'margin': '10px', 'border': '2px solid gray',
                                'padding': '10px', 'borderRadius': '5px'}
                    )
                ], style={'display': 'flex'}
            )
        ])
