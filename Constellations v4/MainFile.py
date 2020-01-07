# Updated Animation Starter Code from 15-112

from tkinter import *
# import random
import math
import time
from Star import Star
from Constellation import Constellation
from ConstellationFamily import ConstellationFamily
from Parametric3D1P import *
from TimeAndDate import TimeAndDate
from InputNumberBox import InputNumberBox
from Cardinal import Cardinal

class Struct(object): pass

def init(data):
    data.mode = "sky"
    data.theme = "dark"
    data.colorfulStars = True
    
    # on-screen dimensions
    data.skyOriginX = data.width/2
    data.skyOriginY = data.height/2
    data.skyRadius = 300
    data.edgeWidth = 10
    data.edgeColor = rgbString(170,170,170)
    
    data.maxVisMag = 4
    
    # to determine angle
    data.xzDeg = 0
    data.headTiltDeg = 0
    data.vernalEquinox = TimeAndDate(2019,3,20, 21,58,0)
    data.currentTimeAndDate = TimeAndDate(2019,10,5, 1,0,0)
    data.siderealDay = 23*3600 + 56*60 + 4.1
    data.orbitalPeriod = 365.256363004 * 86400
    data.referenceLongitude = getReferenceLongitude(data)
    
    data.latitude = 38.6998
    data.longitude = -79.5328
    
    data.longIncrement = 10
    data.latIncrement = 10
    data.xzIncrement = 10
    data.headTiltIncrement = 10
    data.timeIncrement = 0*86400 + 0*3600 + 30*60 + 0
    data.dayIncrement = 1*86400 + 0*3600 + 0*60 + 0
    
    data.xyAngle = 0
    data.yzAngle = 0
    data.xzAngle = 0
    data.headTiltAngle = 0
    
    # constellation info    
    data.constellationLineWidth = 2
    data.constellationDarkLineColor = rgbString(61,32,128)
    data.constellationLightLineColor = rgbString(180,180,180)
    data.constellationFamilies = {}
    
    loadData(data)
    
    # grid info
    data.gridLineWidth = 1
    data.gridLineColor = rgbString(90,90,90)
    
    data.linesOfRA = []
    data.linesOfDec = []
    data.linesOfRADecStep = math.pi/30
    data.numLinesOfRA = 12
    data.numLinesOfDec = 3 # number above equator, 90deg being degenerate
    
    fillLinesOfRA(data)
    fillLinesOfDec(data)
    
    # horizon info
    data.horizonStep = 0.02
    data.horizonColor = rgbString(225,225,225)
    data.horizon = SolidHorizon()
    
    # cardinals
    data.cardinals = []
    getCardinals(data)
    data.cardinalColor = rgbString(200,200,200)
    data.cardinalRadius = 10
    data.cardinalTextColor = "black"
    
    data.inputNumberBoxes = []
    data.currentBox = None
    initializeInputNumberBoxes(data)
    # event delay to prevent stack and recursion overflow
    data.eventDelay = 0.065
    data.lastTime = 0
    
    updateAngles(data)
    update(data)

def mousePressed(event, data):
    data.lastTime = time.time()
    if data.mode=="sky":
        for box in data.inputNumberBoxes:
            if box.inOriginBox(event):
                data.currentBox = box
                if box.label=="Lat":
                    box.inputs = numToList(data.latitude)
                    box.cursorPosition = len(box.inputs)
                    data.mode = "inputNumberBox"
                    data.eventDelay = 0
                if box.label=="Long":
                    box.inputs = numToList(data.longitude)
                    box.cursorPosition = len(box.inputs)
                    data.mode = "inputNumberBox"
                    data.eventDelay = 0

def mouseHeld(event, data):
    pass


