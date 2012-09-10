'''
Created on Oct 4, 2011

@author: kykamath
'''
import sys
sys.path.append('../')
import unittest
import matplotlib.pyplot as plt
from geo import getLidFromLocation, getLocationFromLid, convertMilesToRadians,\
    convertRadiansToMiles, convertKMsToRadians, convertRadiansToKMs,\
    isWithinBoundingBox,getHaversineDistanceForLids, plotPointsOnUSMap, UTMConverter
    
class UTMConverterTests(unittest.TestCase):
    hrbb_lat_long = (30.619058,-96.338798)
    hrbb_utm = ('14R', 755103.23660390463, 3390404.0353642241)
    def test_LLtoUTM(self):
        self.assertEqual(UTMConverterTests.hrbb_utm, 
                         UTMConverter.LLtoUTM(
                                UTMConverterTests.hrbb_lat_long[0],
                                UTMConverterTests.hrbb_lat_long[1])
                         )
        self.assertEqual(('14R', 755, 3390), 
                         UTMConverter.LLtoUTM(
                                UTMConverterTests.hrbb_lat_long[0],
                                UTMConverterTests.hrbb_lat_long[1],
                                UTMConverter.accuracy_1M)
                         )
        self.assertEqual(('14R', 75, 339), 
                         UTMConverter.LLtoUTM(
                                UTMConverterTests.hrbb_lat_long[0],
                                UTMConverterTests.hrbb_lat_long[1],
                                UTMConverter.accuracy_10KM)
                         )
        self.assertEqual(('14R', 7, 33), 
                         UTMConverter.LLtoUTM(
                                UTMConverterTests.hrbb_lat_long[0],
                                UTMConverterTests.hrbb_lat_long[1],
                                UTMConverter.accuracy_100KM)
                         )
    def test_UTMtoLL(self):
        self.assertEqual((30.619058000461653, -96.338797998733185),
                            UTMConverter.UTMtoLL(
                                UTMConverterTests.hrbb_utm[0],
                                UTMConverterTests.hrbb_utm[1],
                                UTMConverterTests.hrbb_utm[2]
                            )
                        )
        self.assertEqual((30.619838288437187, -96.334639070348715),
                         UTMConverter.UTMtoLL(
                                              '14R', 755, 3390, 
                                              UTMConverter.accuracy_1M
                                              )
                         )
        self.assertEqual((30.660507884195773, -96.338739254497924),
                         UTMConverter.UTMtoLL(
                                              '14R', 75, 339, 
                                              UTMConverter.accuracy_10KM
                                              )
                         )
        self.assertEqual((30.255907497032403, -96.401669265383276),
                         UTMConverter.UTMtoLL(
                                              '14R', 7, 33, 
                                              UTMConverter.accuracy_100KM
                                              )
                         )
        
    def test_getUTMIdFromLatLong(self):
        self.assertEqual('14R_755103E_3390404N', 
                         UTMConverter.getUTMIdFromLatLong(
                                            UTMConverterTests.hrbb_lat_long[0],
                                            UTMConverterTests.hrbb_lat_long[1]
                                            )
                         )
        self.assertEqual((30.619057732179147, -96.33880047343645),
                         UTMConverter.getLatLongFromUTMId(
                                                          '14R_755103E_3390404N'
                                                          )
                         )
        
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
    def test_getHaversineDistanceForLids(self): self.assertEqual(553.86484760274641, getHaversineDistanceForLids(getLidFromLocation([25.562265, -80.595703]), getLidFromLocation([37.788081,-73.037109])))
#    def test_plotPointsOnUSMap(self):
#        pointLabels = ['a', 'b', 'c']
#        pointSize = [19.75, 100, 500]
#        pointColor = ['b', 'r', 'g']
#        plotPointsOnUSMap([[40.809, -74.02], [40.809, -76.02], [44.809, -74.02]], pointLabels, pointSize, pointColor)
#        plt.show()
    
if __name__ == '__main__':
    unittest.main()