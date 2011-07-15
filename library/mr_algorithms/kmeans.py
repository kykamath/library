'''
Created on Jul 15, 2011

@author: kykamath
'''
import sys, cjson, os
sys.path.append('/'.join(os.path.abspath( __file__ ).split('/')[:-2]))
from mrjobwrapper import MRJobWrapper
from mr_algorithms.kmeans_mr import KMeansMRJob, KMeansVariables
from mr_algorithms.kmeans_mr_assign import KMeansAssignMRJob
from file_io import FileIO
from itertools import groupby
from operator import itemgetter

def getClustersJSONFromArrayList(arrays):
    lists = []
    for a in arrays:lists.append(a.tolist())
    return cjson.encode({'clusters': lists})

class KMeansAssign(MRJobWrapper):
    def __init__(self, args):
        self.mrjob = KMeansAssignMRJob(args=args)

class KMeans(MRJobWrapper):
    def __init__(self, args):
        self.mrjob = KMeansMRJob(args=args)
        
    @staticmethod
    def cluster(fileName, initialClusters, mrArgs = '-r hadoop', iterations=5, **kwargs):
#        KMeansVariables.CLUSTERS=getClustersJSONFromArrayList(initialClusters)
        KMeansVariables.write(getClustersJSONFromArrayList(initialClusters))
        for i in range(iterations): 
            print 'Iteration: ', i
            KMeansVariables.write(getClustersJSONFromArrayList([a[1] for a in KMeans(args=mrArgs.split()).runJob(inputFileList=[fileName], **kwargs)]))
        idsFromMRJob = zip(*KMeansAssign(args=mrArgs.split()).runJob(inputFileList=[fileName], **kwargs))[0]
        for k, v in groupby(sorted([i.split(':ilab:') for i in idsFromMRJob], key=itemgetter(0)), key=itemgetter(0)): yield int(k), sorted([int(i[1]) for i in v])
        