def keyPressed(event, data):
    print(event.keysym)
    data.lastTime = time.time()
    if data.mode=="inputNumberBox":
        data.eventDelay = 0
        res = data.currentBox.keyPressed(event, data)
        if res!=None:
            if data.currentBox.label=="Lat":
                data.latitude = res
            if data.currentBox.label=="Long":
                data.longitude = res
    
    elif data.mode=="sky":
        # if event.keysym=="u":
        #     data.mode = "inputNumberBox"
        if event.keysym=="Left":
            data.longitude = ((data.longitude+180) + data.longIncrement) % 360 - 180
        elif event.keysym=="Right":
            data.longitude = ((data.longitude+180) - data.longIncrement) % 360 - 180
        elif event.keysym=="Up":
            data.latitude += data.latIncrement
            if data.latitude > 90: data.latitude = 90
        elif event.keysym=="Down":
            data.latitude -= data.latIncrement
            if data.latitude < -90:
                data.latitude = -90
        elif event.keysym=="period":
            data.xzDeg = (data.xzDeg + data.xzIncrement) % 360
            data.xzAngle = data.xzDeg/360 * (2*math.pi)
        elif event.keysym=="slash":
            data.xzDeg = (data.xzDeg - data.xzIncrement) % 360
            data.xzAngle = data.xzDeg/360 * (2*math.pi)
        elif event.keysym=="h":
            data.headTiltDeg += data.headTiltIncrement
            if data.headTiltDeg > 180: data.headTiltDeg = 180
            data.headTiltAngle = data.headTiltDeg/360 * (2*math.pi)
        elif event.keysym=="n":
            data.headTiltDeg -= data.headTiltIncrement
            if data.headTiltDeg < 0: data.headTiltDeg = 0
            data.headTiltAngle = data.headTiltDeg/360 * (2*math.pi)
        elif event.keysym=="a":
            data.currentTimeAndDate.secondForm -= data.timeIncrement
            data.currentTimeAndDate.setFromSecondForm()
        elif event.keysym=="d":
            data.currentTimeAndDate.secondForm += data.timeIncrement
            data.currentTimeAndDate.setFromSecondForm()
        elif event.keysym=="z":
            data.currentTimeAndDate.secondForm -= data.dayIncrement
            data.currentTimeAndDate.setFromSecondForm()
        elif event.keysym=="c":
            data.currentTimeAndDate.secondForm += data.dayIncrement
            data.currentTimeAndDate.setFromSecondForm()
    
    updateAngles(data)
    update(data)


def redrawAll(canvas, data):
    if data.mode=="inputNumberBox":
        data.currentBox.redrawAll(canvas, data)
    elif data.mode=="sky":
        printStatus(data)
        if data.theme=="dark": color = "black"
        else: color = "white"
        canvas.create_rectangle((0,0), (data.width,data.height), fill=color, width=0)
        
        R = data.skyRadius
        originX = data.skyOriginX
        originY = data.skyOriginY
        edge = data.edgeWidth
        
        canvas.create_oval((originX-R-edge,originY-R-edge), (originX+R+edge,originY+R+edge), \
            fill=data.edgeColor, width=0)
        canvas.create_oval((originX-R,originY-R), (originX+R,originY+R), \
            fill=color, width=0)
        data.horizon.draw(data, canvas)
        
        for lineOfRA in data.linesOfRA:
            lineOfRA.draw(data, canvas)
        for lineOfDec in data.linesOfDec:
            lineOfDec.draw(data, canvas)
        
        for cardinal in data.cardinals:
            cardinal.draw(data, canvas)
        
        for constellationFamily in (data.constellationFamilies).values():
            constellationFamily.draw(data, canvas)
        
        if data.theme=="dark": color = "white"
        else: color = "black"
        canvas.create_text((0,0), anchor="nw", text=getStatus(data), font="Courier 10", fill=color)
        
        for box in data.inputNumberBoxes:
            box.drawOriginBox(canvas, data)



####################################
## HELPER FUNCTIONS
####################################

def updateAngles(data):
    relativeLongitude = data.longitude - data.referenceLongitude
    relativeXYAngle1 = - math.radians(relativeLongitude)
    relativeTime = TimeAndDate.secondsBetweenTimeAndDates(data.vernalEquinox, data.currentTimeAndDate)
    relativeXYAngle2 = - ((relativeTime % data.siderealDay) / data.siderealDay) * (2*math.pi)
    data.xyAngle = relativeXYAngle1 + relativeXYAngle2
    
    data.yzAngle = - math.radians(data.latitude)
    
    data.xzAngle = math.radians(data.xzDeg)
    
    data.headTiltAngle = math.radians(data.headTiltDeg)

def update(data):
    for lineOfRA in data.linesOfRA:
        lineOfRA.updatePoints(data)
    for lineOfDec in data.linesOfDec:
        lineOfDec.updatePoints(data)
    for constellationFamily in (data.constellationFamilies).values():
        constellationFamily.update(data)
    for cardinal in data.cardinals:
        cardinal.updatePosition(data)

