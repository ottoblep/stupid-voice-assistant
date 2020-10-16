# -*- coding: utf-8 -*-

from datetime import datetime
from datetime import date
import os
import time
import calendar
import inflection as inflection
import random
import requests
import urllib.request
import pycurl
import pprint
from io import BytesIO
import io

#Forbes Quote
quote_url = "http://www.forbes.com/forbesapi/thought/uri.json?enrich=true&query=1&relatedlimit=5"

#Fixed Texts
greetings = ["Guten Morgen","Wach auf","Mach dich auf die Socken","Steh Auf","Zeit Aufzustehen"]
quoteintros = ["dein zitat lautet","hier ist dein zitat","ein zitat für dich","hier ist was zum nachdenken","hör dir das an","ein weiser mann sagte mal"]

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

def monatsname(monat):
    if monat==1: return "Januar"
    if monat==2: return "Februar"
    if monat==3: return "März"
    if monat==4: return "April"
    if monat==5: return "Mai"
    if monat==6: return "Juni"
    if monat==7: return "Juli"
    if monat==8: return "August"
    if monat==9: return "September"
    if monat==10: return "Oktober"
    if monat==11: return "November"
    if monat==12: return "Dezember"
def wochentag(tag):
    if tag=="Monday": return "Montag"
    if tag=="Tuesday": return "Dienstag"
    if tag=="Wednesday": return "Mittwoch"
    if tag=="Thursday": return "Donnerstag"
    if tag=="Friday": return "Freitag"
    if tag=="Saturday": return "Samstag"
    if tag=="Sunday": return "Sonntag"
def getweather():   
    opener = urllib.request.FancyURLopener({})
    f = opener.open("https://www.wetter.com/wetter_aktuell/wettervorhersage/3_tagesvorhersage/deutschland/gilching/DE0003429.html")
    content = f.read()
    content=str(content, encoding='utf-8', errors='strict')
    content=content.replace("<br />","")
    content=content.replace("<br>","")
    content=content.replace("<p>","")
    start = content.find("<h3>Wetter heute,")
    end = content.find(" liegt in")
    weathertext = content[start+66:end-24]
    weathertext=weathertext.replace("°C","°")
    if start!=-1 and end!=-1:
        return weathertext 

def getquote():
##    response = requests.get(quote_url)
##    data = response.json()
##    quote=data['thought']['quote'].strip("(' )")
##    return quote

    opener = urllib.request.FancyURLopener({})
    f = opener.open("https://www.zitatdestages.net/")
    content = f.read()
    content=str(content, encoding='utf-8', errors='strict')
    start = content.find("<p class=\"blog-title\">")
    end = content.find("</p><p class=\"blog")
    quotetext = content[start+22:end]
    if start!=-1 and end!=-1:
        return quotetext 

def computemessage():
    #creates wav from sentences.txt
    os.system("gtts-cli -l de -f message.txt -o out.mp3 ")
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
    weathermessage=getweather()
    #Compose Message
    message=random.choice(greetings)+". Es ist "+wochentag(weekday)+". "+day+"ter "+monatsname(int(month))+" "+year+"."
    message+=" "+weathermessage+" "
    message+=random.choice(quoteintros)+". "+getquote()       
    print(message)
    # process Unicode text
    with io.open("message.txt",'w',encoding='utf8') as f:
        f.write(message)


createmessage()
computemessage()




