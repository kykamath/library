'''
Created on Jul 15, 2011

@author: kykamath
'''
import cjson
from mrjob.job import MRJob
from mrjob.protocol import HadoopStreamingProtocol
import numpy as np

clusters_file = 'clusters'

class StringToArrayProtocol(HadoopStreamingProtocol):
    @classmethod
    def read(cls, line): 
        data = cjson.decode(line.strip())
        return data['id'], np.array(data['vector'])
    @classmethod
    def write(cls, key, value):
        return cjson.encode({'id':key, 'vector': value.tolist()})
    

class KMeansVariables:
    @staticmethod
    def write(data):
        with open(clusters_file, 'w') as f: f.write(data+'\n')

class KMeansAssignMRJob(MRJob):
    def steps(self):
        return [
                self.mr(self.mapper, self.reducer),
                ]
    DEFAULT_INPUT_PROTOCOL = 'string_to_array'
    DEFAULT_PROTOCOL = 'string_to_array'
    def configure_options(self):
        super(KMeansAssignMRJob, self).configure_options()
        self.add_file_option( '--clusters', dest='clusters', default=clusters_file, help='provide initial clusters file')
        
    def load_options(self, args):
        super(KMeansAssignMRJob, self).load_options(args)
        data = open(self.options.clusters).readlines()[0].strip()
        self.clusters = np.array(cjson.decode(data)['clusters'])
    
    @classmethod
    def protocols(cls):
        protocol_dict = super(KMeansAssignMRJob, cls).protocols()
        protocol_dict['string_to_array'] = StringToArrayProtocol
        return protocol_dict
    
    def mapper(self, id, point):
        n = self._nearest_cluster_id(self.clusters, point)
        point = self._extend_point(point)
        self.set_status('alive!')
        yield '%d:ilab:%s'%(n, id), point
        
    def _nearest_cluster_id(self, clusters, point):
        dist = point - clusters
        dist = np.sum(dist * dist, 1)
        return int(np.argmin(dist))
    
    def _extend_point(self, point):
        point = np.resize(point, len(point) + 1)
        point[-1] = 1
        return point
        
    def reducer(self, n_id, points):
        self.set_status('alive!')
        for p in points: yield n_id, p
        
if __name__ == '__main__':
    KMeansAssignMRJob.run()
    