def printStatus(data):
    print("Latitude: %f" % data.latitude)
    print("Longitude: %f" % data.longitude)
    print(data.currentTimeAndDate)

def getStatus(data):
    str = "Lat: %f\nLong: %f\n" % (data.latitude, data.longitude)
    str += data.currentTimeAndDate.toString()
    return str

def getTime(data):
    h = data.currentTime.hour
    m = data.currentTime.minute
    s = data.currentTime.second
    res = str(h).rjust(2, "0")
    res += ":"
    res += str(m).rjust(2, "0")
    res += ":"
    res += str(round(s, 3))
    return res


####################################
## ONE-TIME HELPER FUNCTIONS
####################################

def loadData(data):
    s = readFile("ZodiacInfo.txt")
    data.constellationFamilies["Zodiac"] = ConstellationFamily(data, "Zodiac", s)
    s = readFile("UrsaMajorInfo.txt")
    data.constellationFamilies["Ursa Major"] = ConstellationFamily(data, "Ursa Major", s)
    s = readFile("PerseusInfo.txt")
    data.constellationFamilies["Perseus"] = ConstellationFamily(data, "Perseus", s)
    s = readFile("HerculesInfo.txt")
    data.constellationFamilies["Hercules"] = ConstellationFamily(data, "Hercules", s)
    s = readFile("OrionInfo.txt")
    data.constellationFamilies["Orion"] = ConstellationFamily(data, "Orion", s)
    s = readFile("HeavenlyWatersInfo.txt")
    data.constellationFamilies["Heavenly Waters"] = ConstellationFamily(data, "Heavenly Waters", s)
    s = readFile("BayerInfo.txt")
    data.constellationFamilies["Bayer"] = ConstellationFamily(data, "Bayer", s)
    s = readFile("LaCailleInfo.txt")
    data.constellationFamilies["La Caille"] = ConstellationFamily(data, "La Caille", s)

def getLineOfRA(data, RA, tStep):
    RAAngle = RAToRadians(RA) + math.pi/2
    xOfT = lambda t : math.cos(RAAngle) * math.cos(t)
    yOfT = lambda t : math.sin(RAAngle) * math.cos(t)
    zOfT = lambda t : math.sin(t)
    tMin = 0
    tMax = 2*math.pi - tStep
    return Parametric3D1P(data, xOfT, yOfT, zOfT, tMin, tMax, tStep)

def getLineOfDec(data, dec, tStep):
    decAngle = decToRadians(dec)
    xOfT = lambda t : math.cos(decAngle) * math.cos(t)
    yOfT = lambda t : math.cos(decAngle) * math.sin(t)
    zOfT = lambda t : math.sin(decAngle)
    tMin = 0
    tMax = 2*math.pi - tStep
    return Parametric3D1P(data, xOfT, yOfT, zOfT, tMin, tMax, tStep)

def fillLinesOfRA(data):
    if data.numLinesOfRA==0:
        return
    interval = 24/data.numLinesOfRA
    for i in range(data.numLinesOfRA):
        data.linesOfRA.append(getLineOfRA(data, [i*interval,0,0], data.linesOfRADecStep))

def fillLinesOfDec(data):
    interval = 90/data.numLinesOfDec
    data.linesOfDec.append(getLineOfDec(data, [1,0,0,0], data.linesOfRADecStep))
    for i in range(data.numLinesOfDec - 1):
        data.linesOfDec.append(getLineOfDec(data, [1,(i+1)*interval,0,0], data.linesOfRADecStep))
    for i in range(data.numLinesOfDec - 1):
        data.linesOfDec.append(getLineOfDec(data, [-1,(i+1)*interval,0,0], data.linesOfRADecStep))

def getHorizon(data):
    xOfT = lambda t : t
    yOfT = lambda t : 0
    zOfT = lambda t : math.sqrt(1-t**2)
    tMin = -1
    tMax = 1
    tStep = data.horizonStep
    return ParametricHorizon3D1P(data, xOfT, yOfT, zOfT, tMin, tMax, tStep)

