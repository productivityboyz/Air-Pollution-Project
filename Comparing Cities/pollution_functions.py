# getdata function
import pandas as pd
import numpy as np

def getdata(*urls):
	import pandas as pd
	for i in urls:
   		yield pd.read_csv(i,skiprows=4)

def cleaner(df):
    '''Takes Pandas DataFrame and sets Date to DateTime, 
    replaces date x : 24:00 hours to data x +1 00:00 hours,
    creates new columns i.e. day of the week, month, quarter,
    drops unneccesary columns i.e. unit.9, unit.8, status.9, status.8 etc'''
    # Changing date from object to datetime
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%d-%m-%Y') # makes sure string is in correct format
    df['Date'] = pd.to_datetime(df['Date']) # converts to datetime
    
    # Loop to add 1 to date for every 24th entry, as they are stored as date x & 24:00 when they need to be date x + 1 & 00:00
    # Potentially a very inefficient way to do it
    counter = 0
    for i, row in df.iterrows():
        counter += 1
        if counter % 24 == 0:
            value = df.at[i,'Date'] + pd.Timedelta(1,unit='d')
            df.at[i,'Date'] = value
    
    # Replacing 24:00 with 00:00
    df['time'] = df['time'].replace(to_replace='24:00',value='00:00') 
    
    # Combining date and time columns
    df['Date String'] = df['Date'].astype(str)
    df['Date Time String'] = df['Date String'] + " " + df['time']
    df['Date Time'] = pd.to_datetime(df['Date Time String'])
    
    # Feature Engineering
    df['Week'] = df['Date Time'].dt.week
    df['Day Of Week'] = df['Date Time'].dt.dayofweek
    df['Quarter'] = df['Date Time'].dt.quarter
    df['Month'] = df['Date Time'].dt.month
    df['Weekday Or Weekend'] = np.where(df['Day Of Week'] >=5,'Weekend','Weekday')
    df['NO + NO2'] = df['Nitric oxide'] + df['Nitrogen dioxide']
    
    # Setting index to be Date Time
    df.index = df['Date Time']
    
    # dropping columns if they exist
    to_drop = ['unit.10','unit.9','unit.8','unit.7','unit.6','unit.5','unit.4','unit.3','unit.2','unit.1','unit',
              'status.10','status.9','status.8','status.7','status.6','status.5','status.4','status.3','status.2','status.1','status',
              'Date','time','Date String','Date Time String']
    for i in to_drop:
        try:
            df.drop(i,axis=1,inplace=True)
        except:
            continue