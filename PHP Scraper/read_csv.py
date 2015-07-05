import sys
import os
import pip
import csv
import re
from datetime import datetime as dt
from dateutil import parser
from urllib import request as r
import lxml
from os.path import exists
import json
#import shapely

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
SUBURB_FILE = ROOT_PATH + r'\Raw Data\walocalitypolygon\WA Shape Modified.csv'
INPUT_PATH = r'C:\Users\dahunt\Downloads\building-polygon.json'
OUT_PATH = ROOT_PATH + r'\PHP Scraper\HOUSE_DATA_BY_POLYGON.csv'


LAT = 0
LONG = 1

# file to redirect log data to
LOG_PATH = ROOT_PATH + r'\log.txt'


#=================
#  MAIN FUNCTIONS
#=================
def getSuburbShapes():
    outData = []
    with open(SUBURB_FILE,'r') as fIn:
        csvReader = csv.reader(fIn,delimiter=',',quotechar='\"')
        for row in csvReader:
            poly = row[0]

            outData.append([row[0],row[6]]) #polygon, suburb name
    return outData

def run(inputPath,outputPath):
    print('Starting extract process with output at: \n')
    print(outputPath)

    outData = []
    shapes = []

    # suburbs = getSuburbShapes()

    with open(SUBURB_FILE,'r') as fIn:
        csvReader = csv.reader(fIn,delimiter=',',quotechar='\"')
        for row in csvReader:
            poly = row[0]

            outData.append([row[0],row[6]]) #polygon, suburb name

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
