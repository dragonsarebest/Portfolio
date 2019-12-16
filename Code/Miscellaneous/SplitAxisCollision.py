#class object collision lab Joshua Byron
import pygame
from vector import *

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
        
    if(isinstance(shape2, Triangle)):
        length = len(shape2.corners)
        for i in range(0, length):
            t = shape2.corners[i] - shape2.corners[(i+1)%length]
            temp = Vector(t.x, t.y, 0)
            temp = cross(temp, Vector(0,0,1))
            axis.append(Vector(temp.x, temp.y))
    if(isinstance(shape1, Triangle)):
        length = len(shape1.corners)
        for i in range(0, length):
            t = shape1.corners[i] - shape1.corners[(i+1)%length]
            temp = Vector(t.x, t.y, 0)
            temp = cross(temp, Vector(0,0,1))
            axis.append(Vector(temp.x, temp.y))

    if(isinstance(shape2, Sphere)):
        temp = (shape2.mPos - shape1.mPos).normalized
        axis.append(temp)
    if(isinstance(shape1, Sphere)):
        temp = (shape1.mPos - shape2.mPos).normalized
        axis.append(temp)
        
    for testAxis in axis:
        testAxis = testAxis.normalized
        range1 = []
        range2 = []
        if(not isinstance(shape2, Sphere)):
            #shape2 is not a sphere
            for corner in shape2.corners:
                projectedPoint = dot(corner, testAxis)
                range2.append(projectedPoint)
        else:
            #shape2 is a sphere
            temp = testAxis * shape2.radius + shape2.mPos
            temp2 = -testAxis * shape2.radius + shape2.mPos

            projectedPoint = dot(temp, testAxis)
            range2.append(projectedPoint)
            
            projectedPoint = dot(temp2, testAxis)
            range2.append(projectedPoint)
            
        if(not isinstance(shape1, Sphere)):
            #shape1 is not a sphere
            for corner in shape1.corners:
                projectedPoint = dot(corner, testAxis)
                range1.append(projectedPoint)
        else:
            #shape1 is a sphere
            temp = testAxis * shape1.radius + shape1.mPos
            temp2 = -testAxis * shape1.radius + shape1.mPos

            projectedPoint = dot(temp, testAxis)
            range1.append(projectedPoint)
            
            projectedPoint = dot(temp2, testAxis)
            range1.append(projectedPoint)

        minRange1 = min(range1)
        maxRange1 = max(range1)
        minRange2 = min(range2)
        maxRange2 = max(range2)

        if(minRange1 >= maxRange2 or  minRange2 >= maxRange1):
            return False
        
    return True
        
def drawArrow(surf, start, end, color, arrowSize = 6):
    """draws am arrow (used for axes)"""
    pygame.draw.line(surf, color, start, end)

    direction = (end - start).normalized
    perp_direction = direction.perpendicular

    left = end - arrowSize * direction + (arrowSize / 2) * perp_direction
    right = left - arrowSize * perp_direction
    pygame.draw.polygon(surf, color, (left, end, right))

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
    return Vector(qx, qy)
    
class Shape:
    """generic shape object"""
    def __init__(self, color, pos):
        """position of the axis, color of shape, and the rotation info for said axis"""
        self.mPos = pos
        self.color = color
        
        self.angle = 0
            
        self.xAxis = Vector2.rotate2D(Vector(1, 0), self.angle)
        self.yAxis = self.xAxis.perpendicular

        self.isSelected = False
        self.corners = []
        
    def drawPygame(self, surf, isSelected, isCollide):
        """draws the axis and position of the shape"""

        self.isSelected = isSelected
        pygame.draw.circle(surf, (255,255,255), self.mPos.i, 5)
        drawArrow(surf, self.mPos, self.mPos + 50 * self.xAxis, (255,255,255), 8)
        drawArrow(surf, self.mPos, self.mPos + 50 * self.yAxis, (255,255,255), 8)

   
    def rotate(self, angle):
        """rotates the axis of the shape by the given angle"""
        if(self.isSelected == False):
            self.angle += angle
            self.xAxis = Vector2.rotate2D(Vector(1, 0), -self.angle)
            self.yAxis = self.xAxis.perpendicular

            for i in range(0, len(self.corners)):
                self.corners[i] = rotatePoint(self.mPos, self.corners[i], -angle)

