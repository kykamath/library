'''
Created on Oct 4, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from geo import getLidFromLocation, getLocationFromLid

class GeoTests(unittest.TestCase):
    def test_getLidFromLocation(self): self.assertEqual('38.930 -77.028', getLidFromLocation([38.929854, -77.027976]))
    def test_getLocationFromLid(self): self.assertEqual([38.93, -77.028000000000006], getLocationFromLid('38.930 -77.028'))

if __name__ == '__main__':
    unittest.main()