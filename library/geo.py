'''
Created on Oct 4, 2011

@author: kykamath
'''
import datetime
def parseData(line):
    data = line.strip().split('\t')
    if len(data)!=7: data.append(None) 
    if len(data)==7: return {'_id':id, 'u': int(data[0]), 'tw': int(data[1]), 'l': [float(data[2]), float(data[3])], 't': datetime.datetime.strptime(data[4], '%Y-%m-%d %H:%M:%S'), 'x': data[5], 'lid': data[6]}