import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input, Output

import numpy as np

app = dash.Dash()

df = pd.DataFrame({'x': np.linspace(0, 10, 100),
                   'y': np.sin(np.linspace(0, 10, 100))})
#df = pd.read_csv('data.csv')

app.layout = html.Div(children=[
    html.H1(children='My Dashboard'),
    html.Hr(),
    html.Div(children='''
        A simple dashboard.
    '''),
    html.Div([
        dcc.Dropdown(
            id='xaxis-column',
            options=[{'label': i, 'value': i} for i in df.columns],
            value='x'
        ),
        dcc.RadioItems(
            id='xaxis-type',
            options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            value='Linear',
            labelStyle={'display': 'inline-block'}
        )
    ],
    style={'width': '48%', 'display': 'inline-block'}),

    dcc.Graph(
        id='indicator-graphic'
    )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('xaxis-type', 'value')])
def update_graph(xaxis_column_name, xaxis_type):
    return {
        'data': [dict(
            x=df[xaxis_column_name],
            y=df['y'],
            type='line'
        )],
        'layout': dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': 'y',
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)