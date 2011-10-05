'''
Created on Oct 4, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
from geo import getLidFromLocation, getLocationFromLid, convertMilesToRadians,\
    convertRadiansToMiles, convertKMsToRadians, convertRadiansToKMs,\
    isWithinBoundingBox

class GeoTests(unittest.TestCase):
    def test_getLidFromLocation(self): self.assertEqual('38.930 -77.028', getLidFromLocation([38.929854, -77.027976]))
    def test_getLocationFromLid(self): self.assertEqual([38.93, -77.028000000000006], getLocationFromLid('38.930 -77.028'))
    def test_convertMilesToRadians(self): self.assertEqual(0.017429695806339407, convertMilesToRadians(69))
    def test_convertRadiansToMiles(self): self.assertEqual(69, convertRadiansToMiles(0.017429695806339407))
    def test_convertKMsToRadians(self): self.assertEqual(1.5696100884490981e-05, convertKMsToRadians(0.1))
    def test_convertRadiansToKMs(self): self.assertEqual(6.3710089999999999, convertRadiansToKMs(0.001))
    def test_isWithinBoundingBox(self):
        boundary = [[24.527135,-124.804687], [50.792047, -60.952148]]
        self.assertFalse(isWithinBoundingBox([25.799891,-153.632812], boundary))
        self.assertFalse(isWithinBoundingBox([24.046464,-88.59375], boundary))
        self.assertFalse(isWithinBoundingBox([38.272689,-44.912109], boundary))
        self.assertFalse(isWithinBoundingBox([51.124213,-104.589844], boundary))
        self.assertTrue(isWithinBoundingBox([44.024422, -105.908203], boundary))
        self.assertTrue(isWithinBoundingBox([37.788081,-73.037109], boundary))
        self.assertTrue(isWithinBoundingBox([25.562265, -80.595703], boundary))
    
if __name__ == '__main__':
    unittest.main()