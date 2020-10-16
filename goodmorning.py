from datetime import datetime
from datetime import date
import os
import time
import calendar
import inflection as inflection
import random
import requests
from pprint import pprint

# OpenWeatherMap

owm_url = "http://pro.openweathermap.org/data/2.5/forecast/hourly?zip=&appid="

greetings = ["Good Morning","Rise and Shine","Wake Up","Get up for your right","Get started"]
quoteintros = ["Your Quote is","Heres your Quote","A Quote for you","Heres something to think about","Get this","A wise man once said"]

##def activator():
##    while True:
##        time = str(datetime.now().time())
##        timelist = time.split(":")
##        # Generiere Sprache um 5:00
##        if timelist[0]=5 and timelist[1]=0:
##            createmessage()
##            computemessage()
##        # Warte auf extra Signal zum Abspielen von 5-10
##        if timelist[0]<10 and timelist[0]>5 and ADDITIONAL CONDITION:
##          ABSPIELEN

def getweather():   
    weather_data = requests.get(owm_url).json()
    pprint(weather_data)

def getquote():
    url = "http://www.forbes.com/forbesapi/thought/uri.json?enrich=true&query=1&relatedlimit=5"
    response = requests.get(url)
    data = response.json()
    quote=data['thought']['quote'].strip("(' )")
    pprint(data)
    return quote

    
def computemessage(message):
    #creates wav from sentences.txt
    os.system("python quick_start.py -b") 
    
def createmessage():
    my_date = date.today()
    datelist = str(my_date).split("-")
    year = datelist[0]
    month = datelist[1]
    day = datelist[2]
    weekday = calendar.day_name[my_date.weekday()]
    
    time = str(datetime.now().time())
    timelist = time.split(":")
    hour = timelist[0];
    minute = timelist[1];
    second = timelist[2];
    
    message=random.choice(greetings)+" Severin. It is "+weekday+". "+inflection.ordinalize(int(day))+" of "+calendar.month_name[int(month)]+" "+year+". "
    message+=random.choice(quoteintros)+": "+getquote()          
    print(message)
    File_object = open(r"sentences.txt","w")
    File_object.write(message)

createmessage()




