import math

class Star():
    def __init__(self, names, constellation, RA, dec, visMag, specClass):
        self.commonName = ""
        self.bayer = ""
        self.constellation = constellation
        self.initializeNames(names)
        
        self.RA = RA
        self.dec = dec
        self.visMag = visMag
        self.specClass = specClass
        
        self.manualVisible = True
        self.positionVisible = (RA[0] < 6) or (RA[0] > 18)
        
        self.radius = 5 - 0.7*self.visMag
        self.color = specClassToColor(specClass)
        
        # initialize coordinates
        self.RAAngle = RAToRadians(RA) + math.pi/2
        self.decAngle = decToRadians(dec)
        self.initialX = math.cos(self.decAngle) * math.cos(self.RAAngle)
        self.initialY = math.cos(self.decAngle) * math.sin(self.RAAngle)
        self.initialZ = math.sin(self.decAngle)
        self.x = self.initialX
        self.y = self.initialY
        self.z = self.initialZ
    
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
                                  data.xyAngle, data.yzAngle, data.xzAngle)
        self.x = newPoint[0]
        self.y = newPoint[1]
        self.z = newPoint[2]
        if self.y<=0:
            self.positionVisible = False
        else:
            self.positionVisible = True
    
    def draw(self, data, canvas):
        if not (self.manualVisible and self.positionVisible):
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
        return rgbString(149,175,255) # blue
    elif letter=="B":
        return rgbString(191,207,255) # blue-white
    elif letter=="A":
        return rgbString(223,232,255) # white
    elif letter=="F":
        return rgbString(255,255,255) # yellow-white
    elif letter=="G":
        return rgbString(255,255,191) # yellow
    elif letter=="K":
        return rgbString(255,218,181) # orange
    elif letter=="M":
        return rgbString(255,186,117) # red


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

def applyRotations(x, y, z, xyAngle, yzAngle, xzAngle):
    x,y = (x*math.cos(xyAngle) - y*math.sin(xyAngle)), \
          (x*math.sin(xyAngle) + y*math.cos(xyAngle))
    y,z = (y*math.cos(yzAngle) - z*math.sin(yzAngle)), \
          (y*math.sin(yzAngle) + z*math.cos(yzAngle))
    x,z = (x*math.cos(xzAngle) - z*math.sin(xzAngle)), \
          (x*math.sin(xzAngle) + z*math.cos(xzAngle))
    return (x,y,z)


# a = Star("^Canopus, α Car, Car", "UMi", [0,0,0], [1,0,0,0], 0, "G")
# print(a.commonName)
# print(a.bayer)
# print(a.constellation)

