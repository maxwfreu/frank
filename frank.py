
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
    if cmdTerm == "search":
        system('say Let me search that for you')
        print("I am pulling up a google search for you now")
        url = "https://www.google.com.tr/search?q={}".format(str.split(' ',1)[1])    
        webbrowser.open(url)
    if cmdTerm == "play":
        system('say Sure thing let me quickly pull up that dank track')
        print str.split(' ', 1)[1]
        print("playing dank tunes as per your request")
        system("sudo spotify play " + str.split(' ', 1)[1])
    return

# this is called from the background thread
def callback(recognizer, audio):
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Frank thinks you said " + recognizer.recognize_google(audio))
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


r = sr.Recognizer()
m = sr.Microphone()
listen = True
with m as source:
    r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening
while listen:
    time.sleep(0.1)
stop_listening()
print 'got signal to stop'