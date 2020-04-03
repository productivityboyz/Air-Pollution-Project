#import the necessary functions for the program
from urllib.request import urlretrieve
import pandas as pd
import datetime
import matplotlib.pyplot as plt
plt.style.use('seaborn')

#defines a function to load in the data, fix the datetimes and set this as the new index
def clean_data(URL):
    urlretrieve(URL,'file')
    data = pd.read_csv('file',skiprows=4)
    data['time'] = data['time'].replace({'24:00':'00:00'})
    data['Datetime'] = pd.to_datetime(data['Date'] + ' ' + data['time'],dayfirst=True)
    for x in data.index:
        if data.iloc[x]['Datetime'].strftime("%H:%M") == "00:00":
            y = data.iloc[x]['Datetime'] + datetime.timedelta(days=1)
            data.at[x,'Datetime'] = y
    data.set_index('Datetime', inplace=True)
    return data