class Cuboid(Shape):
    """4 sided shape"""
    def __init__(self, color, pos, *args):
        """creates a big boy with 4 corners"""
        Shape.__init__(self, color, pos)
        self.width = args[0][0]
        self.height = args[0][1]
        
        self.corners.append(self.mPos-Vector(self.width//2, -self.height//2))
        self.corners.append(self.mPos-Vector(-self.width//2, -self.height//2))
        self.corners.append(self.mPos-Vector(-self.width//2, self.height//2))
        self.corners.append(self.mPos-Vector(self.width//2, self.height//2))

        self.oldPos = self.mPos
        
    def drawPygame(self, surf, isSelected, isCollide):
        """draws the rectangle"""
            
        if(isSelected == True):
            for i in range(0, len(self.corners)):
                self.corners[i] -= self.oldPos-self.mPos
            self.oldPos = self.mPos
        
        if(isCollide == True):
            pygame.draw.polygon(surf, (255,0,0), self.corners)
        else:
            pygame.draw.polygon(surf, self.color, self.corners)
        Shape.drawPygame(self, surf, isSelected, isCollide)
        
        
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
        
class Triangle(Shape):
    """3 sided shape"""
    def __init__(self, color, pos, *args):
        """creates a smaller boy with 3 corners"""
        Shape.__init__(self, color, pos)
        
        for i in range(0, len(args)):
            for item in args[i]:
                self.corners.append(item)
        
        self.oldPos = self.mPos

    def drawPygame(self, surf, isSelected, isCollide):
        """draws the triangle"""

        if(isSelected == True):
            for i in range(0, len(self.corners)):
                self.corners[i] -= self.oldPos-self.mPos
            self.oldPos = self.mPos
        
        if(isCollide == True):
            pygame.draw.polygon(surf, (255,0,0), self.corners)
        else:
            pygame.draw.polygon(surf, self.color, self.corners)
        Shape.drawPygame(self, surf, isSelected, isCollide)

    def SameSide(self, p1, p2, a, b):
        """returns true if the ponint lies between the two lines"""
        #similar to the "did the player turn left problem" if the point and corner c passed in are both in the same direction as b-a then it'll be true
        cp1 = cross(b-a, p1-a)
        cp2 = cross(b-a, p2-a)
        if (dot(cp1, cp2) >= 0):
            return True
        else:
            return False

    def pointInShape(self, mPos):
        """returns true if the position lies in this shape"""
        localMousePos = mPos
        A = self.corners[0]
        B = self.corners[1]
        C = self.corners[2]
        
        if(self.SameSide(localMousePos,A,B,C) and self.SameSide(localMousePos,B,A,C) and self.SameSide(localMousePos,C,A,B)):
            return True
        else:
            return False

    def getCenter(self):
        """gets the center of the triangle"""
        A = self.corners[0]
        B = self.corners[1]
        C = self.corners[2]
        return (A+B+C) / 3
    
class Sphere:
    """creates a circle"""
    def __init__(self, color, pos, radius):
        self.color = color
        self.mPos = pos
        self.radius = radius

        self.angle = 0
            
        self.xAxis = Vector2.rotate2D(Vector(1, 0), self.angle)
        self.yAxis = self.xAxis.perpendicular

        self.isSelected = False

    
    def rotate(self, angle):
        """rotates the axis of the shape by the given angle"""
        if(self.isSelected == False):
            self.angle += angle
            self.xAxis = Vector2.rotate2D(Vector(1, 0), -self.angle)
            self.yAxis = self.xAxis.perpendicular
            
            
    
    def drawPygame(self, surf, isSelected, isCollide):
        """draws the cirlce"""

        if(isSelected == True):
            pass
        
        self.isSelected = isSelected
        if(isCollide == True):
            pygame.draw.circle(surf, (255,0,0), self.mPos.i, self.radius)
        else:
            pygame.draw.circle(surf, self.color, self.mPos.i, self.radius)
        
        pygame.draw.circle(surf, (255,255,255), self.mPos.i, 5)
        drawArrow(surf, self.mPos, self.mPos + 50 * self.xAxis, (255,255,255), 8)
        drawArrow(surf, self.mPos, self.mPos + 50 * self.yAxis, (255,255,255), 8)

    def pointInShape(self, mPos):
        """returns true if the position lies in this shape"""
        if((mPos - self.mPos).magnitude <= self.radius):
            return True
        else:
            return False
        
