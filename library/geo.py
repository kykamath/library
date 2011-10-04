'''
Created on Oct 4, 2011

@author: kykamath
'''
import datetime

earthRadiusMiles = 3958.761
earthRadiusKMs = 6371.009

def parseData(line):
    data = line.strip().split('\t')
    if len(data)!=7: data.append(None) 
    if len(data)==7: return {'_id':id, 'u': int(data[0]), 'tw': int(data[1]), 'l': [float(data[2]), float(data[3])], 't': datetime.datetime.strptime(data[4], '%Y-%m-%d %H:%M:%S'), 'x': data[5], 'lid': data[6]}

def getLidFromLocation(location): return '%0.3f %0.3f'%(location[0], location[1])
def getLocationFromLid(lid): return [float(l) for l in lid.split()]
def convertMilesToRadians(miles): return miles/earthRadiusMiles
def convertRadiansToMiles(radians): return radians*earthRadiusMiles
def convertKMsToRadians(kms): return kms/earthRadiusKMs
def convertRadiansToKMs(radians): return radians*earthRadiusKMs
