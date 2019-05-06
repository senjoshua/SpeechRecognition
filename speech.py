#!/usr/bin/env python3
# Requires PyAudio and PySpeech.

import speech_recognition as sr
from time import ctime
import time
from gtts import gTTS
from playsound import playsound
import os
import random

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
    if(data != ""):
        speak(data)

    # if "what time is it" in data:
    #     speak(ctime())

    # if "stop" in data:
    #     speak("stopping assistant")
    #     exit


# initialization
time.sleep(2)
speak("Hi, what can I do for you?")
while 1:
    response = recordAudio()
    assistant(response)