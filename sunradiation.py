"""  Get the sun position + solar flux
     Projected on a surface
     
"""

import numpy as np
import pandas as pd

import datetime as dt

from numpy import genfromtxt

import math
import pysolar.radiation as radiation
import pysolar.solar as solar


# Profil de l'horizon :
horizon_data = genfromtxt('horizon.csv', delimiter=',').T


def isUpperHorizon( azimuth, altitude_deg ):
    azimuth = -azimuth
    h = np.interp(azimuth, horizon_data[0, :], horizon_data[1, :])

    if h > altitude_deg:
        return 0
    else:
        return 1




    
def get_flux_surface( coords, date, sigma, phi_C ):
    """
    coords: gps deg  (  )
    date: datetime object
    Surface orientation :
    sigma : deg, vertical angle of the surface, ref. to the horizontal
    phi_C : deg, azimuth, relative to south, with positive values
            in the southeast direction and negative values in the southwest
    
    """
    
    # Sun position
    phi_S_deg = solar.get_azimuth( *coords, date ) # deg, azimuth of the sun,relative to south
    beta_deg = solar.get_altitude( *coords, date ) # deg, altitude angle of the sun
    
    I0 = radiation.get_radiation_direct( date, beta_deg )   # W/m2
    I0 = I0* isUpperHorizon( phi_S_deg, beta_deg )
    
    beta = beta_deg*math.pi/180  # rad
    phi_S = phi_S_deg*math.pi/180  #rad
    sigma = sigma*math.pi/180
    phi_C = phi_C*math.pi/180
    
    cosTheta = math.cos(beta)*math.cos( phi_S - phi_C )*math.sin( sigma ) + math.cos( sigma )*math.sin( beta )
    
    if cosTheta >0 :
        Isurf = I0*cosTheta   # flux projeté, W/m2
    else:
        Isurf = 0  # mais diffuse... ?
        
    return Isurf



def get_flux_total( coords, date ):
    # Sun position
    beta_deg = solar.get_altitude( *coords, date ) # deg, altitude angle of the sun
    
    I0 = get_radiation_direct( d, beta_deg )   # W/m2
        
    return I0
