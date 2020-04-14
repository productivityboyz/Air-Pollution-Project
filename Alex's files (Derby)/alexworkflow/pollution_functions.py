# function to let you decide date range to plot, resample type, line or bar, and aggregate type
def date_range_plotter(df,start,end,resample_string,plottype,aggregate,cols,location_string):
    
    from datetime import datetime
    import datetime as dt
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    '''
    Keyword arguments:
    df -- df to use. Will probably always be df_all
    start -- date string in format YYYY-MM-DD
    end -- date string in format YYYY-MM-DD
    resample_string -- string of 'H'/'D'/'W'/'M'
    plottype -- string 'line' or 'bar'
    aggregate -- string 'sum','average','median'
    cols -- if 1, plot total. If 2, plot NO and NO2. If 3, plot total & NO & NO2. If 4, just NO. If 5, just NO2.
    location_string -- string of location, so the title changes
    '''
    # Capitalise user input (in case user were to input 'h' instead of 'H')
    resample_string = resample_string.upper()
    
    # For chart title 
    if resample_string == 'H':
        title_string = 'Hourly'
    elif resample_string == 'D':
        title_string = 'Daily'
    elif resample_string == 'W':
        title_string = 'Weekly'
    elif resample_string == 'M':
        title_string = 'Monthly'
        
    # Data to plot (from 'cols' parameter)
    if cols == 1:
        data_to_plot = ['Total']
    elif cols == 2:
        data_to_plot = ['Nitric oxide', 'Nitrogen dioxide']
    elif cols == 3:
        data_to_plot = ['Total', 'Nitric oxide', 'Nitrogen dioxide']
    elif cols == 4:
        data_to_plot = ['Nitric oxide']
    elif cols == 5:
        data_to_plot = ['Nitrogen dioxide']
    
    # Dates to plot. Convert inputted string to datetime object with strptime
    start = datetime.strptime(start,'%Y-%m-%d')
    end = datetime.strptime(end,'%Y-%m-%d')
    
    # Plot styling
    plt.style.use('seaborn-poster')
    
    # Resampling data based on user input
    if resample_string == 'H':
        df_ = df.loc[start:end]
        if plottype == 'line':
            fig = df_[data_to_plot].plot(figsize=(15,10))
        elif plottype == 'bar':
            fig = df_[data_to_plot].plot.bar(figsize=(15,10))
        fig.set_title('Hourly Emissions Between {} and {}'.format(start,end))
        fig.set_ylim(0)
    else:    
        df_ = df.loc[start:end]
        if plottype == 'line':
            if aggregate == 'sum':
                fig = df_[data_to_plot].resample(resample_string).sum().plot(figsize=(15,10))
            elif aggregate == 'mean':
                fig = df_[data_to_plot].resample(resample_string).mean().plot(figsize=(15,10))
            elif aggregate == 'median': 
                fig = df_[data_to_plot].resample(resample_string).median().plot(figsize=(15,10))
            fig.set_title('{} {} Emissions Between {} and {} for {}'.format(aggregate.title(),title_string,start,end,location_string))
            fig.set_ylim(0)
        elif plottype == 'bar':
            if aggregate == 'sum':
                fig = df[data_to_plot].resample(resample_string).sum().plot.bar(figsize=(15,10))
            elif aggregate == 'mean':
                fig = df[data_to_plot].resample(resample_string).mean().plot.bar(figsize=(15,10))
            elif aggregate == 'median':
                fig = df[data_to_plot].resample(resample_string).median().plot.bar(figsize=(15,10))
            fig.set_title('{} {} Emissions Between {} and {} for {}'.
                          format(aggregate.title(),title_string,start,end,location_string))
            fig.set_ylim(0)
    
    # Stylings
    fig.set_ylim(0,None)
    fig.set_facecolor('#eaeaf2')
    fig.grid(True,color='w',axis='y')
    plt.ylabel('Total Emissions Measured (ugm$^3$)')
    plt.legend(loc='upper center')
    plt.xlabel('')