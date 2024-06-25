###############################################################################
###                                 CODE                                    ###
###############################################################################




#importing packages for vizualization and analysis
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#package used for formatting the axis of the missing values plot
import matplotlib.ticker as mtick
#package used for creating the python date format of each year
import datetime as dt
#package used for formatting the axis of the temperature animation plot
from datetime import timedelta
#package used to create the running line animation of temperature, 
#and to keep only day and month for the x-axis
from matplotlib import animation, dates
#importing module to place C (celcius) sign next to y-axis values
from matplotlib.ticker import EngFormatter
#Gradient Color Bar Plots
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import colors as mcolors, path, cm
from itertools import count

#ONLINE APPLICATION PACKAGES

import plotly.express as px

from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

#package required to make python import and read .png files (used for weather conditions distribution)
from PIL import Image

import requests

#requirements for plots
import plotly.figure_factory as ff  
import plotly.graph_objects as go

#module which allows the website to open automatically in a new tab every time the code runs
import webbrowser

#importing the cleaned dataset
full = pd.DataFrame(pd.read_csv(r"https://raw.githubusercontent.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard/main/Dataset/Cleaned%20Dataset.csv"))

###############################################################################
###                       CONSTRUCTING APPLICATION                          ###
###      TYPE 127.0.0.1:8050 ON CHROME ADRESS BAR TO ACCESS APPLICATION     ###
###############################################################################

#creating empty dataframe for our dataset
df1 = pd.DataFrame([])


#setting the background, and text colors for the web application
colors = {
    'background': '#141414',
    'text': '#E8E8E8'
    }

#defining devaule style for all text in the dashboard
style_text={'text-align': 'left', 'color': colors['text']}


#initializing the application object
app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server
app.title='Toronto Weather Dashboard'

