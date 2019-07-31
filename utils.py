# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import time
import math

#Pandas pivot func
def write_csv(df,file_type,folder):
    DATE_TIME =(time.strftime("%d-%m-%Y"))
    output_file = folder + file_type + "_"  + DATE_TIME + ".csv"
    df.to_csv(output_file, sep=";", encoding="utf-8")
    print (" --- Export to csv file:" + output_file)

#Pandas pivot func
def pivot_gen(df, index_row, value, func):
    pivot = pd.pivot_table(df,index=index_row,values=value,
                         aggfunc=func)
    pivot = pivot.reset_index()
    return pivot

#Pivot simple func
def size(x):
    return len(x)

def nan_size(x):
    return np.count_nonzero(x)

def per25(g):
    return np.percentile(g, 25)

def per50(g):
    return np.percentile(g, 50)

def per75(g):
    return np.percentile(g, 75)

def per95(g):
    return np.percentile(g, 95)

#Find midpoint between 2 Geolocation
#Input values as degrees
#Convert to radians
def midpoint(x1, y1, x2, y2):

    lat1 = math.radians(x1)
    lon1 = math.radians(x2)
    lat2 = math.radians(y1)
    lon2 = math.radians(y2)

    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), \
           math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) \
           + bx) + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + bx)

    return [round(math.degrees(lat3), 2), round(math.degrees(lon3), 2)]

def assign_term(x):
    if x.__contains__('LB'):
        return 'LE BOULOU'
    elif x.__contains__('CAL'):
        return 'CALAIS'
    elif x.__contains__('BTG'):
        return 'BETTEMBOURG'
    elif x.__contains__('PPN'):
        return 'PERPIGNAN'
    elif x.__contains__('MAC'):
        return 'MACON'
    elif x.__contains__('BCN'):
        return 'BARCELONA'
    elif x.__contains__('ORB'):
        return 'ORBASSANO'
    else:
        return 'AUTRE'

colors_ligne = {
'LB-BTG': '#2b7518',
'BTG-LB': '#2b7518',
'PPN-BTG' : '#333F44',
'BTG-PPN': '#333F44',
'BTG-BCN': '#89dd44',
'BCN-BTG': '#89dd44',
'BTG-SETE': '#8224e3',
'SETE-BTG': '#8224e3',
'CAL-LB': '#e32a8a',
'LB-CAL': '#e32a8a',
'CAL-ORBA': '#ed4725',
'ORBA - CAL': '#ed4725',
'CAL-MAC': '#26d0e2',
'MAC - CAL': '#26d0e2',
'LBP - MAC': '#ead835',
'MAC - LBP': '#ead835'}


colors = {'1': 'blue',
        '2': 'lightblue',
        '3': 'lightgreen',
        '4': 'darkgreen',
        '5': 'purple',
        '6': 'mediumpurple',
        '7' : 'salmon',
        '8': 'lightsalmon',
        '9': 'chocolate',
        '10': 'beige',
        '11': 'darkturquoise',
        '12': 'turquoise',
        '13': 'purple',
        '14': 'mediumpurple',
        '15': 'lightgoldenrodyellow',
        '16': 'gold'}