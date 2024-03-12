# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)


all_option=[{'label': 'All Sites', 'value': 'ALL'}]
unique_launch_sites = spacex_df['Launch Site'].unique()
launch_sites_dropdown = [{'label': site, 'value': site} for site in unique_launch_sites]
drop_options=all_option+launch_sites_dropdown



# Create an app layout
# ... (previous code)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
           style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    dcc.Dropdown(id='site-dropdown',
                 options=drop_options,
                 value='ALL',
                 placeholder="Select a Launch Site",
                 searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),  # This is just a placeholder for where the pie chart will be rendered
    html.Br(),
    html.P("Payload range (Kg):"),
    #TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0,
                    max=10000,
                    step=1000,
                    marks={0: '0', 10000: '10000'},
                    value=[min_payload, max_payload]),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),

])  


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
       success_rates = []
       for site in spacex_df['Launch Site'].unique():
            site_data = spacex_df[spacex_df['Launch Site'] == site]
            success_count = site_data[site_data['class'] == 1].shape[0]
            total_count = len(site_data)
            success_rate = success_count / total_count if total_count > 0 else 0
            success_rates.append(success_rate)

    # Create a pie chart for success rates of each launch site
       site_names = spacex_df['Launch Site'].unique()
       fig = px.pie(names=site_names, values=success_rates, title='Success Rates for Each Launch Site')
    else:
        # For a specific site, filter the dataframe and show success and failure counts
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        site_success_count = filtered_df[filtered_df['class'] == 1].shape[0]
        site_failure_count = filtered_df[filtered_df['class'] == 0].shape[0]

        # Create a pie chart for success and failure counts for the selected site
        fig = px.pie(names=['Success', 'Failure'], values=[site_success_count, site_failure_count], title=f'Success vs. Failure Launches for {entered_site}')

    return fig






# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_scatter_chart(selected_site, selected_payload_range):
    if selected_site == 'ALL':
        # Filter the dataframe based on the selected payload range
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]

        # Create a scatter plot for all sites
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                                 color='Booster Version Category', title='Payload vs. Launch Outcome for All Sites')

    else:
        # Filter the dataframe for the selected site and payload range
        filtered_df = spacex_df[(spacex_df['Launch Site'] == selected_site) &
                                (spacex_df['Payload Mass (kg)'] >= selected_payload_range[0]) &
                                (spacex_df['Payload Mass (kg)'] <= selected_payload_range[1])]

        # Create a scatter plot for the selected site
        scatter_fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                                 color='Booster Version Category',
                                 title=f'Payload vs. Launch Outcome for {selected_site}')

    return scatter_fig
# Run the app
if __name__ == '__main__':
    app.run_server()
