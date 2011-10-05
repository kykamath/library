'''
Created on Oct 4, 2011

@author: kykamath
'''
import datetime
import numpy as n

earthRadiusMiles = 3958.761
earthRadiusKMs = 6371.009

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