'''
Created on Jul 5, 2011

@author: kykamath
'''
from classes import GeneralMethods
from collections import defaultdict
from file_io import FileIO
from matplotlib.offsetbox import AnchoredOffsetbox
from matplotlib.offsetbox import TextArea
from numpy.ma.core import exp
from numpy.ma.core import log
from operator import itemgetter
from scipy.interpolate import spline
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize

def getLatexForString(str): return '$'+str.replace(' ', '\\ ')+'$'

def plotMethods(methods): map(lambda method: method(returnAxisValuesOnly=False), methods), plt.show()

def savefig(output_file):
    print 'Saving figure: ', output_file
    FileIO.createDirectoryForFile(output_file)
    plt.savefig(output_file, bbox_inches='tight')
    plt.clf()

def splineSmooth(dataX, dataY):
    newDataX = np.linspace(min(dataX),max(dataX),300)
    dataY = spline(dataX,dataY,newDataX)
    return newDataX, dataY

def plotNorm(maxYValue, mu, sigma, color=None, **kwargs):
    s = np.random.normal(mu, sigma, 1000)
    count, bins = np.histogram(s, 1000, normed=True)
    if not color: color=GeneralMethods.getRandomColor()
    plt.fill_between(bins, ((1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ))/4)*maxYValue, linewidth=1, color=color, alpha=0.3)
    plt.plot(bins, ((1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ))/4)*maxYValue, linewidth=3, color=color, **kwargs)

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

def plot3D(data):
    from mpl_toolkits.mplot3d import axes3d
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    X = sorted(data.keys())
    Y = sorted(data[X[0]].keys())
    Z = []
    for y in Y: Z.append([data[x][y] for x in X])
    X, Y = np.meshgrid(X, Y)
    Z = np.array(Z)
    print X.shape, Y.shape, Z.shape
    ax.plot_wireframe(X,Y,Z)

class CurveFit():
    @staticmethod
    def logFunction(p, x):
        ''' Log function:  = p[0]+log(x*p[1])'''
        return p[0]+log(p[1]*x)
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

def plot_hist(ltuo_x_and_y,
             figsize=(6,3),
             title = None,
             x_label = None,
             y_label = None,
             x_scale = None,
             y_scale = None,
             output_file = None,
             prob_function = lambda p: p,
             probability = False,
            ):
    ''' Input_data_format = [[1.0, 1085874.0], [2.0, 660072.0], [3.0, 395773.0]]
    '''
    ltuo_x_and_y = sorted(ltuo_x_and_y, key=itemgetter(0))
    x_values, y_values = zip(*ltuo_x_and_y)
    if probability:
        total = sum(y_values)
        y_values = map(lambda y: y/total, y_values)
    fig = plt.figure(num=None, figsize=figsize)
    plt.scatter(x_values, y_values, c='k')
    plt.plot(x_values, y_values, '-', c='k')
    
    if title: plt.title(title)
    if y_label: plt.ylabel(y_label)
    if x_label: plt.xlabel(x_label)
    if x_scale: plt.xscale(x_scale)
    if y_scale: plt.yscale(y_scale)
    plt.grid()
    if not output_file: plt.show()
    else: savefig(output_file)

def plot_correlation(ltuo_x_and_y,
             figsize=(6,3),
             title = None,
             x_label = None,
             y_label = None,
             x_scale = None,
             y_scale = None,
             fit_x_values = None,
             output_file = None,
             prob_function = lambda p: p,
             probability = False,
             color = 'k'
            ):
    ''' Input_data_format = [[1.0, 1085874.0], [2.0, 660072.0], [3.0, 395773.0]]
    '''
    ltuo_x_and_y = sorted(ltuo_x_and_y, key=itemgetter(0))
    x_values, y_values = zip(*ltuo_x_and_y)
    fig = plt.figure(num=None, figsize=figsize)
    plt.scatter(x_values, y_values, c=color, lw=0)
    fit = np.polyfit(x_values, y_values, 1)
    fit_fn = np.poly1d(fit) # fit_fn is now a function which takes in x and returns an estimate for y
    if not fit_x_values: fit_x_values = x_values
    plt.plot(fit_x_values, fit_fn(fit_x_values), '--b', lw=2)
    if title: plt.title(title)
    if y_label: plt.ylabel(y_label)
    if x_label: plt.xlabel(x_label)
    if x_scale: plt.xscale(x_scale)
    if y_scale: plt.yscale(y_scale)
    plt.grid()
    if not output_file: plt.show()
    else: savefig(output_file)


