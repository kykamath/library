'''
Created on Oct 4, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from geo import getLidFromLocation, getLocationFromLid, convertMilesToRadians,\
    convertRadiansToMiles, convertKMsToRadians, convertRadiansToKMs

class GeoTests(unittest.TestCase):
    def test_getLidFromLocation(self): self.assertEqual('38.930 -77.028', getLidFromLocation([38.929854, -77.027976]))
    def test_getLocationFromLid(self): self.assertEqual([38.93, -77.028000000000006], getLocationFromLid('38.930 -77.028'))
    def test_convertMilesToRadians(self): self.assertEqual(0.017429695806339407, convertMilesToRadians(69))
    def test_convertRadiansToMiles(self): self.assertEqual(69, convertRadiansToMiles(0.017429695806339407))
    def test_convertKMsToRadians(self): self.assertEqual(1.5696100884490981e-05, convertKMsToRadians(0.1))
    def test_convertRadiansToKMs(self): self.assertEqual(6.3710089999999999, convertRadiansToKMs(0.001))
    
if __name__ == '__main__':
    unittest.main()