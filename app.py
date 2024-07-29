from dash import Dash, html, dcc, page_container, page_registry

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets,
           use_pages=True, prevent_initial_callbacks="initial_duplicate",
           title='Football Data Dashboard')

app.layout = html.Div([
    html.H1('Football Data Dashboard'),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']}", href=page["relative_path"]), style={'margin': '10px'}
        ) for page in page_registry.values()
    ], style={'display': 'flex'}),
    dcc.Location(id='url'),
    html.Div(page_container, style={'margin': '20px'})
])

if __name__ == '__main__':
    app.run(debug=True)