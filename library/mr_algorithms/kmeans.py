'''
Created on Jul 15, 2011

@author: kykamath
'''
import sys, cjson
sys.path.append('../../')
from mrjobwrapper import MRJobWrapper
from mr_algorithms.kmeans_mr import KMeansMRJob, KMeansVariables
from file_io import FileIO
from itertools import groupby
from operator import itemgetter

def getClustersJSONFromArrayList(arrays):
    lists = []
    for a in arrays:lists.append(a.tolist())
    return cjson.encode({'clusters': lists})

class KMeans(MRJobWrapper):
    def __init__(self, args):
        self.mrjob = KMeansMRJob(args=args)
        
#    @staticmethod
#    def cluster(fileName, initialClusters, mrArgs = '-r hadoop', iterations=5):
#        KMeansVariables.CLUSTERS=getClustersJSONFromArrayList(initialClusters)
#        for i in range(iterations): 
#            print 'Iteration: ', i
#            KMeansVariables.CLUSTERS=getClustersJSONFromArrayList([a[1] for a in KMeans(args=mrArgs.split()).runJob(inputFileList=[fileName])])
#        clustering = zip(*(KMeans(args=mrArgs.split()).runMapper(inputFileList=[fileName])))[0]
#        documentClustering = [(clusterId, data['id'])for clusterId, data in zip(clustering, FileIO.iterateJsonFromFile(fileName))]
#        for k, v in groupby(sorted(documentClustering, key=itemgetter(0)), key=itemgetter(0)): yield k, [i[1] for i in v]