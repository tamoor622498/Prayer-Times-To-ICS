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
    for i in range(len(days)):
        unixTime = int(time.mktime(datetime.strptime(days[i], "%Y-%m-%d").timetuple()))
        PARAMS = {"city":"gambrills", "country":"United States"} #Query Parameters
        res = requests.get(' http://api.aladhan.com/v1/timingsByCity'+ "/" + str(unixTime) + "?", params=PARAMS).json() #get and convert to jSON
        for k in range(len(prayers)):
            #print(res["data"]["date"]["gregorian"]["date"] + " " + res["data"]["timings"][prayers[k]] + ":00" + "----" + prayers[k])
            dateString = res["data"]["date"]["gregorian"]["date"] + " " + res["data"]["timings"][prayers[k]] + ":00"
            date=datetime.strptime(dateString,"%d-%m-%Y %H:%M:%S")
            date_eastern=eastern.localize(date,is_dst=None)
            date_utc=date_eastern.astimezone(utc)
            eTime = date_utc.strftime(fmt)[:-8]
            e = Event()
            e.name = prayers[k]
            e.begin = eTime
            c.events.add(e)
            c.events
            print(prayers[k] + " " + eTime)
    with open('my.ics', 'w') as my_file:
        my_file.writelines(c)

    # arr = DaysForMonth(6, 2021)
    # for i in range(len(arr)):
    #     print(int(time.mktime(datetime.strptime(arr[i], "%Y-%m-%d").timetuple())))


if __name__ == "__main__":
    main()