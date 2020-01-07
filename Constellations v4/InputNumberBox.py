import TimeAndDate

class InputNumberBox(object):
    def __init__(self, min, max, includeMin, includeMax, maxLength, numberType, label, dimensionData):
        self.min = min
        self.max = max
        self.includeMin = includeMin
        self.includeMax = includeMax
        self.maxLength = maxLength
        self.numberType = numberType
        self.label = label
        self.legalChars = self.getLegalChars()

        self.originCorner1 = dimensionData.originCorner1
        self.originCorner2 = dimensionData.originCorner2
        self.labelFontSize = dimensionData.labelFontSize
        
        self.returnCorner1 = dimensionData.returnCorner1
        self.returnCorner2 = dimensionData.returnCorner2
        self.inputFontSize = dimensionData.inputFontSize
        
        self.textBoxLeft = dimensionData.textBoxLeft
        
        self.inputs = []
        self.cursorPosition = 0
    
    def keyPressed(self, event, data):
        if event.keysym=="Return" and self.isValidInput():
            data.mode = "sky"
            return self.inputToNum()
        if event.keysym=="BackSpace": self.deleteChar()
        elif event.keysym=="Left": self.moveCursor(self, self.cursorPosition - 1)
        elif event.keysym=="Right": self.moveCursor(self, self.cursorPosition + 1)
        elif (len(self.inputs) < self.maxLength) and (event.char in self.legalChars):
            self.inputs.insert(self.cursorPosition, event.char)
            self.cursorPosition += 1
    
    def redrawAll(self, canvas, data):
        cursorHeight = self.inputFontSize
        canvas.create_line((self.textBoxLeft + self.cursorPosition*self.inputFontSize*0.8, data.height/2 - cursorHeight/2),
            (self.textBoxLeft + self.cursorPosition*self.inputFontSize*0.8, data.height/2 + cursorHeight/2))
        canvas.create_text((self.textBoxLeft, data.height/2), anchor="w", text=self.inputToString(), font="Courier "+str(self.inputFontSize))
    
    def drawOriginBox(self, canvas, data):
        canvas.create_rectangle(self.originCorner1, self.originCorner2, fill="light gray", width=1)
    
    def inOriginBox(self, event):
        if (self.originCorner1[0] <= event.x <= self.originCorner2[0]) and \
           (self.originCorner1[1] <= event.y <= self.originCorner2[1]): return True
        return False
    
    def getLegalChars(self):
        if self.numberType=="positiveInt": return "1234567890"
        elif self.numberType=="int": return "1234567890-"
        elif self.numberType=="positiveDecimal": return "1234567890."
        elif self.numberType=="decimal": return "1234567890-."
        print("invalid numberType")
        assert(False)
    
    def moveCursor(self, position):
        if 0 <= position <= self.inputs: self.cursorPosition = Position
    
    def deleteChar(self):
        if self.cursorPosition > 0:
            self.inputs.pop(self.cursorPosition - 1)
            self.cursorPosition -= 1
    
    def inputToString(self):
        str = ""
        for i in range(len(self.inputs)):
            str += self.inputs[i]
        return str
    
    def inputToNum(self):
        s = self.inputToString()
        if self.numberType=="time":
            t = s.split(":")
            return (t[0], t[1], t[2])
        elif self.numberType=="int" or self.numberType=="positiveInt":
            return int(s)
        else:
            return float(s)
        
    def isValidInput(self):
        if len(self.inputs)==0: return False
        if self.numberType=="decimal" or self.numberType=="positiveDecimal":
            if len(self.inputs)==1 and self.inputs[0]==".": return False
            if self.inputs.count(".") > 1: return False
        if self.numberType=="decimal" or self.numberType=="int":
            if len(self.inputs)==1 and self.inputs[0]=="-": return False
            if self.inputs.count("-") > 1: return False
            if self.inputs.count("-")==1 and self.inputs[0]!="-": return False
        if self.numberType=="time":
            if self.inputs.count(":") != 2: return False
            if self.inputs.count(".") > 1: return False
            parts = (self.inputToString()).split(":")
            h = parts[0]
            m = parts[1]
            s = parts[2]
            if len(h) > 2: return False
            if "." in h: return False
            if not (0 <= int(h) <= 23): return False
            if len(m) != 2: return False
            if "." in m: return False
            if not (0 <= int(m) <= 59): return False
            if not (0 <= float(s) < 60): return False
            return True
        if self.numberType=="date":
            if self.inputs.count("/") != 2: return False
            parts = (self.inputToString()).split("/")
            d = parts[0]
            m = parts[1]
            y = parts[2]
            if len(d) > 2: return False
            if len(m) != 2: return False
            d = int(d)
            m = int(m)
            y = int(y)
            if not (d <= TimeAndDate.numDaysInMonth(m, y)): return False
            if not (1 <= m <= 12): return False
        num = self.inputToNum()
        if self.includeMin and num < self.min: return False
        if (not self.includeMin) and num <= self.min: return False
        if self.includeMax and num > self.max: return False
        if (not self.includeMax) and num >= self.max: return False
        return True
