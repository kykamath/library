'''
Created on Nov 9, 2011

@author: kykamath
'''

import os, commands, cjson
from library.file_io import FileIO
from operator import itemgetter

if 'CLASSPATH' not in os.environ: os.environ['CLASSPATH']='/Applications/Weka/weka-3-6-6/weka.jar'
wekaScriptsDirectory = __file__.rsplit(os.path.sep,1)[0]+os.path.sep

def runWekaCommand(command): return cjson.decode(commands.getoutput(command))

class ARFF:
    @staticmethod
    def getRelationLine(relationName): return '@RELATION %s'%relationName
    @staticmethod
    def getAttributeLine(attributeName): return '@ATTRIBUTE %s REAL'%attributeName
    @staticmethod
    def getDataLine((docId, docVector), keyToIdMap): return '{%s}'%', '.join(['%s %s'%tuple for tuple in sorted([(keyToIdMap[k], v) for k, v in docVector.iteritems()], key=itemgetter(0))])
    @staticmethod
    def writeARFFForClustering(data, relationName):
        keyToIdMap = {}
        fileName = '/tmp/'+relationName+'.arff'
        os.system('rm -rf %s'%fileName)
        for docId in sorted(data):
            docVector = data[docId]
            for k, v in docVector.iteritems():
                if k not in keyToIdMap: keyToIdMap[k]=len(keyToIdMap)
        FileIO.writeToFile(ARFF.getRelationLine(relationName), fileName)
        for attributeName in keyToIdMap: FileIO.writeToFile(ARFF.getAttributeLine(attributeName), fileName)
        FileIO.writeToFile('@data', fileName)
        for d in data.iteritems(): FileIO.writeToFile(ARFF.getDataLine(d, keyToIdMap), fileName)
        return fileName

class Clustering:
    EM = 'em'
    KMeans = 'kmeans'
    @staticmethod
    def cluster(algorithm, dataDict, options):
        wekaCommand = 'jython %sclusterers.py -a %s -f %s -o "%s"'%(wekaScriptsDirectory, algorithm, ARFF.writeARFFForClustering(dataDict, 'clustering'), options)
        assignment = runWekaCommand(wekaCommand)
        returnDict = dict((docId, clusterId) for docId, clusterId in zip(sorted(dataDict), assignment))
        return returnDict