""" Fonctions pour télécharger les données de météo - Darksky
    ## Darksky data

    https://darksky.net/

    Librairie **darkskylib**
    https://github.com/lukaskubis/darkskylib

        pip install darkskylib

"""

import numpy as np
import pandas as pd

from darksky import forecast


# Load the API key for darksky
with open('darksky_key.txt') as f:
    KEY = f.read()
    
    
    
# voir https://darksky.net/dev/docs/response
datalabels = ['temperature', 'cloudCover', 'precipIntensity', 'windSpeed' , 'windBearing',      
            'apparentTemperature', 'humidity']

EXCLUDE = ['currently', 'minutely', 'daily', 'flags']  # from the query

COL2DROP = ['icon', 'apparentTemperature', 'ozone', 'summary', 'uvIndex', 'windGust', 'dewPoint',
               'precipProbability', 'visibility', 'pressure', 'humidity', 'precipType']
               

def buildDFdaily(day, coords):
    """ Construit un dataframe avec les données selectionnées (datalabels), pour un jour particulier
        day: isoformat  ex: '2017-06-23T00:00:00'
        coords: GPS 
    """
    
    data = forecast(KEY, *coords, units='si', lang='fr', time=day)
    
    timeindex = pd.to_datetime( [ hour.time for hour in data.hourly ],  unit='s' , origin='unix' )
    
    dailydata = {}
    for label in datalabels:
        dailydata[label] = [ dataeveryhour[label] for dataeveryhour in data.hourly ]
        
    df = pd.DataFrame(dailydata, index=timeindex )
    return df
    
 
def buildmultidayDF(startday, lastday, coords ):
    """ Concatène plusieurs jours ensemble
        startday, lastday: pandas timestamp
    """

    daterange = pd.date_range(start=startday, end=lastday,  freq='D', normalize=True)

    records = []
    for day in daterange:
        
        day_iso = day.isoformat()
        
        print('%i, '%day.day, end='')
        
        data = forecast(KEY, *coords, units='si', lang='fr', \
             time=day_iso, exclude=EXCLUDE)
        records_oftheday = data['hourly']['data']     
        records.extend( records_oftheday )

    print( 'done' )
    
    # build DF:
    allweatherdata = pd.DataFrame.from_records(records, index='time')
    allweatherdata.drop(COL2DROP, axis=1, inplace=True, errors='ignore')
    
    allweatherdata.index = pd.to_datetime(allweatherdata.index, unit='s')
    
    allweatherdata['cloudCover'] = allweatherdata['cloudCover'].fillna( 0 )

    
    return allweatherdata   
    
    
    