#setting up the layout of the application
app.layout = html.Div(style={'text-align': 'Center', 'backgroundColor':colors['background'], 'color': colors['text']}, children =
                      
                      #intro warning text when entering the website for the first time
                      [dbc.Modal(id = 'intro-warning-messages', size='lg', backdrop = 'static', is_open=True, centered=False, children = [
                           dbc.ModalHeader("WEBSITE REQUIREMENTS:", style = {'color':'red', 'font-size':'45px', 'font-weight':'bold', 'text-decoration': 'underline', 'justify': 'center'}),
                           dbc.ModalBody("(1) USE DESKTOP TO VIEW WEBSITE", style = {'font-weight': 'bold', 'font-size': '35px'}),
                           dbc.ModalBody("(2) SET PAGE ZOOM TO 100%", style = {'font-weight': 'bold', 'font-size': '35px'})
                           ]),
                    
                          
                       #title
                       html.Div(style = {'margin-bottom':'0px'}, children = [html.H1("Toronto Weather Analysis", style = {'margin-bottom': '0px'})]),                     
                       
                       #my info
                       html.Div(style = {'margin-bottom': '0px'}, children = [
                       html.H6("Nikolaos Rizos | HBSc | LinkedIn:", style={'display':'inline-block', 'padding': '5px', 'margin-bottom': '0px'}),
                       html.A('https://www.linkedin.com/in/rizosnikolaos1/', href='https://www.linkedin.com/in/rizosnikolaos1/', target="https://www.linkedin.com/in/rizosnikolaos1/", style = {'margin-bottom': '0px'})]),    
                       
                       #github link
                       html.Div(style = {'margin-bottom': '0px', 'text-align': 'Center', 'font-size': '12px'}, children = [html.H6("GitHub:", style = {'display': 'inline-block', 'font-size': '12px', 'padding': '5px', 'margin-bottom': '0px'}),
                       html.A("https://github.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard", href="https://github.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard", target="https://github.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard", style = {'margin-bottom': '0px'})]),
                       
                       html.Br(),

                       html.Div(style = {'margin-bottom': '0px', 'text-align': 'Left', 'font-size': '22px', 'padding': '10px'}, children = [
                       html.P("The goal of this project is to create an efficient online dashboard used to analyze and better understand Toronto's weather. The dashboard consists of three elegant visualizations: a summary statistics table, a weather conditions distribution, and and hourly evolution graph. The dashboard is designed to be user friendly, with the provided graphs presenting the weather information in a consice way that catches the eye. The user only needs to select a year, a month and a metric of interest, and the dashboard updates all three visualizations automatically. The entire dashboard, including the website, layout, colors, and all the charts and their attributes, are my own original work and made from scratch using only python and its libraries.", style = {'margin-bottom': '0px'})]),
                       
                       #space between info text and dropwdown menus
                       html.Br(),
                       html.Br(),
                       
                      #selection boxes
                      dbc.Row(
                          
                          #1st row begins here
                          [dbc.Col(html.Div(children = [html.H5('Please Select Year:', style={"margin-left": "40px", 'color': colors['text']})]), width = {'order': 1, 'size': 2, 'offset': 1}),
                           
                           #year selection dropdown menu
                           dbc.Col([dcc.Dropdown(id="year_selection", options= [{"label": "2017", "value": 2017},
                                                                       {"label": "2018", "value": 2018},
                                                                       {"label": "2019", "value": 2019},
                                                                       {"label": "2020", "value": 2020}], multi=False, value=2017, style = {'color' : colors['background']}),
                           
                           #populate dropdown box with selection from python function
                           html.Div(id='year_dropdown_box', style = {'color' : colors['background']})], width = {'order': 2, 'size': 2, 'offset': 0}),
                           
                           #prompt for month selection
                           dbc.Col(html.Div(children = [html.H5('Please Select Month:', style={'color': colors['text']})]), width = {'order': 3, 'size': 2, 'offset': 1}),
                          
                           #month selection dropdown menu
                           dbc.Col([dcc.Dropdown(id="month_selection", options= [{"label":"All", "value": 20},
                                                                       {"label": "January", "value": 1},
                                                                       {"label": "February", "value": 2},
                                                                       {"label": "March", "value": 3},
                                                                       {"label": "April", "value": 4},
                                                                       {"label": "May", "value": 5},
                                                                       {"label": "June", "value": 6},
                                                                       {"label": "July", "value": 7},
                                                                       {"label": "August", "value": 8},
                                                                       {"label": "September", "value": 9},
                                                                       {"label": "October", "value": 10},
                                                                       {"label": "November", "value": 11},
                                                                       {"label": "December", "value": 12}], multi=False, value=20, style = {'color' : colors['background']}),
                          
                           #populate dropdown box with selection from python function
                           html.Div(id='month_dropdown_box', style = {"margin-left": "150px", 'color' : colors['background']})], width = {'order': 4, 'size': 2, 'offset': 0}),
                          
                          #1st row stops here
                          ], className="g-0"),
                      
                      #break between the year selection box and radioitems selection
                       html.Br(),
                        
                       #second row
                       dbc.Row(
                           [dbc.Col(html.Div(children=[
                               
                               html.Br(),
                               
                               #prompt for graph selection
                               html.H3("Select a metric:", style={"margin-left": "140px"}),
                               
                               #graph selection (radioitems)
                               dcc.RadioItems(id = 'graph_selection', options = [
                                   {'label' : 'Temperature', 'value':0},
                                   {'label' : 'Humidity', 'value':1},
                                   {'label' : 'Wind Speed', 'value':2},
                                   {'label' : 'Visibility', 'value':3},
                                   {'label' : 'Pressure', 'value':4}
                                   ], value = 0, inline=True, inputStyle={"margin-left": "20px", "margin-right":"5px"}, style = {"margin-left": "50px", "font-size" : 21, "color":'yellow', 'font-weight': 'bold'}),
                               
                               html.Br(),
                               html.Br(),
                               html.Br(),
                               
                               #description of summary statistics
                               html.H3("Summary Statistics:", style={"margin-left": "100px", 'color': colors['text']}),
                               
                               #summary statistics (table)
                               dcc.Loading(id = 'table&loading-anim', type = 'bar', style = {'margin-bottom': '100px'}, children = [html.Div(id = "table", style={'height': '300px'})])]), width = {'order': 1, 'size': 6}),
                               
                               
                               dbc.Col([
                        
                                   #weather conditions bar chart
                                   dcc.Loading(id = 'weather_conditions_bargraph&loading-anim', type = 'bar', style = {'margin-top': '168px', 'font-size': '1000px'}, children = [dcc.Graph(id = 'weather_conditions_bargraph', figure={}, config={'displayModeBar': False}, style={'height': '550px', 'margin': 'auto'})])], width = {'order': 2, 'size': 6})], className = "g-0"
                           ),

                       dbc.Row(
                           
                           #2nd row begins here
                           [dbc.Col(html.Div(children = [
                               
                               #time series graph
                               dcc.Loading(id = 'times_series_graph&loading-anim', type = 'bar', style = {'margin-bottom': '370px'}, children = [dcc.Graph(id='time_series_graph', figure={}, config={'displayModeBar': False}, style={'height': '520px', "margin-left": "-40px"})])]), width = {'size': 12})], className="g-0", align="beginning"
                       )
                       ])
                
                
                                                              
                             
