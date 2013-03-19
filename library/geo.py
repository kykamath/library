'''
Created on Oct 4, 2011

@author: kykamath
'''
import os
import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import datetime, math
import numpy as n
import matplotlib.pyplot as plt
from classes import GeneralMethods
from itertools import groupby
from operator import itemgetter
from math import pi, sin, cos, tan, sqrt

earthRadiusMiles = 3958.761
earthRadiusKMs = 6371.009
earthCircumferenceInMiles = 24901.55

def plotPointsOnUSMap(points, blueMarble=False, bkcolor='#85A6D9', returnBaseMapObject = False, pointLabels=[], *args, **kwargs):
    from mpl_toolkits.basemap import Basemap
    m = Basemap(llcrnrlon=-125.15625, llcrnrlat=20, urcrnrlon=-59.765625, urcrnrlat=49.61071, projection='mill', lat_1=24, lat_2=50, lon_0=-98, resolution='l', area_thresh=10000)
    m.drawmapboundary(fill_color='#85A6D9')
    
    if blueMarble: m.bluemarble()
    else:
        m.drawmapboundary(fill_color=bkcolor)
        m.fillcontinents(color='white',lake_color=bkcolor)
        m.drawcoastlines(color='#6D5F47', linewidth=.4)
        m.drawcountries(color='#6D5F47', linewidth=.4)
        m.drawstates(color='#6D5F47', linewidth=.4)
    
#    m.fillcontinents(color='white',lake_color='#85A6D9')
#    m.drawstates(color='#6D5F47', linewidth=.4)
#    m.drawcoastlines(color='#6D5F47', linewidth=.4)
#    m.drawcountries(color='#6D5F47', linewidth=.4)
    
#    m.drawmeridians(n.arange(-180, 180, 30), color='#bbbbbb')
#    m.drawparallels(n.arange(-90, 90, 30), color='#bbbbbb')
    lats, lngs = zip(*points)
    
    x,y = m(lngs,lats)
    scatterPlot = m.scatter(x, y, zorder = 2, *args, **kwargs)
    
    for population, xpt, ypt in zip(pointLabels, x, y):
        label_txt = str(population)
        plt.text( xpt, ypt, label_txt, color = 'black', size='small', horizontalalignment='center', verticalalignment='center', zorder = 3)
    if not returnBaseMapObject: return scatterPlot
    else: return (scatterPlot, m)
    
def plotPointsOnWorldMap(points, blueMarble=False, bkcolor='#85A6D9', returnBaseMapObject = False, pointLabels=[], pointLabelColor='black', pointLabelSize='small', resolution='l', *args, **kwargs):
    from mpl_toolkits.basemap import Basemap
    m = Basemap(projection='mill', llcrnrlon=-180. ,llcrnrlat=-60, urcrnrlon=180. ,urcrnrlat=80, resolution=resolution)
    if blueMarble: m.bluemarble()
    else:
        m.drawmapboundary(fill_color=bkcolor)
        m.fillcontinents(color='white',lake_color=bkcolor)
        m.drawcoastlines(color='#6D5F47', linewidth=.4)
        m.drawcountries(color='#6D5F47', linewidth=.4)
    
    lats, lngs = zip(*points)
    
    x,y = m(lngs,lats)
    scatterPlot = m.scatter(x, y, zorder = 2, *args, **kwargs)
    for population, xpt, ypt in zip(pointLabels, x, y):
        label_txt = str(population)
        plt.text( xpt, ypt, label_txt, color = pointLabelColor, size=pointLabelSize, horizontalalignment='center', verticalalignment='center', zorder = 3)
    if not returnBaseMapObject: return scatterPlot
    else: return (scatterPlot, m)

