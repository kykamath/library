'''
Created on Oct 4, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from geo import getLidFromLocation

class GeoTests(unittest.TestCase):
    def test_getLidFromLocation(self):
        l1, l2 = [38.929854, -77.027976], [38.899699, -77.089777]
        self.assertEqual('38.930 -77.028', getLidFromLocation(l1))
        self.assertEqual('38.900 -77.090', getLidFromLocation(l2))

if __name__ == '__main__':
    unittest.main()