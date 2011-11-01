'''
Created on Jul 5, 2011

@author: kykamath
'''
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize
from collections import defaultdict
from numpy.ma.core import exp, log
from classes import GeneralMethods

def getLatexForString(str): return '$'+str.replace(' ', '\\ ')+'$'

def plotMethods(methods): map(lambda method: method(returnAxisValuesOnly=False), methods), plt.show()

def plotNorm(maxYValue, mu, sigma, color=None):
    s = np.random.normal(mu, sigma, 1000)
    count, bins = np.histogram(s, 1000, normed=True)
    if not color: color=GeneralMethods.getRandomColor()
    plt.fill_between(bins, ((1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ))/4)*maxYValue, linewidth=1, color=color, alpha=0.3)
    plt.plot(bins, ((1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ))/4)*maxYValue, linewidth=3, color=color)

def smooth(x,window_len=11,window='hanning'):
    ''' Got this code from: http://www.scipy.org/Cookbook/SignalSmooth
    '''
    x=np.array(x)
    if x.ndim != 1: raise ValueError, "smooth only accepts 1 dimension arrays."
    if x.size < window_len: raise ValueError, "Input vector needs to be bigger than window size."
    if window_len<3: return x
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']: raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"
    s=np.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    if window == 'flat': w=np.ones(window_len,'d')
    else: w=eval('np.'+window+'(window_len)')
    y=np.convolve(w/w.sum(),s,mode='valid')
    return y

class CurveFit():
    @staticmethod
    def decreasingExponentialFunction(p, x): 
        ''' Exponential funcion: y = p[0].x^-p[1]    '''
        return p[0]*pow(x, -1*p[1])
    @staticmethod
    def increasingExponentialFunction(p, x): 
        ''' Exponential funcion: y = p[0].x^-p[1]   '''
        return p[0]*pow(x, p[1])
    @staticmethod
    def inverseOfDecreasingExponentialFunction(p, y):
        ''' Inverse exponential funcion: x = e^-(log(y/p[0])/p[1])    '''
        return exp(-1*log(y/p[0])/p[1])
    @staticmethod
    def inverseOfIncreasingExponentialFunction(p, y):
        ''' Inverse exponential funcion: x = e^(log(y/p[0])/p[1])    '''
        return exp(log(y/p[0])/p[1])
    @staticmethod
    def lineFunction(p, x): 
        '''  Line funciton y = p[0]x+p[1]    '''
        return p[0]*x+p[1]
    def __init__(self, functionToFit, initialParameters, dataX, dataY): 
        self.functionToFit, self.initialParameters, self.dataX, self.dataY = functionToFit, initialParameters, dataX, dataY
        if self.functionToFit != None: self.error = lambda p, x, y: self.functionToFit(p, x) - y
    def estimate(self, polyFit=None): 
        if polyFit == None: self.actualParameters, self.success = scipy.optimize.leastsq(self.error, self.initialParameters, args=(self.dataX, self.dataY))
        else: self.actualParameters = np.polyfit(self.dataX, self.dataY, polyFit)
    def errorVal(self):
        xfit=np.polyval(self.actualParameters, self.dataX)
        return scipy.sqrt(sum((self.dataX-xfit)**2)/len(xfit))
    def plot(self, xlabel='', ylabel='', title='', color = 'r'):
        plt.plot(self.dataX, self.dataY, 'o')
        plt.plot(self.dataX, self.functionToFit(self.actualParameters, self.dataX), 'o', color=color)
        plt.xlabel(xlabel), plt.ylabel(ylabel), plt.title(title)
        plt.show()
    def getModeledYValues(self): return self.functionToFit(self.actualParameters, self.dataX)
    @staticmethod
    def getParamsAfterFittingData(x, y, functionToFit, initialParameters):
        cf = CurveFit(functionToFit, initialParameters, x, y)
        cf.estimate()
        return cf.actualParameters
    @staticmethod
    def getYValues(functionToFit, params, x):  return [functionToFit(params, i) for i in x]

def getCumulativeDistribution(probabilityDistribution):
    cumulativeDistribution, cumulative_value = [], 0
    for v in probabilityDistribution: cumulativeDistribution.append(cumulative_value+v); cumulative_value+=v
    return cumulativeDistribution

def getInverseCumulativeDistribution(probabilityDistribution):
    cumulativeDistribution, cumulative_value = [], 1
    for v in probabilityDistribution: cumulativeDistribution.append(cumulative_value); cumulative_value-=v
    return cumulativeDistribution

def getDataDistribution(data):
    dataToPlot = defaultdict(int)
    for i in data: dataToPlot[i]+=1
    dataX = sorted(dataToPlot)
    return dataX, [dataToPlot[i] for i in dataX]

class Map():
    def __init__(self, boundary=[[24.527135,-127.792969], [49.61071,-59.765625]], default=True):
        from mpl_toolkits.basemap import Basemap
        minLat, minLon, maxLat, maxLon = [item for t in boundary for item in t]
        self.m = Basemap(llcrnrlon=minLon, llcrnrlat=minLat, urcrnrlon=maxLon, urcrnrlat = maxLat,  resolution = 'l', projection = 'merc', area_thresh=1000000, lon_0 = minLon+(maxLon-minLon)/2, lat_0 = minLat+(maxLat-minLat)/2)
        if default: self.configure()
    def configure(self):
        self.m.drawcoastlines(linewidth=1.0)
        self.m.drawcountries(linewidth=1.0)
        self.m.fillcontinents(color='#FFFFFF',lake_color='#FFFFFF')
        self.m.drawstates(linewidth=0.5)
        self.m.drawmapboundary(fill_color='#FFFFFF')
    def plotPoints(self, longitude, latitudes, color, lw=0, marker='o', *args, **kwargs):
        mlon, mlat = self.m(longitude,latitudes)
        self.m.plot(mlon,mlat,color=color, lw=lw, marker=marker, *args, **kwargs)
