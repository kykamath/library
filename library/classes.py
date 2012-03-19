'''
Created on Jun 22, 2011

@author: kykamath
'''
from datetime import timedelta, datetime
import time, random, os, inspect
from collections import defaultdict
import numpy as np

def timeit(method):
    '''
    A decorator to time method calls. The code for this method was obtained from
    http://www.zopyx.de/blog/a-python-decorator-for-measuring-the-execution-time-of-methods
    The author of this code might be Andreas Jung.
    '''
    def timed(*args, **kw):
        timeItMessage = 'timeit: '
        ts = time.time()
#        print '%sStarting %r'%(timeItMessage, method.__name__)
        returnTimeDifferenceOnly = kw.get('returnTimeDifferenceOnly', None)
        result = method(*args, **kw)
        te = time.time()
        timeDifference = te-ts
        if returnTimeDifferenceOnly: return (result, timeDifference)
        print '%s%r took %2.2f sec' % (timeItMessage, method.__name__, timeDifference)
        return result
    return timed

class Settings(dict):
    '''
    Part of this class was obtained from Jeff McGee.
    https://github.com/jeffamcgee
    '''
    def __getattr__(self, name): return self[name]
    def __setattr__(self, name, value): self[name] = value
    def convertToSerializableObject(self): return Settings.getSerialzedObject(self)
    @staticmethod
    def getSerialzedObject(map):
        returnData = {}
        for k, v in map.iteritems():
            if isinstance(v, timedelta): returnData[k]=v.seconds
            elif type(v) in [int, float, str, dict, list, tuple]: returnData[k]=v
        return returnData
    
class FixedIntervalMethod:
    def __init__(self, method, interval):
        self.lastCallTime=None
        self.method=method
        self.interval=interval
    def call(self, currentTime, **kwargs):
        if self.lastCallTime==None: self.lastCallTime=currentTime
        if currentTime-self.lastCallTime>=self.interval:
            self.method(**kwargs)
            self.lastCallTime=currentTime
        
class GeneralMethods:
    @staticmethod
    def reverseDict(map): 
        dictToReturn = dict([(v,k) for k,v in map.iteritems()])
        if len(dictToReturn)!=len(map): raise Exception()
        return dictToReturn
    @staticmethod
    def runCommand(command): print '=> ',command; os.system(command)
    @staticmethod
    def getEpochFromDateTimeObject(dateTimeObject): return time.mktime(dateTimeObject.timetuple())
    @staticmethod
    def getRandomColor(): return '#'+''.join(random.choice('0123456789abcdef') for i in range(6))
    @staticmethod
    def approximateToNearest5Minutes(dateTimeObject):return datetime(dateTimeObject.year, dateTimeObject.month, dateTimeObject.day, dateTimeObject.hour, 5*(dateTimeObject.minute/5))
    @staticmethod
    def approximateEpoch(epoch, modInSeconds): return int(epoch/modInSeconds)*modInSeconds
    @staticmethod
    def getValueDistribution(itemList, valueFunction, *args):
        distribution = defaultdict(int)
        for v in itemList: distribution[valueFunction(v, *args)]+=1
        return distribution
    @staticmethod
    def trueWith(p): return True if random.random() < p else False
    @staticmethod
    def weightedChoice(weights):
        ''' 
        Got this code from a comment by Evan Friis http://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/#comment-253694
        Usage: GeneralMethods.weightedChoice([0.8,0.1,0.1])
        '''
        totals = np.cumsum(weights)
        norm = totals[-1]
        throw = np.random.rand()*norm
        return np.searchsorted(totals, throw)
    @staticmethod
    def getRandomNumberFromSimplePowerlawDistribution(numberOfBins=10):
        values = range(1,11)[::-1]
        return 1./values[GeneralMethods.weightedChoice(values)]
    @staticmethod
    def getElementsInWindow(l, window):
        for i in range(len(l)):
            if i+window<=len(l): yield l[i:i+window]
    @staticmethod
    def get_method_id(): 
        stack = inspect.stack()
        index = stack[1][4][0].strip().rfind('(')
        return stack[1][4][0].strip()[:index].replace('.', '/')

        
class TwoWayMap:
    '''
    A data strucutre that enables 2 way mapping.
    '''
    MAP_FORWARD = 1
    MAP_REVERSE = -1
    def __init__(self): self.data = {TwoWayMap.MAP_FORWARD: {}, TwoWayMap.MAP_REVERSE: {}}
    def set(self, mappingDirection, key, value): 
        if value in self.data[-1*mappingDirection]: self.remove(mappingDirection, self.data[-1*mappingDirection][value])
        if key in self.data[mappingDirection]: self.remove(mappingDirection, key)
        self.data[mappingDirection][key]=value
        self.data[-1*mappingDirection][value]=key
    def get(self, mappingDirection, key): return self.data[mappingDirection][key]
    def remove(self, mappingDirection, key):
        if key in self.data[mappingDirection]:
            value = self.data[mappingDirection][key]
            del self.data[mappingDirection][key]; del self.data[-1*mappingDirection][value]
    def getMap(self, mappingDirection): return self.data[mappingDirection]
    def contains(self, mappingDirection, key): return  key in self.data[mappingDirection]
    def __len__(self): return len(self.data[TwoWayMap.MAP_FORWARD])