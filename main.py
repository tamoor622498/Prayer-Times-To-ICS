#https://aladhan.com/prayer-times-api
import time
import pytz
from ics import Calendar, Event
from datetime import date, timedelta, datetime
import requests

utc=pytz.utc
eastern=pytz.timezone('US/Eastern')
fmt='%Y-%m-%d %H:%M:%S %Z%z'
prayers = ["Fajr", "Sunrise", "Dhuhr", "Asr", "Sunset", "Maghrib", "Isha"]

def DaysForMonth(month, year):
    m = month
    y = year
    ndays = (date(y, m+1, 1) - date(y, m, 1)).days #Number of days
    d1 = date(y, m, 1) #First day of the month
    d2 = date(y, m, ndays) #Last day of the month
    delta = d2 - d1
    return [(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

def main():
    days = DaysForMonth(6, 2021) 
    c = Calendar()

    for i in range(len(days)): #For everyday in the month
        unixTime = int(time.mktime(datetime.strptime(days[i], "%Y-%m-%d").timetuple()))#Get's the in UNIXTIME version of the date
        PARAMS = {"city":"baltimore", "country":"United States"} #Query Parameters
        res = requests.get(' http://api.aladhan.com/v1/timingsByCity'+ "/" + str(unixTime) + "?", params=PARAMS).json() #get and convert to jSON
        
        for k in range(len(prayers)): # For every prayer
            dateString = res["data"]["date"]["gregorian"]["date"] + " " + res["data"]["timings"][prayers[k]] + ":00" #Full date and string in DD-MM-YYYY hh:mm:ss format
            date=datetime.strptime(dateString,"%d-%m-%Y %H:%M:%S") #Gets the date and time
            date_eastern=eastern.localize(date,is_dst=None) #Setting it as EDT time
            date_utc=date_eastern.astimezone(utc) #Convert to GMT
            eTime = date_utc.strftime(fmt)[:-8] #TIme saved with out text at the end
            e = Event() #Event made
            e.name = prayers[k] #Prayer
            e.begin = eTime #Time of prayer
            c.events.add(e) #Event added
            c.events #Event finished
            print(prayers[k] + " " + res["data"]["date"]["gregorian"]["date"])
    
    with open('PrayerTimes.ics', 'w') as my_file: #Opening and writing the calinder to ics file
        my_file.writelines(c)


if __name__ == "__main__":
    main()