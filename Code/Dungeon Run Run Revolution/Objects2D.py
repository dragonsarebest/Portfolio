#class object collision lab Joshua Byron
import pygame
from myvector import *

def collides(shape1, shape2):
    """returns True or False to see if the objects are colliding"""
    return splitAxis(shape1, shape2)   

def splitAxis(shape1, shape2):
    """uses split axis theorem to find if two shapes are interseting"""
    axis = []
    if(isinstance(shape2, Cuboid)):
        axis.append(shape2.xAxis)
        axis.append(shape2.yAxis)
    if(isinstance(shape1, Cuboid)):
        axis.append(shape1.xAxis)
        axis.append(shape1.yAxis)
        
    for testAxis in axis:
        testAxis = testAxis.normalized
        range1 = []
        range2 = []
        for corner in shape2.corners:
            projectedPoint = dot(corner, testAxis)
            range2.append(projectedPoint)
            
        #shape1 is not a sphere
        for corner in shape1.corners:
            projectedPoint = dot(corner, testAxis)
            range1.append(projectedPoint)

        minRange1 = min(range1)
        maxRange1 = max(range1)
        minRange2 = min(range2)
        maxRange2 = max(range2)

        if(minRange1 >= maxRange2 or  minRange2 >= maxRange1):
            return False
        
    return True
        

def rotatePoint(origin, point, angle, radians = False):
    """Rotate a point counterclockwise by a given angle around a given origin. The angle should be given in radians."""
    ox, oy = origin
    px, py = point

    if(radians == False):
        qx = ox + math.cos(math.radians(angle)) * (px - ox) - math.sin(math.radians(angle)) * (py - oy)
        qy = oy + math.sin(math.radians(angle)) * (px - ox) + math.cos(math.radians(angle)) * (py - oy)
    else:
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return MyVector(qx, qy)
    
class Shape:
    """generic shape object"""
    def __init__(self, color, pos):
        """position of the axis, color of shape, and the rotation info for said axis"""
        self.mPos = pos
        self.color = color
        
        self.angle = 0
            
        self.xAxis = MyVector(1, 0)
        self.yAxis = self.xAxis.perpendicular

        self.isSelected = False
        self.corners = []
        

class Cuboid(Shape):
    """4 sided shape"""
    def __init__(self, color, pos, args):
        """creates a big boy with 4 corners"""
        Shape.__init__(self, color, pos)
        self.width = args.x
        self.height = args.y

        self.corners.append(self.mPos)
        self.corners.append(self.mPos+MyVector(self.width, 0))
        self.corners.append(self.mPos+MyVector(self.width, self.height))
        self.corners.append(self.mPos+MyVector(0, self.height))

        self.oldPos = self.mPos
        
    def drawPygame(self, surf, offsetx, offsety):
        """draws the rectangle"""
        temp = []
        for item in self.corners:
            temp.append(item-MyVector(offsetx,offsety))
        pygame.draw.polygon(surf, self.color, temp, 1)

    def changeDim(self, newDim):
        self.width = newDim.x
        self.height = newDim.y
        self.corners.append(self.mPos)
        self.corners.append(self.mPos+MyVector(self.width, 0))
        self.corners.append(self.mPos+MyVector(self.width, self.height))
        self.corners.append(self.mPos+MyVector(0, self.height))
        
    def pointInShape(self, mPos):
        """returns true if the position lies in this shape"""        
        localMousePos = mPos
        A = self.corners[0]
        B = self.corners[1]
        C = self.corners[2]
        D = self.corners[3]
        
        CD = C-D
        AD = A-D

        center = 2.0 * localMousePos - A - C
        
        return ((dot(C-D, center - CD) <= 0 and dot(C-D, center + CD) >= 0) and (dot(AD, center - AD) <= 0 and dot(AD, center + AD) >= 0))
 
