from dash import Dash, dash_table, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
from vega_datasets import data
import pandas as pd
import altair as alt


cars = data.cars()

# Initialization
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
table = dash_table.DataTable(
    id='table',
    # The data and columns parameters are set in the callback instead
    column_selectable="single",
    selected_columns=['Miles_per_Gallon'],
    page_size=5,
    sort_action='native',
    filter_action='native',
)
dropdown = dcc.Dropdown(
    id='dropdown',
    options=cars.columns,
    value=['Name', 'Miles_per_Gallon', 'Horsepower'],
    multi=True
)
scatter = dvc.Vega(
    id='scatter',
    opt={'actions': False},  # Remove the three dots button
    style={'width': '100%'}
)
histogram = dvc.Vega(
    id='histogram',
    opt={'actions': False},  # Remove the three dots button
    style={'width': '100%'}
)

# Layout
app.layout = dbc.Container(
    dbc.Row([
        dbc.Col([dropdown, table]),
        dbc.Row([
            dbc.Col(histogram),
            dbc.Col(scatter),
        ]),
    ])
)

@callback(
    Output('table', "columns"),
    Output('table', "data"),
    Input('dropdown', "value"),
)
def update_table(dropdown_cols):
    print(dropdown_cols)
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
