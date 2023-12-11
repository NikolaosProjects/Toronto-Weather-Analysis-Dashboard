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
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc

import plotly.figure_factory as ff




###############################################################################
###                    DATA CLEANING AND PREPARATION                        ###
###############################################################################




#importing excel (.csv) datasets as pandas Data Frames. 4 datasets, one for each year.
d17 = pd.DataFrame(pd.read_csv(r"https://raw.githubusercontent.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard/main/Dataset/YEARLY/2017%20Weather.csv"))
d18 = pd.DataFrame(pd.read_csv(r"https://raw.githubusercontent.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard/main/Dataset/YEARLY/2018%20Weather.csv"))
d19 = pd.DataFrame(pd.read_csv(r"https://raw.githubusercontent.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard/main/Dataset/YEARLY/2019%20Weather.csv"))
d20 = pd.DataFrame(pd.read_csv(r"https://raw.githubusercontent.com/NikolaosProjects/Toronto-Weather-Analysis-Dashboard/main/Dataset/YEARLY/2020%20Weather.csv"))

#creating empty list which will contain the indices of the rows that
#contain missing values

missing_values_indices17 = []
missing_values_indices18 = []
missing_values_indices19 = []
missing_values_indices20 = []

#scanning through the weather data for each year in order to extract the indices of the rows which contain missing values

#2017
for i in range(len(d17.loc[:, 'Is Row Missing Value'])):
    if d17.loc[i, 'Is Row Missing Value'] == 'MISSING VALUE':
        missing_values_indices17.append(i)

#2018
for i in range(len(d18.loc[:, 'Is Row Missing Value'])):
    if d18.loc[i, 'Is Row Missing Value'] == 'MISSING VALUE':
        missing_values_indices18.append(i)
     
#2019
for i in range(len(d19.loc[:, 'Is Row Missing Value'])):
    if d19.loc[i, 'Is Row Missing Value'] == 'MISSING VALUE':
        missing_values_indices19.append(i)
     
#2020
for i in range(len(d20.loc[:, 'Is Row Missing Value'])):
    if d20.loc[i, 'Is Row Missing Value'] == 'MISSING VALUE':
        missing_values_indices20.append(i)
        

#creating arrays containing the amount of times values were missing for each month 
#(each time a value was missing for a month, the month number is recorded into the array.
#[1,1] means 2 values are missing from January)

#2017
mvpm2017 = np.array(d17.loc[missing_values_indices17, 'Month'])

#2018
mvpm2018 = np.array(d18.loc[missing_values_indices18, 'Month'])

#2019
mvpm2019 = np.array(d19.loc[missing_values_indices19, 'Month'])

#2020
mvpm2020 = np.array(d20.loc[missing_values_indices20, 'Month'])


#plotting the distribution of missing values per month for all the years


#2017
plt.figure(figsize=(11.5,11.5))
plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