def plot_graph_clusters_on_world_map(graph, s=0, lw=0, alpha=0.6, bkcolor='#CFCFCF', *args, **kwargs): 
    from graphs import clusterUsingAffinityPropagation 
    no_of_clusters, tuples_of_location_and_cluster_id = clusterUsingAffinityPropagation(graph)
    map_from_location_to_cluster_id = dict(tuples_of_location_and_cluster_id)
    map_from_cluster_id_to_cluster_color = dict([(i, GeneralMethods.getRandomColor()) for i in range(no_of_clusters)])
    points, colors = zip(*map(lambda  location: (getLocationFromLid(location.replace('_', ' ')), map_from_cluster_id_to_cluster_color[map_from_location_to_cluster_id[location]]), graph.nodes()))
    _, m = plotPointsOnWorldMap(points, c=colors, s=s, lw=lw, returnBaseMapObject=True,  *args, **kwargs)
    for u, v, data in graph.edges(data=True):
        if map_from_location_to_cluster_id[u]==map_from_location_to_cluster_id[v]:
            color, u, v, w = map_from_cluster_id_to_cluster_color[map_from_location_to_cluster_id[u]], getLocationFromLid(u.replace('_', ' ')), getLocationFromLid(v.replace('_', ' ')), data['w']
            m.drawgreatcircle(u[1], u[0], v[1], v[0], color=color, alpha=alpha)
    return (no_of_clusters, tuples_of_location_and_cluster_id)
    
def parseData(line):
    data = line.strip().split('\t')
    if len(data)!=7: data.append(None) 
    if len(data)==7: return {'_id':id, 'u': int(data[0]), 'tw': int(data[1]), 'l': [float(data[2]), float(data[3])], 't': datetime.datetime.strptime(data[4], '%Y-%m-%d %H:%M:%S'), 'x': data[5], 'lid': data[6]}

def getLidFromLocation(location): return '%0.3f %0.3f'%(location[0], location[1])
def getLocationFromLid(lid): return [float(l) for l in lid.split()]
def convertMilesToRadians(miles): return miles/earthRadiusMiles
def convertRadiansToMiles(radians): return radians*earthRadiusMiles
def convertKMsToRadians(kms): return kms/earthRadiusKMs
def convertRadiansToKMs(radians): return radians*earthRadiusKMs
def isWithinBoundingBox(point, boundingBox):
    '''
    point [x,y]
    boundingBox = [[lower left][upper right]]
    '''
    lowerLeftPoint, upperRightPoint = boundingBox
    return lowerLeftPoint[0]<=point[0]<=upperRightPoint[0] and lowerLeftPoint[1]<=point[1]<=upperRightPoint[1]

def convexHull(points, smidgen=0.0075):
    '''Calculate subset of points that make a convex hull around points

        Recursively eliminates points that lie inside two neighbouring points until only convex hull is remaining.
        
        :Parameters:
            points : ndarray (2 x m)
                array of points for which to find hull
            smidgen : float
                offset for graphic number labels - useful values depend on your data range
        
        :Returns:
            hull_points : ndarray (2 x n)
                convex hull surrounding points
                
        Code obtained from: http://www.scipy.org/Cookbook/Finding_Convex_Hull
    '''
    def _angle_to_point(point, centre):
        '''calculate angle in 2-D between points and x axis'''
        delta = point - centre
        res = n.arctan(delta[1] / delta[0])
        if delta[0] < 0:
            res += n.pi
        return res
    def area_of_triangle(p1, p2, p3):
        '''calculate area of any triangle given co-ordinates of the corners'''
        return n.linalg.norm(n.cross((p2 - p1), (p3 - p1)))/2.
    n_pts = points.shape[1]
    assert(n_pts > 5)
    centre = points.mean(1)
    angles = n.apply_along_axis(_angle_to_point, 0, points, centre)
    pts_ord = points[:,angles.argsort()]
    pts = [x[0] for x in zip(pts_ord.transpose())]
    prev_pts = len(pts) + 1
    k = 0
    while prev_pts > n_pts:
        prev_pts = n_pts
        n_pts = len(pts)
        i = -2
        while i < (n_pts - 2):
            Aij = area_of_triangle(centre, pts[i],     pts[(i + 1) % n_pts])
            Ajk = area_of_triangle(centre, pts[(i + 1) % n_pts], \
                                   pts[(i + 2) % n_pts])
            Aik = area_of_triangle(centre, pts[i],     pts[(i + 2) % n_pts])
            if Aij + Ajk < Aik:
                del pts[i+1]
            i += 1
            n_pts = len(pts)
        k += 1
    return n.asarray(pts)

