# Updated Animation Starter Code from 15-112

from tkinter import *
import random
import math
from Star import *
from Constellation import *
from ConstellationFamily import *


def init(data):
    data.skyOriginX = data.width/2
    data.skyOriginY = data.height/2
    data.skyRadius = 300
    data.lat = 0
    data.long = 0
    data.headTilt = 0
    data.xyAngle = 0
    data.yzAngle = 0
    data.xzAngle = 0
    data.maxVisMag = 4
    data.lineWidth = 2
    data.lineColor = rgbString(90,90,90)
    data.constellationFamilies = {}
    
    s = readFile("ZodiacInfo.txt")
    data.constellationFamilies["Zodiac"] = ConstellationFamily("Zodiac", s)
    s = readFile("UrsaMajorInfo.txt")
    data.constellationFamilies["Ursa Major"] = ConstellationFamily("Ursa Major", s)
    s = readFile("PerseusInfo.txt")
    data.constellationFamilies["Perseus"] = ConstellationFamily("Perseus", s)
    s = readFile("HerculesInfo.txt")
    data.constellationFamilies["Hercules"] = ConstellationFamily("Hercules", s)
    s = readFile("OrionInfo.txt")
    data.constellationFamilies["Orion"] = ConstellationFamily("Orion", s)
    s = readFile("HeavenlyWatersInfo.txt")
    data.constellationFamilies["Heavenly Waters"] = ConstellationFamily("Heavenly Waters", s)
    s = readFile("BayerInfo.txt")
    data.constellationFamilies["Bayer"] = ConstellationFamily("Bayer", s)
    s = readFile("LaCailleInfo.txt")
    data.constellationFamilies["La Caille"] = ConstellationFamily("La Caille", s)
    

def mousePressed(event, data):
    pass


def mouseHeld(event, data):
    data.cursorX = event.x
    data.cursorY = event.y


def keyPressed(event, data):
    if event.keysym=="Left":
        data.xyAngle -= 0.1
    elif event.keysym=="Right":
        data.xyAngle += 0.1
    elif event.keysym=="Up":
        data.yzAngle -= 0.1
    elif event.keysym=="Down":
        data.yzAngle += 0.1
    elif event.keysym=="period":
        data.xzAngle += 0.1
    elif event.keysym=="slash":
        data.xzAngle -= 0.1
    for constellationFamily in (data.constellationFamilies).values():
        constellationFamily.update(data)


def redrawAll(canvas, data):
    canvas.create_rectangle((0,0), (data.width,data.height), fill="black")
    R = data.skyRadius
    originX = data.skyOriginX
    originY = data.skyOriginY
    edge = 4
    canvas.create_oval((originX-R-edge,originY-R-edge), (originX+R+edge,originY+R+edge), \
        fill=data.lineColor, width=0)
    canvas.create_oval((originX-R,originY-R), (originX+R,originY+R), \
        fill="black", width=0, outline=data.lineColor)
    for constellationFamily in (data.constellationFamilies).values():
        constellationFamily.draw(data, canvas)


####################################
## HELPER FUNCTIONS
####################################

# def applyRotations(point, xyAngle, yzAngle, xzAngle):
#     x = point[0]
#     y = point[1]
#     z = point[2]
#     x,y = (x*math.cos(xyAngle) - y*math.sin(xyAngle)), \
#           (x*math.sin(xyAngle) + y*math.cos(xyAngle))
#     y,z = (y*math.cos(yzAngle) - z*math.sin(yzAngle)), \
#           (y*math.sin(yzAngle) + z*math.cos(yzAngle))
#     x,z = (x*math.cos(xzAngle) - z*math.sin(xzAngle)), \
#           (x*math.sin(xzAngle) + z*math.cos(xzAngle))
#     return [x,y,z]

def readFile(path):
    with open(path, "rt", encoding='utf-8-sig') as f:
        return f.read()

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (int(red), int(green), int(blue))


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
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    
    def mouseHeldWrapper(event, canvas, data):
        mouseHeld(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
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
