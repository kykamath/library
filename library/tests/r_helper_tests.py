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
        self.assertEqual(sorted(list(self.data_frame.colnames)), sorted(list(returned_data_frame.colnames)))
    def test_get_parameter_values(self):
        current_path = os.path.realpath(__file__)
        data_frame = robjects.DataFrame.from_csvfile(current_path[:current_path.rindex('/')] + '/../data/state.df')
        prediction_variable = 'Life.Exp'
        predictor_variables = ['Population', 'Income', 'Illiteracy', 'Murder', 'HS.Grad', 'Frost', 'Area']
        expected_parameter_names_and_values = [
                                               ('(Intercept)', 70.94322411112951),
                                               ('Population', 5.1800363834827194e-05),
                                               ('Income', -2.1804237825318798e-05),
                                               ('Illiteracy', 0.033820321355290311),
                                               ('Murder', -0.30112317045182957),
                                               ('HS.Grad', 0.048929478881717045),
                                               ('Frost', -0.0057350011035554654),
                                               ('Area', -7.3831661447743889e-08)
                                               ]
        expected_parameter_names_and_values2 = [
                                                ('(Intercept)', 71.027128532085925),
                                                ('Population', 5.0139978004722538e-05),
                                                ('Murder', -0.30014880033035229),
                                                ('HS.Grad', 0.046582246664721869),
                                                ('Frost', -0.005943289723506183)
                                                ]

        model = R_Helper.linear_regression_model(data_frame, prediction_variable, predictor_variables)
        parameter_names_and_values = R_Helper.get_parameter_values(model)
        self.assertEqual(expected_parameter_names_and_values, parameter_names_and_values)
        model = R_Helper.linear_regression_model(
                                                 data_frame,
                                                 prediction_variable,
                                                 predictor_variables,
                                                 with_variable_selection=True
                                                )
        parameter_names_and_values = R_Helper.get_parameter_values(model)
        self.assertEqual(expected_parameter_names_and_values2, parameter_names_and_values)
    def test_get_predicted_value(self):
        current_path = os.path.realpath(__file__)
        data_frame = robjects.DataFrame.from_csvfile(current_path[:current_path.rindex('/')] + '/../data/state.df')
        prediction_variable = 'Life.Exp'
        predictor_variables = ['Population', 'Income', 'Illiteracy', 'Murder', 'HS.Grad', 'Frost', 'Area']
        model = R_Helper.linear_regression_model(data_frame, prediction_variable, predictor_variables)
        mf_parameter_names_to_values = dict(R_Helper.get_parameter_values(model))
        mf_variable_name_to_value = {'Population': 1.0}
        self.assertEqual(
                        '%0.5f'%70.9432759115, 
                        '%0.5f'%R_Helper.get_predicted_value(mf_parameter_names_to_values, mf_variable_name_to_value)
                     )
        
if __name__ == '__main__':
    unittest.main()