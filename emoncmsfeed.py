" Fonctions pour télécharger les données depuis EmonCMS - Open Energy Monitor "


import numpy as np
import pandas as pd
import datetime as dt

import requests


emoncms_key = 'f4b65fcf3f3f28c9af1d86bf362e7e5e'
emoncms_ip = '192.168.0.100'
DATAREQUESTLIMIT = 8928



def getfeedmeta( feed_id ):
    """ Get feed meta:
        interval, n points, start_time
    """ 
    query = 'http://%s/emoncms/feed/getmeta.json?id=%i&apikey=%s' \
            % (emoncms_ip, feed_id, emoncms_key  )
    r = requests.get(query)
    return r.json() 
    
    
    
def getfeeddata(feed_id, startdate=None, enddate=None, interval=None ):
    """ Get feed data
        startdate, enddate: pandas datetime
        interval: seconds
    """
    
    if not startdate:
        meta = getfeedmeta( feed_id )
        feed_interval = meta['interval']
        
        # Compute interval for full data range:
        start_unix = meta['start_time']*1000
        end_unix = int( dt.datetime.now().timestamp()*1000 )
        dt_range = (end_unix - start_unix)/1000
        interval = int( np.ceil( dt_range/DATAREQUESTLIMIT / feed_interval )*feed_interval )
    else:
        start_unix = int( startdate.timestamp() )*1000  # feed in milliseconds
        end_unix = int( enddate.timestamp() )*1000

    query = 'http://%s/emoncms/feed/data.json?id=%i&start=%i&end=%i&interval=%i&apikey=%s' \
            % (emoncms_ip, feed_id, start_unix, end_unix, interval,  emoncms_key  )

    r = requests.get(query)
    data = r.json()

    return data
    
    
def getTimeserie( feed_id, feed_name, dataframefreq, **timerangeparams  ):
    """ Pack data from emoncms into a Dataframe
        feed_name: column name
        dataframefreq: string, resample freq, averaging
    """
    
    data = getfeeddata( feed_id, **timerangeparams )
    Mesures = [ v[1] for v in data ]
    DateIndex = pd.to_datetime( [ v[0] for v in data ],  unit='ms' , origin='unix'  )
    
    df = pd.DataFrame( {feed_name:Mesures}, index=DateIndex )
    df = df.resample(dataframefreq).mean().interpolate()

    return df
    
    
def builddataframe(feeds, dataframefreq, **timerangeparams ):
    """ Obtient les données de plusieurs feeds, et créer un unique dataframe
        feeds =  { 'T_ext':2, 'T_int':3 }
    """
    
    D = []
    for  feed_name, feed_id in feeds.items():
        D.append( getTimeserie( feed_id, feed_name, dataframefreq , **timerangeparams  )  )

    df = pd.concat( D, axis=1)
    
    return df
    


