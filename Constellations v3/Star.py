import math

class Star():
    def __init__(self, data, names, constellation, RA, dec, visMag, specClass):
        self.commonName = ""
        self.bayer = "" # single letter
        self.constellation = constellation # abbreviation
        self.initializeNames(names)
        
        self.RA = RA # [h,m,s]
        self.dec = dec # [sign,deg,min,sec]
        self.visMag = visMag
        self.specClass = specClass
        
        self.radius = 5 - 0.7*self.visMag
        self.color = specClassToColor(specClass)
        
        # initialize coordinates
        RAAngle = RAToRadians(RA) + math.pi/2
        decAngle = decToRadians(dec)
        self.initialX = math.cos(decAngle) * math.cos(RAAngle)
        self.initialY = math.cos(decAngle) * math.sin(RAAngle)
        self.initialZ = math.sin(decAngle)
        self.x = self.initialX
        self.y = self.initialY
        self.z = self.initialZ
        
        self.manualVisible = True
        self.positionVisible = (compareRA(RA, [6,0,0]) == -1) or \
            (compareRA(RA, [18,0,0]) == 1)
        self.horizonVisible = self.aboveHorizon(data)
    
    def __repr__(self):
        return self.commonName
    
    def initializeNames(self, names):
        numOfCommas = names.count(",")
        if numOfCommas==0:
            # common name
            self.commonName = names
            if isBayer(names[0]):
                self.bayer = (names.split(" "))[0]
            else:
                self.bayer = None
        elif numOfCommas==1 and names[0]!="^":
            # common name, bayer name
            info = names.split(", ")
            self.commonName = info[0]
            self.bayer = ((info[1]).split(" "))[0]
        elif numOfCommas==1: # and names[0]=="^"
            # ^common name, original constellation
            info = names.split(", ")
            self.commonName = info[0][1:]
            self.bayer = None
            # foreign star, override constellation
            self.constellation = info[1]
        elif numOfCommas==2:
            # ^common name, bayer name(optional), original constellation
            info = names.split(", ")
            self.commonName = info[0][1:]
            self.bayer = ((info[1]).split(" "))[0]
            # foreign star, override constellation
            self.constellation = info[2]
    
    def setManualVisibile(self, boolean):
        self.manualVisible = boolean
    
    def updatePosition(self, data):
        if not self.manualVisible:
            return
        newPoint = applyRotations(self.initialX, self.initialY, self.initialZ, \
                                  data.xyAngle, data.yzAngle, data.xzAngle, data.headTiltAngle)
        self.x = newPoint[0]
        self.y = newPoint[1]
        self.z = newPoint[2]
        if self.y<=0: self.positionVisible = False
        else: self.positionVisible = True
        
        if self.aboveHorizon(data): self.horizonVisible = True
        else: self.horizonVisible = False
        
    
    def aboveHorizon(self, data):
        x = self.x
        if x < -1: x = -1
        elif x > 1: x = 1 # these are so sqrt works with values like 1.000001
        minZ = math.sqrt(1-x**2) * (- math.cos(data.headTiltAngle)) # equation of horizon
        if self.z < minZ: return False
        return True
        
    
    def draw(self, data, canvas):
        if not (self.manualVisible and self.positionVisible and self.horizonVisible):
            return
        R = data.skyRadius
        originX = data.skyOriginX
        originY = data.skyOriginY
        x = self.x
        z = self.z
        r = self.radius
        canvas.create_oval((originX+R*x-r,originY-R*z-r),
                           (originX+R*x+r,originY-R*z+r),
                           fill=self.color, width=0)


################################################################################
## HELPER FUNCTIONS
################################################################################

def isBayer(letter):
    if letter in "αβγδεζηθικλμνξοπρστυφχψω":
        return True
    if letter in "qwertyuiopasdfghjklzxcvbnm":
        return True
    return False

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (int(red), int(green), int(blue))

def specClassToColor(specClass):
    letter = specClass[0]
    if letter=="O":
        # return rgbString(149,175,255) # blue
        return rgbString(96,128,255) # blue
    elif letter=="B":
        # return rgbString(191,207,255) # blue-white
        return rgbString(149,175,255) # blue-white
    elif letter=="A":
        # return rgbString(223,232,255) # light blue-white white
        return rgbString(191,207,255) # light blue-white white
    elif letter=="F":
        return rgbString(255,255,255) # white
    elif letter=="G":
        # return rgbString(255,255,191) # yellow
        return rgbString(255,255,170) # yellow
    elif letter=="K":
        # return rgbString(255,218,181) # orange
        return rgbString(255,200,150) # orange
    elif letter=="M":
        # return rgbString(255,186,117) # red
        return rgbString(255,150,128) # red


def RAToRadians(RA):
    # right ascension to radians
    h = RA[0]
    m = RA[1]
    s = RA[2]
    rad = h/24*(2*math.pi)
    rad += m/(24*60)*(2*math.pi)
    rad += s/(24*60*60)*(2*math.pi)
    return rad

def decToRadians(dec):
    # declination to radians
    sign = dec[0]
    deg = dec[1]
    m = dec[2]
    s = dec[3]
    rad = deg/360*(2*math.pi)
    rad += m/(360*60)*(2*math.pi)
    rad += s/(360*60*60)*(2*math.pi)
    return sign*rad

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

def compareRA(RA1, RA2):
    # compare hours
    if RA1[0] > RA2[0]: return 1
    if RA1[0] < RA2[0]: return -1
    # compare minutes
    if RA1[1] > RA2[1]: return 1
    if RA1[1] < RA2[1]: return -1
    # compare seconds
    if RA1[2] > RA2[2]: return 1
    if RA1[2] < RA2[2]: return -1
    return 0

def coorToCanvasX(x, data):
    return data.skyOriginX + data.skyRadius*x

def canvasToCoorX(x, data):
    return (x - data.skyOriginX) / data.skyRadius

def coorToCanvasY(x, data):
    return data.skyOriginX - data.skyRadius*x

def canvasToCoorY(x, data):
    return - (x - data.skyOriginX) / data.skyRadius

# a = Star("^Canopus, α Car, Car", "UMi", [0,0,0], [1,0,0,0], 0, "G")
# print(a.commonName)
# print(a.bayer)
# print(a.constellation)

