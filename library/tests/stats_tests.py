'''
Created on Jun 17, 2011

@author: kykamath
'''

import unittest
from stats import getWeitzmanOVL

class StatsTests(unittest.TestCase):
    def test_getWeitzmanOVL(self):
        self.assertEqual((0.43215049999999999, 0.00012), getWeitzmanOVL(mu1=2, mu2=4, sd1=3, sd2=1))
        
if __name__ == '__main__':
    unittest.main()