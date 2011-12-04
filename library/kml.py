'''
Created on Nov 20, 2011

@author: kykamath
'''
from classes import GeneralMethods
class KML:
    def __init__(self):
        import simplekml
        self.kml = simplekml.Kml()
    def addLocationPoints(self, points, color=None): 
        if not color: color=GeneralMethods.getRandomColor()
        for point in (list(reversed(point)) for point in points):
            pnt = self.kml.newpoint(coords=[point])
            pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png'
            pnt.iconstyle.color = 'ff'+color[1:]
    def write(self, fileName): self.kml.save(fileName)
    @staticmethod
    def drawKMLsForPoints(pointsIterator, outputKMLFile, color=None):
        kml = KML()
        if not color: color = GeneralMethods.getRandomColor()
        kml.addLocationPoints(pointsIterator, color=color)
        kml.write(outputKMLFile)