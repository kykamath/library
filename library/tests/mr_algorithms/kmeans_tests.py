'''
Created on Jul 14, 2011

@author: kykamath
'''
import sys
sys.path.append('../../')
import unittest
from library.file_io import FileIO
import numpy as np
from mr_algorithms.kmeans import KMeans, StringToArrayProtocol, KMeansVariables

fileName = '../../data/kmeans'

def create_input_file():
    test_in = [(0, [2., 2.]),
                   (1, [1., 1.]),
                   (2, [-1., -1.]),
                   (3, [-2., -2.]),
                   (4, [12., 12.]),
                   (5, [11., 11.]),
                   (6, [9., 9.]),
                   (7, [8., 8.])]
    for id, vector in test_in: FileIO.writeToFileAsJson({'id': id, 'vector': vector}, fileName)
    
class KMeansTests(unittest.TestCase):
    def setUp(self): 
        KMeansVariables.CLUSTERS='{"clusters": [[-1.0, -1.0], [1.0, 1.0]]}'
        self.kmeans = KMeans(args='-r inline'.split())
    def test_mapper(self): 
        test_in = [(0, np.array([2., 2.])),
                   (1, np.array([1., 1.])),
                   (2, np.array([-1., -1.])),
                   (3, np.array([-2., -2.])),
                   (4, np.array([12., 12.])),
                   (5, np.array([11., 11.])),
                   (6, np.array([9., 9.])),
                   (7, np.array([8., 8.]))]
        test_out = [(1, np.array([2., 2., 1.])),
                    (1, np.array([1., 1., 1.])),
                    (0, np.array([-1., -1., 1.])),
                    (0, np.array([-2., -2., 1.])),
                    (1, np.array([12., 12., 1.])),
                    (1, np.array([11., 11., 1.])),
                    (1, np.array([9., 9., 1.])),
                    (1, np.array([8., 8., 1.]))]
        def tolist(s): return [(x[0], x[1].tolist()) for x in s]
        self.assertEqual(tolist(test_out), tolist([list(self.kmeans.mapper(k,v))[0] for k,v in test_in]))
            
    def test_reducer(self): 
        test_in = [
                   (0, [np.array([2., 2., 1.]), np.array([1., 1., 1.]), np.array([-1., -1., 1.]),  np.array([-2., -2., 1.])]),
                   (1, [np.array([12., 12., 1.]), np.array([11., 11., 1.]), np.array([9., 9., 1.]), np.array([8., 8., 1.])])
                ]
        test_out = [(0, np.array([0., 0.])),
                    (1, np.array([10., 10.]))]
        def tolist(s): return [(x[0], x[1].tolist()) for x in s]
        self.assertEqual(tolist(test_out), tolist([list(self.kmeans.reducer(k,v))[0] for k,v in test_in]))
        
    def test_runJob(self): 
        for object in [self.kmeans, KMeans()]:
            ids, arrays = zip(*list(object.runJob(inputFileList=[fileName])))
            self.assertEqual((0, 1), ids)
            self.assertEqual( [[-1.5, -1.5], [7.1666666666700003, 7.1666666666700003]], [a.tolist() for a in arrays])

class StringToArrayProtocolTests(unittest.TestCase):
    def test_read(self):
        id, ar = StringToArrayProtocol.read('{"vector": [2.0, 2.0], "id": 0}')
        self.assertEqual(0, id), self.assertEqual([2.0,2.0], ar.tolist())
    def test_write(self): self.assertEqual('{"vector": [2.0, 2.0], "id": 0}', StringToArrayProtocol.write(0, np.array([2.0,2.0])))

def demo():
    KMeansVariables.CLUSTERS='{"clusters": [[-1.0, -1.0], [1.0, 1.0]]}'
    print list(KMeans().runJob(inputFileList=[fileName]))
    print list(KMeans().runMapper(inputFileList=[fileName]))

if __name__ == '__main__':
#    create_input_file()
#    unittest.main()
    demo()