def geographicConvexHull(points): return convexHull(n.array(zip(*points)))

def getHaversineDistanceForLids(lid1, lid2, radius=earthRadiusMiles): return getHaversineDistance(getLocationFromLid(lid1), getLocationFromLid(lid2))
def getHaversineDistance((lon1, lat1), (lon2, lat2), radius=earthRadiusMiles):
    '''
    Got this code from
    '''
    try:
    #    print (lon1, lat1), (lon2, lat2)
        if str(lon1)==str(lon2) and str(lat1)==str(lat2): return 0.0
    #    if '%0.5f'%(lon1)=='%0.5f'%(lon2) and '%0.5f'%(lat1)=='%0.5f'%(lat2): return 0.0
        p1lat, p1lon = math.radians(lat1), math.radians(lon1)
        p2lat, p2lon = math.radians(lat2), math.radians(lon2)
        return radius * math.acos(math.sin(p1lat) * math.sin(p2lat) + math.cos(p1lat) * math.cos(p2lat) * math.cos(p2lon - p1lon))
    except: return 0.0
    
def getCenterOfMass(points, accuracy=10**-6, error=False): 
    com = getLattice(n.mean(points,0), accuracy=accuracy)
    if not error: return com
    else:
        meanDistance = n.mean([getHaversineDistance(com, p) for p in points])
        return (com, meanDistance)

def breakIntoLattice(boundingBox, latticeDimensions):
    '''latticeDimensions = [x,y] will break bounding box into x*y boxes
    '''
    lowerLeft, upperRight = boundingBox
    numberOfX, numberOfY = latticeDimensions
    y_length = n.abs(upperRight[0]-lowerLeft[0])
    x_length = n.abs(upperRight[1]-lowerLeft[1])
    yUnitLength, xUnitLength = y_length/float(numberOfY), x_length/float(numberOfX)
    yCoords = [lowerLeft[1]]
    for i in range(numberOfY): yCoords.append(yCoords[-1]+yUnitLength)
    xCoords = [lowerLeft[0]]
    for i in range(numberOfX): xCoords.append(xCoords[-1]+xUnitLength)
    i = 0
    ar = []
    for x in xCoords:
        tempAr = []
        for y in yCoords:
            tempAr.append([x,y])
        ar.append(tempAr)
    latticeBoundingBoxes = []
    for i in range(len(xCoords)):
        for j in range(len(yCoords)):
            if i+1<len(xCoords) and j+1<len(yCoords): 
                latticeBoundingBoxes.append([ar[i][j], ar[i+1][j+1]])
    return (latticeBoundingBoxes, xUnitLength, yUnitLength)

def getLatticeBoundingBoxFor(boundingBox, latticeDimensions, point):
    lowerLeft, upperRight = boundingBox
    numberOfX, numberOfY = latticeDimensions
    x_length = n.abs(upperRight[1]-lowerLeft[1])
    y_length = n.abs(upperRight[0]-lowerLeft[0])
    yUnitLength, xUnitLength = y_length/float(numberOfY), x_length/float(numberOfX)
    
def getRadiusOfGyration(points):
    if not points: return None
    centerOfMass = getCenterOfMass(points)
    return math.sqrt((sum(getHaversineDistance(centerOfMass, point)**2 for point in points))/len(points))

def getLattice(point, accuracy=0.0075):
    ''' Accuracy in miles getHaversineDistance([0, 0], [0, 0.0075])
    '''
    return [int(point[0]/accuracy)*accuracy, int(point[1]/accuracy)*accuracy]

def getLatticeLid(point, accuracy=0.0075):
    ''' Accuracy in miles getHaversineDistance([0, 0], [0, 0.0075])
    '''
    return '%0.4f_%0.4f'%(int(point[0]/accuracy)*accuracy, int(point[1]/accuracy)*accuracy)
def point_inside_polygon(x,y,poly):
    ''' Got this code from http://www.ariel.com.au/a/python-point-int-poly.html .
    poly = [[x1,y1], [x2, y2], ...]
    '''
    n = len(poly)
    inside =False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