#linkning the webpage elements to the local code (including the graphs and data)
@app.callback(
    [Output(component_id='year_dropdown_box', component_property='children'),
     Output(component_id='month_dropdown_box', component_property='children'),
      Output(component_id='time_series_graph', component_property='figure'),
      Output(component_id='table', component_property = 'children'),
      Output(component_id='weather_conditions_bargraph', component_property='figure')],
    [Input(component_id='year_selection', component_property='value'),
      Input(component_id='month_selection', component_property='value'),
      Input(component_id='graph_selection', component_property = 'value')]
)

#function for updating the graphs based on year selection in dropdown box

def update_graph(year, month, selected_rows):
    #creating copy of original data
    data = full.copy()

    #year box & month box selection
    #F0R ALL MONTHS#
    if month == 20:
        data = data[data["Year"] == year]
    #FOR SIGNLE MONTH#
    elif (month != 20):
        data = data[data["Year"] == year]
        data = data[data["Month"] == month]
    
    #adding visuals for maximum, minimum, average
    
    #average
    average_temperature = round(np.average(data["Temp (°C)"]), 1)
    average_humidity = round(np.average(data["Rel Hum (%)"]), 1)
    average_windspeed = round(np.average(data['Wind Spd (km/h)']), 1)
    average_winddirection = round(np.average(data['Wind Dir (10s deg)']), 1)
    average_visibility = round(np.average(data["Visibility (km)"]), 1)
    average_pressure = round(np.average(data["Stn Press (kPa)"]), 1)
    
    #maximum
    max_index_temperature = data[data["Temp (°C)"] == max(data["Temp (°C)"])].index.values
    max_index_humidity = data[data["Rel Hum (%)"] == max(data["Rel Hum (%)"])].index.values
    max_index_windspeed = data[data["Wind Spd (km/h)"] == max(data["Wind Spd (km/h)"])].index.values
    max_index_visibility = data[data["Visibility (km)"] == max(data["Visibility (km)"])].index.values
    max_index_pressure = data[data["Stn Press (kPa)"] == max(data["Stn Press (kPa)"])].index.values
    
    
    #minimum
    min_index_temperature = data[data["Temp (°C)"] == min(data["Temp (°C)"])].index.values
    min_index_humidity = data[data["Rel Hum (%)"] == min(data["Rel Hum (%)"])].index.values
    min_index_windspeed = data[data["Wind Spd (km/h)"] == min(data["Wind Spd (km/h)"])].index.values
    min_index_visibility = data[data["Visibility (km)"] == min(data["Visibility (km)"])].index.values
    min_index_pressure = data[data["Stn Press (kPa)"] == min(data["Stn Press (kPa)"])].index.values
    
    #creating a dataframe containing our summary statistics
    df1 = pd.DataFrame({"Category": ["Temperature", "Humidity", "Wind Speed", "Visibility", "Pressure"],
                      "Maximum": [(data["Temp (°C)"][max_index_temperature]).to_string()[-5:] + ' °C', (data["Rel Hum (%)"][max_index_humidity]).to_string()[-5:] + ' %', (data["Wind Spd (km/h)"][max_index_windspeed]).to_string()[-5:] + ' km/h' + ", Bearing:" + (data["Wind Dir (10s deg)"][max_index_windspeed]).to_string()[-5:] + "°", (data["Visibility (km)"][max_index_visibility]).to_string()[-5:] + ' km', (data["Stn Press (kPa)"][max_index_pressure]).to_string()[-6:] + ' kPa'],
                      "Minimum": [(data["Temp (°C)"][min_index_temperature]).to_string()[-5:] + ' °C', (data["Rel Hum (%)"][min_index_humidity]).to_string()[-5:] + ' %', (data["Wind Spd (km/h)"][min_index_windspeed]).to_string()[-5:] + ' km/h' + ", Bearing:" + (data["Wind Dir (10s deg)"][min_index_windspeed]).to_string()[-5:] + "°", (data["Visibility (km)"][min_index_visibility]).to_string()[-5:] + ' km', (data["Stn Press (kPa)"][min_index_pressure]).to_string()[-6:] + ' kPa'],
                      "Average": [str(average_temperature) + ' °C', str(average_humidity) + ' %', str(average_windspeed) + ' km/h' + ", Bearing: " +  str(average_winddirection) + "°", str(average_visibility) + 'km', str(average_pressure) + ' kPa']
                      })
    


                                    # PLOTTING #
                        

    
    #loop for changing the graph and its attributes, based on the radioitems selection
    
    #defining empty strings for each of the selections
    graph_selection = ""
    graph_name = ""
    symbol = ""
    max_ind = ""
    min_ind = ""
    table_index=0
    
    #setting the wanted graph and its attributes based on the radioitems selection
    if (selected_rows == 0):
        graph_selection = "Temp (°C)"
        graph_name = "Temperature"
        symbol = " °C"
        max_ind = max_index_temperature
        min_ind = min_index_temperature
        ticks = 4
        table_index = 0
    elif (selected_rows == 1):
        graph_selection = "Rel Hum (%)"
        graph_name = "Relative Humidity"
        symbol = " %"
        max_ind = max_index_humidity
        min_ind = min_index_humidity
        ticks = 10
        table_index = 1
    elif (selected_rows == 2):
        graph_selection = "Wind Spd (km/h)"
        graph_name = "Wind Speed"
        symbol = " km/h"
        max_ind = max_index_windspeed
        min_ind = min_index_windspeed
        ticks = 7.5
        table_index = 2
    elif (selected_rows == 3):
        graph_selection = "Visibility (km)"
        graph_name = "Visibility"
        symbol = " km"
        max_ind = max_index_visibility
        min_ind = min_index_visibility
        ticks = 2
        table_index = 3
    elif (selected_rows == 4):
        graph_selection = "Stn Press (kPa)"
        graph_name = "Pressure"
        symbol = " kPa"
        max_ind = max_index_pressure
        min_ind = min_index_pressure        
        ticks = 0.5
        table_index = 4

    
    #setting variable for the data used to plot the timeseries graph. This data
    #needs to be independent from the dataset used for the summary statistics
    #and weather conditions distribution
    timeseries_data = data

    #adding two empty space values at the beginning of january 2019, as we have missing
    #values for 10am, and 1am, and for that reason the x-axis labels for january 2019 do not
    #show up if empty space is not provided for these two missing values
    fix = pd.DataFrame([[np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, dt.datetime(2019, 1, 1, 0, 0)],
                        [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, dt.datetime(2019, 1, 1, 1, 0)]],
        columns = ['Longitude (x)', 'Latitude (y)', 'Year', 'Month', 'Day', 'Time', 'Temp (°C)', 'Dew Point Temp (°C)', 'Rel Hum (%)', 'Wind Dir (10s deg)', 'Wind Spd (km/h)', 'Visibility (km)', 'Stn Press (kPa)', 'Weather', 'Date'])
    
    #adding 2 empty rows in front of the january 2019 data used ONLY FOR PLOTTING and NOT for computations of statistics,
    #in order to fix the problem with the first value not appearing on the x-axis for 2019    
    if year == 2019 and (month == 20 or month == 1):
        timeseries_data = pd.concat([fix, data], ignore_index = True)
    elif year != 2019 and month != 20:
        timeseries_data = data
    
    #main plot
    fig = px.line(timeseries_data,
                    x = "Date",
                    y = graph_selection,
                    labels={"Date":"Date", graph_selection: graph_name},
                    )
    
    #updating the style of hoverlabel to make it look better
    fig.update_traces(hovertemplate = graph_name + " = %{y} <br> Date: %{x}")
    
    #chaning the position of the maximum and minimum labels on the time series graph,
    #in the cases where they exist at the extreme ends, and would be otherwise invisible
    #as they would be rendered outside of the graph, which we cannot see 
    
    #converting the dates where the maximum and minimum values occur for each graph, for the 1st time, to 'datetime' objects.
    #This way we can extract the month, and day of each maximum and minimum reading for each graph
    maximum = dt.datetime.strptime(data['Date'][max_ind[0]], "%Y-%m-%d %H:%M:%S")
    minimum = dt.datetime.strptime(data['Date'][min_ind[0]], "%Y-%m-%d %H:%M:%S")
    
    #default positions for the locations of the maximum and minimum labels
    pos_max = "top center"
    pos_min = "bottom center"
    
    #for the label of the maximum reading
    if month == 20:
        if maximum.month == 1:
            pos_max = 'top right'
        elif maximum.month == 12:
            pos_max = 'top left'
    elif month != 20:
        if maximum.day < 3:
            pos_max = 'top right'
        elif maximum.day > 28:
            pos_max = 'top left'
            
    #for the label of the minimum reading
    if month == 20:
        if minimum.month == 1:
            pos_min = 'bottom right'
        elif minimum.month == 12:
            pos_min = 'bottom left'
    elif month != 20:
        if minimum.day < 3:
            pos_min = 'bottom right'
        elif minimum.day > 28:
            pos_min = 'bottom left'
    
    #adding point for the maximum of the given graph
    fig.add_hline(y=max(data[graph_selection]), line_width=0.8, line_dash="dash", line_color="red")
    fig.add_trace(go.Scatter(x = data["Date"][max_ind], y = data[graph_selection][max_ind], mode="markers+text", hovertemplate = "[MAX.] " + graph_name + " = %{y} <br> Date: %{x}", name= "", text=[(data[graph_selection][max_ind]).to_string()[-6:] + symbol], textposition=pos_max, marker = dict(size = 10), textfont_color= 'Red'))
    
    #adding point for the minimum of the given graph
    fig.add_hline(y=min(data[graph_selection]), line_width=1, line_dash="dash", line_color="green")
    fig.add_trace(go.Scatter(x = data["Date"][min_ind], y = data[graph_selection][min_ind], mode="markers+text", hovertemplate = "[MIN.] " + graph_name + " = %{y} <br> Date: %{x}", name= "", text=[(data[graph_selection][min_ind]).to_string()[-6:] + symbol], textposition=pos_min, marker = dict(size = 10), textfont_color= 'Green'))
    
    #adding point for the average of the given graph
    fig.add_hline(y=np.average(data[graph_selection]), line_width=1, line_dash="dash", line_color="white", showlegend = True, name = "Average = "+ str(round(np.average(data[graph_selection]), 1)) + symbol)
    
    #updating the layout of the plot for stylistic reasons
    fig.update_layout({"plot_bgcolor": colors['background'], 'paper_bgcolor': "rgba(0,0,0,0)"},
                      #setting the title of the graph, as well as making it bold, and writting the graph name in red to match the variable of interest selection
                      title_text="Hourly Evolution: <span style='color:yellow'>" + "<b>" + graph_name +"</b>" + "</span>",
                      title={'x':0.5, 'y':0.98, 'xanchor':'center', 'yanchor':'top','font':{'size':30}},
                      autosize=True,
                      yaxis_ticksuffix=symbol,
                      xaxis=dict(showgrid=False, tickfont=dict(size=14), automargin=True, fixedrange = True),
                      xaxis_range=[timeseries_data['Date'].iloc[0], timeseries_data['Date'].iloc[-1]],
                      yaxis=dict(title='', showgrid=False, zeroline = False, tickmode = 'linear', dtick = ticks, fixedrange = True),
                      title_font_color = colors['text'],
                      font_color = colors['text'],
                      showlegend = False,
                      font=dict(size=14),
                      hoverlabel = {'bgcolor': colors['background'], 'font_family':"Times New Roman", 'font_size':18},
                      )
    
    
    
    #reformating the x-axis to make it look better
    if month == 20:    
        fig.update_xaxes(nticks = 13, tickangle=45, ticklabelposition='outside right')
    elif month != 20:
        fig.update_xaxes(nticks = 31, tickangle=45, ticklabelposition='outside right')
    
    #chaning the color to blue
    fig['data'][0]['line']['color']='rgb(44,111,187)' 
    
    #grouping weather condition data
    
    #getting frequency of relevant weather conditions as percentage of total data for the given time period
    weather_conditions_FULL = round(100*data.Weather.value_counts()/len(data["Weather"]), 2)
    
    #defining variable for frequency of weather conditions
    frequency = []
    
    #computing frequency of weather conditions
    for i in range(len(weather_conditions_FULL)):
        frequency.append(weather_conditions_FULL[i])
    
    #outputting the weather conditions descriptions
    conditions = weather_conditions_FULL.index.to_list()
    
    #defining the list of wather conditions we want to map to the x-axis of the bar chart
    wanted_conditions = ['Clear-OR-Cloudy', 'Rain', 'Thunderstorm', 'Snow', 'Freezing-Rain', 'Fog-OR-Haze']
    
    #telling python to include weather conditions on the x-axis of the bar chart even if they did not occur during the selected timeframe
    for i in range(len(wanted_conditions)):
        if wanted_conditions[i] not in conditions:
            conditions.append(wanted_conditions[i])
    
    #telling python to assign a value of 0% frequency of occurance to the conditions which did not appear during the selected time frame
    if len(frequency) != 6:
        for i in range(0, abs(len(frequency)-6)):
            frequency.append(0.0)
    elif len(frequency) == 6:
        frequency = frequency
    
    #creating bar graph of frequency of recorded weather conditions over the specified period
    fig1 = px.bar(x = conditions, y = frequency, labels = {'x':''},
                  text = [str(frequency[0]) + "%", str(frequency[1]) + "%", str(frequency[2]) + "%", str(frequency[3]) + "%", str(frequency[4]) + "%", str(frequency[5]) + "%"]
                  )
    
    #editing the layout of the bargraph    
    fig1.update_layout({"plot_bgcolor": colors['background'], 'paper_bgcolor': "rgba(0,0,0,0)"},
                      title={'text':"Weather Conditions - Hourly Distribution:", 'x':0.5, 'y':0.925, 'xanchor':'center', 'yanchor':'top','font':{'size':33}},
                      hovermode = False,
                      autosize = True,
                      xaxis = dict(showgrid=False, visible = True, tickfont=dict(size=13), fixedrange = True),
                      yaxis = dict(showgrid=False, visible = False, fixedrange = True),
                      yaxis_range = [0,120],
                      title_font_color = colors['text'],
                      font=dict(color=colors["text"], size = 20)
                      )
    
    #define variable for the url
    url = ""
    
    #adding images to bargraph
    for x, y in zip(conditions, frequency):
        url = r"https://raw.githubusercontent.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard/main/Bargraph%20Icons/" + x + ".png"
        fig1.add_layout_image(
            dict(
                source = Image.open(requests.get(url, stream = True).raw),
                x = x,
                y = y+30,
                xref = "x",
                yref = "y",
                sizex=20,
                sizey=20,
                layer = 'above',
                xanchor = "center",
                yanchor = "top"
                )
            )
        
    #placing the percentage frequency of occurance of weather conditions above each of the bars of the barchart
    fig1.update_traces(textposition='outside', marker_color = 'rgb(44,111,187)')
    
    #reducing the width of the bars for asthetic purposes
    fig1['data'][0].width = 0.5
    
    #defining list of wanted colors fwhen highlighting the attributes of the selected variable
    table_background_color = 'white'
    max_color='red'
    min_color='#30b05a'
    average_color='black'
    category_color='rgb(44,111,187)' 
    
    #creating a table object from the previous dataframe
    table = dash_table.DataTable(id='datatable',
                                 data=df1.to_dict('records'),
                                 columns=[{'name': col, 'id': col} for col in df1.columns],
                                 style_table={'maxHeight': '300px', 'maxWidth':'1600px', 'overflowX': 'auto', 'overflowY': 'auto'},
                                 style_cell={'textAlign': 'left', 'height':'30px', 'fontSize':'19px'},
                                 style_data={'color': colors['text'],'backgroundColor': colors['background'], 'font-weight': 'bold'},
                                 style_header={'color': colors['text'],'backgroundColor': colors['background'], 'fontWeight': 'bold'},
                                 style_data_conditional=[{'if' : {"row_index":table_index, "column_id":"Maximum"}, 'backgroundColor':table_background_color, 'color':max_color},
                                                          {'if' : {"row_index":table_index, "column_id":"Minimum"}, 'backgroundColor':table_background_color, 'color':min_color},
                                                          {'if' : {"row_index":table_index, "column_id":"Average"}, 'backgroundColor':table_background_color, 'color':average_color},
                                                          {'if' : {"row_index":table_index, "column_id":"Category"}, 'backgroundColor':table_background_color, 'color':'black'},
                                                          {"if": {"state": "selected"}, "backgroundColor": "inherit !important", "border": "inherit !important"}
                                                          ]
                                 )
    
    #outputting the graphs, and selected values into the application
    return year, month, fig, table, fig1


#running the application in a new tab every time the code is executed
webbrowser.open_new('http://127.0.0.1:8050')

#run the app once code is executed
if __name__ == '__main__':
    app.run_server(debug=False, use_reloader=False)
