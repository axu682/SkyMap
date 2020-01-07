import math

class Cardinal(object):
    def __init__(self, label, angle):
        # initialize coordinates
        self.initialX = math.cos(math.radians(angle))
        self.initialY = 0
        self.initialZ = math.sin(math.radians(angle))
        self.x = self.initialX
        self.y = self.initialY
        self.z = self.initialZ
        
        self.label = label
        
        self.manualVisible = True
        self.positionVisible = True
    
    def __repr__(self):
        return self.label
    
    def updatePosition(self, data):
        if not self.manualVisible: return
        newPoint = applyCardinalRotations(self.initialX, self.initialY, self.initialZ, \
                                  data.xzAngle, data.headTiltAngle)
        self.x = newPoint[0]
        self.y = newPoint[1]
        self.z = newPoint[2]
        if self.y<0: self.positionVisible = False
        else: self.positionVisible = True
        
    
    def draw(self, data, canvas):
        if not (self.manualVisible and self.positionVisible):
            return
        color = data.cardinalColor
        
        R = data.skyRadius
        originX = data.skyOriginX
        originY = data.skyOriginY
        x = self.x
        z = self.z
        r = data.cardinalRadius
        canvas.create_oval((originX+R*x-r,originY-R*z-r),
                           (originX+R*x+r,originY-R*z+r),
                           fill=color, width=0)
        canvas.create_text((originX+R*x,originY-R*z), anchor="center", text=self.label, fill=data.cardinalTextColor)


################################################################################
## HELPER FUNCTIONS
################################################################################

def applyCardinalRotations(x, y, z, xzAngle, yzAngle):
    x,z = (x*math.cos(xzAngle) - z*math.sin(xzAngle)), \
          (x*math.sin(xzAngle) + z*math.cos(xzAngle))
    y,z = (y*math.cos(yzAngle) - z*math.sin(yzAngle)), \
          (y*math.sin(yzAngle) + z*math.cos(yzAngle))
    return (x,y,z)