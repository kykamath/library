'''
Created on Oct 22, 2011

@author: kykamath
'''
from scipy import stats

def getWeitzmanOVL(mu1, mu2, sd1, sd2):
    ''' Code by user whuber of http://stats.stackexchange.com/
    http://stats.stackexchange.com/questions/12209/percentage-of-overlapping-regions-of-two-normal-distributionn
    Returns (overlap, error)
    '''
    import rpy2.robjects as robjects
    r = robjects.r
    robjects.r('''
            min.f1f2 <- function(x, mu1, mu2, sd1, sd2) {
                f1 <- dnorm(x, mean=mu1, sd=sd1)
                f2 <- dnorm(x, mean=mu2, sd=sd2)
                pmin(f1, f2)
            }
            ''')
    if mu1==1 and mu2==1 and sd1==0 and sd2==0: return (0.0, 0.0)
    value = str(r.integrate(robjects.r['min.f1f2'], float('-inf'), float('inf'), mu1=mu1, mu2=mu2, sd1=sd1, sd2=sd2)).split()
    return (float(value[0]), float(value[-1]))

def getOutliersRangeUsingIRQ(data):
    '''
    Uses outlier detection using  Interquartile Ranges suggested in http://www.purplemath.com/modules/boxwhisk3.htm
    '''
    q1 = stats.scoreatpercentile(data, 25)
    q3 = stats.scoreatpercentile(data, 75)
    iqr = q3-q1
    return [q1-1.5*iqr, q3+1.5*iqr]