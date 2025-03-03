from dash import Dash, dash_table, dcc, callback, Input, Output, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from vega_datasets import data
import pandas as pd
import altair as alt


cars = data.cars()

# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
title = html.H1(
    'My splashboard demo',
    style={
        'backgroundColor': 'steelblue',
        'padding': 20,
        'color': 'white',
        'margin-top': 20,
        'margin-bottom': 20,
        'text-align': 'center',
        'font-size': '48px',
        'border-radius': 3,
        'margin-left': -10,  # Align with sidebar
    }
)

table = dbc.Col(
    dash_table.DataTable(
        id='table',
        # The data and columns parameters are set in the callback instead
        column_selectable="single",
        selected_columns=['Miles_per_Gallon'],
        page_size=8,
        sort_action='native',
        filter_action='native',
        style_data_conditional=[{
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }],
         style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_as_list_view=True,
        editable=True,
    ),
)

dropdown = dcc.Dropdown(
    id='dropdown',
    options=cars.columns,
    value=['Name', 'Miles_per_Gallon', 'Horsepower'],
    multi=True
)

density = dbc.Card([
    dbc.CardHeader('Density', style={'fontWeight': 'bold'}),
    dbc.CardBody(
        dvc.Vega(
            id='scatter',
            opt={'actions': False},  # Remove the three dots button
            style={'width': '100%'}
        )
    )
])

histogram = dbc.Card([
    dbc.CardHeader('Histrogram', style={'fontWeight': 'bold'}),
    dbc.CardBody(
        dvc.Vega(
            id='histogram',
            opt={'actions': False},  # Remove the three dots button
            style={'width': '100%'}
        )
    )
])

sidebar = dbc.Col([
    html.H5('Global controls'),
    html.Br(),
    dropdown,
    html.Br(),
    dcc.Dropdown(),
    html.Br(),
    dcc.Dropdown(),
    ],
    md=3,
    style={
        'background-color': '#e6e6e6',
        'padding': 10,
        'border-radius': 3,
    }
)


# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        sidebar,  # Already wrapped in dbc.Col
        dbc.Col([
            table, # Already wrapped in dbc.Col
            dbc.Row([
                dbc.Col(histogram),
                dbc.Col(density),
            ])
        ],
        md=9),
    ])
])

@callback(
    Output('table', "columns"),
    Output('table', "data"),
    Input('dropdown', "value"),
)
def update_table(dropdown_cols):
    return(
        [  # A list of dictionaries, each representing a column
            {
                "name": col.replace('_', ' '),
                "id": col,
                'selectable': False if col == 'Name' else True
            }
            for col in dropdown_cols
        ],
        cars[dropdown_cols].to_dict('records')
    )


@callback(
    Output('histogram', "spec"),
    Output('scatter', "spec"),
    Input('table', "derived_virtual_data"),
    Input('table', "selected_columns"),
    prevent_initial_call=True  # Avoid triggering before the table has a selected column
)
def update_(table_rows, table_column):
    histogram = alt.Chart(pd.DataFrame(table_rows), width='container').mark_bar().encode(
        alt.X(f'{table_column[0]}:Q').bin(maxbins=30),
        alt.Y('count()')
    )
    scatter = alt.Chart(pd.DataFrame(table_rows), width='container').mark_area().transform_density(
        table_column[0],
        as_=[table_column[0], 'density']
    ).encode(
        alt.X(f'{table_column[0]}:Q'),
        alt.Y('density:Q'),
    )
    return histogram.to_dict(), scatter.to_dict()


if __name__ == '__main__':
    app.run()
