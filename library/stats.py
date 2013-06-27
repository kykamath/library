'''
Created on Oct 22, 2011

@author: kykamath
'''
from operator import itemgetter
from scipy import stats
import math
import numpy as np
import random

#def getWeitzmanOVL(mu1, mu2, sd1, sd2):
#    ''' Code by user whuber of http://stats.stackexchange.com/
#    http://stats.stackexchange.com/questions/12209/percentage-of-overlapping-regions-of-two-normal-distributionn
#    Returns (overlap, error)
#    '''
#    import rpy2.robjects as robjects
#    r = robjects.r
#    robjects.r('''
#            min.f1f2 <- function(x, mu1, mu2, sd1, sd2) {
#                f1 <- dnorm(x, mean=mu1, sd=sd1)
#                f2 <- dnorm(x, mean=mu2, sd=sd2)
#                pmin(f1, f2)
#            }
#            ''')
#    if mu1==1 and mu2==1 and sd1==0 and sd2==0: return (0.0, 0.0)
#    value = str(r.integrate(robjects.r['min.f1f2'], float('-inf'), float('inf'), mu1=mu1, mu2=mu2, sd1=sd1, sd2=sd2)).split()
#    return (float(value[0]), float(value[-1]))

def getOutliersRangeUsingIRQ(data):
    '''
    Uses outlier detection using  Interquartile Ranges suggested in http://www.purplemath.com/modules/boxwhisk3.htm
    '''
    q1 = stats.scoreatpercentile(data, 25)
    q3 = stats.scoreatpercentile(data, 75)
    iqr = q3-q1
    return [q1-1.5*iqr, q3+1.5*iqr]

def filter_outliers(data):
    lower_range, upper_range = getOutliersRangeUsingIRQ(data)
    return filter(lambda d: d>=lower_range and d<=upper_range, data)

def entropy(mf_key_to_count, as_bits=True):
    total_value = float(sum(mf_key_to_count.itervalues()))
    probabilities = [count/total_value for key, count in mf_key_to_count.iteritems()]
    entropy = -sum([p*math.log(p,2) for p in probabilities])
    if as_bits: entropy = math.ceil(entropy)
    if entropy==0: return 0.0
    else: return entropy
    
def focus(mf_key_to_count):
    total_value = float(sum(mf_key_to_count.itervalues()))
    max_key, max_value = max(mf_key_to_count.iteritems(), key=itemgetter(1))
    return max_key, max_value/total_value

def get_items_between_distribution(ltuo_x_and_y, x1 = None, x2 = None):
    ''' Input_data_format = [[1.0, 1085874.0], [2.0, 660072.0], [3.0, 395773.0]]
    '''
    group_size = sorted(zip(*ltuo_x_and_y))[0]
    mf_group_size_to_num_of_groups = dict(ltuo_x_and_y)
    if not x1: x1 = group_size[0]
    if not x2: x2 = group_size[-1]
    total = 0.0
    for k in group_size:
        if (x1 <= k <= x2):
            total+=k*mf_group_size_to_num_of_groups[k]
    return total

class MonteCarloSimulation(object):
    '''
    Part of this code was got from the implementation in the book "Statistics is Easy!" By Dennis Shasha and
    Manda Wilson
    '''
    NUM_OF_SIMULATIONS = 10000
    @staticmethod
    def _shuffle(grps):
        num_grps = len(grps)
        pool = []
        # pool all values
        for i in range(num_grps):
            pool.extend(grps[i])
        # mix them up
        random.shuffle(pool)
        # reassign to groups of same size as original groups
        new_grps = []
        start_index = 0
        end_index = 0
        for i in range(num_grps):
            end_index = start_index + len(grps[i])
            new_grps.append(pool[start_index:end_index])
            start_index = end_index
        return new_grps
    @staticmethod
    # subtracts group a mean from group b mean and returns result
    def _meandiff(grpA, grpB):
        return sum(grpB) / float(len(grpB)) - sum(grpA) / float(len(grpA))

    @staticmethod
    def probability_of_data_extracted_from_same_sample(sample1, sample2):
        ''' Difference between Two Means Significance Test
        '''
        samples = [sample1, sample2] 
        a, b = 0, 1
        observed_mean_diff = MonteCarloSimulation._meandiff(samples[a], samples[b])
        count = 0
        num_shuffles = MonteCarloSimulation.NUM_OF_SIMULATIONS
        for i in range(num_shuffles):
            new_samples = MonteCarloSimulation._shuffle(samples)
            mean_diff = MonteCarloSimulation._meandiff(new_samples[a], new_samples[b])
            # if the observed difference is negative, look for differences that are smaller
            # if the observed difference is positive, look for differences that are greater
            if observed_mean_diff < 0 and mean_diff <= observed_mean_diff: count = count + 1
            elif observed_mean_diff >= 0 and mean_diff >= observed_mean_diff: count = count + 1
        return (count / float(num_shuffles))
    @staticmethod
    def mean_probability(method, *args, **kwargs):
        return method(*args, **kwargs)
        