class UTMConverter:
    ''' 
    The Universal Transverse Mercator (UTM) geographic coordinate system uses a
    2-dimensional Cartesian coordinate system to give locations on the surface
    of the Earth. It is a horizontal position representation, i.e. it is used
    to identify locations on the Earth independently of vertical position, but
    differs from the traditional method of latitude and longitude in several
    respects. For more details take a look at:
    http://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system
    
    This class provides methods to convert latitude and longitude
    pairs to UTM and vice versa. The methods in the class were initially
    modified by Aparna.
    
    Tip on accuracy:
    If UTM value is [567890N,78900S]. Removing last 3 digits give 1m accuracy.
    That is any lat long that converts to [567xxxN,78xxxS] will be in the same
    1m square.  Removing 4 digits give 10km accuracy. 5 digits give 100km
    accuracy.

    Similary we can convert from lat/long to UTM . Say we have [567N,78S] with
    a 1m square accuracy. Multiply by 1000. [56000N,78000S] gives bottom left
    corner of 1m square box. Add 500 to each to get mid poiint. [56500N,78500S]
    gives the mid-point of square.UTMtoLL wii give the value in lat/long.
    
    Source:
    Defense Mapping Agency. 1987b. DMA Technical Report: Supplement to
    Department of Defense World Geodetic System 1984 Technical Report.
    Part I and II. Washington, DC: Defense Mapping Agency
    
    Reference ellipsoids derived from Peter H. Dana's website- 
    http://www.utexas.edu/depts/grg/gcraft/notes/datum/elist.html
    Department of Geography, University of Texas at Austin
    Internet: pdana@mail.utexas.edu
    3/22/95
    '''
