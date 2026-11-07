
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load SpaceX dataset
spacex_df = pd.read_csv('spacex_launch_dash.csv')

# Create Dash application
app = dash.Dash(__name__)

# Get unique launch sites
launch_sites = spacex_df['Launch Site'].unique()

# Dashboard layout
app.layout = html.Div(children=[

    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'fontSize': 30
        }
    ),

    # TASK 1: Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in launch_sites
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Success Pie Chart
    dcc.Graph(
        id='success-pie-chart'
    ),

    html.Br(),

    # TASK 3: Payload Mass Range Slider
    html.P('Payload Mass Range (kg):'),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=15000,
        step=1000,
        marks={
            0: '0',
            2500: '2500',
            5000: '5000',
            7500: '7500',
            10000: '10000',
            12500: '12500',
            15000: '15000'
        },
        value=[0, 15000]
    ),

    html.Br(),

    # TASK 4: Payload Scatter Chart
    dcc.Graph(
        id='success-payload-scatter-chart'
    )

])


# CALLBACK 1: Update Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':

        fig = px.pie(
            spacex_df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )

    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Successful vs Unsuccessful Launches for {entered_site}'
        )

    return fig


# CALLBACK 2: Update Scatter Chart
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def get_scatter_chart(entered_site, payload_range):

    low, high = payload_range

    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if entered_site != 'ALL':

        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs Launch Outcome',
        labels={
            'class': 'Launch Outcome',
            'Payload Mass (kg)': 'Payload Mass (kg)'
        }
    )

    return fig


# Run the application
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=8050,
        debug=False
    )
