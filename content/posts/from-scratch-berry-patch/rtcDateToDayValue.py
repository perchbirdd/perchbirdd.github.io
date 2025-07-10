daysPerMonth = [0x1F, 0x1C, 0x1F, 0x1E, 0x1F, 0x1E, 0x1F, 0x1F, 0x1E, 0x1F, 0x1E, 0x1F]

def isLeapYear(year: int) -> bool:
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

class RtcDate():
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, second: int):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __repr__(self) -> str:
        return f"year: {self.year} ({2000 + self.year}) month: {self.month} day: {self.day} result: {self.toDayValue()}"

    def toDayValue(self) -> int:
        yearToDays = 0
        yearVal = self.year

        yearVal -= 1
        if yearVal > 0:
            while True:
                yearToDays += 365
                if isLeapYear(yearVal):
                    yearToDays += 1
                if yearVal <= 0:
                    break
                yearVal -= 1;

        # S3511 has jan as month 1
        monthIndex = self.month - 1

        # accumulate days in previous months
        for i in range(0, monthIndex):
            yearToDays += daysPerMonth[i]
        
        # leap year
        if self.month > 2 and isLeapYear(self.year):
            yearToDays += 1

        return yearToDays + self.day

class SaveDate():
    def __init__(self, days: int, hour: int, minute: int, second: int):
        self.days = days
        self.hour = hour
        self.minute = minute
        self.second = second

    def __repr__(self) -> str:
        return f"days: {self.days} hour: {self.hour} minute: {self.minute} second: {self.second}"

def calcInitialTimeDifference(currentTime: RtcDate, elapsed: SaveDate, initial: SaveDate):

    days = currentTime.toDayValue()

    elapsed.second = currentTime.second - initial.second
    elapsed.minute = currentTime.minute - initial.minute
    elapsed.hour = currentTime.hour - initial.hour
    elapsed.days = days - initial.days

    if elapsed.second < 0:
        elapsed.second += 60
        elapsed.minute -= 1
    
    if elapsed.minute < 0:
        elapsed.minute += 60
        elapsed.hour -= 1
    
    if elapsed.hour < 0:
        elapsed.hour += 24
        elapsed.days -= 1

def calcElapsedTimeDifference(calcDiff: SaveDate, saveElapsed: SaveDate, calcElapsed: SaveDate):
    calcDiff.second = calcElapsed.second - saveElapsed.second
    calcDiff.minute = calcElapsed.minute - saveElapsed.minute
    calcDiff.hour = calcElapsed.hour - saveElapsed.hour
    calcDiff.days = calcElapsed.days - saveElapsed.days

    if calcDiff.second < 0:
        calcDiff.second += 60
        calcDiff.minute -= 1

    if calcDiff.minute < 0:
        calcDiff.minute += 60
        calcDiff.hour -= 1

    if calcDiff.hour < 0:
        calcDiff.hour += 24
        calcDiff.days -= 1
    

def dumpDayValue(year: int, month: int, day: int) -> None:
    print(f"{RtcDate(year, month, day, 0, 0, 0)}")

def calculateTimeDifference(rtcDate: RtcDate, initial: SaveDate, elapsed: SaveDate):
    print(f"calculateTimeDifference")
    calc1 = SaveDate(0, 0, 0, 0)
    calc2 = SaveDate(0, 0, 0, 0)

    calcInitialTimeDifference(rtcDate, calc1, initial)
    
    calcElapsedTimeDifference(calc2, elapsed, calc1)
    
    endResult = calc2.days * 1440 + calc2.hour * 60 + calc2.minute > -1

    print(f"\trtc: {rtcDate}")
    print(f"\tinitial: {initial}")
    print(f"\telapsed: {elapsed}")
    print(f"\tidiff: {calc1}")
    print(f"\tediff: {calc2}")
    print(f"result: {endResult}")

dumpDayValue(1, 6, 2)
dumpDayValue(1, 3, 2)
dumpDayValue(1, 1, 15)
dumpDayValue(1, 1, 15)
dumpDayValue(1, 12, 16)
dumpDayValue(2, 1, 1)

# patch on 2001-01-15 with save and initial 0, 0, 0
# calculateTimeDifference(RtcDate(1, 1, 15, 0, 0, 0), SaveDate(0, 0, 0, 0), SaveDate(0, 0, 0, 0))

#calculateTimeDifference(RtcDate(1, 1, 15, 0, 0, 0), SaveDate(349, 14, 00, 37), SaveDate(0, 10, 0, 0))