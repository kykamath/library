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
        self.assertEqual(
                    ['Population', 'Murder', 'HS.Grad', 'Frost'], 
                     R_Helper.variable_selection_using_backward_elimination(
                                                       data_frame,
                                                       prediction_variable,
                                                       predictor_variables
                                                    )
                     )
        predictor_variables = ['Population', 'Income', 'Illiteracy',
                               'Murder', 'HS.Grad', 'Frost', 'Area']
        self.assertEqual(
                    ['Population', 'Income', 'Murder', 'HS.Grad', 'Frost'], 
                     R_Helper.variable_selection_using_backward_elimination(
                                                       data_frame,
                                                       prediction_variable,
                                                       predictor_variables,
                                                       p_to_remove=0.20
                                                    )
                     )
#    def test_null(self):
#        current_path = os.path.realpath(__file__)
#        data_frame = robjects.DataFrame.from_csvfile(
#                current_path[:current_path.rindex('/')] + '/../data/state.df')
#        print data_frame.colnames
        
if __name__ == '__main__':
    unittest.main()