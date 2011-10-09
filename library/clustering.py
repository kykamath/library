'''
Created on Jun 15, 2011

@author: kykamath
'''

import cjson, math
from numpy import *
from scipy.stats import mode
from nltk import cluster
from collections import defaultdict
from operator import itemgetter
from classes import TwoWayMap
from vector import VectorGenerator
from nltk.cluster import euclidean_distance
from library.file_io import FileIO

def getItemClustersFromItemsets(itemsetIterator, itemDistanceFunction):
    '''
    => Every clustering is associated with a clusterid.
    => A cluster id is said to be a majority cluster id, if the cluster corresponding to this id contains more than half locations in the current itemset.
    => itemDistanceFunction: This function takes two item objects and returns a floating point number, such that
        greater the returned number's value, farer the items are.
    for every itemset in the iterator
        Check if a majority cluster id exists:
            If it exists add it is UN_ASSIGNED. Create a new cluster for all un-assigned items.
            Else add all un-assigned items in current itemset to this cluster.
        If majority cluster id does not exist:
            Add all un-assigned items to the cluster containing their respective closest item im the itemset. 
    '''
    currentClusters, itemToClusterMap, UN_ASSIGNED = defaultdict(set), {}, ':ilab:'
    def getCandidateClusters(itemset):
        candidateClusters = defaultdict(set)
        [candidateClusters[itemToClusterMap.get(item, UN_ASSIGNED)].add(item) for item in itemset]
        return candidateClusters
    def addItemToCluster(item, clusterId):
        currentClusters[clusterId].add(item)
        itemToClusterMap[item] = clusterId
    def addNewCluster(itemset):
        newClusterId = len(currentClusters)
        for item in itemset: 
            assert item not in itemToClusterMap
            addItemToCluster(item, newClusterId)
    def getMajorityCandidateClusterId(candidateClusters, itemsetLength):
        itemsDistribution = sorted(candidateClusters.iteritems(), key=lambda t: len(t[1]), reverse=True)
        if len(itemsDistribution[0][1]) >= itemsetLength/2: return itemsDistribution[0][0]
    def getClosestItem(item, itemset):
        closestItem, currentDistance = None, ()
        for i in itemset:
            d = itemDistanceFunction(item, i)
            if currentDistance>d: 
                closestItem = i
                currentDistance=d
        return closestItem
    for itemset in itemsetIterator:
        candidateClusters = getCandidateClusters(itemset) # Get the distribution of existing spots for current itemset.
        majorityCandidateClusterId = getMajorityCandidateClusterId(candidateClusters, len(itemset))
        if majorityCandidateClusterId:
            if majorityCandidateClusterId==UN_ASSIGNED: addNewCluster(item for item in itemset if item not in itemToClusterMap)
            else: [addItemToCluster(item, majorityCandidateClusterId) for item in itemset if item not in itemToClusterMap]
        else:
            itemsWithClusters=[]
            for clusterId in candidateClusters: 
                if clusterId!=UN_ASSIGNED: itemsWithClusters+=list(candidateClusters[clusterId])
            for item in candidateClusters[UN_ASSIGNED]:
                closestItem = getClosestItem(item, itemsWithClusters)
                addItemToCluster(item, itemToClusterMap[closestItem])
        for item in itemset: assert item in itemToClusterMap
    return currentClusters.values()
    
class EvaluationMetrics:
    '''
    The implementation for many of these metrics was obtained at
    http://blog.sun.tc/2010/11/clustering-evaluation-for-numpy-and-scipy.html.
    The original authors email id is lin.sun84@gmail.com.
    '''
    @staticmethod
    def precision(predicted,labels):
        K=unique(predicted)
        p=0
        for cls in K:
            cls_members=nonzero(predicted==cls)[0]
            if cls_members.shape[0]<=1:
                continue
            real_label=mode(labels[cls_members])[0][0]
            correctCount=nonzero(labels[cls_members]==real_label)[0].shape[0]
            p+=double(correctCount)/cls_members.shape[0]
        return p/K.shape[0]
 
    @staticmethod
    def recall(predicted,labels):
        K=unique(predicted)
        ccount=0
        for cls in K:
            cls_members=nonzero(predicted==cls)[0]
            real_label=mode(labels[cls_members])[0][0]
            ccount+=nonzero(labels[cls_members]==real_label)[0].shape[0]
        return double(ccount)/predicted.shape[0] 
    
    @staticmethod
    def f1(predicted,labels):
        p=EvaluationMetrics.precision(predicted,labels)
        r=EvaluationMetrics.recall(predicted,labels)
        return 2*p*r/(p+r),p,r
    
    @staticmethod
    def purity(predicted,labels):
        correctAssignedItems = 0.0
        for u,v in zip(predicted,labels):
            if u==v: correctAssignedItems+=1
        return correctAssignedItems/len(predicted) 
    
    @staticmethod
    def mutual_info(x,y):
        N=double(x.size)
        I=0.0
        eps = finfo(float).eps
        for l1 in unique(x):
            for l2 in unique(y):
                #Find the intersections
                l1_ids=nonzero(x==l1)[0]
                l2_ids=nonzero(y==l2)[0]
                pxy=(double(intersect1d(l1_ids,l2_ids).size)/N)+eps
                I+=pxy*log2(pxy/((l1_ids.size/N)*(l2_ids.size/N)))
        return I
    
    @staticmethod
    def nmi(x,y):
        N=x.size
        I=EvaluationMetrics.mutual_info(x,y)
        Hx=0
        for l1 in unique(x):
            l1_count=nonzero(x==l1)[0].size
            Hx+=-(double(l1_count)/N)*log2(double(l1_count)/N)
        Hy=0
        for l2 in unique(y):
            l2_count=nonzero(y==l2)[0].size
            Hy+=-(double(l2_count)/N)*log2(double(l2_count)/N)
        denominator = (Hx+Hy)/2
        if denominator==0: return 1.0
        return I/denominator

    @staticmethod
    def _getPredictedAndLabels(clusters):
        labels=[]
        predicted=clusters
        for cluster in clusters:
            classBySize = defaultdict(int)
            for item in cluster: classBySize[item]+=1
            clusterType = sorted(classBySize.iteritems(),key=itemgetter(1), reverse=True)[0][0]
            labels.append([clusterType]*len(cluster))
        p,l=[],[]
        for pre in predicted: p+=pre
        for lab in labels: l+=lab
        return (array(p), array(l))

    @staticmethod
    def getValueForClusters(predicted, evaluationMethod):
        predictedModified = [p for p in predicted if p]
        if predictedModified:
            predicted, labels = EvaluationMetrics._getPredictedAndLabels(predictedModified)
            return evaluationMethod(predicted, labels)
        else: return 0

