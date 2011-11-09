'''
Created on Nov 9, 2011

@author: kykamath
'''
from library.file_io import FileIO

class ARFF:
    @staticmethod
    def getRelationLine(relationName): return '@RELATION %s'%relationName
    @staticmethod
    def getAttributeLine(attributeName): return '@ATTRIBUTE %s REAL'%attributeName
    @staticmethod
    def getDataLine((docId, docVector), keyToIdMap): return  '{%s}'%', '.join(['%s %s'%(keyToIdMap[k], v) for k, v in docVector.iteritems()])
    @staticmethod
    def writeARFFForClustering(data, relationName):
        keyToIdMap = {}
        fileName = './'+relationName+'.arff'
        for docId, docVector in data.iteritems():
            for k, v in docVector.iteritems():
                if k not in keyToIdMap: keyToIdMap[k]=len(keyToIdMap)
        FileIO.writeToFile(ARFF.getRelationLine(relationName), fileName)
        for attributeName in keyToIdMap: FileIO.writeToFile(ARFF.getAttributeLine(attributeName), fileName)
        FileIO.writeToFile('@data', fileName)
        for d in data.iteritems(): FileIO.writeToFile(ARFF.getDataLine(d, keyToIdMap), fileName)
            
data = {1: {'a':10, 'b': 15},
        2: {'c':10},
        3: {'a':10, 'b': 15}}

relationName = 'data'
ARFF.writeARFFForClustering(data, relationName)