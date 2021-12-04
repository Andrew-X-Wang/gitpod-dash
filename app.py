import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
from dash.dependencies import Input, Output
import dash_pivottable

import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')

app = dash.Dash(__name__)
def identity(x): return x

cols = df.columns

app.layout = html.Div(children=[
    html.H2(children='Periodic Pivot Table!!'),
    dcc.Dropdown(
        id="index_dropdown",
        options=[{'label': i, 'value': i} for i in cols],
        multi=False,
        placeholder='Index!!'
    ),
    dcc.Dropdown(
        id="column_dropdown",
        options=[{'label': col, 'value': col} for col in cols],
        multi=False,
        placeholder='Column!!'
    ),
    dcc.Dropdown(
        id="value_dropdown",
        options=[{'label': val, 'value': val} for val in cols],
        multi=False,
        placeholder='Value!!'
    ),
    html.Div(id='pivot-table'),
])

@app.callback(
    Output('pivot-table', 'children'),
    [Input('index_dropdown', 'value'), 
     Input('column_dropdown', 'value'), 
     Input('value_dropdown', 'value')]
)
def update_output(idx, cols, vals):
    if idx is not None and cols is not None and vals is not None:
        pt = df.pivot_table(index=idx, columns=cols, values=vals, aggfunc=identity)
        pt_cols = [{"name": str(c), "id": str(c)} for c in pt.columns]
        print(idx)
        print(cols)
        print(vals)
        print(pt_cols)
        
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=pt_cols,
                data=pt.reset_index().to_dict("rows"),
                style_cell={'width': '300px',
                'height': '60px',
                'textAlign': 'left'})
            ])


app.run_server(debug=True, host="0.0.0.0")
