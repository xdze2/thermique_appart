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
    
    meta = getfeedmeta( feed_id )
    feed_interval = meta['interval'] 
    
     
    if not startdate:  # then take feed start date
        start_unix = meta['start_time']*1000
    else:
        start_unix = int( startdate.timestamp() )*1000  # feed in milliseconds
        
        
    if not enddate: # then take now
        end_unix = int( dt.datetime.now().timestamp()*1000 )
    else:
        end_unix = int( enddate.timestamp() )*1000
        
    # Compute interval for full data range:
    dt_range = (end_unix - start_unix)/1000
    interval_min = int( np.ceil( dt_range/DATAREQUESTLIMIT / feed_interval )*feed_interval )
    
    interval = max( interval_min, feed_interval )  
        
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
    
    # Remove outliers
    mask = np.abs( df[feed_name]-df[feed_name].mean() ) > 4*df[feed_name].std()
    df[feed_name].loc[ mask ] = np.nan
    
    # Resample
    df = df.resample(dataframefreq).mean()

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
    



## Quels sont les intervals réels ?

#data = getfeeds.getfeeddata( 3 )
#intervals = np.array( [ (data[k+1][0]-data[k][0] )/1000 for k in range(len(data)-1)  ] )
#plt.plot( intervals, ',' ); plt.ylabel('intervals (seconde)')
#np.unique(intervals,  return_counts=True )

