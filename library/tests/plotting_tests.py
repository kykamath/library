'''
Created on Jul 5, 2011

@author: kykamath
'''
import unittest
import scipy, random
from plotting import CurveFit, getCumulativeDistribution,\
    getInverseCumulativeDistribution, Map, plot3D, PlotFromHistograms
import matplotlib.pyplot as plt
from classes import GeneralMethods

# class CurveFitTests(unittest.TestCase):
#     def test_curveFitdemo(self):
#         real = lambda p, x: p[0] * scipy.exp(-((x-p[1])/p[2])**2) + scipy.rand(100)
#         functionToFit = lambda p, x: p[0] * scipy.exp(-((x-p[1])/p[2])**2)
#         initialParameters = [5., 7., 3.]
#         dataX = scipy.linspace(0, 10, 100)
#         dataY = real(initialParameters, dataX)
#         cf = CurveFit(functionToFit, initialParameters, dataX, dataY)
#         cf.estimate()
#         cf.plot()
#     def test_exponentialFunctions(self):
#         x, p = 85079, [  1.09194452e+03,   1.03448106e+00]
#         self.assertTrue(x==int(CurveFit.inverseOfDecreasingExponentialFunction(p, CurveFit.decreasingExponentialFunction(p, x))))
#         self.assertTrue(x==int(CurveFit.inverseOfIncreasingExponentialFunction(p, CurveFit.increasingExponentialFunction(p, x))))
#     def test_lineFunction(self):
#         x = range(10)
#         y = range(10)
#         plt.scatter(x,y)
#         params = CurveFit.getParamsAfterFittingData(x, y, CurveFit.lineFunction, [1., 1.])
#         plt.plot(x, CurveFit.getYValues(CurveFit.lineFunction, params, x))
#         plt.show()
# 
# class GlobalMethodTests(unittest.TestCase):
#     def test_getCumulativeDistribution(self):
#         pd = [0.5,0.25, 0.1, 0.1, 0.05]
#         cd = [0.5,0.75,0.85,0.95,1.0]
#         self.assertEqual(cd,getCumulativeDistribution(pd))
#     def test_getInverseCumulativeDistribution(self):
#         pd = [0.5,0.25, 0.1, 0.1, 0.05]
#         cd = [1, 0.5, 0.25, 0.14999999999999999, 0.049999999999999989]
#         self.assertEqual(cd,getInverseCumulativeDistribution(pd))
#     def test_plot3d(self):
#         data =  dict([(i, dict([(j, random.random())for j in range(10)])) for i in range(5)])
#         plot3D(data)
#         plt.show()
# 
# class MapTests(unittest.TestCase):
#     def test_map(self):
#         usMap = Map()
#         usMap.plotPoints([-105.16, -117.16, -77.00], [40.02, 32.73, 38.55], color=GeneralMethods.getRandomColor())
#         usMap.plotPoints([-114.21, -88.10], [48.25, 17.29], color=GeneralMethods.getRandomColor())
#         plt.show()
         
class PlotFromHistogramFileTests(unittest.TestCase):
    f_name = '../data/histogram'
    def test_distribution(self):
        plt.Figure
        ltuo_x_and_y = map(lambda l: map(float, l.split()), open(PlotFromHistogramFileTests.f_name))
        PlotFromHistograms.distribution(ltuo_x_and_y, x_log=True, y_log=True)
#         plt.show()
    def test_probability_distribution(self):
        plt.Figure
        ltuo_x_and_y = map(lambda l: map(float, l.split()), open(PlotFromHistogramFileTests.f_name))
        PlotFromHistograms.probability_distribution(ltuo_x_and_y)
#         plt.show()
    def test_cdf(self):
        plt.Figure
        ltuo_x_and_y = map(lambda l: map(float, l.split()), open(PlotFromHistogramFileTests.f_name))
        PlotFromHistograms.cdf(ltuo_x_and_y)
#         plt.show()
    def test_ccdf(self):
        plt.Figure
        ltuo_x_and_y = map(lambda l: map(float, l.split()), open(PlotFromHistogramFileTests.f_name))
        PlotFromHistograms.ccdf(ltuo_x_and_y)
#         plt.show()
    
if __name__ == '__main__':
    unittest.main()