'''
Created on Sep 13, 2012

@author: krishnakamath
'''

from operator import itemgetter 
import rpy2.robjects as robjects
import cjson

R = robjects.r

class R_Helper(object):
    @staticmethod
    def linear_regression_model(data_frame,
                                prediction_variable,
                                predictor_variables,
                                with_variable_selection = False,
                                *args,
                                **kwargs):
        ''' Builds model using linear regression and returns it.
        '''
        if with_variable_selection:
            predictor_variables = R_Helper.variable_selection_using_backward_elimination(data_frame,
                                                                                         prediction_variable,
                                                                                         predictor_variables,
                                                                                         *args,
                                                                                         **kwargs)
        predictor_string = '+'.join(predictor_variables)
        formula_string = '%s ~ %s'%(prediction_variable, predictor_string)
        return R.lm(formula_string, data=data_frame)
    @staticmethod
    def variable_selection_using_backward_elimination(data_frame,
                                                      prediction_variable,
                                                      predictor_variables,
                                                      p_to_remove = 0.05,
                                                      debug=False):
        '''
        Implements the backward elimination algorithm to select substet of 
        predictor variables using liniear regression. The elimnation is based
        on the algorithm described in Section 10.2 of "Practical Regression and
        ANOVA using R" book by Julian J. Faraway.
        '''
        def get_predictor_to_eliminate(data_frame, prediction_variable, predictor_variables):
            g = R_Helper.linear_regression_model(data_frame, prediction_variable, predictor_variables,)
            summary = R.summary(g)
            predictor_p_values = list(summary.rx2('coefficients').rx(True, 'Pr(>|t|)'))
            if len(predictor_p_values) > 1:
                ltuo_pred_and_pred_p_value = zip(predictor_variables, predictor_p_values[1:])
                ltuo_pred_and_pred_p_value = filter( lambda (_, p_val): p_val > p_to_remove, ltuo_pred_and_pred_p_value)
                if len(ltuo_pred_and_pred_p_value) > 1:
                    predictor_to_eliminate, _ = sorted(ltuo_pred_and_pred_p_value, key=itemgetter(1))[-1]
                    return predictor_to_eliminate
        predictor_to_eliminate = True
        total_variables = len(predictor_variables)
        num_of_variables_eliminated = 0
        while predictor_variables and predictor_to_eliminate:
            if debug: print 'Eliminated %s variables of %s'%(num_of_variables_eliminated, total_variables)
            predictor_to_eliminate = get_predictor_to_eliminate(data_frame, prediction_variable, predictor_variables)
            if predictor_to_eliminate:
                predictor_variables.remove(predictor_to_eliminate)
                num_of_variables_eliminated+=1
        return predictor_variables
    @staticmethod
    def get_json_for_data_frame(data_frame):
        def get_data_type(value):
            if type(value)==type(1): return 'int'
            elif type(value)==type(1.): return 'float'
        data = {}
        for column in data_frame.colnames: 
            column_data = list(data_frame.rx2(column))
            data[column]={'value': list(data_frame.rx2(column)), 'type': get_data_type(column_data[0])}
        return cjson.encode(data)
    @staticmethod
    def get_data_frame_from_json(json_string): 
        data_for_df = {}
        data = cjson.decode(json_string)
        for column in data:
            type = data[column]['type']
            if type == 'int': data_for_df[column] = robjects.IntVector(data[column]['value'])
            elif type == 'float': data_for_df[column] = robjects.FloatVector(data[column]['value'])
        return robjects.DataFrame(data_for_df)
    @staticmethod
    def get_parameter_values(model):
        summary = R.summary(model)
        parameter_names = list(summary.rx2('coefficients').names.rx2(1))
        paramter_values = list(summary.rx2('coefficients').rx(True, 1))
        return zip(parameter_names, paramter_values)
    @staticmethod
    def get_predicted_value(mf_parameter_names_to_values, mf_variable_name_to_value):
        predicted_value = 0.0
        mf_variable_name_to_value['(Intercept)'] = 1.0
        for variable_name, value in mf_variable_name_to_value.iteritems():
            predicted_value+=(mf_parameter_names_to_values.get(variable_name, 0.0)*value)
        return predicted_value

