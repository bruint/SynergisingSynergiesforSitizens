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
INPUT_PATH = r'C:\Users\dahunt\Downloads\building-polygon.json'
OUT_PATH = ROOT_PATH + r'\suburbs_simplified.csv'


LAT = 0
LONG = 1

# file to redirect log data to
LOG_PATH = ROOT_PATH + r'\log.txt'


# hacky workaround to read in large CSV without overflowing C long
maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True

#=================
#  MAIN FUNCTIONS
#=================
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

# def getCoords(inStr):
#     print(inStr)
#     return

def getPolygon(polygon,suburbs,s):
    data = []

    polyStr = 'POLYGON(('
    for coord in polygon:
        polyStr = polyStr + str(coord[LAT]) + ' ' + str(coord[LONG]) + ','
    polyStr = polyStr[:-1] + '))'
    if d: print('Checking polygon:' + str(s))

    data.append(polyStr)

    for row in suburbs:
        if row[0].contains(s):
            if d: print('Checking suburb:' + str(row[1]))
            data.append(row[1])
            break

    return data

def getSuburbShapes():
    csv.field_size_limit(maxInt)
    outData = []
    with open(SUBURB_FILE,'r') as fIn:
        csvReader = csv.reader(fIn,delimiter=',',quotechar='\"')
        next(csvReader)
        for row in csvReader:
            # getCoords(row[0])
            if len(row[0]) > 10000:
                continue
            poly = loads(row[0])
            outData.append([poly,row[7]]) #polygon, suburb name
    return outData

def run(inputPath,outputPath):
    print('Starting extract process with output at: \n')
    print(outputPath)

    outData = []

    suburbs = getSuburbShapes()

    with open(inputPath,'r') as fIn:

        jData = json.load(fIn)

        # outer dict contains either 'properties' or 'polygon'
        for i in range(len(jData)):
            polygonList = jData[i]['geometry']['coordinates']
            for polygon in polygonList:
                s = shape(jData[i]['geometry'])
                x, y = s.exterior.coords.xy
                p = Point(x[0],y[0])
                outData.append(getPolygon(polygon,suburbs,p))


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
