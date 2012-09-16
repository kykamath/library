'''
Created on Sep 14, 2012

@author: krishnakamath
'''
import sys
sys.path.append('../')

from file_io import FileIO
from r_helper import R_Helper
import os
import rpy2.robjects as robjects
import unittest


class R_HelperTests(unittest.TestCase):
    def setUp(self):
        self.data_frame_json = '{"a": {"type": "int", "value": [1, 2, 3]}, '+\
                                                '"b": {"type": "float", "value": [5.2, 6.6, 7.3]}}'
        self.data_frame = robjects.DataFrame({
                                              'a': robjects.IntVector([1,2,3]),
                                              'b': robjects.FloatVector([5.2,6.6,7.3])})
    def test_variable_selection_using_backward_elimination(self):
        current_path = os.path.realpath(__file__)
        data_frame = robjects.DataFrame.from_csvfile(current_path[:current_path.rindex('/')] + '/../data/state.df')
        prediction_variable = 'Life.Exp'
        predictor_variables = ['Population', 'Income', 'Illiteracy', 'Murder', 'HS.Grad', 'Frost', 'Area']
        self.assertEqual(
                    ['Population', 'Murder', 'HS.Grad', 'Frost'], 
                     R_Helper.variable_selection_using_backward_elimination(
                                                                            data_frame,
                                                                            prediction_variable,
                                                                            predictor_variables
                                                                        )
                     )
        predictor_variables = ['Population', 'Income', 'Illiteracy', 'Murder', 'HS.Grad', 'Frost', 'Area']
        self.assertEqual(
                    ['Population', 'Income', 'Murder', 'HS.Grad', 'Frost'], 
                     R_Helper.variable_selection_using_backward_elimination(
                                                                               data_frame,
                                                                               prediction_variable,
                                                                               predictor_variables,
                                                                               p_to_remove=0.20
                                                                            )
                     )
    def test_get_json_for_data_frame(self):
        self.assertEqual(self.data_frame_json, R_Helper.get_json_for_data_frame(self.data_frame))
    def test_get_data_frame_from_json(self):
        returned_data_frame = R_Helper.get_data_frame_from_json(self.data_frame_json)
        print returned_data_frame
        self.assertEqual(sorted(list(self.data_frame.colnames)), sorted(list(returned_data_frame.colnames)))
        
#    def test_null(self):
#        current_path = os.path.realpath(__file__)
#        data_frame = robjects.DataFrame.from_csvfile(
#                current_path[:current_path.rindex('/')] + '/../data/state.df')
#        print data_frame.colnames
        
if __name__ == '__main__':
    unittest.main()