def plot_probability_distribution(ltuo_x_and_y,
             figsize=(6,3),
             title = None,
             x_label = None,
             y_label = None,
             x_scale = None,
             y_scale = None,
             output_file = None,
             prob_function = lambda p: p
            ):
    ''' Input_data_format = [[1.0, 1085874.0], [2.0, 660072.0], [3.0, 395773.0]]
    '''
    ltuo_x_and_y = sorted(ltuo_x_and_y, key=itemgetter(0))
    x_values, y_values = zip(*ltuo_x_and_y)
    total_count = sum(y_values)
    current_count, cdf = 0.0, []
    for y in y_values:
        current_count+=y
        cdf+=[prob_function(current_count/total_count)]
    fig = plt.figure(num=None, figsize=figsize)
    plt.scatter(x_values, cdf, c='k')
    plt.plot(x_values, cdf, '-', c='k')
    
    if title: plt.title(title)
    if y_label: plt.ylabel(y_label)
    if x_label: plt.xlabel(x_label)
    if x_scale: plt.xscale(x_scale)
    if y_scale: plt.yscale(y_scale)
    plt.grid()
    if not output_file: plt.show()
    else: savefig(output_file)

def plot_cdf(*args, **kwargs): plot_probability_distribution(*args, **kwargs)

def plot_ccdf(*args, **kwargs): plot_probability_distribution(prob_function = lambda p: 1-p, *args, **kwargs)

def get_distribution_values_at(ltuo_x_and_y, prob_function = lambda p: p, *args, **kwargs):
    ltuo_x_and_y = sorted(ltuo_x_and_y, key=itemgetter(0))
    x_values, y_values = zip(*ltuo_x_and_y)
    total_count = sum(y_values)
    current_count, cdf = 0.0, []
    for y in y_values:
        current_count+=y
        cdf+=[prob_function(current_count/total_count)]

def cdf_values_at(*args, **kwargs):
    pass

class AnchoredText(AnchoredOffsetbox):
    '''
    Code to plot anchored text from: http://matplotlib.org/examples/pylab_examples/anchored_artists.html
    '''
    def __init__(self, s, loc, pad=0.4, borderpad=0.5, prop=None, frameon=True):
        self.txt = TextArea(s, minimumdescent=False)
        super(AnchoredText, self).__init__(loc, pad=pad, borderpad=borderpad,
                                           child=self.txt,
                                           prop=prop,
                                           frameon=frameon)
def plot_anchored_text(text, loc=1):
    ax = plt.gca()
    at = AnchoredText(text, loc=loc, frameon=True)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
    ax.add_artist(at)

class PlotFromHistograms(object):
    @staticmethod
    def distribution(ltuo_x_and_y, xlabel='x-value', ylabel='y-value', color='k',
                     x_log=False, y_log=False
                     ):
        x_values, y_values = zip(*ltuo_x_and_y)
        plt.figure(num=None, figsize=(6,3))
        ax = plt.subplot(111)
        plt.subplots_adjust(bottom=0.2, top=0.9)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if x_log: ax.set_xscale('log')
        if y_log: ax.set_yscale('log')
        plt.scatter(x_values, y_values, c=color, )
        plt.grid(True)
    @staticmethod
    def probability_distribution(ltuo_x_and_y, xlabel='x-value', ylabel='y-value', color='k',
                                 x_log=False, y_log=False
                                 ):
        x_values, y_values = zip(*ltuo_x_and_y)
        total_y = sum(y_values) + 0.0
        y_values = map(lambda v: v/total_y, y_values)
        plt.figure(num=None, figsize=(6,3))
        ax = plt.subplot(111)
        plt.subplots_adjust(bottom=0.2, top=0.9)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if x_log: ax.set_xscale('log')
        if y_log: ax.set_yscale('log')
        plt.scatter(x_values, y_values, c=color)
        plt.grid(True)
    @staticmethod
    def cdf(ltuo_x_and_y, xlabel='x-value', ylabel='y-value', color='k', x_log=False, y_log=False):
        x_values, y_values = zip(*ltuo_x_and_y)
        ax = plt.subplot(111)
        total_y = sum(y_values) + 0.0
        current_val = 0.0
        new_y_values = []
        for y in y_values:
            next_val=y+current_val
            new_y_values+=[next_val/total_y]
            current_val = next_val
        y_values = new_y_values
        plt.figure(num=None, figsize=(6,3))
        plt.subplots_adjust(bottom=0.2, top=0.9)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if x_log: ax.set_xscale('log')
        if y_log: ax.set_yscale('log')
        plt.scatter(x_values, y_values, c=color, )
        plt.grid(True)
    @staticmethod
    def ccdf(ltuo_x_and_y, xlabel='x-value', ylabel='y-value', color='k', x_log=False, y_log=False):
        x_values, y_values = zip(*ltuo_x_and_y)
        ax = plt.subplot(111)
        total_y = sum(y_values) + 0.0
        current_val = sum(y_values) + 0.0
        new_y_values = []
        for y in y_values:
            new_y_values+=[current_val/total_y]
            current_val-=y
        y_values = new_y_values
        plt.figure(num=None, figsize=(6,3))
        plt.subplots_adjust(bottom=0.2, top=0.9)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if x_log: ax.set_xscale('log')
        if y_log: ax.set_yscale('log')
        plt.scatter(x_values, y_values, c=color, )
        plt.grid(True)

        