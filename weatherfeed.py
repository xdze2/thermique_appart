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
    key = f.read()
    
    
    
# voir https://darksky.net/dev/docs/response
datalabels = ['temperature', 'cloudCover', 'precipIntensity', 'windSpeed' , 'windBearing',      
            'apparentTemperature']




def buildDFdaily(day, coords):
    """ Construit un dataframe avec les données selectionnées (datalabels), pour un jour particulier
        day: isoformat  ex: '2017-06-23T00:00:00'
        coords: GPS 
    """
    
    data = forecast(key, *coords, units='si', lang='fr', time=day)
    
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

    D = []
    for day in daterange:
        day_iso = day.isoformat()
        D.append(  buildDFdaily(day_iso, coords)  )
    
    allweatherdata = pd.concat(D, axis=0)
    return allweatherdata   
    
    
    