def getReferenceLongitude(data):
    eq = data.vernalEquinox
    eqSecondOfDay = TimeAndDate.timeToSecondOfDay(eq.hour, eq.minute, eq.second)
    if eqSecondOfDay >= 43200:
        secondsSinceLastNoon = eqSecondOfDay - 43200
    else:
        secondsSinceLastNoon = eqSecondOfDay + 43200
    
    # suppose the Earth is at vernal equinox. It is an overhead view above Sun-Earth system with Earth to the left of the sun
    # now suppose we rewind to last noon. Angles are relative to the center of Earth, with rightwards being 0
    # this assumes a perfectly circular orbit, which is valid for mean solar time
    orbitalPeriodsSinceLastNoon = secondsSinceLastNoon / data.orbitalPeriod
    longitude0AngleLastNoon = - 2*math.pi * orbitalPeriodsSinceLastNoon
    axisRotationsSinceLastNoon = secondsSinceLastNoon / data.siderealDay
    longitude0AngleNow = longitude0AngleLastNoon + (2*math.pi * axisRotationsSinceLastNoon)
    longitude0AngleNowDeg = longitude0AngleNow * 180 / math.pi
    return (180 - (longitude0AngleNowDeg-0)) % 360 - 180

def initializeInputNumberBoxes(data):
    dimensionData = Struct()
    
    dimensionData.labelFontSize = 10
    dimensionData.returnCorner1 = (0,0)
    dimensionData.returnCorner2 = (30,30)
    dimensionData.inputFontSize = 10
    dimensionData.textBoxLeft = 30
    
    dimensionData.originCorner1 = (770,0)
    dimensionData.originCorner2 = (800,30)
    data.inputNumberBoxes.append(InputNumberBox(-90, 90, True, True, 10, "decimal", "Lat", dimensionData))
    
    dimensionData.originCorner1 = (770,30)
    dimensionData.originCorner2 = (800,60)
    data.inputNumberBoxes.append(InputNumberBox(-180, 180, False, True, 10, "decimal", "Long", dimensionData))

def getCardinals(data):
    data.cardinals.append(Cardinal("N", 90))
    data.cardinals.append(Cardinal("NW", 45))
    data.cardinals.append(Cardinal("W", 0))
    data.cardinals.append(Cardinal("SW", 315))
    data.cardinals.append(Cardinal("S", 270))
    data.cardinals.append(Cardinal("SE", 225))
    data.cardinals.append(Cardinal("E", 180))
    data.cardinals.append(Cardinal("NE", 135))



####################################
## UTILITY FUNCTIONS
####################################

def readFile(path):
    with open(path, "rt", encoding='utf-8-sig') as f:
        return f.read()

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (int(red), int(green), int(blue))

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

def numToList(num):
    s = str(num)
    res = []
    maxDecimalPlaces = 6
    decimalPlace = None
    for i in range(len(s)):
        res.append(s[i])
        if decimalPlace==None and s[i]==".": decimalPlace = 0
        elif decimalPlace==None: pass
        else: decimalPlace += 1
        
        if decimalPlace==maxDecimalPlaces: return res
    return res

# def addRA(RA1, RA2):
#     # [h, m, s]
#     seconds1 = RA1[0]*3600 + RA1[1]*60 + RA1[2]
#     seconds2 = RA2[0]*3600 + RA2[1]*60 + RA2[2]
#     remainingSeconds = seconds1 + seconds2
#     hours = remainingSeconds/3600
#     hours = hours%24
#     remainingSeconds = remainingSeconds%3600
#     minutes = remainingSeconds/60
#     seconds = remainingSeconds%60
#     return [hours, minutes, seconds]

# def compareRA(RA1, RA2):
#     # [h,m,s]
#     seconds1 = RA1[0]*3600 + RA1[1]*60 + RA1[2]
#     seconds2 = RA2[0]*3600 + RA2[1]*60 + RA2[2]
#     if seconds1 < seconds2: return -1
#     elif seconds1 > seconds2: return 1
#     return 0

# def compareDec(dec1, dec2):
#     # [sign,deg,min,sec]
#     seconds1 = dec1[0] * (dec1[1]*3600 + dec1[2]*60 + dec1[3])
#     seconds2 = dec2[0] * (dec2[1]*3600 + dec2[2]*60 + dec2[3])
#     if seconds1 < seconds2: return -1
#     elif seconds1 > seconds2: return 1
#     return 0

####################################
## RUN FUNCTION
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        if time.time() - data.lastTime < data.eventDelay: return
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        if time.time() - data.lastTime < data.eventDelay: return
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    
    def mouseHeldWrapper(event, canvas, data):
        mouseHeld(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    # class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
                            mouseHeldWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800,800)
