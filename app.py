
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import requests
import pandas as pd
import datetime


########### Define a few variables ######

tabtitle = 'Weather'
sourceurl = 'https://openweathermap.org/api'
githublink = 'https://github.com/austinlasseter/weather-api-dash-app'
dc_latitude=38.9
dc_longitude=-77.0



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    html.H1('Check the weather'),
    # Dropdowns
    html.Div(children=[
        # left side
        html.Div([
            html.Div("Enter coordinates and press 'Return'"),
            html.H3(id='lat-div', children='Latitude:'),
            dcc.Input(id='latitude_input', type='number', debounce=True, min=-90, max=90, step=0.1, value=dc_latitude, placeholder=dc_latitude, style={'marginLeft':'10px'}),
            html.H3(id='lon-div', children='Longitude:'),
            dcc.Input(id='longitude_input', type='number', debounce=True, min=-180, max=180, step=0.1, value=dc_longitude, placeholder=dc_longitude, style={'marginLeft':'10px'}),
        ], className='three columns'),
        # right side
        html.Div([
                html.H4(id="message-div"),
        ], className='nine columns'),


    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Callbacks
@app.callback(Output('message-div', 'children'),
              [Input('latitude_input', 'value'),
              Input('longitude_input', 'value')],
             )
def update_message(latitude, longitude):

    austins_api_key = '9eb078023ce1d3136bbb540b8fee91ca'
    request_string = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=imperial&appid={austins_api_key}'
    result = requests.get(request_string)
    weather_result = result.json()
    try:
        temp = weather_result['main']['temp']
        place = weather_result['name']
        epoch_time=weather_result["sys"]["sunrise"]
        datetime_time = datetime.datetime.fromtimestamp(epoch_time)
        date=datetime_time.date()
        message = f'The temperature is {temp} degrees in {place} on {date}!'
        return message
    except:
        message = f'Error: {weather_result}'
        return message


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
