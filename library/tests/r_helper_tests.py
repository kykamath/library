'''
Created on Sep 14, 2012

@author: krishnakamath
'''
import sys
sys.path.append('../')

from r_helper import R_Helper
import os
import rpy2.robjects as robjects
import unittest


class R_HelperTests(unittest.TestCase):
    def test_variable_selection_using_backward_elimination(self):
        current_path = os.path.realpath(__file__)
        data_frame = robjects.DataFrame.from_csvfile(
                current_path[:current_path.rindex('/')] + '/../data/state.df')
        prediction_variable = 'Life.Exp'
        predictor_variables = ['Population', 'Income', 'Illiteracy',
                               'Murder', 'HS.Grad', 'Frost', 'Area']
        expected_variables = ['Population', 'Murder', 'HS.Grad', 'Frost']
        self.assertEqual(
                    expected_variables, 
                     R_Helper.variable_selection_using_backward_elimination(
                                                       data_frame,
                                                       prediction_variable,
                                                       predictor_variables
                                                    )
                     )
        
if __name__ == '__main__':
    unittest.main()