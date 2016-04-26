
import speech_recognition as sr
import webbrowser
import json 
import spotipy
import time
from os import system

def handleCmd(str):
    split = str.split()
    cmdTerm = split[0]
    if str == "good morning frank":
        print("good morning max")
        system('say Good morning max')
    if str == "stop listening":
        system('say Goodbye max')
        print("goodbye max")
        listen = False
        stop_listening()
    if cmdTerm == "search":
        system('say Let me search that for you')
        print("I am pulling up a google search for you now")
        url = "https://www.google.com.tr/search?q={}".format(str.split(' ',1)[1])    
        webbrowser.open(url)
    if cmdTerm == "play":
        system('say Sure thing let me quickly pull up that dank track')
        print("playing dank tunes as per your request")
        if len(split) > 1:
            system("sudo spotify play " + str.split(' ', 1)[1])
        else:
            system("sudo spotify play")
    return
r = sr.Recognizer()
m = sr.Microphone()
# this is called from the background thread
def startListening():
    # received audio data, now we'll recognize it using Google Speech Recognition
    while True:
        with m as source:
            r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
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
            handleCmd(cmd)
        except sr.UnknownValueError:
            print("Frnak could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))



startListening()
