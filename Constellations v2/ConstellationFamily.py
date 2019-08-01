from Constellation import *

class ConstellationFamily(object):
    def __init__(self, name, constellationInfo):
        self.name = name
        self.constellations = {}
        self.numConstellations = 0
        
        self.manualVisible = True
        
        self.parseConstellationInfo(constellationInfo)
    
    def parseConstellationInfo(self, constellationInfo):
        constellationInfo = constellationInfo.split("\n")
        
        # clear whitespace at beginning and end
        while constellationInfo[0][0] == "\t":
            constellationInfo.pop(0)
        while constellationInfo[-1][0] == "\t":
            constellationInfo.pop[-1]
        
        while len(constellationInfo)>0:
            starsInfo = []
            while (len(constellationInfo) > 0 and \
                constellationInfo[0][0] != "\t"):
                starsInfo.append(constellationInfo.pop(0))
            for i in range(len(starsInfo)):
                starsInfo[i] = starsInfo[i].split("\t")
            abbrev = extractBetweenChars(starsInfo[0][0], "(", ")")
            constellation = Constellation(self.name, starsInfo)
            self.constellations[abbrev] = constellation
            self.numConstellations += 1
            
            if len(constellationInfo) > 0:
                # check is needed because there is no blank line at end
                constellationInfo.pop(0) # remove the blank line
    
    def setManualVisible(self, boolean):
        self.manualVisible = boolean
        for constellation in self.constellations:
            constellation.setManualVisible(boolean)
    
    def update(self, data):
        for constellation in (self.constellations).values():
            constellation.update(data)
    
    def draw(self, data, canvas):
        for constellation in (self.constellations).values():
            constellation.draw(data, canvas)



def extractBetweenChars(str, frontChar, backChar):
    frontIndex = str.index(frontChar)
    backIndex = str.index(backChar)
    return str[frontIndex+1:backIndex]
