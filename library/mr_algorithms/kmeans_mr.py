'''
Created on Jul 14, 2011

@author: kykamath
'''
import cjson
from mrjob.job import MRJob
from mrjob.protocol import HadoopStreamingProtocol
import numpy as np

class StringToArrayProtocol(HadoopStreamingProtocol):
    @classmethod
    def read(cls, line): 
        data = cjson.decode(line.strip())
        return data['id'], np.array(data['vector'])
    @classmethod
    def write(cls, key, value):
        return cjson.encode({'id':key, 'vector': value.tolist()})

class KMeansVariables:
    CLUSTERS=None

class KMeansMRJob(MRJob):
    
    def steps(self):
        return [
                self.mr(self.mapper, self.reducer),
                ]
    '''
    A MR implementation for kMeans.
    This is a port of hadoop_vision/kmeans code written for hadoopy by Brandyn White (http://brandynwhite.com/).
    The original source code is at: https://github.com/bwhite/hadoop_vision/tree/master/kmeans 
    '''
    DEFAULT_INPUT_PROTOCOL = 'string_to_array'
    DEFAULT_PROTOCOL = 'string_to_array'
    def configure_options(self):
        super(KMeansMRJob, self).configure_options()
        self.add_passthrough_option( '--clusters', dest='clusters', default=KMeansVariables.CLUSTERS, help='provide initial clusters')
        
    def load_options(self, args):
        """Parse stop_words option."""
        super(KMeansMRJob, self).load_options(args)
        self.clusters = np.array(cjson.decode(self.options.clusters)['clusters'])
    
    @classmethod
    def protocols(cls):
        protocol_dict = super(KMeansMRJob, cls).protocols()
        protocol_dict['string_to_array'] = StringToArrayProtocol
        return protocol_dict
    
    def mapper(self, unused_i, point):
        """Take in a point, find its NN.

        Args:
            unused_i: point id (unused)
            point: numpy array

        Yields:
            A tuple in the form of (key, value)
            key: nearest cluster index (int)
            value: partial sum (numpy array)
        """
        n = self._nearest_cluster_id(self.clusters, point)
        point = self._extend_point(point)
        yield n, point
        
    def reducer(self, n, points):
        """Take in a series of points, find their sum.

        Args:
            n: nearest cluster index (int)
            points: partial sums (numpy arrays)

        Yields:
            A tuple in the form of (key, value)
            key: cluster index (int)
            value: cluster center (numpy array)
        """
        s = 0
        for p in points:
            s += np.array(p)
        m = self._compute_centroid(s)
        yield n, m 
        
    def _nearest_cluster_id(self, clusters, point):
        """Find L2 squared nearest neighbor

        Args:
            clusters: A numpy array of shape (M, N). (N=Dims, M=NumClusters)
            point: A numpy array of shape (N,) or (1, N). (N=Dims)
        Returns:
            An int representing the nearest neighbor index into clusters.
        """
        dist = point - clusters
        dist = np.sum(dist * dist, 1)
        return int(np.argmin(dist))
    
    def _extend_point(self, point):
        point = np.resize(point, len(point) + 1)
        point[-1] = 1
        return point
    
    def _compute_centroid(self, s):
        return s[0:-1] / s[-1]
    
if __name__ == '__main__':
    KMeansMRJob.run()

    