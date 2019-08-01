from Star import Star

class Constellation(object):
    def __init__(self, family, starsInfo):
        self.family = family
        self.fullName = ""
        self.abbrev = ""
        
        self.manualVisible = True
        self.externalConstellations = []
        
        self.stars = []
        self.lines = []
        self.foreignStars = []
        self.incomingLines = []
        self.outgoingLines = []
        self.numStars = 0
        self.numForeignStars = 0
        
        self.parseStarsInfo(starsInfo)
    
    def parseStarsInfo(self, starsInfo):
        nameInfo = starsInfo[0][0] # "fullName (abbrev) [externalConstellations]"
        
        self.fullName = (nameInfo.split("("))[0] # "fullName "
        self.fullName = (self.fullName)[:-1] # "fullName"
        self.abbrev = extractBetweenChars(nameInfo, "(", ")")
        if len(starsInfo)==1: # no stars
            return
        if "[" in nameInfo: # has some of its own stars in external Constellations
            self.externalConstellations = \
                (extractBetweenChars(nameInfo, "[", "]")).split(" ")
        
        starsInfo.pop(0) # these...
        starsInfo.pop(0) # ...remove the heading
        
        for i in range(len(starsInfo)):
            # print(starsInfo[i])
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
            star = Star(names, self.abbrev, RA, dec, visMag, specClass)
            if starsInfo[i][0][0] != "^": # normal star
                self.stars.append(star)
                self.numStars += 1
            else: # foreign star
                self.foreignStars.append(star)
                self.numForeignStars += 1
    
    def setManualVisibile(self, boolean):
        self.manualVisible = boolean
        for star in self.stars:
            star.setManualVisible(boolean)
    
    def update(self, data):
        for star in self.stars:
            star.updatePosition(data)
        for star in self.foreignStars:
            star.updatePosition(data)
    
    def draw(self, data, canvas):
        for star in self.stars:
            star.draw(data, canvas)
        for star in self.foreignStars:
            star.draw(data, canvas)
        
        

def extractBetweenChars(str, frontChar, backChar):
    frontIndex = str.index(frontChar)
    backIndex = str.index(backChar)
    return str[frontIndex+1:backIndex]