class TrainingAndTestDocuments:
    @staticmethod
    def generate(numberOfDocuments = 2500, dimensions = 52):
        def pickOneByProbability(objects, probabilities):
            initialValue, objectToRange = 0.0, {}
            for i in range(len(objects)):
                objectToRange[objects[i]]=(initialValue, initialValue+probabilities[i])
                initialValue+=probabilities[i]
            randomNumber = random.random()
            for object, rangeVal in objectToRange.iteritems():
                if rangeVal[0]<=randomNumber<=rangeVal[1]: return object
                
        topics = {
                  'elections':{'prob': 0.3, 'tags': {'#gop': 0.4, '#bachmann': 0.2, '#perry': 0.2, '#romney': 0.2}},
                  'soccer': {'prob': 0.2, 'tags': {'#rooney': 0.15, '#chica': 0.1, '#manutd': 0.6, '#fergie': 0.15}},
                  'arab': {'prob': 0.3, 'tags': {'#libya': 0.4, '#arab': 0.3, '#eqypt': 0.15, '#syria': 0.15}},
                  'page3': {'prob': 0.2, 'tags': {'#paris': 0.2, '#kim': 0.4, '#britney': 0.2, '#khloe': 0.2}},
                  }
        stopwords = 'abcdefghijklmnopqrstuvwxyz1234567890'
        
        print '#', cjson.encode({'dimensions': dimensions})
        for i in range(numberOfDocuments):
            topic = pickOneByProbability(topics.keys(), [topics[k]['prob'] for k in topics.keys()])
            print ' '.join([topic] + [pickOneByProbability(topics[topic]['tags'].keys(), [topics[topic]['tags'][k] for k in topics[topic]['tags'].keys()]) for i in range(2)] + [random.choice(stopwords) for i in range(5)])

class Clustering(object):
    '''
    Clusters documents given in the form 
    [(id, text), (id, text), ...., (id, text)]
    '''
    PHRASE_TO_DIMENSION = TwoWayMap.MAP_FORWARD
    DIMENSION_TO_PHRASE = TwoWayMap.MAP_REVERSE
    def __init__(self, documents, numberOfClusters): 
        self.documents, self.means, self.numberOfClusters, self.vectors = list(documents), [], numberOfClusters, None
        if self.vectors==None: self._convertDocumentsToVector()
    def _convertDocumentsToVector(self):
        self.vectors = []
        dimensions = TwoWayMap()
        for docId, document in self.documents:
            for w in document.split(): 
                if not dimensions.contains(Clustering.PHRASE_TO_DIMENSION, w): dimensions.set(Clustering.PHRASE_TO_DIMENSION, w, len(dimensions))
        for docId, document in self.documents:
            vector = zeros(len(dimensions))
            for w in document.split(): vector[dimensions.get(Clustering.PHRASE_TO_DIMENSION, w)]+=1 
            self.vectors.append(vector)
    def dumpDocumentVectorsToFile(self, fileName):
        for document, vector in zip(self.documents, self.vectors):
            FileIO.writeToFileAsJson({'id': document[0], 'vector': vector.tolist()}, fileName)
    
class EMTextClustering(Clustering):
    def cluster(self):
        for i in range(self.numberOfClusters): self.means.append(VectorGenerator.getRandomGaussianUnitVector(len(self.vectors[0]), 4, 1).values())
        clusterer = cluster.EMClusterer(self.means, bias=0.1) 
        return clusterer.cluster(self.vectors, True, trace=True)

class KMeansClustering(Clustering):
    def cluster(self, **kwargs):
        clusterer = cluster.KMeansClusterer(self.numberOfClusters, euclidean_distance, **kwargs)
        return clusterer.cluster(self.vectors, True)

class MRKmeansClustering(Clustering):
    def cluster(self, **kwargs):
        print self.vectors
