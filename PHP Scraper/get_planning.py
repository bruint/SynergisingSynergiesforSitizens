import sys
import os
import csv
import re
from datetime import datetime as dt
from dateutil import parser
from urllib import request as r
import lxml
from os.path import exists
import json
from shapely.geometry import shape, polygon
from shapely.wkt import loads

#==============
#  HEADER
#==============
__author__ = "Daniel Hunt"
__version__ = "1.0"
__email__ = ["danhunt.90@gmail.com"]
__status__ = "Script for personal use"

#==============
#  FLAGS
#==============

# FLAGS
# verbose
v = True
# v = False

# debug
# d = True
d = False

#==============
#  CONSTANTS
#==============
SEPARATOR = '\n=======================================\n'

ROOT_PATH = r'C:\Users\dahunt\Dropbox\GovHack (1)'
SUBURB_FILE = ROOT_PATH + r'\Raw Data\walocalitypolygon\WA Shape Modified.csv'
INPUT_PATH = r'C:\Users\dahunt\Downloads\local-structure-plans.json'
OUT_PATH = ROOT_PATH + r'\PHP Scraper\HOUSE_DATA_BY_POLYGON.csv'

HAS_PROPERTIES = True

LAT = 0
LONG = 1

# file to redirect log data to
LOG_PATH = ROOT_PATH + r'\log.txt'

PROPERTY_LIST = ['pub_title','adopt_lga','pub_dwell_','est_dwell_','pub_lot_yi','est_lot_yi','shape_area']
HEADER_LIST = PROPERTY_LIST.append('polygon')

#=================
#  MAIN FUNCTIONS
#=================
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

# def getCoords(inStr):
#     print(inStr)
#     return

def getProperties(properties):
    data = []
    for property in PROPERTY_LIST:
        if property in properties:
            data.append(properties[property])
        else:
            data.append('')
    return data

def getPolygon(polygon):
    # get polygon string
    data = []
    polyStr = 'POLYGON(('
    for coord in polygon:
        polyStr = polyStr + str(coord[LAT]) + ' ' + str(coord[LONG]) + ','
    polyStr = polyStr[:-1] + '))'
    data.append(polyStr)

    return data

def run(inputPath,outputPath):
    print('Starting extract process with output at: \n')
    print(outputPath)

    outData = []

    with open(inputPath,'r') as fIn:

        jData = json.load(fIn)

        row = []
        # outer dict contains either 'properties' or 'polygon'
        for i in range(len(jData)):
            if i % 2 == 0 and HAS_PROPERTIES:
                properties = jData[i]['properties']
                row = getProperties(properties)
            else:
                polygonList = jData[i]['geometry']['coordinates']
                for polygon in polygonList:
                    temp = row.append(getPolygon(polygon))
                    outData.append(temp)


    with open(outputPath,'w',newline='') as fOut:
        writer = csv.writer(fOut,delimiter='|',quoting=csv.QUOTE_NONE)
        writer.writerows(outData)

    print('Finished extracting data.')

#========================
# KICK-OFF MAIN FUNCTION
#========================
# clear export file
# if exists(OUT_PATH):
#     os.remove(OUT_PATH)

# pipe print statements to a log file
# orig_stdout = sys.stdout
# f = open(LOG_PATH, 'w')
# sys.stdout = f

# run
run(INPUT_PATH,OUT_PATH)


# sys.stdout = orig_stdout
# f.close()
