# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.io as pio

pio.templates.default="plotly_dark"

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("data/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': 'white',
                                               'font-size': 40, 'backgroundColor': 'black'},
                                        ),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All Sites', 'value': 'ALL'}, ] \
                                                     + [{'label': i, 'value': i} for i in \
                                                        spacex_df["Launch Site"].unique()],
                                             value='ALL',
                                             placeholder="Select a Launch Site here",
                                             searchable=True
                                             ),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload_slider',
                                                min=0, max=10000, step=1000,
                                                marks={i: '{}'.format(str(i) + " kg") for i in (range(0, 11000, 1000))},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df,
                     names='Launch Site',
                     title='All Launch Sites',
                     hole=0.3)
    else:
        fig = px.pie(filtered_df,
                     names='class',
                     title='Launch site: '+entered_site,
                     hole=0.3)
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload_slider", component_property="value")])
def get_scatter_chart(entered_site, payload_slider):
    df = spacex_df
    low, high = payload_slider
    mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
    df = df[mask]
    if entered_site == 'ALL':
        fig = px.scatter(df,
                         x='Payload Mass (kg)',
                         y='class',
                         color="Booster Version Category",
                         title='Correlation between Payload and Success for all launch sites',
                         hover_data=['Payload Mass (kg)']
                         )
    else:
        filtered_df = df[df["Launch Site"] == entered_site]
        fig = px.scatter(filtered_df,
                         x='Payload Mass (kg)',
                         y='class',
                         color="Booster Version Category",
                         title='Correlation between Payload and Success for: ' + entered_site,
                         hover_data=['Payload Mass (kg)'])
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
