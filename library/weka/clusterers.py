'''
Created on Nov 8, 2011

@author: kykamath
'''
import os
from weka.core import Instances
from optparse import OptionParser
from java.io import BufferedReader, FileReader
from weka.clusterers import ClusterEvaluation
from weka.clusterers import EM, SimpleKMeans
from weka.core import Instances

algorithmMap = dict(
                    em=EM,
                    kmeans = SimpleKMeans
                    )

def cluster(algorithm, filename, options = ''):
    reader = BufferedReader(FileReader(filename))
    data = Instances(reader)
    reader.close()
    cl = algorithm()
    cl.setOptions(options.split())
    cl.buildClusterer(data)
    returnData = []
    for instance in data.enumerateInstances(): returnData.append(cl.clusterInstance(instance))
    print returnData

parser = OptionParser()
parser.add_option("-f", "--file", dest="filename", help="ARFF file to cluster")
parser.add_option("-a", "--algorithm", dest="algorithm", default=True, help="algorithm to cluster")
parser.add_option("-o", "--options", dest="options", default=True, help="WEKA clustering options corresponding to clustering algorithm")
(options, args) = parser.parse_args()
cluster(algorithmMap[options.algorithm], options.filename, options.options)

