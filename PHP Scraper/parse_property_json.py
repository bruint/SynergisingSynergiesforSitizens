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
d = True
# d = False

#==============
#  CONSTANTS
#==============
SEPARATOR = '\n=======================================\n'

ROOT_PATH = r'C:\Users\dahunt\Dropbox\GovHack (1)'
INPUT_PATH = ROOT_PATH + r'\PHP Scraper\features.json'
SUBURB_FILE = ROOT_PATH + r'\Raw Data\walocalitypolygon\WA Shape Modified.csv'
INPUT_PATH_LARGER = r'C:\Users\dahunt\Downloads\building-polygon.json'
OUT_PATH = ROOT_PATH + r'\PHP Scraper\HOUSE_DATA_BY_POLYGON.csv'


LAT = 0
LONG = 1

# file to redirect log data to
LOG_PATH = ROOT_PATH + r'\log.txt'

HEADER = ['FCSUBTYPE','FCSUBTYPE_desc','STYLE_NAME','FULL_NAME','DATEFEATURECREATED','DATEFEATUREMODIFIED','ACCESSLEVEL','METADATAID','FEATURETEXT','NAMEID','GLOBALID','BUILDINGTYPE','BUILDINGTYPE_desc','HEIGHT','CAPTUREMETHOD','CAPTUREMETHOD_desc','DATASOURCE','DATASOURCE_desc','PLANACCURACY','SPATIALRELIABILITYDATE','ATTRIBUTERELIABILITYDATE','TARGETDISPLAYSCALE','TARGETDISPLAYSCALE_desc','DATACUSTODIAN','DATACUSTODIAN_desc','gx_id']

#=================
#  MAIN FUNCTIONS
#=================
def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def getPolygon(polygon):
    polyStr = 'POLYGON(('
    for coord in polygon:
        polyStr = polyStr + str(coord[LAT]) + ' ' + str(coord[LONG]) + ','

    return polyStr[:-1] + '))'

def getSuburbShapes():
    with open(SUBURB_FILE,'r') as fIn:
        csvReader = csv.reader(fIn)


def run(inputPath,outputPath):
    print('Starting extract process with output at: \n')
    print(outputPath)

    outData = []

    suburbs = getSuburbShapes()

    with open(inputPath,'r') as fIn:

        jData = json.load(fIn)

        # outer dict contains either 'properties' or 'polygon'
        for i in range(len(jData)):
            if i % 2 == 0 and HAS_PROPERTIES:
                continue
            else:
                polygonList = jData[i]['geometry']['coordinates']
                for polygon in polygonList:
                    outData.append([getPolygon(polygon)])

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
if LARGER:
    run(INPUT_PATH_LARGER,OUT_PATH)
else:
    run(INPUT_PATH,OUT_PATH)


# sys.stdout = orig_stdout
# f.close()
