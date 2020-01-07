from Star import Star

class Constellation(object):
    def __init__(self, data, family, starsInfo):
        self.family = family
        self.fullName = ""
        self.abbrev = ""
        
        self.noStars = False
        self.familyVisible = True
        self.constellationVisible = True
        self.externalConstellations = []
        
        self.stars = []
        self.lines = []
        self.foreignStars = []
        self.incomingLines = []
        self.outgoingLines = []
        self.numStars = 0
        self.numForeignStars = 0
        
        self.parseStarsInfo(data, starsInfo)
    
    def parseStarsInfo(self, data, starsInfo):
        nameInfo = starsInfo[0][0] # "fullName (abbrev) [externalConstellations]"
        
        self.fullName = (nameInfo.split("("))[0] # "fullName "
        self.fullName = (self.fullName)[:-1] # "fullName"
        self.abbrev = extractBetweenChars(nameInfo, "(", ")")
        
        if len(starsInfo)==1: # no stars
            self.noStars = True
            return
        if "[" in nameInfo: # has some of its own stars in external Constellations
            self.externalConstellations = \
                (extractBetweenChars(nameInfo, "[", "]")).split(" ")
        
        starsInfo.pop(0) # these...
        heading = starsInfo.pop(0) # ...remove the heading
        
        for i in range(len(starsInfo)):
            names = starsInfo[i][0]
            specClass = starsInfo[i][1]
            RAh = int(starsInfo[i][2])
            RAm = int(starsInfo[i][3])
            RAs = float(starsInfo[i][4])
            decSign = int(starsInfo[i][5])
            decDeg = int(starsInfo[i][6])
            decMin = int(starsInfo[i][7])
            decSec = float(starsInfo[i][8])
            visMag = float(starsInfo[i][9])
            RA = [RAh, RAm, RAs]
            dec = [decSign, decDeg, decMin, decSec]
            star = Star(data, names, self.abbrev, RA, dec, visMag, specClass)
            if starsInfo[i][0][0] != "^": # normal star
                self.stars.append(star)
                self.numStars += 1
            else: # foreign star
                self.foreignStars.append(star)
                self.numForeignStars += 1
        
        starsInfo.insert(0, heading) # this has necessary info for initializeLines
        self.initializeLines(starsInfo)
    
    def initializeLines(self, starsInfo):
        for col in range(11,17):
            numStarsInARow = int(starsInfo[0][col])
            if numStarsInARow==0: break
            currentRow = None
            for i in range(1, numStarsInARow):
                if currentRow == None:
                    currentRow = findInCol(starsInfo[1:], col, str(i))
                nextRow = findInCol(starsInfo[1:], col, str(i+1))
                
                if currentRow >= self.numStars: # incoming line
                    self.incomingLines.append((currentRow-self.numStars, nextRow))
                elif nextRow >= self.numStars: # outgoing line
                    self.outgoingLines.append((currentRow, nextRow-self.numStars))
                else: # normal line
                    self.lines.append((currentRow, nextRow))
                
                currentRow = nextRow
    
    def setFamilyVisibile(self, boolean):
        self.familyVisible = boolean
        for star in self.stars:
            star.setFamilyVisible(boolean)
    
    def setConstellationVisible(self, boolean):
        self.constellationVisible = boolean
        for star in self.stars:
            star.setConstellationVisible(boolean)
    
    def update(self, data):
        for star in self.stars:
            star.updatePosition(data)
        for star in self.foreignStars:
            star.updatePosition(data)
    
    def draw(self, data, canvas):
        if not (self.familyVisible and self.constellationVisible): return
        for line in self.lines:
            star1 = self.stars[line[0]]
            star2 = self.stars[line[1]]
            self.drawLine(star1, star2, data, canvas)
        for line in self.outgoingLines:
            star1 = self.stars[line[0]]
            star2 = self.foreignStars[line[1]]
            self.drawLine(star1, star2, data, canvas)
        for line in self.incomingLines:
            star1 = self.foreignStars[line[0]]
            star2 = self.stars[line[1]]
            self.drawLine(star1, star2, data, canvas)
        
        for star in self.stars:
            star.draw(data, canvas)
        for star in self.foreignStars:
            star.draw(data, canvas)
    
    def drawLine(self, star1, star2, data, canvas):
        if not (star1.manualVisible and star1.positionVisible and
            star2.manualVisible and star2.positionVisible): return
        R = data.skyRadius
        originX = data.skyOriginX
        originY = data.skyOriginY
        x1 = originX + R*star1.x
        y1 = originY - R*star1.z
        x2 = originX + R*star2.x
        y2 = originY - R*star2.z
        if data.theme=="dark": color = data.constellationDarkLineColor
        else: color = data.constellationLightLineColor
        canvas.create_line((x1,y1), (x2,y2), \
            width=data.constellationLineWidth, \
            fill=color)
        


################################################################################
## HELPER FUNCTIONS
################################################################################ 

def extractBetweenChars(str, frontChar, backChar):
    frontIndex = str.index(frontChar)
    backIndex = str.index(backChar)
    return str[frontIndex+1:backIndex]

def findInCol(array2D, col, target):
    for row in range(len(array2D)):
        if array2D[row][col] == target:
            return row
    return None

def findColMax(array2D, col):
    max = None
    for row in range(len(array2D)):
        current = array2D[row][col]
        if current=="": continue
        if max==None or int(current)>max:
            max = int(current)
    return max