ax = plt.subplot(2, 2, 1)
plt.title("2017: Proportions of missing values per month \n (" + str(d17.iloc[0, 15]) + "% of the 2017 Data is Missing)")
labels, counts = np.unique(mvpm2017, return_counts = True)
plt.bar(labels, (counts/sum(counts))*100, align = 'center', color = 'Green')
plt.xticks(labels, ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"])
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xlabel("Month")
plt.ylabel("% of Missing Values per Month")

#2018
ax = plt.subplot(2, 2, 2)
plt.title("2018: Proportions of missing values per month \n (" + str(d18.iloc[0, 15]) + "% of the 2018 Data is Missing)")
labels, counts = np.unique(mvpm2018, return_counts = True)
plt.bar(labels, (counts/sum(counts))*100, align = 'center', color = 'Green')
plt.xticks(labels, ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"])
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xlabel("Month")
plt.ylabel("% of Missing Values per Month")

#2019
ax = plt.subplot(2, 2, 3)
plt.title("2019: Proportions of missing values per month \n (" + str(d19.iloc[0, 15]) + "% of the 2019 Data is Missing)")
labels, counts = np.unique(mvpm2019, return_counts = True)
plt.bar(labels, (counts/sum(counts))*100, align = 'center', color = 'Green')
plt.xticks(labels, ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"])
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xlabel("Month")
plt.ylabel("% of Missing Values per Month")

#2020
ax = plt.subplot(2, 2, 4)
plt.title("2020: Proportions of missing values per month \n (" + str(d20.iloc[0, 15]) + "% of the 2020 Data is Missing)")
labels, counts = np.unique(mvpm2020, return_counts = True)
plt.bar(labels, (counts/sum(counts))*100, align = 'center', color = 'Green')
plt.xticks(labels, ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"])
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xlabel("Month")
plt.ylabel("% of Missing Values per Month")
plt.show()

#removing missing and unwanted data from the datasets and rearanginng the indices for the clean dataset

#2017
d17 = d17.drop(missing_values_indices17, axis = 0, inplace=False).reset_index() #missing
data2017 = d17.drop(['% Of Dataset That Contains Missing Values', 'Is Row Missing Value', 'index'], axis = 1) #unwanted

#2018
d18 = d18.drop(missing_values_indices18, axis = 0, inplace=False).reset_index() #missing
data2018 = d18.drop(['% Of Dataset That Contains Missing Values', 'Is Row Missing Value', 'index'], axis = 1) #unwanted

#2019
d19 = d19.drop(missing_values_indices19, axis = 0, inplace=False).reset_index() #missing
data2019 = d19.drop(['% Of Dataset That Contains Missing Values', 'Is Row Missing Value', 'index'], axis = 1) #unwanted

#2020
d20 = d20.drop(missing_values_indices20, axis = 0, inplace=False).reset_index() #missing
data2020 = d20.drop(['% Of Dataset That Contains Missing Values', 'Is Row Missing Value', 'index'], axis = 1) #unwanted



#creating empty list which will contain the dates in date format for each of the dataset
date_data2017 = []
date_data2018 = []
date_data2019 = []
date_data2020 = []

#date format for 2017
for i in range(len(data2017.loc[:, "Temp (°C)"])):
    date_data2017.append(dt.datetime(data2017.loc[i, "Year"], data2017.loc[i, "Month"], data2017.loc[i, "Day"], 
                         int(str(data2017.loc[i, "Time"][0:2])),
                         int(str(data2017.loc[i, "Time"][3:5])),
                         int(str(data2017.loc[i, "Time"][6:]))))

#adding column of date format to 2017 data
data2017['Date'] = date_data2017

#date format for 2018
for i in range(len(data2018.loc[:, "Temp (°C)"])):
    date_data2018.append(dt.datetime(data2018.loc[i, "Year"], data2018.loc[i, "Month"], data2018.loc[i, "Day"],
                         int(str(data2018.loc[i, "Time"][0:2])),
                         int(str(data2018.loc[i, "Time"][3:5])),
                         int(str(data2018.loc[i, "Time"][6:]))))

#adding column of date format to 2018 data
data2018['Date'] = date_data2018


#date format for 2019
for i in range(len(data2019.loc[:, "Temp (°C)"])):
    date_data2019.append(dt.datetime(int(data2019.loc[i, "Year"]), int(data2019.loc[i, "Month"]), int(data2019.loc[i, "Day"]),
                         int(str(data2019.loc[i, "Time"][0:2])),
                         int(str(data2019.loc[i, "Time"][3:5])),
                         int(str(data2019.loc[i, "Time"][6:]))))

#adding column of date format to 2019 data
data2019['Date'] = date_data2019


#date format for 2020
for i in range(len(data2020.loc[:, "Temp (°C)"])):
    date_data2020.append(dt.datetime(data2020.loc[i, "Year"], data2020.loc[i, "Month"], data2020.loc[i, "Day"],
                         int(str(data2020.loc[i, "Time"][0:2])),
                         int(str(data2020.loc[i, "Time"][3:5])),
                         int(str(data2020.loc[i, "Time"][6:]))))

#adding column of date format to 2020 data
data2020['Date'] = date_data2020


#merging data into one dataset
full = pd.concat([data2017, data2018, data2019, data2020], ignore_index=True)


for i in range(len(full['Weather'])):
    if full['Weather'][i] == 'Thunderstorms' or full['Weather'][i] == 'Thunderstorms,Fog' or full['Weather'][i] == 'Thunderstorms,Heavy Rain' or full['Weather'][i] == 'Thunderstorms,Heavy Rain,Fog' or full['Weather'][i] == 'Thunderstorms,Moderate Rain' or full['Weather'][i] == 'Thunderstorms,Moderate Rain,Fog' or full['Weather'][i] == 'Thunderstorms,Rain' or full['Weather'][i] == 'Thunderstorms,Rain,Fog':
        full['Weather'][i] = 'Thunderstorm'
    elif full['Weather'][i] == 'No Precipitation or Fog':
        full['Weather'][i] = 'Clear-OR-Cloudy'
    elif full['Weather'][i] == 'Rain' or full['Weather'][i] == 'Heavy Rain,Fog' or full['Weather'][i] == 'Moderate Rain' or full['Weather'][i] == 'Moderate Rain,Fog' or full['Weather'][i] == 'Rain,Fog':
        full['Weather'][i] = 'Rain'
    elif full['Weather'][i] == 'Rain,Snow' or full['Weather'][i] == 'Snow' or full['Weather'][i] == 'Moderate Snow' or full['Weather'][i] == 'Heavy Snow' or full['Weather'][i] == 'Snow,Blowing Snow':
        full['Weather'][i] = 'Snow'
    elif full['Weather'][i] == 'Freezing Rain' or full['Weather'][i] == 'Freezing Rain,Fog' or full['Weather'][i] == 'Freezing Rain,Snow':
        full['Weather'][i] = 'Freezing-Rain'
    elif full['Weather'][i] == 'Fog' or full['Weather'][i] == 'Haze' or full['Weather'][i] == 'Haze,Blowing Snow':
        full['Weather'][i] = 'Fog-OR-Haze'

full.to_csv(r"C:\Users\nick-\OneDrive\Desktop\Cleaned Dataset.csv")
