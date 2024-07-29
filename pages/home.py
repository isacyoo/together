from dash import html, register_page

register_page(__name__, path='/')

layout = html.Div(
    [
        html.Div(
            [
                html.H1("Introduction"),
                html.P("This is a football data dashboard that provides insights into football data. "
                       "You can navigate through the different pages using the links above."),
                html.P("The dataset was obtained from Kaggle."
                       "It is a SQLite dump file that contains data about football matches, teams, and players "
                       "from 11 leagues in 8 seasons, starting from 2008/2009 to 2015/2016."
                       "It was obtained from Kaggle and is available at "),
                html.A("European Soccer Database", href="https://www.kaggle.com/hugomathien/soccer/data"),
                html.Hr(),
                html.H1("Head to Head"),
                html.P("This page provides insights into head-to-head records between two teams. "
                       "You can select the league and the two teams to compare. "),
                html.P("The page then displays the list of matches between the two teams. "
                       "By selecting a match, you can view the match details, including the result,"
                       "the date, the lineup and the formation of the teams. "
                       "The page also provides a tool to compare their team attributes in FIFA in different seasons.")
            ], style={'margin': '10px', 'border': '2px solid gray',
                      'padding': '10px', 'borderRadius': '5px', 'width': '30%'}
        ),
        html.Div(
            [
                html.H1("Team History"),
                html.P("This page provides insights into the history of a team. "
                       "You can select the league and the team to view the history."),
                html.P("It first shows how the FIFA team attributes of the team have changed over the seasons. "
                       "It then shows the trend of the number of matches won, lost, and drawn "
                       "by the team over the seasons depending on whether it was playing at home or away."
                       "Below the graph, you can view the trend of the number of goals scored and conceded by the team."),
                html.Hr(),
                html.H1("Season Summary"),
                html.P("This page provides insights into the summary of a team's season. "
                       "You can select the season, league, and the team to view the summary."),
                html.P("It shows all the league matches in that season played by the team and their details, "
                       "including the result, the date, the lineup, and the formation of the team. "
                       "It also shows the FIFA team attributes that season along with the league average for each of them. "
                       "The graph on the top right shows the form of the team throughout the season.")
            ], style={'margin': '10px', 'border': '2px solid gray',
                      'padding': '10px', 'borderRadius': '5px', 'width': '30%'}
        )
    ], style={'display': 'flex'}
)
