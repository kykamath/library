'''
Created on Jun 17, 2011

@author: kykamath
'''

import unittest
from stats import entropy, focus

class StatsTests(unittest.TestCase):
#    def test_getWeitzmanOVL(self):
#        self.assertEqual((0.43215049999999999, 0.00012), getWeitzmanOVL(mu1=2, mu2=4, sd1=3, sd2=1))
    def test_entropy(self):
        self.assertEqual(2., entropy({1:5,2:4,3:1}))
        self.assertEqual(1., entropy({1:5,2:5}))
        self.assertEqual(1., entropy({1:5,2:5}, False)) 
        self.assertEqual(0., entropy({1:5}, False))
    def test_focus(self):
        self.assertEqual((1, 0.5), focus({1:5,2:4,3:1}))
        self.assertEqual((1, 1.0), focus({1:5}))
if __name__ == '__main__':
    unittest.main()