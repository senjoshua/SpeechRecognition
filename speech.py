#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
from time import ctime
import time
from gtts import gTTS
from playsound import playsound
import os
import random
import webbrowser
import re
import subprocess
from bs4 import BeautifulSoup as soup
import urllib
from urllib.request import urlopen

def speak(audioString):
    # Text to Speech with Google Text to Speech
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    rand = random.randint(1,1000)
    filename = "audio" + str(rand) + ".mp3"
    tts.save(filename)
    playsound(filename)
    os.remove(filename)


def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    response = ""
    try:
        response = r.recognize_google(audio)
        print("You said: " + response)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return response

def assistant(data):
    if "what time is it" in data:
        speak(ctime())

    elif "Google" in data:
        reg_ex = re.search("Google (.+)", data)
        if reg_ex:
            search = reg_ex.group(1)
            speak("Hold on, I will search " + search)
            urL='https://www.google.com/search?q=' + search
            chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path),1)
            webbrowser.get('chrome').open_new_tab(urL)

    elif "open" in data:
        reg_ex = re.search("open (.+)", data)
        if reg_ex:
            domain = reg_ex.group(1)
            speak("Hold on, I will open " + domain)
            url = "https://www." + domain + ".com"
            webbrowser.open(url)

    elif 'launch' in data:
        reg_ex = re.search('launch (.*)', data)
        if reg_ex:
            appname = reg_ex.group(1)
            # appname1 = appname+".app"
            speak("Hold on, I will launch " + appname)
            # subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)

    elif 'news' in data:
        try:
            news_url="https://news.google.com/news/rss"
            Client=urlopen(news_url)
            xml_page=Client.read()
            Client.close()
            soup_page=soup(xml_page,"xml")
            news_list=soup_page.findAll("item")
            for news in news_list[:5]:
                # print(news.title.text)
                speak(news.title.text)
        except Exception as e:
                print(e)

    elif "call me" in data:
        reg_ex = re.search("call me (.+)", data)
        if reg_ex:
            global name
            callname = reg_ex.group(1)
            name = callname
            file = open("name.txt","w+") 
            file.write(callname)
            file.close()
            speak("Ok, I will call you " + callname)


    elif "stop" in data:
        speak("stopping assistant")
        exit()

    else:
        speak("sorry I cannot help you with that")

# initialization
time.sleep(2)
name = ""
file = open("name.txt","r") 
name = file.read()
file.close()
speak("Hi, what can I do for you " + name + "?")
while 1:
    response = recordAudio()
    assistant(response)
    speak("Anything else " + name + "?")