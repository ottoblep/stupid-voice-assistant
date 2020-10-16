from datetime import datetime
from datetime import date
import os
import time
import calendar
import inflection as inflection
import random
import requests
import pycurl
from io import BytesIO

#Forbes Quote
quote_url = "http://www.forbes.com/forbesapi/thought/uri.json?enrich=true&query=1&relatedlimit=5"
# OpenWeatherMap
#owm_url = "http://pro.openweathermap.org/data/2.5/weather?zip=82205,de&appid=375638db77406af8706d8dae70aedaeb"

#Fixed Texts
greetings = ["good morning","rise and shine","wake up","get up for your right","get started","time to get up","get your lazy ass out of bed"]
quoteintros = ["your quote is","heres your quote","a quote for you","heres something to think about","get this","a wise man once said"]

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
    #weather_data = requests.get(owm_url).json()
    #Fileweather_object = open(r"sentences.txt","w")
    #Fileweather_object.write(str(weather_data))
    #pprint(weather_data)
    c = pycurl.Curl()
    buffer = BytesIO()
    c.setopt(c.URL, "wttr.in/Gilching?format=%C|+%t|+%p|+%D|+%w")
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()
    body = buffer.getvalue()
    body = str(body)
    body=body.strip("\"' '")
    weatherlist = body.split("|")
    weatherlist[0]=weatherlist[0][2:]
    return weatherlist
    

def getquote():
    response = requests.get(quote_url)
    data = response.json()
    quote=data['thought']['quote'].strip("(' )")
    return quote

    
def computemessage():
    #creates wav from sentences.txt
    os.system("gtts-cli -f sentences.txt -o out.mp3 ")
    os.system("vlc out.mp3")
    
    
def createmessage():
    #Date
    my_date = date.today()
    datelist = str(my_date).split("-")
    year = datelist[0]
    month = datelist[1]
    day = datelist[2]
    weekday = calendar.day_name[my_date.weekday()]
    #Time
    time = str(datetime.now().time())
    timelist = time.split(":")
    hour = timelist[0];
    minute = timelist[1];
    second = timelist[2];
    #Weather
    weatherlist=getweather()
    condition = weatherlist[0]
    condition = condition.split(',')
    if condition[1]!="":
        condition[0] = condition[0]+" and "+condition[1]
    temp = weatherlist[1]
    temp = temp.split('\\',1)
    rain = weatherlist[2]
    sunrisetime = weatherlist[3]
    wind=weatherlist[4]
    windlist = wind.split('\\x97')
    
    message=random.choice(greetings)+" severin. It is "+weekday+". "+inflection.ordinalize(int(day))+" of "+calendar.month_name[int(month)]+" "+year+"."
    message+=" weather condition is "+condition[0]+". current temperature "+temp[0]+" Degrees. Wind Speed "+windlist[1]+". predicted rainfall amount "+rain+". sunrise is at "+sunrisetime[:6]+"."
    message+=random.choice(quoteintros)+". "+getquote()       
    print(message)
    File_object = open(r"sentences.txt","w")
    File_object.write(message)

createmessage()
#computemessage()




