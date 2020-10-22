# -*- coding: utf-8 -*-

import sys
from datetime import datetime
from datetime import date
import os
import time
import calendar
import random
import requests
import urllib.request
import pycurl
import pprint
from io import BytesIO
import io
from vosk import Model, KaldiRecognizer
import pyaudio
from playsound import playsound
import json
import threading
from gtts import gTTS
import wikipedia
wikipedia.set_lang('de')

#Fixed Texts
quoteintros = ["hier ist ein zitat","ein zitat für dich","hier ein zitat","das zitat des tages","das heutige zitat"]

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
    
def getquote():
    opener = urllib.request.FancyURLopener({})
    f = opener.open("https://www.zitatdestages.net/")
    content = f.read()
    content=str(content, encoding='utf-8', errors='strict')
    start = content.find("<p class=\"blog-title\">")
    end = content.find("</p><p class=\"blog")
    quotetext = content[start+22:end]
    if start!=-1 and end!=-1:
        out = random.choice(quoteintros)+". "+quotetext
        return out
    else: print("Scraper Failed")
def getdate():
    #Date
    my_date = date.today()
    datelist = str(my_date).split("-")
    year = datelist[0]
    month = datelist[1]
    day = datelist[2]
    weekday = calendar.day_name[my_date.weekday()]
    message="Es ist "+wochentag(weekday)+". "+day+"ter "+monatsname(int(month))+" "+year+"."
    return message
def gettime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time
def getweather():
    opener = urllib.request.FancyURLopener({})
    f = opener.open("https://www.wetter.com/wetter_aktuell/wettervorhersage/3_tagesvorhersage/deutschland/gilching/DE0003429.html")
    content = f.read()
    content=str(content, encoding='utf-8', errors='strict')
    content=content.replace("<br />","")
    content=content.replace("<br>","")
    content=content.replace("<p>","")
    start = content.find("<h3>Wetter heute,")
    end = content.find("Böen")
    weathertext = content[start+66:end-3]
    weathertext=weathertext.replace("°C","°")
    if start!=-1 and end!=-1:
        return weathertext
def radio(channel):
    os.system("omxplayer blup.mp3")
    if channel=="jazz":os.system("omxplayer https://live.wostreaming.net/direct/ppm-jazz24aac-ibc1")
    if channel=="rock":os.system("omxplayer http://www.rockradio.de:8090")
    if channel=="klassik":os.system("omxplayer http://br-brklassik-live.cast.addradio.de/br/brklassik/live/mp3/mid")
    if channel=="nachrichten":os.system("omxplayer http://br-b5aktuell-live.cast.addradio.de/br/b5aktuell/live/mp3/mid")
def play(message):
    os.system("omxplayer blup.mp3")
    print("Output: "+message)
    # process Unicode text
    with io.open("message.txt",'w',encoding='utf8') as f:
        f.write(message)
    #write tts out to file like object or mp3 and play it
#    mp3_fp = BytesIO()
    tts = gTTS(message, lang='de')
#    tts.write_to_fp(mp3_fp)
    tts.save('out.mp3')
    os.system("omxplayer out.mp3")
    
def actionthread(command):
    print ("Input:"+command)
    if command=="wetter": play(getweather())
    if command=="datum" or command=="wochentag": play(getdate())
    if command=="uhrzeit": play(gettime())
    if command=="zitat": play(getquote())
#    if command=="test": play("Test Test Test")
    if command[:9]=="wikipedia": play("Wikipedia Artikel für "+command[10:]+". "+wikipedia.summary(command[10:]))
    if command=="stopp": os.system("pkill omxplayer")
    if command=="jazz": radio("jazz")
    if command=="rock": radio("rock")
    if command=="klassik": radio("klassik")
    if command=="nachrichten": radio("nachrichten")
     
    
def listenloop():
    if not os.path.exists("model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)
    model = Model("model")
    rec = KaldiRecognizer(model, 44100)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=22050)
    stream.start_stream()
    while True:

            data = stream.read(11025, exception_on_overflow = False)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                t = threading.Thread(target=actionthread, args=(res['text'],))
                t.start()

                

listenloop()




