# Import required libraries
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
spacex_df['Landing Outcome'] = spacex_df['class'].apply(lambda x: 'Failed Landing' if (x == 0) else 'Successful Landing')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = Dash(__name__)

# Create an app layout
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1('SpaceX Launch Records Dashboard',
                style={'textAlign': 'center', 'color': '#503D36','font-size': 40}
            )
        ], className='element-wrapper'),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        html.Div(
            dcc.Dropdown(id='site-dropdown',
                options=[
                    {'label': 'All Sites', 'value': 0},
                    {'label': 'CCAFS LC-40', 'value': 1},
                    {'label': 'CCAFS SLC-40', 'value': 2},
                    {'label': 'KSC LC-39A', 'value': 3},
                    {'label': 'VAFB SLC-4E', 'value': 4}
                ],
                value=0,
                placeholder="Select a Launch Site",
                searchable=True
            )
        ),
        html.Br(),

        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div([
            dcc.Graph(id='success-pie-chart')
        ], className='element-wrapper'),
        html.Br(),

        html.Div([
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
            dcc.RangeSlider(id='payload-slider',
                min=0, max=10000, step=1000,
                value=[min_payload,max_payload],
            )
        ], className='element-wrapper'),
        html.Br(),

        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div([
            dcc.Graph(id='success-payload-scatter-chart')
        ], className='element-wrapper')
    ], id='content-wrapper')
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def get_pie_chart(entered_site):
    launchSites = ['All sites', 'CCAFS LC-40', 'CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E']
    if entered_site == 0:
        df_pie = spacex_df[spacex_df['class'] == 1]
        title = 'Total launches for all sites'
        fig = px.pie(df_pie, names='Launch Site', hole=0.25, title=title)
    else:
        df_pie = spacex_df[spacex_df['Launch Site'] == launchSites[entered_site]]
        title = 'Total launches for ' + launchSites[entered_site]
        fig = px.pie(df_pie, names='Landing Outcome',hole=0.25, title=title)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def get_scatter_chart(entered_site, payload_range):
    launchSites = ['All sites', 'CCAFS LC-40', 'CCAFS SLC-40', 'KSC LC-39A', 'VAFB SLC-4E']
    low, high = payload_range
    mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    if entered_site == 0:
        df_scatter = spacex_df.copy()
        title = 'Total launches for all sites'
        fig = px.scatter(df_scatter[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)
    else:
        df_scatter = spacex_df[spacex_df['Launch Site'] == launchSites[entered_site]]
        title = 'Total launches for ' + launchSites[entered_site]
        fig = px.scatter(df_scatter[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title=title)
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=3000)