#    accuracy_exact = 0
#    accuracy_1M = 1
#    accuracy_10KM = 2
#    accuracy_100KM = 3

    earthRadiusMiles = 3958.761
    earthRadiusKMs = 6371.009
    earthCircumferenceInMiles = 24901.55
    
    _deg2rad = pi / 180.0
    _rad2deg = 180.0 / pi
    
    _EquatorialRadius = 2
    _eccentricitySquared = 3
    
    _ellipsoid = [
        # Id, Ellipsoid name, Equatorial Radius, square of eccentricity    
        # first once is a placeholder only, To allow array indices to match id
        # numbers
        [ -1, "Placeholder", 0, 0],
            [ 1, "Airy", 6377563, 0.00667054],
            [ 2, "Australian National", 6378160, 0.006694542],
            [ 3, "Bessel 1841", 6377397, 0.006674372],
            [ 4, "Bessel 1841 (Nambia] ", 6377484, 0.006674372],
            [ 5, "Clarke 1866", 6378206, 0.006768658],
            [ 6, "Clarke 1880", 6378249, 0.006803511],
            [ 7, "Everest", 6377276, 0.006637847],
            [ 8, "Fischer 1960 (Mercury] ", 6378166, 0.006693422],
            [ 9, "Fischer 1968", 6378150, 0.006693422],
            [ 10, "GRS 1967", 6378160, 0.006694605],
            [ 11, "GRS 1980", 6378137, 0.00669438],
            [ 12, "Helmert 1906", 6378200, 0.006693422],
            [ 13, "Hough", 6378270, 0.00672267],
            [ 14, "International", 6378388, 0.00672267],
            [ 15, "Krassovsky", 6378245, 0.006693422],
            [ 16, "Modified Airy", 6377340, 0.00667054],
            [ 17, "Modified Everest", 6377304, 0.006637847],
            [ 18, "Modified Fischer 1960", 6378155, 0.006693422],
            [ 19, "South American 1969", 6378160, 0.006694542],
            [ 20, "WGS 60", 6378165, 0.006693422],
            [ 21, "WGS 66", 6378145, 0.006694542],
            [ 22, "WGS-72", 6378135, 0.006694318],
            [ 23, "WGS-84", 6378137, 0.00669438]
            ]
    
    @staticmethod
    def _UTMLetterDesignator(Lat):
        ''' This routine determines the correct UTM letter designator for the
        given latitude returns 'Z' if latitude is outside the UTM limits of 84N
        to 80S.
        Written by Chuck Gantz- chuck.gantz@globalstar.com
        '''
        if 84 >= Lat >= 72: return 'X'
        elif 72 > Lat >= 64: return 'W'
        elif 64 > Lat >= 56: return 'V'
        elif 56 > Lat >= 48: return 'U'
        elif 48 > Lat >= 40: return 'T'
        elif 40 > Lat >= 32: return 'S'
        elif 32 > Lat >= 24: return 'R'
        elif 24 > Lat >= 16: return 'Q'
        elif 16 > Lat >= 8: return 'P'
        elif  8 > Lat >= 0: return 'N'
        elif  0 > Lat >= -8: return 'M'
        elif -8> Lat >= -16: return 'L'
        elif -16 > Lat >= -24: return 'K'
        elif -24 > Lat >= -32: return 'J'
        elif -32 > Lat >= -40: return 'H'
        elif -40 > Lat >= -48: return 'G'
        elif -48 > Lat >= -56: return 'F'
        elif -56 > Lat >= -64: return 'E'
        elif -64 > Lat >= -72: return 'D'
        elif -72 > Lat >= -80: return 'C'
        else: return 'Z'    # if the Latitude is outside the UTM limits
    
    @staticmethod
    def LLtoUTM(Lat, Long, accuracy = 1):
        ''' Converts lat/long to UTM coords.  Equations from USGS Bulletin 1532 
        East Longitudes are positive, West longitudes are negative. 
        North latitudes are positive, South latitudes are negative
        Lat and Long are in decimal degrees
        Modified code written by Chuck Gantz- chuck.gantz@globalstar.com
        
        accuracy in square metres.
        '''
        ReferenceEllipsoid = 23
        a = UTMConverter._ellipsoid[ReferenceEllipsoid]\
                                            [UTMConverter._EquatorialRadius]
        eccSquared = UTMConverter._ellipsoid[ReferenceEllipsoid]\
                                            [UTMConverter._eccentricitySquared]
        k0 = 0.9996
    
        #Make sure the longitude is between -180.00 .. 179.9
        LongTemp = (Long+180)-int((Long+180)/360)*360-180 # -180.00 .. 179.9
    
        LatRad = Lat*UTMConverter._deg2rad
        LongRad = LongTemp*UTMConverter._deg2rad
    
        ZoneNumber = int((LongTemp + 180)/6) + 1
    
        if Lat >= 56.0 and Lat < 64.0 and LongTemp >= 3.0 and LongTemp < 12.0:
            ZoneNumber = 32
    
        # Special zones for Svalbard
        if Lat >= 72.0 and Lat < 84.0:
            if  LongTemp >= 0.0  and LongTemp <  9.0:ZoneNumber = 31
            elif LongTemp >= 9.0  and LongTemp < 21.0: ZoneNumber = 33
            elif LongTemp >= 21.0 and LongTemp < 33.0: ZoneNumber = 35
            elif LongTemp >= 33.0 and LongTemp < 42.0: ZoneNumber = 37
    
        LongOrigin = (ZoneNumber - 1)*6 - 180 + 3
        #+3 puts origin in middle of zone
        LongOriginRad = LongOrigin * UTMConverter._deg2rad
    
        #compute the UTM Zone from the latitude and longitude
        UTMZone = "%d%c" % (ZoneNumber, UTMConverter._UTMLetterDesignator(Lat))
    
        eccPrimeSquared = (eccSquared)/(1-eccSquared)
        N = a/sqrt(1-eccSquared*sin(LatRad)*sin(LatRad))
        T = tan(LatRad)*tan(LatRad)
        C = eccPrimeSquared*cos(LatRad)*cos(LatRad)
        A = cos(LatRad)*(LongRad-LongOriginRad)
    
        M = a*((1
                    - eccSquared/4
                    - 3*eccSquared*eccSquared/64
                    - 5*eccSquared*eccSquared*eccSquared/256)*LatRad 
                    - (3*eccSquared/8
                    + 3*eccSquared*eccSquared/32
                    + 45*eccSquared*eccSquared*eccSquared/1024)*sin(2*LatRad)
                    + (15*eccSquared*eccSquared/256 + 45*eccSquared*eccSquared*\
                       eccSquared/1024)*sin(4*LatRad) 
                    - (35*eccSquared*eccSquared*eccSquared/3072)*sin(6*LatRad))
    
        UTMEasting = (k0*N*(A+(1-T+C)*A*A*A/6
                    + (5-18*T+T*T+72*C-58*eccPrimeSquared)*A*A*A*A*A/120)
                    + 500000.0)
    
        UTMNorthing = (k0*(M+N*tan(LatRad)*(A*A/2+(5-T+9*C+4*C*C)*A*A*A*A/24
                        + (61
                        -58*T
                        +T*T
                        +600*C
                        -330*eccPrimeSquared)*A*A*A*A*A*A/720)))
    
        if Lat < 0:
            UTMNorthing = UTMNorthing + 10000000.0; 
            #10000000 meter offset for southern hemisphere
        UTMZone, UTMEasting, UTMNorthing
        UTMEasting = int(UTMEasting/accuracy)
        UTMNorthing = int(UTMNorthing/accuracy)
        return (UTMZone, UTMEasting, UTMNorthing)
    
    @staticmethod
    def UTMtoLL(zone, easting, northing, accuracy = 1):
        ''' Converts UTM coords to lat/long.  Equations from USGS Bulletin 1532 
        East Longitudes are positive, West longitudes are negative. 
        North latitudes are positive, South latitudes are negative
        Lat and Long are in decimal degrees. 
        Written by Chuck Gantz- chuck.gantz@globalstar.com
        Converted to Python by Russ Nelson <nelson@crynwr.com>
        '''
        half_accuracy = accuracy/2.
        easting = (easting*accuracy) + half_accuracy
        northing = (northing*accuracy) + half_accuracy
        
        ReferenceEllipsoid = 23
        k0 = 0.9996
        a = UTMConverter._ellipsoid[ReferenceEllipsoid]\
                                            [UTMConverter._EquatorialRadius]
        eccSquared = UTMConverter._ellipsoid[ReferenceEllipsoid]\
                                            [UTMConverter._eccentricitySquared]
        e1 = (1-sqrt(1-eccSquared))/(1+sqrt(1-eccSquared))
        #NorthernHemisphere; //1 for northern hemispher, 0 for southern
    
        x = easting - 500000.0 #remove 500,000 meter offset for longitude
        y = northing
    
        ZoneLetter = zone[-1]
        ZoneNumber = int(zone[:-1])
        if ZoneLetter >= 'N':
            NorthernHemisphere = 1  # point is in northern hemisphere
        else:
            NorthernHemisphere = 0  # point is in southern hemisphere
            y -= 10000000.0         
            # remove 10,000,000 meter offset used for southern hemisphere
    
        LongOrigin = (ZoneNumber - 1)*6 - 180 + 3  
            # +3 puts origin in middle of zone
    
        eccPrimeSquared = (eccSquared)/(1-eccSquared)
    
        M = y / k0
        mu = M/(a*(1-eccSquared/4-3*eccSquared*eccSquared/64-5*eccSquared*\
                                                    eccSquared*eccSquared/256))
    
        phi1Rad = (mu + (3*e1/2-27*e1*e1*e1/32)*sin(2*mu) 
                + (21*e1*e1/16-55*e1*e1*e1*e1/32)*sin(4*mu)
                +(151*e1*e1*e1/96)*sin(6*mu))
        phi1 = phi1Rad*UTMConverter._rad2deg;
    
        N1 = a/sqrt(1-eccSquared*sin(phi1Rad)*sin(phi1Rad))
        T1 = tan(phi1Rad)*tan(phi1Rad)
        C1 = eccPrimeSquared*cos(phi1Rad)*cos(phi1Rad)
        R1 = a*(1-eccSquared)/pow(1-eccSquared*sin(phi1Rad)*sin(phi1Rad), 1.5)
        D = x/(N1*k0)
    
        Lat = phi1Rad - (N1*tan(phi1Rad)/R1)*(D*D/2-(5+3*T1+10*C1-4*C1*\
                                            C1-9*eccPrimeSquared)*D*D*D*D/24
                +(61+90*T1+298*C1+45*T1*T1-252*eccPrimeSquared-3*C1*C1)*D*D*D*\
                                                                    D*D*D/720)
        Lat = Lat * UTMConverter._rad2deg
    
        Long = (D-(1+2*T1+C1)*D*D*D/6+(5-2*C1+28*T1-3*C1*C1+8*eccPrimeSquared+\
                                                                    24*T1*T1)
            *D*D*D*D*D/120)/cos(phi1Rad)
        Long = LongOrigin + Long * UTMConverter._rad2deg
        return (Lat, Long)
    
    @staticmethod
    def getUTMIdFromLatLong(Lat, Long, accuracy = 1):
        ''' Returns UTM id corresponding to the point = [latitude, longitude]
        at the accuracy specified.
        '''
        UTMZone, UTMEasting, UTMNorthing = UTMConverter.LLtoUTM(Lat,
                                                                Long,
                                                                accuracy)
        return '%s_%dE_%dN'%(UTMZone, UTMEasting, UTMNorthing)
        
    @staticmethod
    def getLatLongFromUTMId(UTMId, accuracy = 1):
        ''' Returns lat long corresponding to a UTM id.
        '''
        UTMZone, UTMEasting, UTMNorthing = UTMId.split('_')
        UTMEasting = float(UTMEasting[:-1])
        UTMNorthing = float(UTMNorthing[:-1])
        return UTMConverter.UTMtoLL(UTMZone, UTMEasting, UTMNorthing, accuracy)
    
    @staticmethod
    def getUTMIdInLatLongFormFromLatLong(Lat, Long, accuracy = 1):
        ''' Returns UTM id corresponding to the point = [latitude, longitude]
        at the accuracy specified.
        '''
        UTMZone, UTMEasting, UTMNorthing = UTMConverter.LLtoUTM(Lat,
                                                                Long,
                                                                accuracy)
        return '%s_%s'%UTMConverter.UTMtoLL(UTMZone,
                                            UTMEasting,
                                            UTMNorthing,
                                            accuracy) +\
                '_%s'%accuracy
    @staticmethod
    def getAccuracyFromUTMIdInLatLongForm(utm_id):
        _,_,accuracy = utm_id.split('_')
        return float(accuracy)
    @staticmethod
    def getLatLongUTMIdInLatLongForm(utm_id):
        lat, long, _ = utm_id.split('_')
        return float(lat), float(long)

    
