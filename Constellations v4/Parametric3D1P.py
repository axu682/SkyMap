import math
import copy

class Parametric3D1P(object):
    def __init__(self, data, xOfT, yOfT, zOfT, tMin, tMax, tStep):
        self.xOfT = xOfT
        self.yOfT = yOfT
        self.zOfT = zOfT
        self.tMin = tMin
        self.tMax = tMax
        self.tStep = tStep
        
        self.initialPoints = []
        self.points = []
        self.initializePoints()
        self.updatePoints(data)
        
        self.manualVisible = True
        self.hideNegativeY = True
        self.isLoop = True
        
        self.width = data.gridLineWidth
        self.color = data.gridLineColor
    
    def initializePoints(self):
        tCurrent = self.tMin
        while tCurrent < self.tMax:
            x = (self.xOfT)(tCurrent)
            y = (self.yOfT)(tCurrent)
            z = (self.zOfT)(tCurrent)
            self.initialPoints.append([tCurrent, x, y, z])
            self.points.append([x, y, z])
            tCurrent += self.tStep
        x = (self.xOfT)(self.tMax)
        y = (self.yOfT)(self.tMax)
        z = (self.zOfT)(self.tMax)
        self.initialPoints.append([self.tMax, x, y, z])
        self.points.append([x, y, z])
    
    def updatePoints(self, data):
        xyAngle = data.xyAngle
        yzAngle1 = data.yzAngle
        xzAngle = data.xzAngle
        yzAngle2 = data.headTiltAngle
        for i in range(len(self.points)):
            x = self.initialPoints[i][1]
            y = self.initialPoints[i][2]
            z = self.initialPoints[i][3]
            newPoint = applyRotations(x, y, z, xyAngle, yzAngle1, xzAngle, yzAngle2)
            newX = newPoint[0]
            newY = newPoint[1]
            newZ = newPoint[2]
            self.points[i][0] = newX
            self.points[i][1] = newY
            self.points[i][2] = newZ
    
    def draw(self, data, canvas):
        for i in range(len(self.points) - 1):
            self.drawLine(self.points[i], self.points[i+1], data, canvas)
        if self.isLoop:
            self.drawLine(self.points[-1], self.points[0], data, canvas)
    
    def drawLine(self, point1, point2, data, canvas):
        if self.hideNegativeY and \
            ((point1[1] < 0) or (point2[1] < 0)):
            # at least one point is hidden
            return
        if not self.manualVisible: return
        R = data.skyRadius
        originX = data.skyOriginX
        originY = data.skyOriginY
        x1 = originX + R*point1[0]
        y1 = originY - R*point1[2]
        x2 = originX + R*point2[0]
        y2 = originY - R*point2[2]
        canvas.create_line((x1,y1), (x2,y2), \
            width=self.width, fill=self.color)


# class ParametricHorizon3D1P(Parametric3D1P):
#     def __init__(self, data, xOfT, yOfT, zOfT, tMin, tMax, tStep):
#         self.initialPoints = []
#         self.points = []
#         self.initializePoints(data, xOfT, yOfT, zOfT, tMin, tMax, tStep)
#         self.updatePoints(data)
#         
#         self.manualVisible = True
#         self.hideNegativeY = False
#         self.isLoop = False
#         
#         self.width = 1
#         self.tStep = tStep
#         self.color = data.horizonColor
#         self.horizonHeight = - math.cos(data.headTiltAngle)
#      
#     def initializePoints(self, data, xOfT, yOfT, zOfT, tMin, tMax, tStep):
#         tCurrent = tMin
#         while tCurrent < tMax:
#             x = (xOfT)(tCurrent)
#             y = (yOfT)(tCurrent)
#             z = (zOfT)(tCurrent)
#             self.initialPoints.append([tCurrent, x, y, z])
#             self.points.append([x, y, z])
#             tCurrent += tStep
#         x = (xOfT)(tMax)
#         y = (yOfT)(tMax)
#         z = (zOfT)(tMax)
#         self.initialPoints.append([tCurrent, x, y, z])
#         self.points.append([x, y, z])
#     
#     def updatePoints(self, data):
#         self.horizonHeight = - math.cos(data.headTiltAngle)
#         for i in range(len(self.points)):
#             z = self.initialPoints[i][3] * self.horizonHeight
#             self.points[i][2] = z

class SolidHorizon(object):
    def _init__(self):
        pass
    
    def draw(self, data, canvas):
        lo = int(data.skyOriginX - data.skyRadius) + 1
        hi = int(data.skyOriginX + data.skyRadius) + 1
        for i in range(lo, hi+1):
            bottom = canvasToCoorX(i, data)
            if bottom < -1: bottom = -1
            elif bottom > 1 : bottom = 1
            top = bottom
            bottom = - math.sqrt(1-bottom**2)
            bottom = coorToCanvasY(bottom, data)
            
            top = math.sqrt(1-top**2) * (- math.cos(data.headTiltAngle))
            top = coorToCanvasY(top, data)
            
            canvas.create_line((i,bottom), (i,top), fill=data.horizonColor)



####################################
## HELPER FUNCTIONS
####################################

def applyRotations(x, y, z, xyAngle, yzAngle1, xzAngle, yzAngle2):
    x,y = (x*math.cos(xyAngle) - y*math.sin(xyAngle)), \
          (x*math.sin(xyAngle) + y*math.cos(xyAngle))
    y,z = (y*math.cos(yzAngle1) - z*math.sin(yzAngle1)), \
          (y*math.sin(yzAngle1) + z*math.cos(yzAngle1))
    x,z = (x*math.cos(xzAngle) - z*math.sin(xzAngle)), \
          (x*math.sin(xzAngle) + z*math.cos(xzAngle))
    y,z = (y*math.cos(yzAngle2) - z*math.sin(yzAngle2)), \
          (y*math.sin(yzAngle2) + z*math.cos(yzAngle2))
    return (x,y,z)

def coorToCanvasAxis(pointXZ, data):
    x = data.skyOriginX + data.skyRadius*pointXZ[0]
    y = data.skyOriginY - data.skyRadius*pointXZ[1]
    return (x,y)

def canvasToCoorAxis(pointXY, data):
    x = (pointXY[0] - data.skyOriginX) / data.skyRadius
    z = - (pointXY[1] - data.skyOriginY) / data.skyRadius
    return (x,z)

def coorToCanvasX(x, data):
    return data.skyOriginX + data.skyRadius*x

def canvasToCoorX(x, data):
    return (x - data.skyOriginX) / data.skyRadius

def coorToCanvasY(x, data):
    return data.skyOriginX - data.skyRadius*x

def canvasToCoorY(x, data):
    return - (x - data.skyOriginX) / data.skyRadius