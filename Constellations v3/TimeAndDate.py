import math


class TimeAndDate(object):    
    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        
        self.secondForm = TimeAndDate.timeAndDateToSecondForm(year, month, day, hour, minute, second)
    
    def setTimeAndDate(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.setFromTimeAndDate()
    def setYear(self, year):
        self.year = year
        self.setFromTimeAndDate()
    def setMonth(self, month):
        self.month = month
        self.setFromTimeAndDate()
    def setDay(self, day):
        self.day = day
        self.setFromTimeAndDate()
    def setHour(self, hour):
        self.hour = hour
        self.setFromTimeAndDate()
    def setMinute(self, minute):
        self.minute = minute
        self.setFromTimeAndDate()
    def setSecond(self, second):
        self.second = second
        self.setFromTimeAndDate()
    def setSecondForm(self, secondForm):
        self.secondForm = secondForm
        self.setFromSecondForm()
    
    def setFromSecondForm(self):
        newTimeAndDate = TimeAndDate.secondFormToTimeAndDate(self.secondForm)
        self.year = newTimeAndDate[0]
        self.month = newTimeAndDate[1]
        self.day = newTimeAndDate[2]
        self.hour = newTimeAndDate[3]
        self.minute = newTimeAndDate[4]
        self.second = newTimeAndDate[5]
    def setFromTimeAndDate(self):
        self.secondForm = TimeAndDate.timeAndDateToSecondForm(self.year, self.month, self.day, self.hour, self.minute, self.second)
    
    def __eq__(self, timeAndDate):
        return isinstance(timeAndDate, TimeAndDate) \
            and self.year == timeAndDate.year \
            and self.month == timeAndDate.month \
            and self.day == timeAndDate.day \
            and self.hour == timeAndDate.hour \
            and self.minute == timeAndDate.minute \
            and self.second == timeAndDate.second
    
    def __repr__(self):
        return "year: %d, month: %d, day: %d, \n hour: %d, minute: %d, second: %f" % \
            (self.year, self.month, self.day, self.hour, self.minute, self.second)
    
    @staticmethod
    def timeAndDateToSecondForm(year, month, day, hour, minute, second):
        numDays = TimeAndDate.numDaysBetweenDates(day, month, year, 1, 1, 0)
        secondForm = numDays*86400
        secondForm += hour*3600 + minute*60 + second
        return secondForm
    
    @staticmethod
    def secondFormToTimeAndDate(secondForm):
        secondsInLeapYear = 366 * 86400
        secondsIn400Years = (400*365 + 100 - 4 + 1) * 86400
        fourCenturies = math.floor(secondForm/secondsIn400Years)
        year = 400*fourCenturies
        secondsRemaining = secondForm - fourCenturies*secondsIn400Years
        
        minRemainingYears = int(secondsRemaining/secondsInLeapYear)
        oldYear = year
        year += minRemainingYears
        secondsRemaining -= (365*(year-oldYear) + TimeAndDate.numLeapYearsBetweenYears(oldYear, year)) * 86400
        dayOfYear = int(secondsRemaining/86400)
        secondsRemaining = secondsRemaining % 86400
        dayOfYear += 1
        while dayOfYear > TimeAndDate.numDaysInYear(year):
            dayOfYear -= TimeAndDate.numDaysInYear(year)
            year += 1
        newDate = TimeAndDate.dayOfYearToDate(dayOfYear, year)
        day = newDate[0]
        month = newDate[1]
        year = newDate[2]
        
        newTime = TimeAndDate.secondOfDayToTime(secondsRemaining)
        hour = newTime[0]
        minute = newTime[1]
        second = newTime[2]
        
        return (year, month, day, hour, minute, second)
    
    @staticmethod
    def secondsBetweenTimeAndDates(timeAndDate1, timeAndDate2):
        return timeAndDate2.secondForm - timeAndDate1.secondForm
    
    @staticmethod
    def numDaysInYear(year):
        if TimeAndDate.isLeapYear(year): return 366
        return 365
    
    @staticmethod
    def isLeapYear(year):
        if year%4 != 0: return False
        if year%400 == 0: return True
        if year%100 == 0: return False
        return True
    
    @staticmethod
    def isValidTimeAndDate(timeAndDate):
        assert(isinstance(timeAndDate, TimeAndDate))
        if not isIntEquivalent(timeAndDate.year): return False
        if not isIntEquivalent(timeAndDate.month): return False
        if not isIntEquivalent(timeAndDate.day): return False
        if not isIntEquivalent(timeAndDate.hour): return False
        if not isIntEquivalent(timeAndDate.minute): return False
        if not (1 <= timeAndDate.month <= 12): return False
        
        maxDay = TimeAndDate.daysInMonth(timeAndDate.month, timeAndDate.year)
        if not (1 <= timeAndDate.day <= maxDay): return False
        
        if not (0 <= timeAndDate.hour <= 23): return False
        if not (0 <= timeAndDate.minute <= 59): return False
        if not (0 <= timeAndDate.second < 60): return False
        
        return True
    
    @staticmethod
    def compareTimeAndDate(timeAndDate1, timeAndDate2):
        dateComparison = TimeAndDate.compareDate(timeAndDate1.day, timeAndDate1.month, timeAndDate1.year,
            timeAndDate2.day, timeAndDate2.month, timeAndDate2.year)
        if dateComparison == -1: return -1
        elif dateComparison == 1: return 1
        
        timeComparison = TimeAndDate.compareDate(timeAndDate1.hour, timeAndDate1.minute, timeAndDate1.second,
            timeAndDate2.hour, timeAndDate2.minute, timeAndDate2.second)
        if timeComparison == -1: return -1
        elif timeComparison == 1: return 1
        
        return 0
    
    @staticmethod
    def compareDate(day1, month1, year1, day2, month2, year2):
        if year1 < year2: return -1
        elif year1 > year2: return 1
        elif month1 < month2: return -1
        elif month1 > month2: return 1
        elif day1 < day2: return -1
        elif day1 > day2: return 1
        return 0
    
    @staticmethod
    def compareDate2(dayOfYear1, year1, dayOfYear2, year2):
        if year1 < year2: return -1
        elif year1 > year2: return 1
        elif dayOfYear1 < dayOfYear2: return -1
        elif dayOfYear1 > dayOfYear2: return 1
        return 0
    
    @staticmethod
    def compareTime(hour1, minute1, second1, hour2, minute2, second2):
        if hour1 < hour2: return -1
        elif hour1 > hour2: return 1
        elif minute1 < minute2: return -1
        elif minute1 > minute2: return 1
        elif second1 < second2: return -1
        elif second1 > second2: return 1
        return 0
    
    @staticmethod
    def daysInMonth(month, year):
        if month==2 and TimeAndDate.isLeapYear(year): return 29
        elif month==2: return 28
        elif month in [4,6,9,11]: return 30
        else: return 31
    
    @staticmethod
    def dateToDayOfYear(inputDay, inputMonth, inputYear):
        sum = 0
        for month in range(1, inputMonth):
            sum += TimeAndDate.daysInMonth(month, inputYear)
        sum += inputDay
        return sum
    
    @staticmethod
    def dayOfYearToDate(dayOfYear, year):
        sum = 0
        month = 1
        while sum + TimeAndDate.daysInMonth(month, year) < dayOfYear:
            sum += TimeAndDate.daysInMonth(month, year)
            month += 1
        day = dayOfYear - sum
        return (day, month, year)
    
    @staticmethod
    def numLeapYearsBetweenYears(year1, year2):
        # not inclusive of end year
        numMultiplesOf4 = math.floor(year2/4) - math.ceil(year1/4) + 1
        if year2%4==0: numMultiplesOf4 -= 1 # not inclusive of end year
        numMultiplesOf100 = math.floor(year2/100) - math.ceil(year1/100) + 1
        if year2%100==0: numMultiplesOf100 -= 1 # not inclusive of end year
        numMultiplesOf400 = math.floor(year2/400) - math.ceil(year1/400) + 1
        if year2%400==0: numMultiplesOf400 -= 1 # not inclusive of end year
        return numMultiplesOf4 - numMultiplesOf100 + numMultiplesOf400
    
    @staticmethod
    def numDaysBetweenDates(day1, month1, year1, day2, month2, year2):
        if TimeAndDate.compareDate(day1, month1, year1, day2, month2, year2)==1:
            day1, day2 = day2, day1
            month1, month2 = month2, month1
            year1, year2 = year2, year1
        numLeapYears = TimeAndDate.numLeapYearsBetweenYears(year1, year2)
        dayDifference = TimeAndDate.dateToDayOfYear(day2, month2, year2) - TimeAndDate.dateToDayOfYear(day1, month1, year1)
        return (year2-year1)*365 + numLeapYears + dayDifference
    
    @staticmethod
    def numDaysBetweenDates2(dayOfYear1, year1, dayOfYear2, year2):
        if TimeAndDate.compareDate2(dayOfYear1, year1, dayOfYear2, year2)==1:
            dayOfYear1, dayOfYear2 = dayOfYear2, dayOfYear1
            year1, year2 = year2, year1
        numLeapYears = TimeAndDate.numLeapYearsBetweenYears(year1, year2)
        dayDifference = dayOfYear2 - dayOfYear1
        return (year2-year1)*365 + numLeapYears + dayDifference
    
    # @staticmethod
    # def daysAfterDate(day, month, year, daysIncr):
    #     daysIn400Years = 365*400 + 100 - 4 + 1
    #     
    #     fourCenturies = int(daysIncr/daysIn400Years)
    #     year += 400*fourCenturies
    #     daysIncr = daysIncr % daysIn400Years
    #     
    #     oldYear = year
    #     oldDayOfYear = TimeAndDate.dateToDayOfYear(day, month, year)
    #     minExtraYears = int(daysIncr/366)
    #     year += minExtraYears
    #     dayOfYear = oldDayOfYear
    #     if dayOfYear==366 and not TimeAndDate.isLeapYear(year):
    #         dayOfYear = 365
    #     daysIncr -= TimeAndDate.numDaysBetweenDates2(oldDayOfYear, oldYear, dayOfYear, year)
    #     
    #     dayOfYear += daysIncr
    #     daysIncr = 0
    #     
    #     while dayOfYear > TimeAndDate.numDaysInYear(year):
    #         dayOfYear -= TimeAndDate.numDaysInYear(year)
    #         year += 1
    #     
    #     return TimeAndDate.dayOfYearToDate(dayOfYear, year)
    
    @staticmethod
    def daysAfterDate(day, month, year, daysIncr):
        secondForm = TimeAndDate.timeAndDateToSecondForm(year, month, day, 0, 0, 0)
        secondForm += daysIncr*86400
        newDateAndTime = TimeAndDate.secondFormToTimeAndDate(secondForm)
        year = newDateAndTime[0]
        month = newDateAndTime[1]
        day = newDateAndTime[2]
        return (day, month, year)
    
    @staticmethod
    def daysBeforeDate(day, month, year, daysIncr):
        return TimeAndDate.daysAfterDate(day, month, year, -daysIncr)
        
    
    # @staticmethod
    # def daysBeforeDate(day, month, year, daysDecr):
    #     daysIn400Years = 365*400 + 100 - 4 + 1
    #     
    #     fourCenturies = int(daysDecr/daysIn400Years)
    #     year -= 400*fourCenturies
    #     daysDecr = daysDecr % daysIn400Years
    #     
    #     oldYear = year
    #     oldDayOfYear = TimeAndDate.dateToDayOfYear(day, month, year)
    #     minExtraYears = int(daysDecr/366)
    #     year -= minExtraYears
    #     dayOfYear = oldDayOfYear
    #     if dayOfYear==366 and not TimeAndDate.isLeapYear(year):
    #         year += 1
    #         dayOfYear = 1
    #     daysDecr -= TimeAndDate.numDaysBetweenDates2(oldDayOfYear, oldYear, dayOfYear, year)
    #     
    #     dayOfYear -= daysDecr
    #     daysDecr = 0
    #     
    #     while dayOfYear < 1:
    #         dayOfYear += TimeAndDate.numDaysInYear(year-1)
    #         year -= 1
    #     
    #     return TimeAndDate.dayOfYearToDate(dayOfYear, year)
        
    @staticmethod
    def timeToSecondOfDay(hour, minute, second):
        return hour*3600 + minute*60 + second
    
    @staticmethod
    def secondOfDayToTime(secondOfDay):
        hour = int(secondOfDay/3600)
        secondsLeft = secondOfDay % 3600
        minute = int(secondsLeft/60)
        second = secondsLeft % 60
        return (hour, minute, second)
    
    # @staticmethod
    # def addToTimeAndDate(timeAndDate, incrDay, incrHour, incrMinute, incrSecond):
    #     newDate = TimeAndDate.daysAfterDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, incrDay)
    #     timeAndDate.day = newDate[0]
    #     timeAndDate.month = newDate[1]
    #     timeAndDate.year = newDate[2]
    #     currentSecondOfDay = TimeAndDate.timeToSecondOfDay(timeAndDate.hour, timeAndDate.minute, timeAndDate.second)
    #     secondsToAdd = TimeAndDate.timeToSecondOfDay(incrHour, incrMinute, incrSecond)
    #     newSecondOfDay = currentSecondOfDay + secondsToAdd
    #     
    #     additionalDays = int(newSecondOfDay/86400)
    #     newDate = TimeAndDate.daysAfterDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, additionalDays)
    #     timeAndDate.day = newDate[0]
    #     timeAndDate.month = newDate[1]
    #     timeAndDate.year = newDate[2]
    #     
    #     newSecondOfDay = newSecondOfDay - 86400*additionalDays
    #     newTime = TimeAndDate.secondOfDayToTime(newSecondOfDay)
    #     timeAndDate.hour = newTime[0]
    #     timeAndDate.minute = newTime[1]
    #     timeAndDate.second = newTime[2]
    
    # @staticmethod
    # def subFromTimeAndDate(timeAndDate, decrDay, decrHour, decrMinute, decrSecond):
    #     newDate = TimeAndDate.daysBeforeDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, decrDay)
    #     timeAndDate.day = newDate[0]
    #     timeAndDate.month = newDate[1]
    #     timeAndDate.year = newDate[2]
    #     currentSecondOfDay = TimeAndDate.timeToSecondOfDay(timeAndDate.hour, timeAndDate.minute, timeAndDate.second)
    #     secondsToSub = TimeAndDate.timeToSecondOfDay(decrHour, decrMinute, decrSecond)
    #     newSecondOfDay = currentSecondOfDay - secondsToSub
    #     
    #     additionalDays = int(-newSecondOfDay/86400)
    #     newDate = TimeAndDate.daysBeforeDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, additionalDays)
    #     timeAndDate.day = newDate[0]
    #     timeAndDate.month = newDate[1]
    #     timeAndDate.year = newDate[2]
    #     

    #     newSecondOfDay = newSecondOfDay + 86400*(additionalDays)
    #     if newSecondOfDay < 0:
    #         newSecondOfDay += 86400
    #         newDate = TimeAndDate.daysBeforeDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, 1)
    #         timeAndDate.day = newDate[0]
    #         timeAndDate.month = newDate[1]
    #         timeAndDate.year = newDate[2]
    #     newTime = TimeAndDate.secondOfDayToTime(newSecondOfDay)
    #     timeAndDate.hour = newTime[0]
    #     timeAndDate.minute = newTime[1]
    #     timeAndDate.second = newTime[2]

####################################
## HELPER FUNCTIONS
####################################

def isIntEquivalent(num):
    return num==int(num)

def testNumDaysBetweenDates():
    print("Testing numDaysBetweenDates... ", end = "")
    assert(TimeAndDate.numDaysBetweenDates(1,1,2000,1,1,2000) == 0)
    assert(TimeAndDate.numDaysBetweenDates(1,1,2000,2,1,2000) == 1)
    assert(TimeAndDate.numDaysBetweenDates(1,1,2000,31,1,2000) == 30)
    assert(TimeAndDate.numDaysBetweenDates(1,1,2000,1,2,2000) == 31)
    assert(TimeAndDate.numDaysBetweenDates(1,1,2000,2,2,2000) == 32)
    assert(TimeAndDate.numDaysBetweenDates(2,2,2000,1,1,2000) == 32)
    assert(TimeAndDate.numDaysBetweenDates(1,1,2000,1,1,2001) == 366)
    assert(TimeAndDate.numDaysBetweenDates(1,1,2001,1,1,2002) == 365)
    assert(TimeAndDate.numDaysBetweenDates(3,11,801,22,8,1178) == 137623)
    assert(TimeAndDate.numDaysBetweenDates(25,6,1144, 24,7,2216) == 391569)
    print("Passed!")

def testDaysAfterDate():
    print("Testing daysAfterDay... ", end = "")
    assert(TimeAndDate.daysAfterDate(1,1,2000,0) == (1,1,2000))
    assert(TimeAndDate.daysAfterDate(1,1,2000,1) == (2,1,2000))
    assert(TimeAndDate.daysAfterDate(1,1,2000,30) == (31,1,2000))
    assert(TimeAndDate.daysAfterDate(1,1,2000,31) == (1,2,2000))
    assert(TimeAndDate.daysAfterDate(1,1,2000,32) == (2,2,2000))
    assert(TimeAndDate.daysAfterDate(1,1,2000,366) == (1,1,2001))
    assert(TimeAndDate.daysAfterDate(1,1,2001,365) == (1,1,2002))
    
    assert(TimeAndDate.daysAfterDate(1,1,2001,0) == (1,1,2001))
    assert(TimeAndDate.daysAfterDate(1,1,2001,1) == (2,1,2001))
    assert(TimeAndDate.daysAfterDate(1,1,2001,30) == (31,1,2001))
    assert(TimeAndDate.daysAfterDate(1,1,2001,31) == (1,2,2001))
    assert(TimeAndDate.daysAfterDate(1,1,2001,32) == (2,2,2001))
    assert(TimeAndDate.daysAfterDate(1,1,2001,366) == (2,1,2002))
    assert(TimeAndDate.daysAfterDate(1,1,2003,365) == (1,1,2004))
    
    assert(TimeAndDate.daysAfterDate(3,11,801,137623) == (22,8,1178))
    assert(TimeAndDate.daysAfterDate(25,6,1144,391569) == (24,7,2216))
    assert(TimeAndDate.daysAfterDate(31,12,2000,366) == (1,1,2002))
    print("Passed!")

def testDaysBeforeDate():
    print("Testing daysBeforeDay... ", end = "")
    assert(TimeAndDate.daysBeforeDate(1,1,2000,0) == (1,1,2000))
    assert(TimeAndDate.daysBeforeDate(2,1,2000,1) == (1,1,2000))
    assert(TimeAndDate.daysBeforeDate(31,1,2000,30) == (1,1,2000))
    assert(TimeAndDate.daysBeforeDate(1,2,2000,31) == (1,1,2000))
    assert(TimeAndDate.daysBeforeDate(2,2,2000,32) == (1,1,2000))
    assert(TimeAndDate.daysBeforeDate(1,1,2001,366) == (1,1,2000))
    assert(TimeAndDate.daysBeforeDate(1,1,2002,365) == (1,1,2001))
    
    assert(TimeAndDate.daysBeforeDate(1,1,2001,0) == (1,1,2001))
    assert(TimeAndDate.daysBeforeDate(2,1,2001,1) == (1,1,2001))
    assert(TimeAndDate.daysBeforeDate(31,1,2001,30) == (1,1,2001))
    assert(TimeAndDate.daysBeforeDate(1,2,2001,31) == (1,1,2001))
    assert(TimeAndDate.daysBeforeDate(2,2,2001,32) == (1,1,2001))
    assert(TimeAndDate.daysBeforeDate(2,1,2002,366) == (1,1,2001))
    assert(TimeAndDate.daysBeforeDate(1,1,2004,365) == (1,1,2003))
    
    assert(TimeAndDate.daysBeforeDate(22,8,1178,137623) == (3,11,801))
    assert(TimeAndDate.daysBeforeDate(24,7,2216,391569) == (25,6,1144))
    assert(TimeAndDate.daysBeforeDate(31,12,2000,366) == (31,12,1999))
    print("Passed!")

# def testAddToTimeAndDate():
#     print("Testing addToTimeAndDate... ", end = "")
#     t = TimeAndDate(2000, 1, 1, 0, 0, 0)
#     TimeAndDate.addToTimeAndDate(t, 366, 25, 10, 71)
#     assert(t == TimeAndDate(2001, 1, 2, 1, 11, 11))
#     TimeAndDate.subFromTimeAndDate(t, 366, 25, 10, 71)
#     assert(t == TimeAndDate(2000, 1, 1, 0, 0, 0))
#     print("Passed!")

def test():
    testNumDaysBetweenDates()
    testDaysAfterDate()
    testDaysBeforeDate()
    # testAddToTimeAndDate()
    print("Testing done!")


# test()



