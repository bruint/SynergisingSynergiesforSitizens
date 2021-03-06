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
import itertools

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
INPUT_PATH = r'C:\Users\dahunt\Dropbox\GovHack (1)\Raw Data\local-structures-plans.json'
OUT_PATH = ROOT_PATH + r'\PHP Scraper\PLANNING_DATA_BY_POLYGON.csv'

HAS_PROPERTIES = True

LAT = 0
LONG = 1

# file to redirect log data to
LOG_PATH = ROOT_PATH + r'\log.txt'

PROPERTY_LIST = ['pub_title','pub_dwell_','est_dwell_','pub_lot_yi','est_lot_yi','shape_area']
HEADER_LIST = ['int_id','pub_title','pub_dwell_','est_dwell_','pub_lot_yi','est_lot_yi','shape_area','polygon']

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
    # data = []
    polyStr = 'POLYGON(('
    for coord in polygon:
        polyStr = polyStr + str(coord[LAT]) + ' ' + str(coord[LONG]) + ','
    polyStr = polyStr[:-1] + '))'

    # print(polyStr)

    if '[' in polyStr:
        polyStr = polyStr.replace('[','')
        polyStr = polyStr.replace(',','')
        polyStr = polyStr.replace('\'','')
        polyStr = polyStr.replace(']',',')
        polyStr = polyStr[:-3] + '))'

    # data.append(polyStr)

    return polyStr

def getPolygonList(shapes):
    shapeList = []
    if str(type(shapes)) == '<class \'shapely.geometry.multipolygon.MultiPolygon\'>':
        for s in shapes.geom:
            shapeList.append(s)
    else:
        shapeList = [shapes]
    return shapeList


def run(inputPath,outputPath):
    print('Starting extract process with output at: \n')
    print(outputPath)

    outData = []

    with open(inputPath,'r') as fIn:

        jData = json.load(fIn)

        row = []
        int_id = 0
        # outer dict contains either 'properties' or 'polygon'
        for i in range(len(jData)):
            if i % 2 == 0 and HAS_PROPERTIES:
                properties = jData[i]['properties']
                row = getProperties(properties)
            else:
                polygonList = jData[i]['geometry']['coordinates']
                for polygon in polygonList:
                    temp = list(itertools.chain([int_id],row[:]))
                    temp.append(getPolygon(polygon))
                    outData.append(temp)
                    int_id = int_id + 1



    with open(outputPath,'w',newline='') as fOut:
        writer = csv.writer(fOut,delimiter='|',quoting=csv.QUOTE_MINIMAL,escapechar='\"')
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
