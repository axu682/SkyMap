import math

class TimeAndDate(object):
    def __init__(self, year, month, day, hour, minute, second):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        
        self.dayOfYear = TimeAndDate.dateToDayOfYear(day, month, year)
        
        self.secondFrom = timeAndDateToSecondForm(year, month, day, hour, minute, second)
    
    @staticmethod
    def timeAndDateToSecondForm(year, month, day, hour, minute, second):
        dayOfYear = TimeAndDate.dateToDayOfYear(day, month, year)
        
    
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
    
    @staticmethod
    def daysAfterDate(day, month, year, daysIncr):
        daysIn400Years = 365*400 + 100 - 4 + 1
        
        fourCenturies = int(daysIncr/daysIn400Years)
        year += 400*fourCenturies
        daysIncr = daysIncr % daysIn400Years
        
        oldYear = year
        oldDayOfYear = TimeAndDate.dateToDayOfYear(day, month, year)
        minExtraYears = int(daysIncr/366)
        year += minExtraYears
        dayOfYear = oldDayOfYear
        if dayOfYear==366 and not TimeAndDate.isLeapYear(year):
            dayOfYear = 365
        daysIncr -= TimeAndDate.numDaysBetweenDates2(oldDayOfYear, oldYear, dayOfYear, year)
        
        dayOfYear += daysIncr
        daysIncr = 0

        while dayOfYear > TimeAndDate.numDaysInYear(year):
            dayOfYear -= TimeAndDate.numDaysInYear(year)
            year += 1
        
        return TimeAndDate.dayOfYearToDate(dayOfYear, year)
    
    @staticmethod
    def daysBeforeDate(day, month, year, daysDecr):
        daysIn400Years = 365*400 + 100 - 4 + 1
        
        fourCenturies = int(daysDecr/daysIn400Years)
        year -= 400*fourCenturies
        daysDecr = daysDecr % daysIn400Years
        
        oldYear = year
        oldDayOfYear = TimeAndDate.dateToDayOfYear(day, month, year)
        minExtraYears = int(daysDecr/366)
        year -= minExtraYears
        dayOfYear = oldDayOfYear
        if dayOfYear==366 and not TimeAndDate.isLeapYear(year):
            year += 1
            dayOfYear = 1
        daysDecr -= TimeAndDate.numDaysBetweenDates2(oldDayOfYear, oldYear, dayOfYear, year)
        
        dayOfYear -= daysDecr
        daysDecr = 0

        while dayOfYear < 1:
            dayOfYear += TimeAndDate.numDaysInYear(year-1)
            year -= 1
        
        return TimeAndDate.dayOfYearToDate(dayOfYear, year)
        
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
    
    @staticmethod
    def addToTimeAndDate(timeAndDate, incrDay, incrHour, incrMinute, incrSecond):
        newDate = TimeAndDate.daysAfterDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, incrDay)
        timeAndDate.day = newDate[0]
        timeAndDate.month = newDate[1]
        timeAndDate.year = newDate[2]
        currentSecondOfDay = TimeAndDate.timeToSecondOfDay(timeAndDate.hour, timeAndDate.minute, timeAndDate.second)
        secondsToAdd = TimeAndDate.timeToSecondOfDay(incrHour, incrMinute, incrSecond)
        newSecondOfDay = currentSecondOfDay + secondsToAdd
        
        additionalDays = int(newSecondOfDay/86400)
        newDate = TimeAndDate.daysAfterDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, additionalDays)
        timeAndDate.day = newDate[0]
        timeAndDate.month = newDate[1]
        timeAndDate.year = newDate[2]
        
        newSecondOfDay = newSecondOfDay - 86400*additionalDays
        newTime = TimeAndDate.secondOfDayToTime(newSecondOfDay)
        timeAndDate.hour = newTime[0]
        timeAndDate.minute = newTime[1]
        timeAndDate.second = newTime[2]
    
    @staticmethod
    def subFromTimeAndDate(timeAndDate, decrDay, decrHour, decrMinute, decrSecond):
        newDate = TimeAndDate.daysBeforeDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, decrDay)
        timeAndDate.day = newDate[0]
        timeAndDate.month = newDate[1]
        timeAndDate.year = newDate[2]
        currentSecondOfDay = TimeAndDate.timeToSecondOfDay(timeAndDate.hour, timeAndDate.minute, timeAndDate.second)
        secondsToSub = TimeAndDate.timeToSecondOfDay(decrHour, decrMinute, decrSecond)
        newSecondOfDay = currentSecondOfDay - secondsToSub
        
        additionalDays = int(-newSecondOfDay/86400)
        newDate = TimeAndDate.daysBeforeDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, additionalDays)
        timeAndDate.day = newDate[0]
        timeAndDate.month = newDate[1]
        timeAndDate.year = newDate[2]
        

        newSecondOfDay = newSecondOfDay + 86400*(additionalDays)
        if newSecondOfDay < 0:
            newSecondOfDay += 86400
            newDate = TimeAndDate.daysBeforeDate(timeAndDate.day, timeAndDate.month, timeAndDate.year, 1)
            timeAndDate.day = newDate[0]
            timeAndDate.month = newDate[1]
            timeAndDate.year = newDate[2]
        newTime = TimeAndDate.secondOfDayToTime(newSecondOfDay)
        timeAndDate.hour = newTime[0]
        timeAndDate.minute = newTime[1]
        timeAndDate.second = newTime[2]