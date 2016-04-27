
import speech_recognition as sr
import webbrowser
import json 
import spotipy
import time
import wikipedia

from os import system
from pprint import pprint

def handleSearches(split, cmdstr):
    if split[1] == 'google':
        system('say pulling up a google search now')
        # print("I am pulling up a google search for you now")
        if split[2] == 'for':
            url = "https://www.google.com.tr/search?q={}".format(str.split(' ',3)[3])    
            webbrowser.open(url)
        else:
            url = "https://www.google.com.tr/search?q={}".format(str.split(' ',2)[2])    
            webbrowser.open(url)
    if split [1] == 'Wikipedia':
        system('say pulling the wikipedia page now')
        if split[2] == 'for':
            page = wikipedia.page(cmdstr.split(' ', 3)[3])
            webbrowser.open(page.url)
        else:
            try:
                page = wikipedia.page(cmdstr.split(' ', 2)[2])
                webbrowser.open(page.url)
            except wikipedia.exceptions.DisambiguationError as e:
                system('say Disambiguation Error. Here is a list of possible searches')
                print(e)
def handleCmd(str):
    split = str.split()
    cmdTerm = split[0]
    if str == "who are you":
        system('say You made me. I am not real. What else do you want to know?')
        iamnotarobot()
    if str == "good morning frank":
        print("good morning max")
        system('say Good morning max')
    if str == "stop listening":
        system('say Goodbye max')
        print("goodbye max")
        return True
    if cmdTerm == "search":
        handleSearches(split, str)
    if cmdTerm == "play":
        system('say Sure thing let me quickly pull up that dank track')
        print("playing dank tunes as per your request")
        if len(split) > 1:
            system("sudo spotify play " + str.split(' ', 1)[1])
        else:
            system("sudo spotify play")
    if cmdTerm.lower() == "playlist":
        system('say Sure, thats a good playlist')
        system("sudo spotify play list " + str.split(' ', 1)[1])
    return False


r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
# this is called from the background thread
def startListening():
    # received audio data, now we'll recognize it using Google Speech Recognition
    while True:
        with m as source:
            audio = r.listen(source)
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Frank thinks you said " + r.recognize_google(audio))
            obj = r.recognize_google(audio, show_all=True)
            n = json.dumps(obj)  
            o = json.loads(n)
            cmd = "" + o['alternative'][0]['transcript']
            if handleCmd(cmd):
                break
        except sr.UnknownValueError:
            print("Frank could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def answerSelfQuestion(cmd):
    split = cmd.split()
    cmdTerm = split[0]
    with open('whoami.json') as data_file:    
        data = json.load(data_file)

    pprint(data)
    if str == 'what is your name':
        if data['name']:
            system('say My name is ' + data['name'])
        else:    
            system('say I dont know')

def iamnotarobot():
    while True:
        with m as source:
            audio = r.listen(source)
        try:
            # for testing purposes, we're just using the default API key
            # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("Frank thinks you said " + r.recognize_google(audio))
            from pprint import pprint
            obj = r.recognize_google(audio, show_all=True)
            n = json.dumps(obj)  
            o = json.loads(n)
            cmd = "" + o['alternative'][0]['transcript']
            if answerSelfQuestion(cmd):
                break
        except sr.UnknownValueError:
            print("Frank could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

startListening()
