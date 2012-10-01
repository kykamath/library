'''
Created on Jun 17, 2011

@author: kykamath
'''
from stats import MonteCarloSimulation
from stats import entropy
from stats import focus
import numpy as np
import unittest

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
        
class MonteCarloSimulationTests(unittest.TestCase):
    def test_probability_of_data_extracted_from_same_sample(self):
        observed_data = [54, 51, 58, 44, 55, 52, 42, 47, 58, 46]
        expected_data = [54, 73, 53, 70, 73, 68, 52, 65, 65]
        mean_probability = MonteCarloSimulation.mean_probability(
                                                 MonteCarloSimulation.probability_of_data_extracted_from_same_sample,
                                                 observed_data,
                                                 expected_data
                                             )
        self.assertFalse(mean_probability>0.05)
        
if __name__ == '__main__':
    unittest.main()