#print breakIntoLattice([[0,-10], [10,0]], [2,2])
#getLatticeBoundingBoxFor([[0,-10], [10,0]], [2,2], [2.5, -7.5])
#print convertRadiansToMiles(49-24)
#print getLatticeLid([30.436834,-98.242493], 0.725)
#print getLatticeLid([30.259067,-97.695923], 0.725)
#print getLatticeLid([3.141545,101.691685], 0.725)
#print getLattice([37.073,-122.640381])
#print getHaversineDistance([0., 1.45], [0.,0.])
#print getHaversineDistance([37.699999999999996, -122.23499999999999], [37.700000000000003, -122.235])
#print getCenterOfMass([[-115.303551,36.181283],[-115.297509,36.181283],[-115.297509,36.186214],[-115.303551,36.186214]], error=True, accuracy=0.5)
#print getHaversineDistance((33.747123999999999, -84.379047), (33.747124669999998, -84.379047))
#print breakIntoLattice([[40.491, -74.356], [41.181, -72.612]], [250,100])[1:]

#print UTMConverter.getUTMIdFromLatLong(40.759202, -73.984654, accuracy=1000) #ts
#print UTMConverter.getUTMIdFromLatLong(40.750435,-73.993512, accuracy=1000) #msq
#print UTMConverter.getUTMIdFromLatLong(40.748492,-73.985585, accuracy=1000) #es
#print UTMConverter.getUTMIdFromLatLong(40.779827,-73.967091, accuracy=1000) #cp


