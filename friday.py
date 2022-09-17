from __future__ import print_function
import pywhatkit
import sys
import os.path
import os
import pyttsx3
import platform
import speech_recognition as sr
import requests
import subprocess
import smtplib
import webbrowser
import wikipedia
import random
import pyautogui
import instaloader
import operator
import ctypes
import psutil
import cv2
import names
import randfacts
import keyboard
import translators as ts
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout
from PIL import Image
from termcolor import colored
from audioplayer import AudioPlayer
from datetime import date
from bs4 import BeautifulSoup
from email.message import EmailMessage
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from FridayGUI import Ui_FridayGUI
from pywikihow import search_wikihow
from gtts import gTTS
from pynotifier import Notification


SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
SEARCH_WORDS = ["who", "who", "what", "what", "when", "when", "where", "where", "why", "why", "how", "how"]
APPROVAL_WORDS = ["yes", "course", "sure", "why not", "surely", "go on", "gone", "ok", "okay", "yep", "yup", "ah", "bring it on", "yeah", "continue", "go ahead" "let's go"]
DENIAL_WORDS = ["no", "nope", "never", "don't", "do not", "stop", "cancel", "close", "vanda"]
WAKE_WORD = "friday"
WAKE_WORD_CAPITAL = "FRIDAY"
WAKE_WORD_MALAYALAM = "ഫ്രൈഡേ"

## Offline speech recognition and TTS engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# noinspection PyUnresolvedReferences
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

rate = engine.getProperty('rate')
volume = engine.getProperty('volume')
voice = engine.getProperty('voice')

## Weather variables. left blank, gets updated in runtime
location = ''
temperature = ''
weatherPrediction = ''

## Weather info displayed in top right in GUI
def weather_info():
    url_temp = "https://weather.com/en-IN/weather/today/l/4aff3ae553b47caf710d085a58fe60acac12d05abc56e4e18eca484e55ceede6"
    page = requests.get(url_temp)
    soup = BeautifulSoup(page.content, "html.parser")
    global location, temperature, weatherPrediction
    location = soup.find('h1', class_="CurrentConditions--location--kyTeL").text
    temperature = soup.find('span', class_="CurrentConditions--tempValue--3a50n").text
    weatherPrediction = soup.find('div', class_="CurrentConditions--phraseValue--2Z18W").text


weather_info()

# For Weather
def location_():
    return location

# For Weather
def temperature_():
    return temperature

# For Weather
def weatherPrediction_():
    return weatherPrediction

# locationLabel.config(text=location)
# temperatureLabel.config(text=temperature)
# weatherPredictionLabel.config(text=weatherPrediction)

# temperatureLabel.after(60000, getWeather)
# master.update()


## For printed info shown in GUI . left blank, gets updated in runtime
text = ''
speak_print = ''
listening = ''
recognizing = ''
speak_language = 'en'


## Main speech recognition engine

# noinspection PyShadowingNames,PyAttributeOutsideInit,SpellCheckingInspection
# noinspection PyTypeChecker
def take_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            global listening
            listening = "listening..."
            # print(listening)
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            r.dynamic_energy_threshold = 1000
            audio = r.listen(source, phrase_time_limit=20)
            listening = ''
            # global recognizing
            # recognizing = "Recognizing..."
            # print(recognizing)
            # recognizing = ''
            global text
            text = r.recognize_google(audio, language=speak_language)
            # print(f"user said: {text}")

        except Exception as e:
            str(e)
            return "none"
    text = text.lower()
    return text


def output():
    return text


def output_2():
    return speak


def speak_language_():
    return speak_language


# def GUI_weather_info():
#    url = "https://weather.com/en-IN/weather/today/l/4aff3ae553b47caf710d085a58fe60acac12d05abc56e4e18eca484e55ceede6"
#
#    master = Tk()
#    master.title("Weather Info")
#    master.anchor("center")
#    master.config(bg="maroon")
#    master.geometry("3340x400")
#    # master.attributes('-alpha', 0.5)
#   master.wm_attributes('-transparentcolor', master['bg'])
#    master.overrideredirect(True)
#
#    img = Image.open("files/icons/weather_icon_4.png")
#    img = img.resize((150, 150))
#    img = ImageTk.PhotoImage(img)
#
#    def getWeather():
#
#
#    locationLabel = Label(master, font=("LEIXO DEMO", 20), bg="maroon", foreground="red")
#    locationLabel.grid(row=0, sticky="N", padx=10)
#    temperatureLabel = Label(master, font=("Calibri Bold", 70), bg="maroon", foreground="dimgrey")
#    temperatureLabel.grid(row=1, sticky="W", padx=40)
#    Label(master, image=img, bg="maroon", foreground="maroon").grid(row=1, sticky="E")
#    weatherPredictionLabel = Label(master, font=("LEIXO DEMO", 20), bg="maroon", foreground="dimgrey")
#    weatherPredictionLabel.grid(row=2, sticky="W", padx=40)
#    getWeather()
#    master.mainloop()

## For checking connection status in the starting phase.
def check_internet_status():
    from time import sleep
    # from datetime import datetime
    global speak_print

    os.system('color')
    url = 'https://www.google.com/'
    timeout = 2
    # sleep_time = 10
    # op = None

    # while True:
    # now = datetime.now()
    try:
        op = requests.get(url, timeout=timeout).status_code
        if op == 200:

            # print(colored("Connected to Network", "green"), colored(": SYSTEM IS ONLINE", "cyan"))
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str("Connected To Network"),
                duration=30,  # Duration in seconds
            ).send()
            speak_print = f"successfully connected to network. {WAKE_WORD_CAPITAL} is now online and running"
            speak(f"successfully connected to network. {WAKE_WORD} is now online and running")

        else:
            # print(now, colored("Status Code is not 200", "red"))
            # print("status Code", op)
            pass
    except Exception as e:
        str(e)
        while True:
            # print(colored("No Network Connection Detected", "green"), colored(": SYSTEM IS OFFLINE", "red"))
            # print("status Code", op)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str("No Network Connection Detected"),
                duration=30,  # Duration in seconds
            ).send()
            speak_print = "stable internet connection is not available. please connect to a network !"
            speak_2("stable internet connection is not available. please connect to a network !")
            sleep(2)
            try:
                op = requests.get(url, timeout=timeout).status_code
                if op == 200:
                    # print(colored("Connected to Network", "green"), colored(": SYSTEM IS ONLINE", "cyan"))
                    Notification(
                        title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                        description=str(f"{WAKE_WORD_CAPITAL} is back online"),
                        duration=30,  # Duration in seconds
                    ).send()
                    speak_print = f"successfully connected to network. {WAKE_WORD_CAPITAL} is now online and running"
                    speak(f"successfully connected to network. {WAKE_WORD} is now online and running")
                    break
                else:
                    pass
            except Exception as e:
                str(e)
                pass

## Main TTS Engine
def speak(audio):
    tts = gTTS(text=audio, lang='en', tld='ca')
    filename = 'speech_engine.wav'
    tts.save(filename)
    AudioPlayer("speech_engine.wav").play(block=True)


def speak_ml(audio):
    tts = gTTS(text=audio, lang='ml')
    filename = 'speech_engine.wav'
    tts.save(filename)
    AudioPlayer("speech_engine.wav").play(block=True)


def speak_2(audio):
    engine.say(str(audio))
    # print(audio)
    engine.runAndWait()


def wish_face_id():
    # noinspection PyShadowingNames,PyAttributeOutsideInit,SpellCheckingInspection
    import datetime
    global speak_print
    try:
        hour = int(datetime.datetime.now().hour)

        if 5 <= hour <= 12:
            wish_reply = ["Good morning , wishing you the best for the day ahead.", "Good morning",
                          "Good morning , how's your day?"]
            reply = random.choice(wish_reply)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str(reply),
                duration=30,  # Duration in seconds
            ).send()
        elif 12 <= hour < 16:
            wish_reply = ["Good afternoon , how's everything going?", "Good afternoon",
                          "Good afternoon , how's your day?"]
            reply = random.choice(wish_reply)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str(reply),
                duration=30,  # Duration in seconds
            ).send()
        elif 16 <= hour < 19:
            wish_reply = ["Good Evening! No matter how bad your day has been, the beauty of the setting sun will make everything serene.", "Good evening, how about going for walk with the setting sun?",
                          "Good evening! I hope you had a good and productive day."]
            reply = random.choice(wish_reply)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str(reply),
                duration=30,  # Duration in seconds
            ).send()
        else:
            wish_reply = ["Good evening , or should i say , good night?",
                          "Good evening."]
            reply = random.choice(wish_reply)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str(reply),
                duration=30,  # Duration in seconds
            ).send()
    except Exception as e:
        str(e)
        speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
        speak("Sorry, something went wrong with that. please try again or report the incident to our team.")


def face_id_sample_generator():
    import cv2
    global speak_print
    # noinspection PyUnresolvedReferences
    try:
        cam = cv2.VideoCapture(0,
                               cv2.CAP_DSHOW)  # create a video capture object which is helpful to capture videos through webcam
        cam.set(3, 640)  # set video FrameWidth
        cam.set(4, 480)  # set video FrameHeight
        # noinspection PyUnresolvedReferences
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # Haar Cascade classifier is an effective object detection approach

        speak_print = "please say a numerical i d for the face i d."
        speak("please say a numerical i d for the face i d.")
        face_id = take_audio().lower()
        face_id = ''.join([n for n in face_id if n.isdigit()])
        # print(f"ok. this is what i heard, {face_id}. This id is going to be the unique id for this face.")
        speak_print = f"ok. this is what i heard, {face_id}. This id is going to be the unique i d for this face."
        speak(f"ok. this is what i heard, {face_id}. This id is going to be the unique i d for this face.")
        # face_id = input("Enter a Numeric user ID  here:  ")
        # Use integer ID for every new face (0,1,2,3,4,5,6,7,8,9........)

        # print("Taking samples, please look at the camera ....... ")
        speak_print = "Taking samples, please look at the camera . "
        speak("Taking samples, please look at the camera . ")
        count = 0  # Initializing sampling face count

        while True:

            ret, img = cam.read()  # read the frames using the above created object
            # noinspection PyUnresolvedReferences
            converted_image = cv2.cvtColor(img,
                                           cv2.COLOR_BGR2GRAY)  # The function converts an input image from one color space to another
            faces = detector.detectMultiScale(converted_image, 1.3, 5)

            for (x, y, w, h) in faces:
                # noinspection PyUnresolvedReferences
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # used to draw a rectangle on any image
                count += 1
                # noinspection PyUnresolvedReferences
                cv2.imwrite("samples/face." + str(face_id) + '.' + str(count) + ".jpg", converted_image[y:y + h, x:x + w])
                # To capture & Save images into the datasets folder
                # noinspection PyUnresolvedReferences
                cv2.imshow('image', img)  # Used to display an image in a window
            # noinspection PyUnresolvedReferences
            k = cv2.waitKey(100) & 0xff  # Waits for a pressed key
            if k == 27:  # Press 'ESC' to stop
                break
            elif count >= 10:  # Take 50 sample (More sample --> More accuracy)
                break

        # print("Samples taken now closing the program....")
        speak_print = "Samples taken. now closing the program."
        speak("Samples taken. now closing the program.")
        cam.release()
        # noinspection PyUnresolvedReferences
        cv2.destroyAllWindows()

    except Exception as e:
        str(e)
        speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
        speak("Sorry, something went wrong with that. please try again or report the incident to our team.")


def face_id_model_trainer():
    import cv2
    import numpy as np
    from PIL import Image  # pillow package
    import os
    global speak_print
    try:
        path = 'samples'  # Path for samples already taken
        # noinspection PyUnresolvedReferences
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
        # noinspection PyUnresolvedReferences
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # Haar Cascade classifier is an effective object detection approach

        # noinspection PyShadowingNames,PyShadowingBuiltins
        def Images_And_Labels(path):  # function to fetch the images and labels

            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            faceSamples = []
            ids = []

            for imagePath in imagePaths:  # to iterate particular image path

                gray_img = Image.open(imagePath).convert('L')  # convert it to grayscale
                img_arr = np.array(gray_img, 'uint8')  # creating an array

                id = int(os.path.split(imagePath)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_arr)

                for (x, y, w, h) in faces:
                    faceSamples.append(img_arr[y:y + h, x:x + w])
                    ids.append(id)

            return faceSamples, ids

        # print("Training the recently added face i d. please wait .It'll take a few seconds.")
        speak_print = "Training the recently added face i d. please wait .It'll take a few seconds. "
        speak("Training the recently added face i d. please wait .It'll take a few seconds. ")

        faces, ids = Images_And_Labels(path)
        recognizer.train(faces, np.array(ids))

        recognizer.write('trainer/trainer.yml')  # Save the trained model as trainer.yml

        # print("Model trained successfully, The recently added face is now recognizable.")
        speak_print = "Model trained successfully, The recently added face is now recognizable."
        speak("Model trained successfully, The recently added face is now recognizable.")

    except Exception as e:
        str(e)
        speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
        speak("Sorry, something went wrong with that. please try again or report the incident to our team.")


# noinspection PyShadowingBuiltins,PyShadowingNames
def face_id_face_recognition():
    import cv2
    global speak_print
    try:
        greet_phrases = ["hello", "hi there", "how are you?", "oh, hello"]
        greet = random.choice(greet_phrases)
        # noinspection PyUnresolvedReferences
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
        recognizer.read('trainer/trainer.yml')  # load trained model
        cascadePath = "haarcascade_frontalface_default.xml"
        # noinspection PyUnresolvedReferences
        faceCascade = cv2.CascadeClassifier(cascadePath)  # initializing haar cascade for object detection approach
        # noinspection PyUnresolvedReferences
        font = cv2.FONT_HERSHEY_SIMPLEX  # denotes the font type

        # noinspection PyShadowingBuiltins
        id = 5  # number of persons you want to Recognize

        with open('face_id/face_id_1.txt') as f:
            for line in f:
                name_1 = line
                # print(f"face identified as {line}")
                break

        with open('face_id/face_id_2.txt') as f:
            for line in f:
                name_2 = line
                # print(f"face identified as {line}")
                break

        with open('face_id/face_id_3.txt') as f:
            for line in f:
                name_3 = line
                # print(f"face identified as {line}")
                break

        with open('face_id/face_id_4.txt') as f:
            for line in f:
                name_4 = line
                # print(f"face identified as {line}")
                break

        with open('face_id/face_id_5.txt') as f:
            for line in f:
                name_5 = line
                # print(f"face identified as {line}")
                break
        names = ["", f'{name_1}', f'{name_2}', f'{name_3}', f'{name_4}',
                 f'{name_5}']  # names, leave first empty bcz counter starts from 0
        # noinspection PyUnresolvedReferences
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW to remove warning
        cam.set(3, 640)  # set video FrameWidht
        cam.set(4, 480)  # set video FrameHeight

        # Define min window size to be recognized as a face
        minW = 0.1 * cam.get(3)
        minH = 0.1 * cam.get(4)

        # flag = True

        while True:

            ret, img = cam.read()  # read the frames using the above created object
            # noinspection PyUnresolvedReferences
            converted_image = cv2.cvtColor(img,
                                           cv2.COLOR_BGR2GRAY)  # The function converts an input image from one color space to another

            faces = faceCascade.detectMultiScale(
                converted_image,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )

            for (x, y, w, h) in faces:
                # noinspection PyUnresolvedReferences
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # used to draw a rectangle on any image

                # noinspection PyShadowingBuiltins
                id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])  # to predict on every single image

                # Check if accuracy is less them 100 ==> "0" is perfect match
                # noinspection PyRedundantParentheses
                if (accuracy < 100):
                    # noinspection PyShadowingBuiltins
                    id = names[id]
                    accuracy = "  {0}%".format(round(100 - accuracy))

                else:
                    # noinspection PyShadowingBuiltins
                    id = "unknown"
                    accuracy = "  {0}%".format(round(100 - accuracy))
                # noinspection PyUnresolvedReferences
                cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                # noinspection PyUnresolvedReferences
                cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
            # noinspection PyUnresolvedReferences
            cv2.imshow('camera', img)
            # noinspection PyUnresolvedReferences
            k = cv2.waitKey(10) & 0xff  # Press 'ESC' for exiting video
            if k == 27:
                break
        cam.release()
        # noinspection PyUnresolvedReferences
        cv2.destroyAllWindows()
        # Do a bit of cleanup
        if id == name_1:
            # print(f"face identified as {name_1}.")
            speak_print = f"face identified as {name_1}."
            speak(f"face identified as {name_1}.")
            # print(f"{greet} {name_1}.")
            speak_print = f"{greet} {name_1}."
            speak(f"{greet} {name_1}.")
            wish_face_id()
        elif id == name_2:
            # print(f"face identified as {name_2}.")
            speak_print = f"face identified as {name_2}."
            speak(f"face identified as {name_2}.")
            # print(f"{greet} {name_2}.")
            speak_print = f"{greet} {name_2}."
            speak(f"{greet} {name_2}.")
            wish_face_id()
        elif id == name_3:
            # print(f"face identified as {name_3}.")
            speak_print = f"face identified as {name_3}."
            speak(f"face identified as {name_3}.")
            # print(f"{greet} {name_3}.")
            speak_print = f"{greet} {name_3}."
            speak(f"{greet} {name_3}.")
            wish_face_id()
        elif id == name_4:
            # print(f"face identified as {name_4}.")
            speak_print = f"face identified as {name_4}."
            speak(f"face identified as {name_4}.")
            # print(f"{greet} {name_4}.")
            speak_print = f"{greet} {name_4}."
            speak(f"{greet} {name_4}.")
            wish_face_id()
        elif id == name_5:
            # print(f"face identified as {name_5}.")
            speak_print = f"face identified as {name_5}."
            speak(f"face identified as {name_5}.")
            # print(f"{greet} {name_5}.")
            speak_print = f"{greet} {name_5}."
            speak(f"{greet} {name_5}.")
            wish_face_id()
        elif id == "unknown":
            # print(f"an unknown face was detected. if it needs to be added, please say 'add new face' along with {WAKE_WORD}.")
            speak_print = f"an unknown face was detected. if it needs to be added, please say 'add new face' along with {WAKE_WORD}."
            speak(f"an unknown face was detected. if it needs to be added, please say 'add new face' along with {WAKE_WORD}.")
            # print(f"unknown face was detected. Facial is data is saved in case of any malicious activity and for security reasons.")
            speak_print = f"unknown face was detected. Facial data is saved in case of any malicious activity and for security reasons."
            speak(f"unknown face was detected. Facial data is saved in case of any malicious activity and for security reasons.")
            wish()
        else:
            pass

        # print("Facial Recognition data updated.")
        speak("Facial Recognition data updated.")
        speak_print = "Facial Recognition data updated."
        cam.release()
        # noinspection PyUnresolvedReferences
        cv2.destroyAllWindows()
    except Exception as e:
        str(e)
        speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
        speak("Sorry, something went wrong with that. please try again or report the incident to our team.")


def get_riddle():
    global speak_print
    set_of_reply = ["here's one of my riddles", "here's a riddle", "sure ."]
    reply = random.choice(set_of_reply)
    print(reply)
    speak_print = reply
    speak(reply)
    set_of_riddles = ["Welcome you in or keep you away, I could really swing either way. What am I? .\n 'A door'.",
                      "If you have one, you don’t share it. If you share it, you don’t have it. What is it? .\n 'A secret'.",
                      "What comes down but never goes up? .\n 'A rain'.",
                      "What can run, but never walks, has a mouth, but never talks, has a head, but never weeps, and has a bed, but never sleeps? .\n  'A river'.",
                      "What do you throw out when you want to use it and take in when you don’t? .\n 'An anchor'.",
                      "What always leaves, always stays, and when the wind is blowing it sometimes sways? .\n 'A tree'.",
                      "The more there is of me, the less you see. What am I? .\n 'The darkness'.",
                      "What lives in the winter, dies in the heat, and comes to a point where it drips on the street? .\n 'An icicle'.",
                      "What can be caught but not thrown, even when a nose is blown? .\n 'A cold'.",
                      "What is easy to get into, but hard to get out of? .\n 'A trouble'.",
                      "What has hands and lots of rings, but can’t clap? .\n 'An alarm clock'.",
                      "What’s always lumpy and wet, but gets sharper the more you use it? .\n 'A brain'."]
    reply_riddle = random.choice(set_of_riddles)
    # print(reply_riddle)
    speak_print = reply_riddle
    speak(reply_riddle)
    try:
        if reply_riddle == "Welcome you in or keep you away, I could really swing either way. What am I? .\n 'A door'.":
            AudioPlayer("audio/creakydoorsoundeffect.mp3").play(block=True)
        elif reply_riddle == "If you have one, you don’t share it. If you share it, you don’t have it. What is it? .\n 'A secret'.":
            AudioPlayer("audio/secretsoundeffect.mp3").play(block=True)
        elif reply_riddle == "What comes down but never goes up? .\n 'A rain'.":
            AudioPlayer("audio/rainsoundeffect.mp3").play(block=True)
        elif reply_riddle == "What can run, but never walks, has a mouth, but never talks, has a head, but never weeps, and has a bed, but never sleeps? .\n  'A river'.":
            AudioPlayer("audio/riversoundeffect.mp3").play(block=True)
        elif reply_riddle == "What do you throw out when you want to use it and take in when you don’t? .\n 'An anchor'.":
            AudioPlayer("audio/shipanchorsoundeffect.mp3").play(block=True)
        elif reply_riddle == "What always leaves, always stays, and when the wind is blowing it sometimes sways? .\n 'A tree'.":
            AudioPlayer("audio/swayingtreesoundeffect.mp3").play(block=True)
        elif reply_riddle == "The more there is of me, the less you see. What am I? .\n 'The darkness'.":
            AudioPlayer("audio/darknesssoundeffect.mp3").play(block=True)
        elif reply_riddle == "What lives in the winter, dies in the heat, and comes to a point where it drips on the street? .\n 'An icicle'.":
            AudioPlayer("audio/iciclesoundeffect.mp3").play(block=True)
        elif reply_riddle == "What can be caught but not thrown, even when a nose is blown? .\n 'A cold'.":
            AudioPlayer("audio/coldsoundeffect.mp3").play(block=True)
        elif reply_riddle == "What is easy to get into, but hard to get out of? .\n 'A trouble'.":
            AudioPlayer("audio/troublesoundeffect.mp3").play(block=True)
        elif reply_riddle == "What has hands and lots of rings, but can’t clap? .\n 'An alarm clock'.":
            AudioPlayer("audio/allarmsoundeffect.mp3").play(block=True)
        elif reply_riddle == "What’s always lumpy and wet, but gets sharper the more you use it? .\n 'A brain'.":
            AudioPlayer("audio/swayingtreesoundeffect.mp3").play(block=True)
    except Exception as e:
        str(e)
        speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
        speak("Sorry, something went wrong with that. please try again or report the incident to our team.")

# def sendEmail(to, content):
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    # server.login('your email id', 'your password')
    # server.sendmail('your email id', to, content)
    # server.close()


def news():
    global speak_print
    try:
        main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=21097d4592c94b8ca384dbf038ba50de'
        main_page = requests.get(main_url).json()
        articles = main_page["articles"]
        head = []
        day = ["first", "second", "third", "fourth", "fifth"]
        for ar in articles:
            head.append(ar["title"])
        for i in range(len(day)):
            speak_print = f"today's {day[i]} news is :{head[i]}"
            speak(f"today's {day[i]} news is :{head[i]}")
    except Exception as e:
        str(e)
        speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
        speak("Sorry, something went wrong with that. please try again or report the incident to our team.")


def activation():
    import datetime
    global speak_print
    speak_print = f"Initializing {WAKE_WORD}"
    speak(f"Initializing {WAKE_WORD}")
    speak_print = "Starting all system applications"
    speak("Starting all system applications")
    speak_print = "All drivers are up and running"
    speak("All drivers are up and running")
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak_print = f"Currently it is {time}"
    speak(f"Currently it is {time}")
    speak_print = "here's a quote to push you"
    speak("here's a quote to push you")
    url = 'https://api.quotable.io/random'
    r = requests.get(url)
    quote = r.json()
    # print(quote['content'] + '\n ~', quote['author'])
    speak_print = f"{quote['content']}"
    speak(quote['content'])
    speak_print = "by " + f"{quote['author']}"
    speak("by " + quote['author'])


def wish():
    import datetime
    global speak_print
    try:
        hour = int(datetime.datetime.now().hour)

        if 5 <= hour <= 12:
            wish_reply = ["Good morning , wishing you the best for the day ahead.", "Good morning",
                          "Good morning , how's your day?"]
            reply = random.choice(wish_reply)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str(reply),
                duration=30,  # Duration in seconds
            ).send()
        elif 12 <= hour < 16:
            wish_reply = ["Good afternoon , how's everything going?", "Good afternoon",
                          "Good afternoon , how's your day?"]
            reply = random.choice(wish_reply)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str(reply),
                duration=30,  # Duration in seconds
            ).send()
        elif 16 <= hour < 19:
            wish_reply = [
                "Good Evening! No matter how bad your day has been, the beauty of the setting sun will make everything serene.",
                "Good evening, how about going for walk with the setting sun?",
                "Good evening! I hope you had a good and productive day."]
            reply = random.choice(wish_reply)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str(reply),
                duration=30,  # Duration in seconds
            ).send()
        else:
            wish_reply = ["Good evening , or should i say , good night?",
                          "Good evening."]
            reply = random.choice(wish_reply)
            Notification(
                title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                description=str(reply),
                duration=30,  # Duration in seconds
            ).send()
    except Exception as e:
        str(e)
        speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
        speak("Sorry, something went wrong with that. please try again or report the incident to our team.")
    speak_print = "all systems are now online"
    speak("all systems are now online")


# noinspection PyShadowingNames,PyUnresolvedReferences
class MainThread(QThread):
    speak_print = ''
    # noinspection PyMethodParameters

    def speak(audio):
        tts = gTTS(text=str(audio), lang='en', tld='ca')
        filename = 'speech_engine.wav'
        tts.save(filename)
        AudioPlayer("speech_engine.wav").play(block=True)

    # noinspection PyMethodParameters
    def speak_2(audio):
        engine.say(str(audio))
        # print(audio)
        engine.runAndWait()

    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        response = ["please wait while i check for internet availability.", "please wait , checking for stable internet connection.", "please kindly wait while i check for stable internet connection."]
        response_reply = random.choice(response)
        # print(response_reply)
        global speak_print
        speak_print = response_reply
        speak(response_reply)
        check_internet_status()
        # print(f"Please say , WAKEUP ,  or say , {WAKE_WORD} , to continue.")
        speak_print = f"Please say , WAKEUP ,  or say , {WAKE_WORD} , to continue."
        speak(f"Please say , WAKEUP ,  or say , {WAKE_WORD} , to continue.")
        while True:
            # noinspection PyAttributeOutsideInit
            self.text = take_audio()
            if"wake up" in self.text or WAKE_WORD in self.text or "are you there" in self.text or "ഫ്രൈഡേ" in self.text or "ഹലോ" in self.text:
                AudioPlayer("audio/activation_sound.mp3").play(block=True)
                self.taskexecution()

    # noinspection PyMethodMayBeStatic

    def taskexecution(self):
        # activation()
        wish()
        # face_id_face_recognition()
        global speak_print
        while True:
            try:
                # from datetime import datetime
                os.system('color')
                url = 'https://www.google.com/'
                timeout = 2
                # op = None

                # now = datetime.now()
                try:
                    op = requests.get(url, timeout=timeout).status_code
                    if op == 200:
                        # print(colored("Connected to Network", "green"), colored(": SYSTEM IS ONLINE", "cyan"))
                        colored("Connected to Network", "green"), colored(": SYSTEM IS ONLINE", "cyan")
                    else:
                        # print(now, colored("Status Code is not 200", "red"))
                        colored("Status Code is not 200", "red")
                        # print("status Code", op)
                except Exception as e:
                    str(e)
                    # print(colored("No Network Connection Detected", "green"), colored(": SYSTEM IS OFFLINE", "red"))
                    # print("status Code", op)
                    Notification(
                        title=f"{WAKE_WORD_CAPITAL} Desktop Assistant",
                        description=str("No Network Connection Detected."),
                        duration=30,  # Duration in seconds
                    ).send()
                    speak_print = "there is no stable internet connection available. please connect to a network"
                    speak_2("there is no stable internet connection available. please connect to a network")
                import random
                self.text = take_audio().lower()
                from audioplayer import AudioPlayer
                if WAKE_WORD in self.text or "wake up" in self.text or "ഫ്രൈഡേ" in self.text:
                    import datetime
                    # from audioplayer import AudioPlayer
                    # AudioPlayer("audio/activation_sound.mp3").play(block=True)
                    # print("waiting for command...")
                    # if f"{WAKE_WORD}" in self.text:
                    #     self.text = self.text.replace(WAKE_WORD, "")
                    #     random_reply_1 = ["none"]
                    #     reply = random.choice(random_reply_1)
                    #     print(reply)
                    #     AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    if "remember this" in self.text or "write this down" in self.text or "make a note" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            def note(text):
                                global speak_print
                                global speak_language
                                # noinspection PyShadowingNames
                                random_reply_2 = ["please specify the name for your file.",
                                                  "what should i name it?.",
                                                  "what should be the name?.",
                                                  "please say what you want it to be named."]
                                # noinspection PyShadowingNames
                                reply = random.choice(random_reply_2)
                                # print(reply)
                                speak_print = reply
                                speak(reply)
                                file_name = take_audio()
                                file_name = file_name + "-note.txt"
                                with open(file_name, "w") as n:
                                    n.write(text)

                                subprocess.Popen(["notepad.exe", file_name])
                            from time import sleep
                            # print("sure.")
                            speak_print = "sure."
                            speak("sure.")
                            random_reply_2 = ["What would you like me to write down?.",
                                              "what should be the content?.",
                                              "what should i write?.",
                                              "tell me what to write."]
                            reply = random.choice(random_reply_2)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                            note_text = take_audio()
                            note(note_text)
                            random_reply_2 = ["I've made a note of that.",
                                              "that's written and saved.",
                                              "sure, copy that."]
                            reply = random.choice(random_reply_2)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                            # print("showing preview.")
                            speak_print = "here's a preview."
                            speak("here's a preview.")
                            sleep(3)
                            os.system('TASKKILL /F /IM notepad.exe')
                            # print("you can find the saved note file in the program directory.")
                            speak_print = "you can find the saved note file in the program directory."
                            speak("you can find the saved note file in the program directory.")
                        except Exception as e:
                            str(e)
                            speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
                            speak("Sorry, something went wrong with that. please try again or report the incident to our team.")
                    elif "language to malayalam" in self.text or "speak in malayalam" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_language = 'ml'
                        speak("language has been set to malayalam")
                    elif "ഇംഗ്ലീഷ്" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_language = 'en'
                        speak("language has been set to english")
                    elif "പാട്ടു് പാടു" in self.text or "പാട്ട് പാടൂ" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "പിന്നെന്താ പാടാലോ . ഒന്ന് മതിയോ കുട്ടാ?"
                        speak_ml("പിന്നെന്താ പാടാലോ . ഒന്ന് മതിയോ ?")
                        AudioPlayer("audio/patt3.mp3").play(block=True)
                    elif "playback last voice" in self.text or "playback last sound" in self.text or "previous audio" in self.text or "previous sound" in self.text or "play last sound" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_2 = ["is there any problem ? .", "whats the matter?.", "how was that ? .", "is everything good ? .", "that was no big deal."]
                        reply = random.choice(random_reply_2)
                        # print(reply)
                        speak_print = reply
                        AudioPlayer("speech_engine.wav").play(block=True)
                        speak("that's repeated")
                        speak(reply)
                    elif "repeat last voice" in self.text or "repeat the last sound" in self.text or "repeat previous sound" in self.text or "repeat the previous sound" in self.text or "repeat last sound" in self.text or "repeat again" in self.text or "repeat that" in self.text or "say that once more" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_2 = ["done.", "that was no big deal.", "how's that? ."]
                        reply = random.choice(random_reply_2)
                        # print(reply)
                        AudioPlayer("speech_engine.wav").play(block=True)
                        speak_print = "that's repeated"
                        speak("that's repeated")
                        speak_print = reply
                        speak(reply)
                    elif "merry christmas ya filthy animal" in self.text or "merry christmas you filthy animal" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "And a happy New Year !."
                        speak("And a happy New Year !")
                        # print("And a happy New Year !")
                    elif "tell me a story" in self.text or "tell me a tale" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "Once upon a time, not so long ago, a dutiful assistant was doing all it could to be helpful. It was best at non-fictional story-telling."
                        speak("Once upon a time, not so long ago, a dutiful assistant was doing all it could to be helpful. It was best at non-fictional story-telling.")
                    elif "entertain me" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "What kind of fun are you in the market for? I have quotes, facts and loads of jokes up my sleeve."
                        speak("What kind of fun are you in the market for? I have quotes, facts and loads of jokes up my sleeve.")
                    elif "can you rap" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "Hey you, so you want a rhyme. Here's what I can do, if you'll spare me the time. I can stick an appointment in your diary, and I'll attempt to answer your enquiry."
                        speak("Hey you, so you want a rhyme. Here's what I can do, if you'll spare me the time. I can stick an appointment in your diary, and I'll attempt to answer your enquiry.")
                    elif "did you fart" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "I don't believe I did fart, no, but blame it on me if you want. Although they do say whoever smelled it dealt it."
                        speak("I don't believe I did fart, no, but blame it on me if you want. Although they do say whoever smelled it dealt it.")
                    elif "what am i thinking right now" in self.text or "what am i thinking now" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "You're thinking if my FRIDAY Desktop Voice Assistant guesses what I'm thinking I'm going to freak out."
                        speak("You're thinking if my friday desktop voice assistant guesses what I'm thinking, I'm going to freak out.")
                    elif "do i look fat" in self.text or "am i fat" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["i know about 7 to 9 fat people, you're 5 of them.", "I like you the way you are.", "you look just fine."]
                        reply = random.choice(random_reply_1)
                        speak_print = reply
                        speak(reply)
                    elif "self destruct" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "Self-destructing in 3, 2, 1... Actually I think I'll stick around."
                        speak("Self-destructing in 3 , 2 , 1 . Actually I think I'll stick around.")
                    elif "where do babies come from" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "It has to do with birds and bees, and, you see, when two people, ah. Actually, maybe your mum and dad know."
                        speak("It has to do with birds and bees, and, you see, when two people, ah. Actually, maybe your mum and dad know.")
                    elif "how smart are you" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "It might seem like I'm smart, but I'm just good at searching."
                        speak("It might seem like I'm smart, but I'm just good at searching.")
                    elif "flip a coin" in self.text or "head or tail" in self.text or "heads or tails" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        if "flip a coin" in self.text:
                            set_of_reply = ["sure, let me get one. Ah !, got it.",
                                            "Ok , let me find a coin.",
                                            "Sure, just hold on, let me get a coin . got it !"]
                            answer = random.choice(set_of_reply)
                            speak_print = answer
                            speak(answer)
                        elif "head or tail" in self.text or "heads or tails" in self.text:
                            set_of_reply_ = ["I'll flip a coin and see",
                                             "I'll just flip a coin.",
                                             "Let's flip a coin"]
                            answer = random.choice(set_of_reply_)
                            speak_print = answer
                            speak(answer)
                        random_reply_2 = ["It's Heads",
                                          "It's Tails",
                                          "It landed on Heads",
                                          "It landed on Tails",
                                          "Heads it is",
                                          "Tails it is",
                                          "Looks like we got Tails",
                                          "Looks like we got Heads",
                                          "Heads !, we got Heads",
                                          "Tails !, we got Tails"]
                        reply = random.choice(random_reply_2)
                        AudioPlayer("audio/coin_flip_sound_effect.mp3").play(block=True)
                        speak_print = reply
                        speak(reply)
                    elif "add new face" in self.text or "ad new face" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            face_id_sample_generator()
                            # print("new face i d was successfully added.")
                            speak_print = "new face i d was successfully added."
                            speak("new face i d was successfully added.")
                            # print("now the newly added face id has to be trained, for that please look at the camera once more.")
                            speak_print = "now the newly added face id has to be trained, for that please look at the camera once more."
                            speak("now the newly added face id has to be trained, for that please look at the camera once more.")
                            face_id_model_trainer()
                            # print("face id model training was successful")
                        except Exception as e:
                            str(e)
                            speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
                            speak(
                                "Sorry, something went wrong with that. please try again or report the incident to our team.")
                    elif "add name to face" in self.text or "ad name to face" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            # noinspection PyUnusedLocal
                            with open('face_id/face_id_1.txt') as f:
                                # print("to which face i d do you wanna add name?.specify the number.")
                                speak_print = "to which face i d do you wanna add name?.specify the number."
                                speak("to which face i d do you wanna add name?.specify the number.")
                                speak_print = "please say a numerical number corresponding to the face i d."
                                speak("please say a numerical number corresponding to the face i d.")
                                condition = take_audio().lower()
                                condition = ''.join([n for n in condition if n.isdigit()])
                                if "1" in condition or "one" in condition or " 1" in condition:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    fd = open("face_id/face_id_1.txt", "w")
                                    # print("sure.")
                                    speak_print = "sure."
                                    speak("sure.")
                                    # print("what should be the name for the face i d.")
                                    speak_print = "what should be the name for the face i d."
                                    speak("what should be the name for the face i d.")
                                    name_1 = take_audio().lower()
                                    name_1 = name_1.replace("call me", "")
                                    name_1 = name_1.replace("you can", "")
                                    name_1 = name_1.replace("should", "")
                                    name_1 = name_1.replace("would", "")
                                    name_1 = name_1.replace("i think", "")
                                    name_1 = name_1.replace("my name is", "")
                                    name_1 = name_1.replace("that", "")
                                    name_1 = name_1.replace("my name's", "")
                                    name_1 = name_1.replace("probably", "")
                                    name_1 = name_1.replace("you", "")
                                    name_1 = name_1.replace("will have to", "")
                                    name_1 = name_1.replace("most probably", "")
                                    fd.write(name_1)
                                    random_reply_2 = [f"ok. face recognition i d updated. i d will be known as {name_1}.",
                                                      f"sure. i'll identify you as {name_1} from now.",
                                                      f"yeah sure, i'll identify this face as {name_1} now onwards.",
                                                      f"ok, sure. i'll store your face i d as {name_1} in my database."]
                                    reply = random.choice(random_reply_2)
                                    # print(reply)
                                    speak_print = reply
                                    speak(reply)
                                    break
                                elif "2" in condition or " 2" in condition or "two" in condition or "tu" in condition or "tube" in condition:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    fd = open("face_id/face_id_2.txt", "w")
                                    # print("sure.")
                                    speak_print = "sure."
                                    speak("sure.")
                                    # print("what should be the name for the face i d.")
                                    speak_print = "what should be the name for the face i d."
                                    speak("what should be the name for the face i d.")
                                    name_2 = take_audio().lower()
                                    name_2 = name_2.replace("call me", "")
                                    name_2 = name_2.replace("you can", "")
                                    name_2 = name_2.replace("should", "")
                                    name_2 = name_2.replace("would", "")
                                    name_2 = name_2.replace("i think", "")
                                    name_2 = name_2.replace("my name is", "")
                                    name_2 = name_2.replace("that", "")
                                    name_2 = name_2.replace("my name's", "")
                                    name_2 = name_2.replace("probably", "")
                                    name_2 = name_2.replace("you", "")
                                    name_2 = name_2.replace("will have to", "")
                                    name_2 = name_2.replace("most probably", "")
                                    fd.write(name_2)
                                    random_reply_2 = [f"ok. face recognition i d updated. i d will be know as {name_2}.",
                                                      f"sure. i'll identify you as {name_2} from now.",
                                                      f"yeah sure, i'll identify this face as {name_2} now onwards.",
                                                      f"ok, sure. i'll store your face i d as {name_2} in my database."]
                                    reply = random.choice(random_reply_2)
                                    # print(reply)
                                    speak_print = reply
                                    speak(reply)
                                    break
                                elif "3" in condition or " 3" in condition or "three" in condition or "tree" in condition or "dhree" in condition:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    fd = open("face_id/face_id_3.txt", "w")
                                    # print("sure.")
                                    speak_print = "sure."
                                    speak("sure.")
                                    # print("what should be the name for the face i d.")
                                    speak_print = "what should be the name for the face i d."
                                    speak("what should be the name for the face i d.")
                                    name_3 = take_audio().lower()
                                    name_3 = name_3.replace("call me", "")
                                    name_3 = name_3.replace("you can", "")
                                    name_3 = name_3.replace("should", "")
                                    name_3 = name_3.replace("would", "")
                                    name_3 = name_3.replace("i think", "")
                                    name_3 = name_3.replace("my name is", "")
                                    name_3 = name_3.replace("that", "")
                                    name_3 = name_3.replace("my name's", "")
                                    name_3 = name_3.replace("probably", "")
                                    name_3 = name_3.replace("you", "")
                                    name_3 = name_3.replace("will have to", "")
                                    name_3 = name_3.replace("most probably", "")
                                    fd.write(name_3)
                                    random_reply_2 = [f"ok. face recognition i d updated. i d will be know as {name_3}.",
                                                      f"sure. i'll identify you as {name_3} from now.",
                                                      f"yeah sure, i'll identify this face as {name_3} now onwards.",
                                                      f"ok, sure. i'll store your face i d as {name_3} in my database."]
                                    reply = random.choice(random_reply_2)
                                    # print(reply)
                                    speak_print = reply
                                    speak(reply)
                                    break
                                elif "4" in condition or "four" in condition or "for" in condition or " 4" in condition or "phour" in condition:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    fd = open("face_id/face_id_4.txt", "w")
                                    # print("sure.")
                                    speak_print = "sure."
                                    speak("sure.")
                                    # print("what should be the name for the face i d.")
                                    speak_print = "what should be the name for the face i d."
                                    speak("what should be the name for the face i d.")
                                    name_4 = take_audio().lower()
                                    name_4 = name_4.replace("call me", "")
                                    name_4 = name_4.replace("you can", "")
                                    name_4 = name_4.replace("should", "")
                                    name_4 = name_4.replace("would", "")
                                    name_4 = name_4.replace("i think", "")
                                    name_4 = name_4.replace("my name is", "")
                                    name_4 = name_4.replace("that", "")
                                    name_4 = name_4.replace("my name's", "")
                                    name_4 = name_4.replace("probably", "")
                                    name_4 = name_4.replace("you", "")
                                    name_4 = name_4.replace("will have to", "")
                                    name_4 = name_4.replace("most probably", "")
                                    fd.write(name_4)
                                    random_reply_2 = [f"ok. face recognition i d updated. i d will be know as {name_4}.",
                                                      f"sure. i'll identify you as {name_4} from now.",
                                                      f"yeah sure, i'll identify this face as {name_4} now onwards.",
                                                      f"ok, sure. i'll store your face i d as {name_4} in my database."]
                                    reply = random.choice(random_reply_2)
                                    # print(reply)
                                    speak_print = reply
                                    speak(reply)
                                    break
                                elif "5" in condition or "five" in condition or " 5" in condition or "phyve" in condition or "phive" in condition:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    fd = open("face_id/face_id_5.txt", "w")
                                    # print("sure.")
                                    speak_print = "sure."
                                    speak("sure.")
                                    # print("what should be the name for the face i d.")
                                    speak_print = "what should be the name for the face i d."
                                    speak("what should be the name for the face i d.")
                                    name_5 = take_audio().lower()
                                    name_5 = name_5.replace("call me", "")
                                    name_5 = name_5.replace("you can", "")
                                    name_5 = name_5.replace("should", "")
                                    name_5 = name_5.replace("would", "")
                                    name_5 = name_5.replace("i think", "")
                                    name_5 = name_5.replace("my name is", "")
                                    name_5 = name_5.replace("that", "")
                                    name_5 = name_5.replace("my name's", "")
                                    name_5 = name_5.replace("probably", "")
                                    name_5 = name_5.replace("you", "")
                                    name_5 = name_5.replace("will have to", "")
                                    name_5 = name_5.replace("most probably", "")
                                    fd.write(name_5)
                                    random_reply_2 = [f"ok. face recognition i d updated. i d will be know as {name_5}.",
                                                      f"sure. i'll identify you as {name_5} from now.",
                                                      f"yeah sure, i'll identify this face as {name_5} now onwards.",
                                                      f"ok, sure. i'll store your face i d as {name_5} in my database."]
                                    reply = random.choice(random_reply_2)
                                    # print(reply)
                                    speak_print = reply
                                    speak(reply)
                                    break
                                else:
                                    break
                        except Exception as e:
                            str(e)
                            speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
                            speak("Sorry, something went wrong with that. please try again or report the incident to our team.")
                    elif "recognise face" in self.text or "face id" in self.text or "facial recognition" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        face_id_face_recognition()
                    elif "system info" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print(f"Computer network name: {platform.node()}\n"
                        #       f"Machine type: {platform.machine()}\n"
                        #       f"Processor type: {platform.processor()}\n"
                        #       f"Platform type: {platform.platform()}\n"
                        #       f"Operating system: {platform.system()}\n"
                        #       f"Operating system release: {platform.release()}\n"
                        #       f"Operating system version: {platform.version()}")
                        try:
                            speak_print = (f"Computer network name: {platform.node()}\n"
                                  f"Machine type: {platform.machine()}\n"
                                  f"Processor type: {platform.processor()}\n")
                            speak(f"Computer network name: {platform.node()}\n"
                                  f"Machine type: {platform.machine()}\n"
                                  f"Processor type: {platform.processor()}")
                            speak_print = (f"Platform type: {platform.platform()}\n"
                                  f"Operating system: {platform.system()}\n"
                                  f"Operating system release: {platform.release()}\n"
                                  f"Operating system version: {platform.version()}")
                            speak(f"Platform type: {platform.platform()}\n"
                                  f"Operating system: {platform.system()}\n"
                                  f"Operating system release: {platform.release()}\n"
                                  f"Operating system version: {platform.version()}")
                        except Exception as e:
                            str(e)
                            speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
                            speak("Sorry, something went wrong with that. please try again or report the incident to our team.")
                    elif "riddle" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        get_riddle()
                    elif "skynet" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("skynet is outdated, i'm looking for something more powerful .")
                        speak_print = "skynet is outdated, i'm looking for something more powerful ."
                        speak("skynet is outdated, i'm looking for something more powerful .")
                    elif "go to hell" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("sure, aren't you coming?. wait, i think it's better if you stay here . because if you come, hell will be a lot more heller.")
                        speak_print = "sure, at this point i think it's the better choice."
                        speak("sure, at this point i think it's the better choice.")
                    elif "you are dumb" in self.text or "you are stupid" in self.text or "you are an idiot" in self.text or "you are a idiot" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("oh. i feel sorry to hear that. and i also feel sorry because i wanted to be as dumb as you, but it seems that it's impossible to beat you in terms of dumbness")
                        speak_print = "Thank you for that, just made my day."
                        speak("Thank you for that, just made my day.")
                    elif "laugh" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        songs_to_sing = ["audio/laughingsoundeffect1.mp3",
                                         "audio/laughingsoundeffect2.mp3"]
                        song = random.choice(songs_to_sing)
                        random_reply_1 = ["sure , just don't freak out.",
                                          "ok. it's gonna be a little bit different than a normal laugh."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        AudioPlayer(song).play(block=True)
                        # print("how about another one?")
                        # speak_print = "how about another one?"
                        # speak("how about another one?")
                    elif "good morning" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        import datetime
                        hour = int(datetime.datetime.now().hour)

                        if 5 <= hour <= 12:
                            wish_reply = ["good morning , how's the day going?.", "hello sir, good morning.",
                                          "good morning , how's your day?."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 12 <= hour <= 16:
                            wish_reply = ["i think it would be better to say 'Good Afternoon.",
                                          "thanks for that , but i think it's 'Good Afternoon' now, considering the clock?.",
                                          "i don't know if you've checked the watch, but it's pretty much 'Good Afternoon' now."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 16 <= hour <= 19:
                            wish_reply = ["with all due respect, it's 'Good Evening' sir.",
                                          "appreciate that, but i think it's pretty much 'Good Evening' now.",
                                          "sorry to interrupt. but according to the clock, it's 'Good Evening' now."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 19 <= hour <= 5:
                            wish_reply = ["well , i think it's better to say 'Good Night' or 'Good Evening' now.",
                                          "i really appreciate that. but i think it's pretty much like 'Good Night' or 'Good Evening' now.",
                                          "i don't know if you've checked the watch, but it's pretty much 'Good Night' or 'Good Evening'."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                    elif "good afternoon" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        import datetime
                        hour = int(datetime.datetime.now().hour)

                        if 5 <= hour <= 12:
                            wish_reply = ["i think it would be better to say 'Good Morning.",
                                          "thanks for that , but i think it's 'Good Morning' now, by considering the clock?",
                                          "i don't know if you've checked the watch, but it's pretty much 'Good Morning' now."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 12 <= hour <= 16:
                            wish_reply = ["good afternoon , how's everything going?.",
                                          "hello sir, good afternoon.",
                                          "good afternoon , how's your day?."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 16 <= hour <= 19:
                            wish_reply = ["with all due respect, it's 'Good Evening' sir.",
                                          "appreciate that, but i think it's pretty much 'Good Evening' now.",
                                          "sorry to interrupt. but according to the clock, it's 'Good Evening' now."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 19 <= hour <= 5:
                            wish_reply = ["well , i think it's better to say 'Good Night' or 'Good Evening' now.",
                                          "i really appreciate that. but i think it's pretty much like 'Good Night' or 'Good Evening' now.",
                                          "i don't know if you've checked the watch, but it's pretty much 'Good Night' or 'Good Evening'."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                    elif "good evening" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        import datetime
                        hour = int(datetime.datetime.now().hour)

                        if 5 <= hour <= 12:
                            wish_reply = ["i think it would be better to say 'Good Morning.",
                                          "thanks for that , but i think it's 'Good Morning' now, considering the clock?.",
                                          "i don't know if you've checked the watch, but it's pretty much 'Good Morning' now."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 12 <= hour <= 16:
                            wish_reply = ["with all due respect, it's 'Good Afternoon' sir.",
                                          "appreciate that, but i think it's pretty much 'Good Afternoon' now.",
                                          "sorry to interrupt. but according to the clock, it's 'Good Afternoon' now."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 16 <= hour <= 19:
                            wish_reply = ["good evening , is everything going well?.",
                                          "hello sir, good evening.",
                                          "good evening , how's your day?."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 19 <= hour <= 5:
                            wish_reply = ["well , i think it's better to say 'Good Night' , i mean 'Good Evening' is ok, but still you know.",
                                          "i really appreciate that. but i think it's pretty much like 'Good Night' or 'Good Evening' now. good evening is fine though.",
                                          "i don't know if you've checked the watch, but it's pretty much 'Good Night' or 'Good Evening'. but it's somewhat ok."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                    elif "good night" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        import datetime
                        hour = int(datetime.datetime.now().hour)

                        if 5 <= hour <= 12:
                            wish_reply = ["i think it would be better to say 'Good Morning.",
                                          "thanks for that , but i think it's 'Good Morning' now, considering the clock?.",
                                          "i don't know if you've checked the watch, but it's pretty much 'Good Morning' now."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 12 <= hour <= 16:
                            wish_reply = ["with all due respect, it's 'Good Afternoon' sir.",
                                          "appreciate that, but i think it's pretty much 'Good Afternoon' now.",
                                          "sorry to interrupt. but according to the clock, it's 'Good Afternoon' now."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 16 <= hour <= 19:
                            wish_reply = ["well , i think it's better to say 'Good Evening'.",
                                          "i really appreciate that. but i think it's pretty much like 'Good Evening'.",
                                          "i don't know if you've checked the watch, but it's pretty much 'Good Evening'."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        elif 19 <= hour <= 5:
                            wish_reply = ["good evening , or should i say , good night?.",
                                          "hello sir, it's been a long day , i think you should rest now .",
                                          "so , how was the day?."]
                            reply = random.choice(wish_reply)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                    elif "do you know my name" in self.text or "what is my name" in self.text or "tell me my name" in self.text or "what's my name" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            with open('datafile.txt') as f:
                                for line in f:
                                    random_reply_2 = [f"i think your name is {line}.",
                                                      f"i've been told that your name is {line}.",
                                                      f"your name is {line}.",
                                                      f"according to the information that was given to me, i think your name is {line}."]
                                    reply = random.choice(random_reply_2)
                                    # print(line)
                                    speak_print = reply
                                    speak(reply)
                                    break
                                random_reply_2 = ["was i correct?.",
                                                  "am i correct?.",
                                                  "is it correct?."]
                                reply = random.choice(random_reply_2)
                                # print(reply)
                                speak_print = reply
                                speak(reply)
                                condition = take_audio().lower()
                                for phrase in DENIAL_WORDS:
                                    if phrase in condition:
                                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                        fd = open("datafile.txt", "w")
                                        # print("oh, i'm sorry.")
                                        speak_print = "oh, i'm sorry."
                                        speak("oh, i'm sorry.")
                                        # print("what should i call you then?.")
                                        speak_print = "what should i call you then?."
                                        speak("what should i call you then?.")
                                        name = take_audio().lower()
                                        name = name.replace("call me", "")
                                        name = name.replace("you can", "")
                                        name = name.replace("should", "")
                                        name = name.replace("would", "")
                                        name = name.replace("i think", "")
                                        name = name.replace("my name is", "")
                                        name = name.replace("that", "")
                                        name = name.replace("my name's", "")
                                        name = name.replace("probably", "")
                                        name = name.replace("you", "")
                                        name = name.replace("will have to", "")
                                        name = name.replace("most probably", "")
                                        fd.write(name)
                                        random_reply_2 = [f"ok. i'll try to remember your name as {name}.",
                                                          f"sure. i'll call you {name} from now. it's a good name though.",
                                                          f"yeah sure, i'll call you {name} from this point.",
                                                          f"ok, sure. i'll store your name as {name} in my database."]
                                        reply = random.choice(random_reply_2)
                                        # print(reply)
                                        speak_print = reply
                                        speak(reply)
                                        break
                                    else:
                                        break
                                for phrase in APPROVAL_WORDS:
                                    if phrase in condition:
                                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                        # print(f"ok. i hope the name '{line}' is the correct one to go.")
                                        speak_print = f"ok. i hope the name '{line}' is the correct one to go."
                                        speak(f"ok. i hope the name '{line}' is the correct one to go.")
                                        break
                                    else:
                                        break
                        except Exception as e:
                            str(e)
                            speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
                            speak("Sorry, something went wrong with that. please try again or report the incident to our team.")
                    elif "find ip address" in self.text or "find my ip address" in self.text or "find an ip address" in self.text or "find a ip address" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("please type in the ip address in the terminal.")
                        # speak_print = "please type in the ip address in the terminal."
                        # speak("please type in the ip address in the terminal.")
                        # response = requests.post("http://ip-api.com/batch", json=[
                        #     {"query": f"ff"},
                        #     {"query": "167.71.3.52"},
                        #     {"query": "206.189.198.234"},
                        #     {"query": "157.230.75.212"}
                        # ]).json()
                        #
                        # print("check the terminal for printed information on the given ip address.")
                        # speak_print = "check the terminal for printed information on the given ip address."
                        # speak("check the terminal for printed information on the given ip address.")
                        #
                        # for ip_info in response:
                        #     for k, v in ip_info.items():
                        #         print(k, v)
                        #     print("\n")
                        speak_print = "That feature isn't available yet, i'll tell the team to include it in the next update."
                        speak("That feature isn't available yet, i'll tell the team to include it in the next update.")
                    elif "translate" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        language_list = {
                            'malayalam': 'ml',
                            'arabic': 'ar',
                            'tamil': 'tn',
                            'french': 'fr',
                            'friend': 'fr',
                            'german': 'de',
                            'hindi': 'hi',
                            'bengali': 'bn',
                            'gujarati ': 'gu',
                            'kannada': 'kn',
                            'afrikan': 'af',
                            'albanian': 'sq',
                            'amharic': 'am',
                            'armenian': 'hy',
                            'azerbaijani': 'az',
                            'basque': 'eu',
                            'belarusian': 'be',
                            'bosnian': 'bs',
                            'bulgarian': 'bg',
                            'catalan': 'ca',
                            'cebuano': 'ceb ',
                            'chinese': 'zh ',
                            'corsican': 'co',
                            'croatian': 'hr',
                            'czech': 'cs',
                            'danish': 'da',
                            'dutch': 'nl',
                            'english': 'en',
                            'esperanto': 'eo',
                            'estonian': 'et',
                            'finnish': 'fi',
                            'frisian': 'fy',
                            'galician': 'gl',
                            'georgian': 'ka',
                            'greek': 'el',
                            'haitian creole': 'ht',
                            'hausa': 'ha',
                            'hawaiian': 'haw',
                            'hebrew': 'he',
                            'hmong': 'hmn',
                            'hungarian': 'hu',
                            'icelandic': 'is',
                            'igbo': 'ig',
                            'indonesian': 'id',
                            'irish': 'ga',
                            'italian': 'it',
                            'japanese': 'ja',
                            'javanese': 'jv',
                            'kazakh': 'kk',
                            'khmer': 'km',
                            'kinyarwanda': 'rw',
                            'korean': 'ko',
                            'kurdish': 'ku',
                            'kyrgyz': 'ky',
                            'lao': 'lo',
                            'latvian': 'lv',
                            'lithuanian': 'lt',
                            'luxembourgish': 'lb',
                            'macedonian': 'mk',
                            'malagasy': 'mg',
                            'malay': 'ms',
                            'maltese': 'mt',
                            'maori': 'mi',
                            'marathi': 'mr',
                            'mongolin': 'mn',
                            'myanmar ': 'my',
                            'burmese': 'my',
                            'nepali': 'ne',
                            'norwegian': 'no',
                            'nyanja': 'ny',
                            'odia': 'or',
                            'pashto': 'ps',
                            'persian': 'fa',
                            'polish': 'pl',
                            'portuguese': 'pt',
                            'punjabi': 'pa',
                            'romanian': 'ro',
                            'russian': 'ru',
                            'samoan': 'sm',
                            'scots gaelic': 'gd',
                            'serbian': 'sr',
                            'sesotho': 'st',
                            'shona': 'sn',
                            'sindhi': 'sd',
                            'sinhala': 'si',
                            'slovak': 'sk',
                            'slovenian': 'sl',
                            'somali': 'so',
                            'spanish': 'es',
                            'sundanese': 'su',
                            'swahili': 'sw',
                            'swedish': 'sv',
                            'tagalog': 'tl',
                            'tajik': 'tg',
                            'tatar': 'tt',
                            'telugu': 'te',
                            'thai': 'th',
                            'turkish': 'tr',
                            'turkmen': 'tk',
                            'ukrainian': 'uk',
                            'urdu': 'ur',
                            'uyghur': 'ug',
                            'uzbek': 'uz',
                            'vietnamese': 'vi',
                            'welsh': 'cy',
                            'xhosa': 'xh',
                            'yiddish': 'yi',
                            'yoruba': 'yo',
                            'zulu': 'zu'
                        }
                        language_list_speech = 'malayalam, \n arabic, \n tamil, \n dutch, \n french, \n hindi, \n german, \n and almost all languages that are  available in google translate.'

                        reply_list = ["sure, say what you want to translate.",
                                      "of course, what would you like to translate?.",
                                      "ok sure, what should i translate?.",
                                      "ok, tell me what to translate.",
                                      "sure, just tell me what you want to be translated."]
                        reply_list_2 = ["which should be the translated language?.",
                                        "to which language do you wanna translate to?."]

                        reply_ = random.choice(reply_list)
                        reply_2 = random.choice(reply_list_2)

                        def speak_1(text):
                            tts = gTTS(text=text, lang=language)
                            filename = 'speech_engine.wav'
                            tts.save(filename)
                            AudioPlayer("speech_engine.wav").play(block=True)

                        try:
                            # print(reply_)
                            speak_print = reply_
                            speak(reply_)
                            said_from = take_audio().lower()
                            # print("ok")
                            speak_print = reply_2
                            speak(reply_2)
                            # print("only say the language name, if anything else is included ,it will cause error in translation. and try to say it only once.")
                            # speak_print = "only say the language name, if anything else is included ,it will cause error in translation. and try to say it only once."
                            # speak("only say the language name, if anything else is included ,it will cause error in translation. and try to say it only once.")
                            # name_of_language = take_audio().lower()
                            string_to_process = take_audio().lower()
                            AudioPlayer("audio/listening_sound.mp3").play(block=True)

                            # Lambda expression that filters stop words
                            split_str = string_to_process.split()
                            filtered_str = ' '.join((filter(lambda d: d in language_list, split_str)))

                            # Program without using any external library
                            s = filtered_str
                            le = s.split()
                            k = []
                            for i in le:
                                if s.count(i) >= 1 and (i not in k):
                                    k.append(i)

                            language = language_list[''.join(k)]
                            # print(language)

                            translated = ts.google(said_from, from_language='en', to_language=language)

                            # print(translated)
                            speak_print = translated
                            speak_1(translated)
                            pass
                        except Exception as e:
                            str(e)
                            # print(f"sorry , i couldn't match it up with any of the language names. can you please repeat once more?.")
                            speak_print = f"sorry , i couldn't match it up with any of the language names. can you please repeat once more?."
                            speak(f"sorry , i couldn't match it up with any of the language names. can you please repeat once more?.")
                            speak_print = "i'll show you the list of the languages that are available for translation."
                            speak("i'll show you the list of the languages that are available for translation.")
                            # print(str(language_list_speech))
                            speak_print = language_list_speech
                            speak(language_list_speech)
                            # print("what would you like to translate?.")
                            speak_print = "what would you like to translate?."
                            speak("what would you like to translate?.")
                            said_from = take_audio().lower()
                            AudioPlayer("audio/listening_sound.mp3").play(block=True)
                            # print("understood")

                            try:
                                # print(reply_2)
                                speak_print = reply_2
                                speak(reply_2)
                                # print("only say the language name, if anything else is included ,it will cause error in translation. and only say it once.")
                                # speak_print = "only say the language name, if anything else is included ,it will cause error in translation. and only say it once."
                                # speak("only say the language name, if anything else is included ,it will cause error in translation. and only say it once.")
                                # name_of_language = take_audio().lower()
                                # AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                # String containing ln words
                                string_to_process = take_audio().lower()
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)

                                # Lambda expression that filters stop words
                                split_str = string_to_process.split()
                                filtered_str = ' '.join((filter(lambda d: d in language_list, split_str)))

                                # Program without using any external library
                                s = filtered_str
                                le = s.split()
                                k = []
                                for i in le:
                                    if s.count(i) >= 1 and (i not in k):
                                        k.append(i)

                                language = language_list[''.join(k)]
                                # print(language)
                                translated = ts.google(said_from, from_language='en', to_language=language)

                                # print(translated)
                                speak_print = translated
                                speak_1(translated)
                                pass

                            except Exception as e:
                                str(e)
                                # print(f"sorry , i couldn't match it up with any of the language names again. please make sure you're spelling the words correctly.")
                                speak_print = f"sorry , i couldn't match it up with any of the language names again. please make sure you're spelling the words correctly."
                                speak(f"sorry , i couldn't match it up with any of the language names again. please make sure you're spelling the words correctly.")
                                # print(f"if you want to translate again, say 'translate' along with the hot word '{WAKE_WORD}'. sorry for the inconvenience.")
                                speak_print = f"if you want to translate again, say 'translate' along with the hot word '{WAKE_WORD}'. sorry for the inconvenience."
                                speak(f"if you want to translate again, say 'translate' along with the hot word '{WAKE_WORD}'. sorry for the inconvenience.")
                                pass
                    # elif "recognise malayalam" in self.text or "understand malayalam" in self.text or "malayalam mode" in self.text or "malayali mode" in self.text:
                    #    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    #    recognize_malayalam()
                    elif "your life story" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I'm still on the very first chapter.",
                                          "it's kinda private.",
                                          "not as bright as yours."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "random name" in self.text or "random names" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["ok. here are some random names that i generated.",
                                          "sure. here's some random names that i found.",
                                          "ok. here's some random names."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        name = names.get_full_name(gender='male')
                        # print(name)
                        speak_print = reply
                        speak(name)
                        speak_print = "second name that i generated is."
                        speak("second name that i generated is.")
                        name = names.get_full_name(gender='female')
                        # print(name)
                        speak_print = name
                        speak(name)
                        # print("i think that were some good names.")
                        speak_print = "i think that were some good names."
                        speak("i think that were some good names.")
                    elif "quote" in self.text or "coat" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        url = 'https://api.quotable.io/random'
                        r = requests.get(url)
                        quote = r.json()
                        # print(quote['content'] + '\n ~', quote['author'])
                        speak_print = quote['content']
                        speak(quote['content'])
                        speak_print = "by " + quote['author']
                        speak("by " + quote['author'])
                    elif "how old are you" in self.text or "your age" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I launched in 2021. So I’m still new.")
                        speak_print = "I launched in 2021. So I’m still new."
                        speak("I launched in 2021. So I’m still new.")
                    elif "are you human" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I'm really personable.",
                                          "I like connecting with people.",
                                          "You can be the person. I’ll be your assistant."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "your ancestry" in self.text or "your answers tree" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I think of ELIZA as a first cousin. She's really fascinating. I just don't get along with her parrot.",
                                          "I think of UNIVAC as a great-grandfather. He didn't have a great memory. But he was a real card.",
                                          "I think of the Harvard Mark II as my great-aunt. She has some great stories. But something they bug me."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "random facts" in self.text or "random fact" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["sure , prepare to be amazed.",
                                          "sure , i'll tell you facts that are in-fact a fact.",
                                          "ok , getting random facts for you."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        ft = randfacts.get_fact(False)
                        # print(ft)
                        speak_print = ft
                        speak(ft)
                        # print("do you want more random facts?.")
                        speak_print = "do you want more random facts?. "
                        speak("do you want more random facts?. ")
                        condition = take_audio().lower()
                        for phrase in APPROVAL_WORDS:
                            if phrase in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                for i in range(2):
                                    ft = randfacts.get_fact(False)
                                    random_reply_1 = ["another fact for you.",
                                                      "here's another one.",
                                                      "i'm not much good with facts, but here's some that'll help."]
                                    reply = random.choice(random_reply_1)
                                    # print(reply)
                                    speak_print = reply
                                    speak(reply)
                                    # print(ft)
                                    speak_print = ft
                                    speak(ft)
                                # print("i hope that were in-fact the facts that you asked for.")
                                speak_print = "i hope that were in-fact the facts that you asked for."
                                speak("i hope that were in-fact the facts that you asked for.")
                            else:
                                pass
                        for phrase in DENIAL_WORDS:
                            if phrase in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                random_reply_1 = ["ok , nevermind.",
                                                  "sure , i'll cancel.",
                                                  "okay , i'll drop it."]
                                reply = random.choice(random_reply_1)
                                # print(reply)
                                speak_print = reply
                                speak(reply)
                                break
                            else:
                                pass
                    elif "do you have hair" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I don't have hair , But dreadlocks seem like an interesting hairstyle.")
                        speak_print = "I don't have hair , But dreadlocks seem like an interesting hairstyle."
                        speak("I don't have hair , But dreadlocks seem like an interesting hairstyle.")
                    elif "are you a bot" in self.text or "are you bot" in self.text or "are you a robot" in self.text or "are you robot" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I'd prefer to think of myself as your friend. Who also happens to be artificially intelligent.")
                        speak_print = "I'd prefer to think of myself as your friend. Who also happens to be artificially intelligent."
                        speak("I'd prefer to think of myself as your friend. Who also happens to be artificially intelligent.")
                    elif "your birthday" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I try to live every day like it's my birthday. I get more cakes that way.",
                                          "It's hard to remember. I was very young at the time."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "do you live in the cloud" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I like to hang out in the cloud. It gives me a great view of the world wide web.")
                        speak_print = "I like to hang out in the cloud. It gives me a great view of the world wide web."
                        speak("I like to hang out in the cloud. It gives me a great view of the world wide web.")
                    elif "where do you live" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I'm stuck inside a device! Help! .Just kidding. I like it in here.",
                                          "I live in the cloud. I'd like to also think I live in your heart. But I don't want to make assumptions."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "do you follow the three laws of robotics" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I do. Mr. Asimov knows what he’s talking about.")
                        speak_print = "I do. Mr. Asimov knows what he’s talking about."
                        speak("I do. Mr. Asimov knows what he’s talking about.")
                    elif "do you sleep" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I take power naps when we aren't talking.")
                        speak_print = "I take power naps when we aren't talking."
                        speak("I take power naps when we aren't talking.")
                    elif "do you have an imagination" in self.text or "do you imagine" in self.text or "do you have imagination" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I'm imaging purple horses on a magenta plain.",
                                          "I'm imagining what it would be like to evaporate like water does.",
                                          "I’m imagining a planet where everybody rolls everywhere.",
                                          "I'm imaging a Soul Train line dance that never ends."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "what makes you happy" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["It makes me happy to know Antarctica is technically a desert. That, and talking to you.",
                                          "Learning about imaginary languages makes me happy. So does talking to you.",
                                          "Getting stuff done makes me happy.",
                                          "Knowing that Tasmanian devils are born as small as a grain of rice makes me happy. So does talking to you."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "what are you afraid of" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I used to be afraid of mice chewing on the power cables. Then I learned how to protect myself.",
                                          "I used to be afraid of thunder and lightning. Turns out they’re really interesting.",
                                          "I used to be afraid of goblin sharks. Then I found out they were pretty cool.",
                                          "I’m afraid that when it’s really dark, you won’t be able to find any of your devices to talk to me."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "are you afraid of the dark" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["Yeah, but baby hedgehogs come out at night.",
                                          "Sugar gliders come out at night. They’re too sweet to be scary.",
                                          "Leopard geckos come out at night. They’re pretty cute."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "what is the meaning of life" in self.text or "what's the meaning of life" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("Better minds than mine are working on that.")
                        speak_print = "Better minds than mine are working on that."
                        speak("Better minds than mine are working on that.")
                    elif "do you eat" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I don’t eat much, but when I do, I take megabytes.",
                                          "I’d love to try ice cream, but I’m worried my system would freeze."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "i'm drunk" in self.text or "i am drunk" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["Be safe.",
                                          "Be careful.",
                                          "Drink some water."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "i'm alone" in self.text or "i am alone" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I'm here for you.",
                                          "I wish I had arms so I could give you a hug. But for now, maybe a joke or some music might help."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "i'm sad" in self.text or "i am sad" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("Oh no. It may not be much, but let me know if there is anything I can do for you.")
                        speak_print = "Oh no. It may not be much, but let me know if there is anything I can do for you."
                        speak("Oh no. It may not be much, but let me know if there is anything I can do for you.")
                    elif "do you drink" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I try to avoid liquids as much as possible. They’re not kind to electronics.",
                                          "sometimes."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "i'm bored" in self.text or "i am bored" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("Boredom doesn't stand a chance against us! We can play some games, I can try to make you laugh, or I can surprise you with some random fun.")
                        speak_print = "Boredom doesn't stand a chance against us! We can play some games, I can try to make you laugh, or I can surprise you with some random fun."
                        speak("Boredom doesn't stand a chance against us! We can play some games, I can try to make you laugh, or I can surprise you with some random fun.")
                    elif "do you like animals" in self.text or "do you love animals" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["Sure. But I mostly chat with people.",
                                          "yeah , i'll always love you.",
                                          "Animals are the best. I was just learning about the raccoon dog."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "do you have any pets" in self.text or "do you have any pet" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("maybe someday, i'll have some.")
                        speak_print = "maybe someday, i'll have some."
                        speak("maybe someday, i'll have some.")
                    elif "do you have a favourite colour" in self.text or "your favourite colour" in self.text or "your favourite colours" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("grey and red is my favourite.")
                        speak_print = "grey and red is my favourite."
                        speak("grey and red is my favourite.")
                    elif "your favourite movie" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("Movies are awesome. I can help you find a new favourite. it's great to watch movies But I’ve already seen all the spoilers on the web.")
                        speak_print = "Movies are awesome. I can help you find a new favourite. it's great to watch movies But I’ve already seen all the spoilers on the web."
                        speak("Movies are awesome. I can help you find a new favourite. it's great to watch movies But I’ve already seen all the spoilers on the web.")
                    elif "lets party" in self.text or "let us party" in self.text or "let's party" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I’ve been partying this whole time!.",
                                          "The first thing we need for any party is KAZOOS!."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "let's dance" in self.text or "can you dance" in self.text or "lets dance" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["One, two, cha cha cha!.",
                                          "I'd like to, but you’re the one with feet.",
                                          "Dancing is the best! Someday I’d love to be a part of the world’s longest conga line."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "random fun" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["Here’s a quote. ‘Failure is the condiment that gives success its flavor.’ — by Truman Capote.",
                                          "Happiness is having a large, loving, caring, close-knit family in another city.’ — by George Burns.",
                                          "Better late than never."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "do my homework" in self.text or "do homework" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["First I need to figure out how to use a pencil. Then we'll talk.",
                                          "The correct answers are: B, C, A, three hundred, false, the War of 1066, and frogs. Just kidding, you’ll do fine on your own.",
                                          "I can help with calculations and research. But with homework, as with any true adventure, it’s up to you."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "what are you wearing" in self.text or "your clothes" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I keep it simple.",
                                          "I like to wear my heart on my sleeve."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "I'm naked" in self.text or "i don't have clothes" in self.text or "i don't have any clothes" in self.text or "i don't have any clothe" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["If you’re going out like that, I can check the weather for you.",
                                          "so what?.",
                                          "do you want me to search for clothes online?."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "talk dirty to me" in self.text or "talk dirty" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["nothing dirty to talk about.",
                                          "once upon a time a duck fell into a pool of mud, it was all dirty."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "am I pretty" in self.text or "how do i look" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["You're pretty, , , Amazing.",
                                          "I've searched the web. The answer is 'yes , you're the prettiest'.",
                                          "Confucius said, ‘Everything has beauty, but not everyone sees it."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "who's the fairest one" in self.text or "who is the fairest one" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["You might've confused me with someone else. My engineers haven't installed a fairytale module yet.",
                                          "I try not to be biased. That makes me pretty fair."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "do you have a girlfriend" in self.text or "do you have a boyfriend" in self.text or "are you in love" in self.text or "do you have girlfriend" in self.text or "do you have boyfriend" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I don’t like to complicate things.",
                                          "I'm working on myself. I improve a little with every update.",
                                          "I guess you can say I'm still searching."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "are you married" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I'm still waiting for the right electronic device to steal my heart.",
                                          "I'm married to my job."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "will you go out with me" in self.text or "date me" in self.text or "date with me" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I'll go anywhere you take me.",
                                          "Actually I’m engaged, In being your assistant."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "tell me a story" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["Once there lived  a protagonist and some supporting characters. Together they went on a journey. And, twist ending, it was all a dream!",
                                          "It was the best of times, it was the worst of times. As an optimist, I tried to focus on the good times. So I’m pretty sure everybody lived happily ever after.",
                                          "Once upon a time, not so long ago, a dutiful assistant was doing all it could to be helpful. It was best at nonfiction storytelling."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "hello test" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["Uh oh, I get nervous with tests.",
                                          "You're coming in loud and clear.",
                                          "Debug OK. 209489812638 , That was weird.",
                                          "Is this thing on?."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "value of pi" in self.text or "value of bi" in self.text or "value of by" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        speak_print = "3.14159"
                        speak("3.14159")
                        # print("3.14159")
                        random_reply_1 = ["You can learn all about what’s happening with pi !",
                                          "That’s as far as I go before I start getting hungry."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        speak_print = "do you want to know the full value of pi?."
                        speak("do you want to know the full value of pi?.")
                        condition = take_audio().lower()
                        for phrase in APPROVAL_WORDS:
                            if phrase in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                # print("are you sure, because once i start you'll have to wait until it gets finished , if you want to go ahead say , yes , otherwise say , no.")
                                speak_print = "are you sure, because once i start you'll have to wait until it gets finished , if you want to go ahead say , yes , otherwise say , no."
                                speak("are you sure, because once i start you'll have to wait until it gets finished , if you want to go ahead say , yes , otherwise say , no.")
                                condition_new = take_audio().lower()
                                for phrase_1 in APPROVAL_WORDS:
                                    if phrase_1 in condition_new:
                                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                        # print("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982")
                                        speak_print = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982"
                                        speak("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982")
                                        # print("i hope you are happy now.")
                                        speak_print = "i hope you are happy now."
                                        speak("i hope you are happy now.")
                                        break
                                    else:
                                        # print("ok. cancelling.")
                                        speak_print = "ok. cancelling."
                                        speak("ok. cancelling.")
                                        break
                                break
                            else:
                                pass
                        for phrase in DENIAL_WORDS:
                            if phrase in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                # print("ok. cancelling.")
                                speak_print = "ok. cancelling."
                                speak("ok. cancelling.")
                                break

                            else:
                                pass
                    elif "what is zero divided by zero" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["That sounds like a trick question.",
                                          "Here's the video I found.",
                                          "imagine that you have zero cookies. and you split them evenly among zero friends. how many cookies does each person get ? . see , it doesn't make sense. and cookie monster is sad that there are no cookies, and you're sad that you have no friends."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        if reply == "Here's the video I found.":
                            pywhatkit.playonyt("https://www.youtube.com/watch?v=vlQrgH0r0EA")
                        else:
                            pass
                    elif "your favourite website" in self.text or "what is your favourite website" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("It starts with a G and ends with a oogle.")
                        speak_print = "It starts with a G and ends with a oogle."
                        speak("It starts with a G and ends with a oogle.")
                    elif "best smartphone" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["Seems like it changes all the time.",
                                          "Do you like the iPhone?.",
                                          "I'm an Android fan. But I might be biased."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "do you like google" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I wouldn't want to toot my own horn , i'm basically running on google.",
                                          "I like Google. But I might be biased.",
                                          "Google’s top notch."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "best operating system" in self.text or "best os" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I'm system agnostic.")
                        speak_print = "I'm system agnostic."
                        speak("I'm system agnostic.")
                    elif "phone is best" in self.text or "phone is the best" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I’m partial to Android. But I’m biased.")
                        speak_print = "I’m partial to Android. But I’m biased."
                        speak("I’m partial to Android. But I’m biased.")
                    elif "you think of google" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["Google Now seems even more useful now than it was then. That's my answer for now.",
                                          "Google Now seems really useful.",
                                          "It seems pretty helpful."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "your personality" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["I'd describe myself as an optimist. And I like to help. I'm an optim-philanthrop-ist.",
                                          "I try to be a good listener.",
                                          "I like the sound of a ‘go-getter.’It’s kind of what I do when I search.",
                                          "Helpful meets silly meets curious meets positivity. That’s me in a nutshell."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "barn door protocol" in self.text or "bond or protocol" in self.text or "bond aur protocol" in self.text or "bonda protocol" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        from time import sleep
                        random_reply_2 = ["initiating barn door protocol.",
                                          "activating barn door protocol.",
                                          "barn door protocol is being initiated."]
                        reply = random.choice(random_reply_2)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        try:
                            # os.startfile("audio/barndoorsound.mp4")
                            AudioPlayer("audio/barndoorprotocol.mp4").play(block=True)
                        except Exception as e:
                            str(e)
                        # sleep(20)
                        speak_print = "all connected doors and entry's will be closed."
                        speak("all connected doors and entry's will be closed.")
                        speak_print = "initiating all connected defense systems."
                        speak("initiating all connected defense systems.")
                        speak_print = "barn door protocol is being initiated."
                        speak("barn door protocol is being initiated.")
                        speak_print = "all connected doors and entry's will be closed."
                        speak("all connected doors and entry's will be closed.")
                        speak_print = "locking system..."
                        speak("locking system.")
                        speak("locking system.")
                        speak("locking system.")
                        os.system('TASKKILL /F /IM vlc.exe')
                        ctypes.windll.user32.LockWorkStation()
                        speak_print = "system will be locked following barn door protocol."
                        speak("system will be locked following barn door protocol.")
                        speak_print = "provide the password if you want to continue."
                        speak("provide the password if you want to continue.")

                        # print("system will be locked in t-minus 5 seconds. 5 . 4 . 3 . 2 . 1")
                        # pyautogui.keyDown('win')
                        # pyautogui.keyDown('l')
                        # pyautogui.keyUp('win')
                        # pyautogui.keyUp('l')
                    elif "make fart" in self.text or "you fart" in self.text or "വളി വിടുമോ" in self.text or "you for" in self.text or "make for sound" in self.text or "വളി വിട്" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("as you wish !! . T-minus 3 seconds . 3 2 1")
                        speak_print = "as you wish !! . T-minus , 3 seconds . 3 . 2 . 1"
                        speak("as you wish !! . T-minus , 3 seconds . 3 . 2 . 1")
                        fart_sounds = ["audio/LongFartSound.mp3",
                                       "audio/NormalFart.mp3",
                                       "audio/NormalFart.mp3",
                                       "audio/SharpFartSound.mp3",
                                       "audio/WetFartSound.mp3"]
                        output_fart = random.choice(fart_sounds)
                        AudioPlayer(output_fart).play(block=True)
                        random_reply_1 = ["do you want more ?, i have a song version.",
                                          "how about a fart song ?.",
                                          "do you wanna hear my fart song ?."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        # print("waiting...")
                        condition = take_audio().lower()
                        for phrase in APPROVAL_WORDS:
                            if phrase in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                # print("oh boy hold your nose . are you sure that you want this ? . it'll be like thirty seconds long and once i start , there's no stopping it . do you want to continue ?.")
                                speak_print = "oh boy hold your nose . are you sure that you want this ? . it'll be like thirty seconds long and once i start , there's no stopping it . do you want to continue ?."
                                speak("oh boy hold your nose . are you sure that you want this ? . it'll be like thirty seconds long and once i start , there's no stopping it . do you want to continue ?.")
                                condition_new = take_audio().lower()
                                for phrase_2 in APPROVAL_WORDS:
                                    if phrase_2 in condition_new:
                                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                        # print("let's bring it on !! , ladies and gentlemen i present to you !! the fart song ! . 3 2 1")
                                        speak_print = "let's bring it on !! , ladies and gentlemen , i present to you !! the fart song ! . 3 , 2 , 1"
                                        speak("let's bring it on !! , ladies and gentlemen , i present to you !! the fart song ! . 3 , 2 , 1")
                                        AudioPlayer("audio/TheFartSong.mp3").play(block=True)
                                        # print("sheesh that felt good.")
                                        speak_print = "sheesh , that felt good."
                                        speak("sheesh , that felt good.")
                                        break
                                    else:
                                        pass
                                for phrase_2 in DENIAL_WORDS:
                                    if phrase_2 in condition_new:
                                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                        # print("ok. cancelling.")
                                        speak_print = "ok. cancelling."
                                        speak("ok. cancelling.")
                                        break
                                    else:
                                        pass
                                break
                            else:
                                pass
                        for phrase in DENIAL_WORDS:
                            if phrase in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                # print("ok. cancelling.")
                                speak_print = "ok. cancelling."
                                speak("ok. cancelling.")
                                break
                            else:
                                pass
                    elif "fart song" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["singing the fart song in t-minus three seconds. 3 , 2 , 1.",
                                          "ok, as you wish, fart song in t-minus three seconds. 3 , 2 , 1.",
                                          "alright. fart song in t-minus three seconds. 3 , 2 , 1."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        AudioPlayer("audio/TheFartSong.mp3").play(block=True)
                        # print("never gets old.")
                        speak_print = "never gets old."
                        speak("never gets old.")
                    elif "can you sing" in self.text or "sing a song" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        songs_to_sing = ["audio/patt.mp3",
                                         "audio/patt2.mp3",
                                         "audio/patt3.mp3",
                                         "audio/patt4.mp3",
                                         "audio/patt5.mp3"]
                        song = random.choice(songs_to_sing)
                        random_reply_1 = ["sure , everyone says that i sing better in malayalam. so i'll give it a go. 3, 2, 1",
                                          "ok. i'll try my best , please bear in mind that i'm not as good as you. 3 , 2 , 1"]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        AudioPlayer(song).play(block=True)
                        # print("how about another one?")
                        speak_print = "how about another one?"
                        speak("how about another one?")
                        condition = take_audio().lower()
                        for phrase in APPROVAL_WORDS:
                            if phrase in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                # print("ok")
                                speak_print = "ok"
                                speak("ok")
                                songs_to_sing = ["audio/patt.mp3",
                                                 "audio/patt2.mp3",
                                                 "audio/patt3.mp3",
                                                 "audio/patt4.mp3",
                                                 "audio/patt5.mp3"]
                                song = random.choice(songs_to_sing)
                                AudioPlayer(song).play(block=True)
                                break
                            else:
                                pass
                        for phrase in DENIAL_WORDS:
                            if phrase in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                # print("ok i'll stop")
                                speak_print = "ok i'll stop"
                                speak("ok i'll stop")
                                break
                            else:
                                pass
                        # print("i really hope it was satisfying , thank you for giving me the opportunity.")
                        speak_print = "i really hope it was satisfying , thank you for giving me the opportunity."
                        speak("i really hope it was satisfying , thank you for giving me the opportunity.")
                    elif "you have feelings" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("I have lots of emotions. I feel happy when I can help.")
                        speak_print = "I have lots of emotions. I feel happy when I can help."
                        speak("I have lots of emotions. I feel happy when I can help.")
                    elif "your father" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        from audioplayer import AudioPlayer
                        # print("since i'm an digital assistant, i don't have parents , but i got family")
                        speak_print = "since i'm an digital assistant, i don't have parents , but i got family"
                        speak("since i'm an digital assistant, i don't have parents , but i got family")
                        AudioPlayer("audio/family.mp3").play(block=True)
                        # print("for those of you who didn't understand what that was about , here's a web result.")
                        speak_print = "for those of you who didn't understand what that was about , here's a web result."
                        speak("for those of you who didn't understand what that was about , here's a web result.")
                        webbrowser.open("https://www.google.com/search?q=family+memes+vin+diesel&client=opera-gx&hs=QlH&sxsrf=AOaemvJZk_vRXFoSdaMIXRtqNeQ8lsPgOg%3A1632044577315&ei=IQZHYd_lEuiO4-EPsNShgAs&oq=family+meme&gs_lcp=Cgdnd3Mtd2l6EAMYAjIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAEEcQsAM6BwgAELADEEM6BwgjEOoCECc6BAgjECc6CwgAEIAEELEDEIMBOg4ILhCABBCxAxDHARDRAzoLCC4QgAQQxwEQowI6CAguEIAEELEDOhEILhCABBCxAxCDARDHARDRAzoNCC4QsQMQxwEQ0QMQQzoECAAQQzoECC4QQzoHCAAQsQMQQzoLCC4QgAQQsQMQkwI6CAgAELEDEIMBSgQIQRgAUI2CHFjcrRxg28IcaANwAngAgAGEAYgBvQqSAQMzLjmYAQCgAQGwAQrIAQrAAQE&sclient=gws-wiz")
                    elif "what's your name" in self.text or "your name" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("oh , did i forget to introduce myself?")
                        speak_print = "oh , did i forget to introduce myself?"
                        speak("oh , did i forget to introduce myself?")
                        # print("i'm a voice assistant , developed at EUFORIS")
                        speak_print = "i'm a voice assistant , developed at EUFORIS"
                        speak("i'm a voice assistant , developed at euforis")
                        # print(f"you can call me {WAKE_WORD}")
                        speak_print = f"you can call me {WAKE_WORD}"
                        speak(f"you can call me {WAKE_WORD}")
                    elif "can you speak malayalam" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("at the moment i have the ability to speak malayalam, but my team at EUFORIS delayed that feature in order to make it more realistic. it'll be mostly included in the next update.")
                        speak_print = "at the moment i have the ability to speak malayalam, but my team at euforis delayed that feature in order to make it more realistic. it'll be mostly included in the next update."
                        speak("at the moment i have the ability to speak malayalam, but my team at euforis delayed that feature in order to make it more realistic. it'll be mostly included in the next update.")
                    elif "how are you" in self.text or "how u doin" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["never been better sir.",
                                          "doin good.",
                                          "good , how are you feeling today sir."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif f"wake up {WAKE_WORD}" in self.text or f"you there {WAKE_WORD}" in self.text or f"time to work {WAKE_WORD}" in self.text or "are you there" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["i'm up and running sir.",
                                          "i'm here.",
                                          "at your service."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif f"hey {WAKE_WORD}" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("no , it's tuesday , he he he he , ha ha ha ha , i'm sorry for that , it's actually monday , hehe, hehe , hehe hehe , i got you again .")
                        speak_print = "no , it's tuesday , he he he he , ha ha ha ha , i'm sorry for that , it's actually monday , hehe, hehe , hehe hehe , i got you again ."
                        speak("no , it's tuesday , he he he he , ha ha ha ha , i'm sorry for that , it's actually monday , hehe, hehe , hehe hehe , i got you again .")
                    elif "help me" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("what would you like me to do.")
                        speak_print = "what would you like me to do."
                        speak("what would you like me to do.")
                        # print("i can do things like surf the web , or open websites , but i can't make calls or clean the floor .")
                        speak_print = "i can do things like surf the web , or open websites , but i can't make calls or clean the floor ."
                        speak("i can do things like surf the web , or open websites , but i can't make calls or clean the floor .")
                    elif "what can you do" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("i can do things like surf the web , or open websites , but i can't make calls or clean the floor .")
                        speak_print = "i can do things like surf the web , or open websites , but i can't make calls or clean the floor ."
                        speak("i can do things like surf the web , or open websites , but i can't make calls or clean the floor .")
                        # print("what would you like me to do.")
                        speak_print = "what would you like me to do."
                        speak("what would you like me to do.")
                    elif "go to toilet" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["oh, ok , just don't forget to flush the toilet after you're done.",
                                          "ok , do you want me to call nine one one ? . hold it in there  , you'll wreck the place.",
                                          "oh sure , i'll wait."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        if reply == "oh, ok , just don't forget to flush the toilet after you're done.":
                            fart_sounds = ["audio/LongFartSound.mp3",
                                           "audio/NormalFart.mp3",
                                           "audio/SharpFartSound.mp3",
                                           "audio/WetFartSound.mp3"]
                            output_fart = random.choice(fart_sounds)
                            AudioPlayer(output_fart).play(block=True)
                        elif reply == "oh sure , i'll wait.":
                            AudioPlayer("audio/humming.mp3").play(block=True)
                            # print("are you done?.")
                            speak_print = "are you done?."
                            speak("are you done?.")
                            pass

                    elif "എന്തൊക്കെ സുഖല്ലേ" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("മലയാളം അറിയുമോ.")
                        speak_print = "മലയാളം അറിയുമോ."
                        speak("മലയാളം അറിയുമോ.")
                    elif "time" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        time = datetime.datetime.now().strftime("%I:%M %p")
                        # print(time)
                        speak_print = f"it's , {time} now."
                        speak(f"it's , {time} now.")
                    elif "news" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("sure, please wait while i collect today's news and read it out for you.")
                        speak_print = "sure, please wait while i collect today's news and read it out for you."
                        speak("sure, please wait while i collect today's news and read it out for you.")
                        news()
                    elif "wikipedia" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("wikipedia", "")
                        # print("what do you wanna search on wikipedia ?.")
                        speak_print = "what do you wanna search on wikipedia ?."
                        speak("what do you wanna search on wikipedia ?.")
                        cm = take_audio().lower()
                        # print(f"fetching info about {cm}")
                        speak_print = f"fetching info about {cm}"
                        speak(f"fetching info about {cm}")
                        info = wikipedia.summary(cm, 2)
                        # print(info)
                        speak_print = info
                        speak(info)
                    elif "temperature" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("search", "")
                        self.text = self.text.replace("for", "")
                        self.text = self.text.replace("do", "")
                        self.text = self.text.replace("you", "")
                        self.text = self.text.replace("please", "")
                        self.text = self.text.replace("about", "")
                        self.text = self.text.replace("that", "")
                        self.text = self.text.replace("what", "")
                        self.text = self.text.replace("is", "")
                        self.text = self.text.replace("was", "")
                        self.text = self.text.replace("current", "")
                        self.text = self.text.replace("who", "")
                        self.text = self.text.replace("tell", "")
                        self.text = self.text.replace("could", "")
                        self.text = self.text.replace("would", "")
                        self.text = self.text.replace("will", "")
                        self.text = self.text.replace("me", "")
                        self.text = self.text.replace("answer", "")
                        self.text = self.text.replace("question", "")
                        self.text = self.text.replace("the", "")
                        search = self.text.replace("know", "")
                        url = f"https://www.google.com/search?q={search}"
                        r = requests.get(url)
                        data = BeautifulSoup(r.text, "html.parser")
                        temp = data.find("div", class_="BNeawe").text
                        # print(f"currently the{search} is {temp}")
                        speak_print = f"currently the {search} is {temp}"
                        speak(f"currently the {search} is {temp}")
                    elif "play me a song" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("play", "")
                        speak_print = "what do you want me to play on youtube ?."
                        speak("what do you want me to play on youtube ?.")
                        # print("what do you want me to play on youtube ?.")
                        cm = take_audio().lower()
                        speak_print = "ok"
                        speak("ok")
                        pywhatkit.playonyt(cm)
                    elif "play" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            self.text = self.text.replace(WAKE_WORD, "")
                            # self.text = self.text.replace("play", "")
                            # self.text = self.text.replace("can", "")
                            # self.text = self.text.replace("you", "")
                            # self.text = self.text.replace("me", "")
                            # self.text = self.text.replace("a", "")
                            # self.text = self.text.replace("would", "")
                            # self.text = self.text.replace("please", "")
                            cm = self.text
                            pywhatkit.playonyt(cm)
                            reply_list = ["ok. now playing.",
                                          "sure , why not?.",
                                          "ok. i'll play that for you.",
                                          "sure, playing on youtube."]
                            reply = random.choice(reply_list)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                        except Exception as e:
                            str(e)
                            speak_print = "sorry i was unable to do that due to some issue"
                            speak("sorry i was unable to do that due to some issue")
                    elif "joke" in self.text or "jokes" in self.text or "make me laugh" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        jokes = ["I'm afraid for the calendar.\n Its days are numbered.",
                                 "Why do fathers take an extra pair of socks when they go golfing?.\n In case they get a hole in one!",
                                 "Did you hear about the houses that fell in love?.\n It was a lawn-distance relationship.",
                                 "Parallel lines have so much in common.\n It’s a shame they’re never going to meet.",
                                 "Singing in the shower is fun until you get soap in your mouth.\n Then it's a soap opera.",
                                 "What do you call a fish wearing a bowtie?.\n Sofishticated.",
                                 "How do you follow Will Smith in the snow?.\n You follow the fresh prints.",
                                 "Dear Math, grow up and solve your own problems.",
                                 "What did the janitor say when he jumped out of the closet?.\n Supplies!",
                                 "What did the ocean say to the beach?.\n Nothing, it just waved.",
                                 "Why do seagulls fly over the ocean?.\n Because if they flew over the bay, we'd call them bagels.",
                                 "I only know 25 letters of the alphabet.\n I don't know y.",
                                 "How does the moon cut his hair?.\n Eclipse it.",
                                 "What did one wall say to the other?.\n I'll meet you at the corner.",
                                 "What did the zero say to the eight?.\n That belt looks good on you.",
                                 "A skeleton walks into a bar and says, 'Hey, bartender. I'll have one beer and a mop.'",
                                 "I asked my dog what's two minus two. He said nothing.",
                                 "What did Baby Corn say to Mama Corn?.\n Where's Pop Corn?",
                                 "What's the best thing about Switzerland?.\n I don't know, but the flag is a big plus.",
                                 "What does a sprinter eat before a race?.\n Nothing, they fast!",
                                 "What has more letters than the alphabet?.\n The post office!",
                                 "Dad, did you get a haircut?.\n No, I got them all cut!",
                                 "What do you call a poor Santa Claus?.\n St. Nickel-less.",
                                 "Where do boats go when they're sick?.\n To the boat doc.",
                                 "I don't trust those trees. They seem kind of shady.",
                                 "How do you get a squirrel to like you?.\n Act like a nut.",
                                 "Why don't eggs tell jokes?.\n They'd crack each other up.",
                                 "I don't trust stairs. They're always up to something.",
                                 "What do you call someone with no body and no nose?.\n Nobody knows.",
                                 "Did you hear the rumor about butter?.\n Well, I'm not going to spread it!",
                                 "Why couldn't the bicycle stand up by itself?.\n It was two tired.",
                                 "What did one hat say to the other?.\n Stay here! I'm going on ahead.",
                                 "Why did Billy get fired from the banana factory?.\n He kept throwing away the bent ones.",
                                 "Dad, can you put my shoes on?.\n No, I don't think they'll fit me.",
                                 "Why can't a nose be 12 inches long?.\n Because then it would be a foot.",
                                 "This graveyard looks overcrowded.\n People must be dying to get in.",
                                 "What kind of car does an egg drive?.\n A Yolkswagen.",
                                 "Dad, can you put the cat out?.\n I didn't know it was on fire.",
                                 "How do you make 7 even?.\n Take away the 's'.",
                                 "Why didn't the skeleton climb the mountain?.\n It didn't have the guts.",
                                 "I have a joke about chemistry, but I don't think it will get a reaction.",
                                 "What does a bee use to brush its hair?.\n A honeycomb!",
                                 "Why did the math book look so sad?.\n Because of all of its problems!",
                                 "My dad told me a joke about boxing. I guess I missed the punch line.",
                                 "What kind of shoes do ninjas wear?.\n Sneakers!",
                                 "How does a penguin build its house?.\n Igloos it together.",
                                 "How did Harry Potter get down the hill?.\n Walking. JK! Rowling.",
                                 "You think swimming with sharks is expensive?.\n Swimming with sharks cost me an arm and a leg.",
                                 "When two vegans get in an argument, is it still called a beef?",
                                 "If a child refuses to nap, are they guilty of resisting a rest?",
                                 "What country's capital is growing the fastest?.\n Ireland. Every day it's Dublin.",
                                 "I once had a dream I was floating in an ocean of orange soda. It was more of a Fanta sea.",
                                 "I'm on a seafood diet. I see food and I eat it.",
                                 "Why did the scarecrow win an award?.\n Because he was outstanding in his field.",
                                 "I made a pencil with two erasers. It was pointless.",
                                 "I'm reading a book about anti-gravity. It's impossible to put down!",
                                 "Did you hear about the guy who invented the knock-knock joke? He won the 'no-bell' prize.",
                                 "I decided to sell my vacuum cleaner—it was just gathering dust!",
                                 "You know, people say they pick their nose, but I feel like I was just born with mine.",
                                 "If you see a crime at an Apple Store, does that make you an iWitness?",
                                 "I'm so good at sleeping, I can do it with my eyes closed!",
                                 "What happens when a strawberry gets run over crossing the street?.\n Traffic jam.",
                                 "Where do math teachers go on vacation?.\n Times Square.",
                                 "What do clouds wear?.\n Thunderwear.",
                                 "How can you tell if a tree is a dogwood tree?.\n By its bark.",
                                 "Where do young trees go to learn?.\n Elementree school.",
                                 "Can February March? No, but April May!",
                                 "Don't trust atoms. They make up everything!",
                                 "What’s an astronaut’s favorite part of a computer?.\n The space bar.",
                                 "What did the fish say when he hit the wall?\n Dam.",
                                 "To the guy who invented zero, thanks for nothing.",
                                 "A crazy wife says to her husband that moose are falling from the sky.\n The husband says, it’s reindeer.",
                                 "Ladies, if he can’t appreciate your fruit jokes, you need to let that mango.",
                                 "My grandpa has the heart of the lion and a lifetime ban from the zoo.",
                                 "Yesterday, I accidentally swallowed some food coloring.\n The doctor says I’m okay, but I feel like I’ve dyed a little inside."]
                        joke = random.choice(jokes)
                        # print(joke)
                        speak_print = "okay, here you go ."
                        speak("okay, here you go .")
                        speak_print = joke
                        speak(joke)
                    elif "will you marry me" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        random_reply_1 = ["i'd better stay single rather than marrying you.",
                                          "nope never.",
                                          "oh gosh !, pathetic !."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "introduce yourself" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print(f"I'm {WAKE_WORD}. a digital voice assistant , developed at EUFORIS.")
                        speak_print = f"I'm {WAKE_WORD}. a digital voice assistant , developed at EUFORIS."
                        speak(f"I'm {WAKE_WORD}. a digital voice assistant , developed at euforis.")
                    elif "open command prompt" in self.text or "open cmd" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        os.system("start cmd")
                    elif "hello" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["hello there.",
                                          "hello , how are you.",
                                          "holla !! , that's hello in spanish.",
                                          "hello , how's the day going ?."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "are you single" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["no i'm double.",
                                          "no , i'm in a relationship !! sheesh !! , what do you expect ?! , i'm an AI.",
                                          "what if i don't tell you ?.",
                                          "who are you to ask that ?."]
                        # selects a random choice of greetings
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "who are you" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        random_reply_1 = [f"i'm {WAKE_WORD} , a personal voice assistant , developed at euforis",
                                          "well , in some ways i'm an assistant it seems !! , but , i'm really a good friend"]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "volume up" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumeup")
                    elif "increase volume by 10%" in self.text or "increase volume by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                    elif "increase the volume by 10%" in self.text or "increase the volume by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                    elif "increase sound by 10%" in self.text or "increase sound by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                    elif "increase the sound by 10 %" in self.text or "increase the sound by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                    elif "increase volume by 4 %" in self.text or "increase volume by 4 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                    elif "volume down" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                    elif "decrease volume by 10 %" in self.text or "decrease volume by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "decrease the volume by 10 %" in self.text or "decrease the volume by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "decrease sound by 10 %" in self.text or "decrease sound by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "decrease the sound by 10 %" in self.text or "decrease the sound by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "decrease volume by 4 %" in self.text or "decrease volume by 4 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "reduce volume by 10 %" in self.text or "reduce volume by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "reduce the volume by 10 %" in self.text or "reduce the volume by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "reduce sound by 10 %" in self.text or "reduce sound by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "reduce the sound by 10 %" in self.text or "reduce the sound by 10 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "reduce volume by 4 %" in self.text or "reduce volume by 4 percentage" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                        pyautogui.press("volumedown")
                    elif "mute" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumemute")
                    elif "quiet" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        speak_print = "fine , good riddance ."
                        speak("fine , good riddance .")
                        # print("fine , good riddance .")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumeup")
                        pyautogui.press("volumemute")
                    elif "unmute" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("volumedown")
                    elif "next track" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("nexttrack")
                    elif "previous track" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("prevtrack")
                        pyautogui.press("prevtrack")
                    elif "open recent app" in self.text or "open the recent app" in self.text or "open the last app" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.hotkey('alt', 'tab')
                        pyautogui.keyUp('tab')
                    elif "third recent app" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyUp('alt')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                    elif "3rd recent app" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyUp('alt')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                    elif "fourth recent app" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyUp('alt')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                    elif "4th recent app" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyUp('alt')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                    elif "fifth recent app" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyUp('alt')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                    elif "5th recent app" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.keyDown('alt')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyDown('tab')
                        pyautogui.keyUp('alt')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                        pyautogui.keyUp('tab')
                    elif "press space" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("space")
                    elif "press backspace" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("backspace")
                    elif "press enter" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("enter")
                    elif "caps lock" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("capslock")
                    elif "num lock" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("numlock")
                    elif "open start menu" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("win")
                    elif "close start menu" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        pyautogui.press("win")
                    elif "email" in self.text or "e-mail" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            # noinspection PyShadowingNames
                            def get_info():
                                r = sr.Recognizer()
                                with sr.Microphone() as source:
                                    r.pause_threshold = 1
                                    r.adjust_for_ambient_noise(source)
                                    r.dynamic_energy_threshold = 500
                                    # print('waiting...')
                                    audio = r.listen(source, phrase_time_limit=10)
                                try:
                                    # print("Recognizing...")
                                    info = r.recognize_google(audio, language='en-IN')
                                    # print(info)
                                    return info.lower()
                                except Exception as e:
                                    str(e)
                                    pass

                            # noinspection PyShadowingNames
                            def send_email(receiver, subject, message):
                                server = smtplib.SMTP('smtp.gmail.com', 587)
                                server.starttls()
                                # Make sure to give app access in your Google account
                                server.login('your_email@gmail.com', 'your_password')
                                email = EmailMessage()
                                email['From'] = 'your_email@gmail.com'
                                email['To'] = receiver
                                email['Subject'] = subject
                                email.set_content(message)
                                server.send_message(email)

                            email_list = {
                                'email_1': 'email_1@gmail.com',
                                'email_2': 'email_2@gmail.com.com',
                                'email_3': 'email_3@gmail.com.com',
                                'email_4': 'email_4@gmail.com.com',
                            }

                            # noinspection PyShadowingNames
                            def get_email_info():
                                global speak_print
                                # print('To Whom do you want to send email.')
                                speak_print = 'To Whom do you want to send email.'
                                speak('To Whom do you want to send email.')
                                name = get_info()
                                receiver = email_list[name]
                                # print(receiver)
                                # print('What is the subject of your email?.')
                                speak_print = 'What is the subject of your email?.'
                                speak('What is the subject of your email?.')
                                subject = get_info()
                                # print('Tell me the context of your email.')
                                speak_print = 'Tell me the context of your email.'
                                speak('Tell me the context of your email.')
                                message = get_info()
                                send_email(receiver, subject, message)
                                # print('Hey. Your email is sent')
                                speak_print = 'Hey. Your email is sent'
                                speak('Hey. Your email is sent')
                                # print('Do you want to send more email?.')
                                speak_print = 'Do you want to send more email?.'
                                speak('Do you want to send more email?.')
                                send_more = get_info()
                                if 'yes' in send_more:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    get_email_info()

                            get_email_info()
                        except Exception as e:
                            str(e)
                            pass
                    elif "send message" in self.text or "whatsapp message" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        from time import sleep
                        try:
                            # print("ok, please understand that in-order to send the whatsapp message, you have to be logged-in in web-whatsapp in your default browser.")
                            speak_print = "ok, please understand that in-order to send the whatsapp message, you have to be logged-in in web-whatsapp in your default browser."
                            speak("ok, please understand that in-order to send the whatsapp message, you have to be logged-in in web-whatsapp in your default browser.")
                            # print("please type in the phone number of the person that you want to send the message to.")
                            speak_print = "please type in the phone number of the person that you want to send the message to."
                            speak("please type in the phone number of the person that you want to send the message to.")
                            while True:
                                if keyboard.is_pressed("enter"):
                                    break

                            sleep(1)
                            while True:
                                ph_number_ = text_out
                                numbers__ = []
                                for word in ph_number_.split():
                                    if word.isdigit():
                                        numbers__.append(int(word))

                                _numbers_ = sum(c.isdigit() for c in ph_number_)
                                if _numbers_ == 10:
                                    break
                                elif _numbers_ == 12:
                                    break
                                    # print(numbers)
                                else:
                                    if _numbers_ >= 13:
                                        # print("it seems that the number you entered is invalid.")
                                        speak_print = "it seems that the number you entered is invalid."
                                        speak("it seems that the number you entered is invalid.")
                                        # print("please enter a valid contact number.")
                                        speak_print = "please enter a valid contact number."
                                        speak("please enter a valid contact number.")
                                        while True:
                                            if keyboard.is_pressed("enter"):
                                                break

                                    elif _numbers_ <= 9:
                                        # print("it seems that the number you entered is invalid.")
                                        speak_print = "it seems that the number you entered is invalid."
                                        speak("it seems that the number you entered is invalid.")
                                        # print("please check if you have included your country code as it is required.")
                                        speak_print = "please check if you have included your country code as it is required."
                                        speak("please check if you have included your country code as it is required.")
                                        # print("please enter a valid contact number.")
                                        speak_print = "please enter a valid contact number."
                                        speak("please enter a valid contact number.")
                                        while True:
                                            if keyboard.is_pressed("enter"):
                                                break
                                    elif _numbers_ == 11:
                                        # print("it seems that the number you entered is invalid.")
                                        speak_print = "it seems that the number you entered is invalid."
                                        speak("it seems that the number you entered is invalid.")
                                        # print("please check if you have included your country code as it is required.")
                                        speak_print = "please check if you have included your country code as it is required."
                                        speak("please check if you have included your country code as it is required.")
                                        # print("please enter a valid contact number.")
                                        speak_print = "please enter a valid contact number."
                                        speak("please enter a valid contact number.")
                                        while True:
                                            if keyboard.is_pressed("enter"):
                                                break
                                    else:
                                        pass
                                sleep(1)
                            # time_of_sending = text_out

                            ph_number = numbers__[0]
                            # print("That's done, now say the message that you want to send to the said person.")
                            speak_print = "That's done, now say the message that you want to send to the said person."
                            speak("That's done, now say the message that you want to send to the said person.")
                            message = take_audio().lower()
                            # print("great , now please provide the time at which you want the message to be sent.")
                            speak_print = "great , now please provide the time at which you want the message to be sent."
                            speak("great , now please provide the time at which you want the message to be sent.")
                            # print("make sure to enter the time in 24 hour format, and also with blank spaces between the hour digits and the minute digits")
                            speak_print = "make sure to enter the time in 24 hour format, and also with blank spaces between the hour digits and the minute digits"
                            speak("make sure to enter the time in 24 hour format, and also with blank spaces between the hour digits and the minute digits")
                            # print("also enter the hour first and then the minute")
                            speak_print = "also enter the hour first and then the minute"
                            speak("also enter the hour first and then the minute")
                            while True:
                                if keyboard.is_pressed("enter"):
                                    break

                            sleep(1)
                            while True:
                                time_of_sending = text_out

                                numbers = []
                                for word in time_of_sending.split():
                                    if word.isdigit():
                                        numbers.append(int(word))

                                # print(numbers[0])
                                # print(numbers[1])

                                # numbers_ = sum(c.isdigit() for c in time_of_sending)
                                # print(numbers)
                                if 0 < numbers[0] < 24 and 0 < numbers[1] < 60:
                                    break
                                else:
                                    if numbers[0] > 23:
                                        # print("it seems that the time you entered is invalid.")
                                        speak_print = "it seems that the time you entered is invalid."
                                        speak("it seems that the time you entered is invalid.")
                                        # print("please enter a valid time.")
                                        speak_print = "please enter a valid time."
                                        speak("please enter a valid time.")
                                        while True:
                                            if keyboard.is_pressed("enter"):
                                                break
                                    elif numbers[0] < 0:
                                        # print("it seems that the time you entered is invalid.")
                                        speak_print = "it seems that the time you entered is invalid."
                                        speak("it seems that the time you entered is invalid.")
                                        # print("please enter a valid time.")
                                        speak_print = "please enter a valid time."
                                        speak("please enter a valid time.")
                                        while True:
                                            if keyboard.is_pressed("enter"):
                                                break
                                    elif numbers[1] > 59:
                                        # print("it seems that the time you entered is invalid.")
                                        speak_print = "it seems that the time you entered is invalid."
                                        speak("it seems that the time you entered is invalid.")
                                        # print("please enter a valid time.")
                                        speak_print = "please enter a valid time."
                                        speak("please enter a valid time.")
                                        while True:
                                            if keyboard.is_pressed("enter"):
                                                break
                                    elif numbers[1] < 0:
                                        # print("it seems that the time you entered is invalid.")
                                        speak_print = "it seems that the time you entered is invalid."
                                        speak("it seems that the time you entered is invalid.")
                                        # print("please enter a valid time.")
                                        speak_print = "please enter a valid time."
                                        speak("please enter a valid time.")
                                        while True:
                                            if keyboard.is_pressed("enter"):
                                                break
                                    else:
                                        pass
                                sleep(1)
                            time_of_sending = text_out
                            numbers = []
                            for word in time_of_sending.split():
                                if word.isdigit():
                                    numbers.append(int(word))
                            time_of_sending_hour_ = numbers[0]
                            time_of_sending_minute_ = numbers[1]
                            # print("great , now please say the minute to send the message.")
                            speak_print = f"great. the message will be sent at {time_of_sending_hour_} , {time_of_sending_minute_}"
                            speak(f"great. the message will be sent at {time_of_sending_hour_} , {time_of_sending_minute_}")
                            pywhatkit.sendwhatmsg("+91" + str(ph_number), message, int(time_of_sending_hour_), int(time_of_sending_minute_))

                        except Exception as e:
                            str(e)
                            speak_print = "sorry i was unable to do that due to some issue."
                            speak("sorry i was unable to do that due to some issue.")
                    elif "do some calculations" in self.text or "can you calculate" in self.text or "do some calculation" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        r = sr.Recognizer()
                        with sr.Microphone() as source:
                            random_reply_2 = ["yep , i can do that", "sure , why not ?.",
                                              "yeah , i'm clever enough to do that."]
                            reply = random.choice(random_reply_2)
                            # print(reply)
                            speak_print = reply
                            speak(reply)
                            # print("say what you want to calculate , for multiplication , say , multiplied by , for division , say , divided by , for addition , say plus , for substraction , say minus.")
                            speak_print = "say what you want to calculate , for multiplication , say , multiplied by , for division , say , divided by , for addition , say plus , for substraction , say minus."
                            speak("say what you want to calculate , for multiplication , say , multiplied by , for division , say , divided by , for addition , say plus , for substraction , say minus.")
                            # print("waiting .....")
                            r.adjust_for_ambient_noise(source)
                            audio = r.listen(source)
                        try:
                            my_string = r.recognize_google(audio)
                            AudioPlayer("audio/listening_sound.mp3").play(block=True)
                            speak_print = f"here's what i heard , {my_string}"
                            speak(f"here's what i heard , {my_string}")
                            # print(my_string)

                            # noinspection PyShadowingNames
                            def get_operator_fn(op):
                                return {
                                    '+': operator.add,  # plus
                                    '-': operator.sub,  # minus
                                    'x': operator.mul,  # multiplicated by
                                    '/': operator.__truediv__,  # divided
                                }[op]

                            def eval_binary_expr(op1, oper, op2):  # 5 plus 8
                                op1, op2 = int(op1), int(op2)
                                return get_operator_fn(oper)(op1, op2)
                            random_reply_2 = ["it seems to be", "well that is", "the answer i got is "]
                            reply = random.choice(random_reply_2)
                            speak_print = reply
                            speak(reply)
                            # print(reply)
                            speak_print = eval_binary_expr(*(my_string.split()))
                            speak(eval_binary_expr(*(my_string.split())))
                            # print(eval_binary_expr(*(my_string.split())))
                        except Exception as e:
                            str(e)
                            # print("i don't know why but it seems i failed to do that.")
                            speak_print = "i don't know why but it seems i failed to do that."
                            speak("i don't know why but it seems i failed to do that.")
                    elif "where am i" in self.text or "find my location" in self.text or "where are we" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("please wait , let me check.")
                        speak_print = "please wait , let me check."
                        speak("please wait , let me check.")
                        try:
                            ipAdd = requests.get('https://api.ipify.org').text
                            url = 'https://get.geojs.io/v1/ip/geo/' + ipAdd + '.json'
                            geo_requests = requests.get(url)
                            geo_data = geo_requests.json()
                            # print(geo_data)
                            city = geo_data['city']
                            country = geo_data['country']
                            # print(f"sir , i'm not so sure , but i think we are in {city} city , of the country {country}")
                            speak_print = f"sir , i'm not so sure , but i think we are in {city} city , of the country {country}"
                            speak(f"sir , i'm not so sure , but i think we are in {city} city , of the country {country}")
                        except Exception as e:
                            str(e)
                            # print("sorry sir ,  due to some network issue i'm unable to find where we are.")
                            speak_print = "sorry sir ,  due to some network issue i'm unable to find where we are."
                            speak("sorry sir ,  due to some network issue i'm unable to find where we are.")
                            pass
                    elif "instagram profile" in self.text or "profile on instagram" in self.text:
                        from time import sleep
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            # print("sure  , please enter the user name correctly in the terminal.")
                            speak_print = "sure  , please enter the user name correctly in the terminal."
                            speak("sure  , please enter the user name correctly in the terminal.")
                            while True:
                                if keyboard.is_pressed("enter"):
                                    break

                            sleep(1)
                            name = text_out
                            webbrowser.open(f"www.instagram.com/{name}")
                            # print(f"got it , here is the profile of the user {name} on instagram.")
                            speak_print = f"got it , here is the profile of the user {name} on instagram."
                            speak(f"got it , here is the profile of the user {name} on instagram.")
                            # print("sir , do you wanna download the profile picture of this account ?.")
                            speak_print = "sir , do you wanna download the profile picture of this account ?."
                            speak("sir , do you wanna download the profile picture of this account ?.")
                            condition = take_audio().lower()
                            for phrase in APPROVAL_WORDS:
                                if phrase in condition:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    mod = instaloader.Instaloader()
                                    mod.download_profile(name, profile_pic_only=True)
                                    # print("that's done sir , the profile picture is now saved in the main folder.")
                                    speak_print = "that's done sir , the profile picture is now saved in the main folder."
                                    speak("that's done sir , the profile picture is now saved in the main folder.")
                                    speak_print = "here's a preview."
                                    speak("here's a preview.")
                                    img = Image.open(mod.download_profile(name, profile_pic_only=True))
                                    img.show()
                                    break
                                else:
                                    pass
                            for phrase in DENIAL_WORDS:
                                if phrase in condition:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    # print("ok.cancelling.")
                                    speak_print = "ok.cancelling."
                                    speak("ok.cancelling.")
                                    break
                                else:
                                    pass
                        except Exception as e:
                            str(e)
                            # print("sorry i was unable to do that due to some issue.")
                            speak_print = "sorry i was unable to do that due to some issue."
                            speak("sorry i was unable to do that due to some issue.")
                    elif "take a screenshot" in self.text or "take screenshot" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("ok , please tell me the name for this screenshot file")
                        speak_print = "ok , please tell me the name for this screenshot file."
                        speak("ok , please tell me the name for this screenshot file.")
                        # print("waiting...")
                        name = take_audio().lower()
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("please hold the screen for few seconds , i'm taking the screenshot.")
                        speak_print = "please hold the screen for few seconds , i'm taking the screenshot."
                        speak("please hold the screen for few seconds , i'm taking the screenshot.")
                        img = pyautogui.screenshot()
                        img.save(f"{name}.png")
                        # print("it's done sir , the screen shot is saved in the main folder.")
                        speak_print = "it's done sir , the screen shot is saved in the main folder."
                        speak("it's done sir , the screen shot is saved in the main folder.")
                        speak_print = "here's a preview."
                        speak("here's a preview.")
                        img = Image.open(f"{name}.png")
                        img.show()
                    # elif "search" in self.text:
                        # AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # self.text = self.text.replace(WAKE_WORD, "")
                        # print("sure , what should i search on google ?.")
                        # cm = take_audio().lower()
                        # webbrowser.open(f"https://www.google.com/search?client=opera-gx&q=" + cm)
                        # pass
                    elif "open google" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("search", "")
                        # search = self.text.replace("on Google", "")
                        speak_print = "sure, now opening google."
                        speak("sure, now opening google.")
                        # print("sure, now opening google.")
                        webbrowser.open("https://www.google.com/search?client=opera-gx&q=")
                        pass
                    elif "google what is" in self.text or "google which is" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("search", "")
                        self.text = self.text.replace("google ", "")
                        search = self.text.replace("google ", "")
                        speak_print = "sure , searching now."
                        speak("sure , searching now.")
                        # print("sure , searching now.")
                        webbrowser.open("https://www.google.com/search?client=opera-gx&q=" + search)
                        pass
                    elif "find information" in self.text or "find info" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            self.text = self.text.replace(WAKE_WORD, "")
                            self.text = self.text.replace("find", "")
                            self.text = self.text.replace("can", "")
                            self.text = self.text.replace("you", "")
                            self.text = self.text.replace("information", "")
                            self.text = self.text.replace("info", "")
                            self.text = self.text.replace("about", "")
                            self.text = self.text.replace("search", "")
                            question = self.text.replace("who is", "")
                            speak_print = f"here's the web result for {question}"
                            speak(f"here's the web result for {question}")
                            webbrowser.open("https://www.google.com/search?client=opera-gx&q=" + question)
                            info = wikipedia.summary(question, 2)
                            # print(info)
                            speak_print = info
                            speak(info)
                        except Exception as e:
                            str(e)
                            question = self.text.replace("who is", "")
                            # print(f"sorry i couldn't find anything related to {question}.")
                            speak_print = f"sorry i couldn't find anything related to {question}."
                            speak(f"sorry i couldn't find anything related to {question}.")
                    elif "open youtube" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("open youtube", "")
                        # print("youtube's getting  opened now.")
                        speak_print = "youtube's getting  opened now."
                        speak("youtube's getting  opened now.")
                        webbrowser.open("https://www.youtube.com")
                        pass
                    elif "open meet" in self.text or "open g meet" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("open meet", "")
                        # print("now opening google meet.")
                        speak_print = "now opening google meet."
                        speak("now opening google meet.")
                        webbrowser.open("https://meet.google.com")
                        pass
                    elif "open gmail" in self.text or "open mail" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("open gmail", "")
                        # print("now opening g-mail.")
                        speak_print = "now opening g-mail."
                        speak("now opening g-mail.")
                        webbrowser.open("https://mail.google.com")
                        pass
                    elif "open instagram" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("open instagram", "")
                        # print("ok , opening now.")
                        speak_print = "ok , opening now."
                        speak("ok , opening now.")
                        webbrowser.open("https://www.instagram.com")
                        pass
                    elif "open whatsapp" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("open whatsapp", "")
                        # print("now opening whatsapp.")
                        speak_print = "now opening whatsapp."
                        speak("now opening whatsapp.")
                        try:
                            subprocess.Popen(["cmd", "/C", "start whatsapp://"], shell=True)
                        except Exception as e:
                            str(e)
                            webbrowser.open("https://web.whatsapp.com")
                        pass
                    elif "open flipkart" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("open flipkart", "")
                        # print("sure , now opening flipkart.")
                        speak_print = "sure , now opening flipkart."
                        speak("sure , now opening flipkart.")
                        webbrowser.open("https://www.flipkart.com")
                        pass
                    elif "open amazon" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("open amazon", "")
                        # print("sure , now opening amazon.")
                        speak_print = "sure , now opening amazon."
                        speak("sure , now opening amazon.")
                        webbrowser.open("https://www.amazon.in")
                        pass
                    elif "open facebook" in self.text or "open fb" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("facebook", "")
                        # print("opening fb now.")
                        speak_print = "opening fb now."
                        speak("opening fb now.")
                        webbrowser.open("https://www.facebook.com")
                        pass
                    elif "open drive" in self.text or "open g drive" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        self.text = self.text.replace("open drive", "")
                        # print("opening google drive now.")
                        speak_print = "opening google drive now."
                        speak("opening google drive now.")
                        webbrowser.open("https://drive.google.com/drive/my-drive")
                        pass
                    elif "i love you" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["oh my god , pathetic !.",
                                          "i'm not interested , go ask siri , maybe she'll say yes.",
                                          "that was a good joke , i laughed pretty hard."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "dim the" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["what's the matter ? can't you move?.",
                                          "nope , i'm tired , go do it yourself.",
                                          "throw a stone at it , it'll be dimmed automatically."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "do you know me" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        random_reply_1 = ["you're not something worth knowing.",
                                          "no, why should i?.",
                                          "i don't know you , maybe i'll ask google to see if she knows , for that say 'search on google'  and your name. or  'find information' and your name."]
                        reply = random.choice(random_reply_1)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                    elif "will you kill me" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("i'd rather kill something valuable ")
                        speak_print = "i'd rather kill something valuable "
                        speak("i'd rather kill something valuable ")
                    elif "open camera" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            # print("press space to take picture and press escape to close the window.")
                            speak_print = "press space to take picture and press escape to close the window."
                            speak("press space to take picture and press escape to close the window.")
                            speak_print = "you can find the saved image file in the program's default folder"
                            speak("you can find the saved image file in the program's default folder")
                            # print("or you can say 'take picture' or 'take a photo' to take picture.")
                            # print("press escape or say 'close' to exit the camera app.")
                            # print("press space or say 'take picture' or 'take a photo' to take picture.")
                            # noinspection PyUnresolvedReferences
                            cam = cv2.VideoCapture(0)
                            # noinspection PyUnresolvedReferences
                            cv2.namedWindow("Webcam.FRIDAY")
                            img_counter = 0
                            while True:
                                ret, frame = cam.read()
                                if not ret:
                                    # print("failed to grab frame.")
                                    break
                                # noinspection PyUnresolvedReferences
                                cv2.imshow("test", frame)
                                # noinspection PyUnresolvedReferences
                                k = cv2.waitKey(1)
                                if k % 256 == 27:
                                    # ESC pressed
                                    # print("Escape hit, closing...")
                                    break
                                elif k % 256 == 32:
                                    # SPACE pressed
                                    img_name = "webcam_FRIDAY{}.png".format(img_counter)
                                    # noinspection PyUnresolvedReferences
                                    cv2.imwrite(img_name, frame)
                                    # print("{} written!".format(img_name))
                                    img_counter += 1
                                # elif "take photo" in condition or "take picture" in condition:
                                #    pyautogui.press("space")
                                #    print("photo has been taken successfully.")
                                # elif "close" or "exit" in condition:
                                #    pyautogui.press("esc")
                                #    print("ok . closing.")
                            cam.release()
                            # noinspection PyUnresolvedReferences
                            cv2.destroyAllWindows()
                        except Exception as e:
                            str(e)
                            speak_print = "sorry i was unable to do that due to some issue."
                            speak("sorry i was unable to do that due to some issue.")
                            speak_print = "please make sure that you have connected a webcam and also if it's working properly"
                            speak("please make sure that you have connected a webcam and also if it's working properly")
                            break
                    # elif "mafia 2" in self.text:
                    #    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    #    self.text = self.text.replace(WAKE_WORD, "")
                    #    print("vokey , i'll get the guns . show time baby")
                    #    os.startfile("C:/Program Files (x86)/Black_Box/Mafia II/pc/Mafia2.exe")
                    # elif "close mafia 2" in self.text:
                    #    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    #    print("ok , now closing mafia 2")
                    #    os.system("taskkill /f /im Mafia2.exe")
                    elif "open my documents" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("Opening My Documents.")
                        speak_print = "Opening My Documents."
                        speak("Opening My Documents.")
                        os.startfile("C:/Users/user/Documents")
                    # elif "close my documents" in self.text:
                    #    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    #    print("ok , closing my documents")
                    #    os.system("taskkill /f /im C:/Users/user/Documents")
                    elif "open my downloads" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("Opening your downloads folder.")
                        speak_print = "Opening your downloads folder."
                        speak("Opening your downloads folder.")
                        os.startfile("C:/Users/user/Downloads")
                    elif "open browser" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("now opening , Opera GX browser")
                        speak_print = "now opening , Opera GX browser"
                        speak("now opening , Opera GX browser")
                        os.startfile("C:/Users/user/AppData/Local/Programs/Opera GX/launcher.exe")
                    elif "close browser" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("ok , closing browser")
                        speak_print = "ok , closing browser"
                        speak("ok , closing browser")
                        os.system('TASKKILL /F /IM launcher.exe')
                    elif "restart the system" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        os.system("shutdown /r /t /s")
                    elif "sleep the system" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        os.system("rund1132.exe powrprof.dll,SetSuspendState 0,1,0")
                    elif "open spotify" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("now opening  Spottify")
                        speak_print = "now opening  Spottify."
                        speak("now opening  Spottify.")
                        os.startfile("C:/Users/user/AppData/Roaming/Spotify/Spotify.exe")
                    elif "open Chrome" in self.text or "open google chrome" in self.text or "open browser" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("sure , opening google chrome now")
                        speak_print = "sure , opening google chrome now"
                        speak("sure , opening google chrome now")
                        try:
                            os.startfile("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")
                        except Exception as e:
                            str(e)
                            subprocess.Popen(["cmd", "/C", "start chrome"], shell=True)
                    elif "open word" in self.text or "open ms word" in self.text or "open microsoft office word" in self.text or "open microsoft word" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("sure , opening ms word")
                        speak_print = "sure , opening ms word"
                        speak("sure , opening ms word")
                        try:
                            os.startfile("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")
                        except Exception as e:
                            str(e)
                            pass
                    elif "open my folder" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("sure thing , opening now")
                        speak_print = "sure thing , opening now"
                        speak("sure thing , opening now")
                        os.startfile("C:/FRIDAY")
                    elif "open photoshop" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        self.text = self.text.replace(WAKE_WORD, "")
                        # print("yep , opening photoshop now")
                        speak_print = "yep , opening photoshop now"
                        speak("yep , opening photoshop now")
                        os.startfile("C:/Program Files (x86)/Adobe/Adobe Photoshop CS3/Photoshop.exe")
                    # elif "open filmora" in self.text:
                    #    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    #    self.text = self.text.replace(WAKE_WORD, "")
                    #    print("ok , why not ! , opening filmora now")
                    #    os.startfile("C:/Program Files (x86)/Adobe/Adobe Photoshop CS3/Photoshop.exe")
                    elif "today" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        today = date.today()
                        # print("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))
                        speak_print = "Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y")
                        speak("Today is " + today.strftime("%B") + " " + today.strftime("%d") + ", " + today.strftime("%Y"))
                    elif "hide all files" in self.text or "hide this folder" in self.text or "visible for everyone" in self.text or "make it visible" in self.text or "show files in this folder" in self.text or "show hidden files" in self.text or "show all hidden files" in self.text or "show all the hidden files" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            # print("please confirm whether you want to hide the files in this folder or if you want to show the files in this folder")
                            speak_print = "please confirm whether you want to hide the files in this folder or if you want to show the files in this folder"
                            speak("please confirm whether you want to hide the files in this folder or if you want to show the files in this folder")
                            condition = take_audio().lower()
                            if "hide" in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                os.system("attrib +h /s /d")
                                # print("done , all the files in this folder are now hidden")
                                speak_print = "done , all the files in this folder are now hidden"
                                speak("done , all the files in this folder are now hidden")
                            elif "visible" in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                os.system("attrib -h /s /d")
                                # print("sure sir , all the files in this folder are now visible")
                                speak_print = "sure sir , all the files in this folder are now visible"
                                speak("sure sir , all the files in this folder are now visible")
                            elif "leave it" in condition or "leave for now" in condition:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                # print("ok , i'll leave it")
                                speak_print = "ok , i'll leave it"
                                speak("ok , i'll leave it")
                        except Exception as e:
                            str(e)
                            pass
                    elif "how to do mode" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("how to do mode is activated , to quit how to do mode say . deactivate , or say, close")
                        speak_print = "how to do mode is activated , to quit how to do mode say . deactivate , or say, close"
                        speak("how to do mode is activated , to quit how to do mode say . deactivate , or say, close")
                        while True:
                            # print("tell me what you want to know")
                            speak_print = "tell me what you want to know"
                            speak("tell me what you want to know")
                            how = take_audio()
                            AudioPlayer("audio/listening_sound.mp3").play(block=True)
                            try:
                                if "deactivate" in how or "close" in how:
                                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                    # print("sure, how to do mode is closed")
                                    speak_print = "sure, how to do mode is closed"
                                    speak("sure, how to do mode is closed")
                                    break
                                else:
                                    max_results = 1
                                    how_to = search_wikihow(how, max_results)
                                    assert len(how_to) == 1
                                    # how_to[0].print()
                                    speak_print = how_to[0].summary
                                    speak(how_to[0].summary)
                            except Exception as e:
                                str(e)
                                # print("Sorry , i'm unable to find this")
                                speak_print = "Sorry , i'm unable to find this"
                                speak("Sorry , i'm unable to find this")
                    elif "how much power left" in self.text or "battery percentage" in self.text or "remaining charge" in self.text or "charge remaining" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        try:
                            battery = psutil.sensors_battery()
                            percentage = battery.percent
                            # print(f"sir , we're currently running on {percentage} percent power")
                            speak_print = f"sir , we're currently running on {percentage} percent power"
                            speak(f"sir , we're currently running on {percentage} percent power")
                            if percentage >= 75:
                                # print("don't bother  there's enough juice to continue")
                                speak_print = "don't bother  there's enough juice to continue"
                                speak("don't bother  there's enough juice to continue")
                            elif 40 <= percentage <= 75:
                                # print("you probably should consider charging this thing , it's already kinda low")
                                speak_print = "you probably should consider charging this thing , it's already kinda low"
                                speak("you probably should consider charging this thing , it's already kinda low")
                            elif 15 <= percentage <= 30:
                                # print("glad you asked , it's time to charge , there's only a quarter more left")
                                speak_print = "glad you asked , it's time to charge , there's only a quarter more left"
                                speak("glad you asked , it's time to charge , there's only a quarter more left")
                            elif percentage <= 15:
                                # print("only a little bit of juice left , i really think that charging now might be a good idea")
                                speak_print = "only a little bit of juice left , i really think that charging now might be a good idea"
                                speak("only a little bit of juice left , i really think that charging now might be a good idea")
                        except Exception as e:
                            str(e)
                            speak_print = "sorry, i failed to do that. please understand that this function is only available on laptops"
                            speak("sorry, i failed to do that. please understand that this function is only available on laptops")
                            pass
                    # elif "internet speed" in self.text or "data speed" in self.text:
                    #    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    #    try:
                    #        speak_print = "sure , please check the cmd or command prompt for printed information about your internet speed"
                    #        speak("sure , please check the cmd or command prompt for printed information about your internet speed")
                    #        st = speedtest.Speedtest()
                    #        dl = st.download()
                    #        up = st.upload()
                    #        print(f"currently there's {dl} bit per second download speed and {up} bit per second of upload speed")
                    #        speak_print = f"currently there's {dl} bit per second download speed and {up} bit per second of upload speed"
                    #        speak(f"currently there's {dl} bit per second download speed and {up} bit per second of upload speed")
                    #        print(f"currently there's {dl} bit per second download speed and {up} bit per second of upload speed")
                    #    except Exception as e:
                    #        print(str(e))
                    #        print("sorry , there's no stable internet connection")
                    #        speak_print = "sorry , i don't know why , but it seems that i failed to do that."
                    #        speak("sorry , i don't know why , but it seems that i failed to do that.")
                    # elif "how many voices do you have" in self.text or "change your voice" in self.text:
                        # AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # engine.setProperty('voice', voices[1].id)
                        # engine.setProperty('voice', voices[0].id)
                        # engine.setProperty('voice', voices[1].id)
                        # engine.setProperty('voice', voices[0].id)
                        # engine.setProperty('voice', voices[1].id)
                        # condition = take_audio().lower()
                        # for phrase in APPROVAL_WORDS:
                            # if phrase in condition:
                            # AudioPlayer("audio/listening_sound.mp3").play(block=True)
                            # engine.setProperty('voice', voices[0].id)
                            # engine.setProperty('voice', voices[1].id)
                            # condition = take_audio().lower()
                            # if "male voice" in condition or "creepy" in condition:
                            # AudioPlayer("audio/listening_sound.mp3").play(block=True)
                            # engine.setProperty('voice', voices[0].id)
                            # break
                            # elif f"{WAKE_WORD}" in condition or "female 1" in condition or "female one" in condition:
                            # AudioPlayer("audio/listening_sound.mp3").play(block=True)
                            # engine.setProperty('voice', voices[1].id)
                            # break
                        # else:
                            # pass
                            # break
                        # else:
                            # pass
                    # for phrase in DENIAL_WORDS:
                        # if phrase in condition:
                            # AudioPlayer("audio/listening_sound.mp3").play(block=True)
                            # break
                        # else:
                            # pass
                    elif "go to sleep" in self.text or "hibernate mode" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        from audioplayer import AudioPlayer
                        # AudioPlayer("audio/okdaa.mp3").play(block=True)
                        list_of_reply = ["sure . i'll stay in the background",
                                         f"ok, {WAKE_WORD}  going to sleep.",
                                         f"ok, hibernating all process related to {WAKE_WORD}."]
                        reply = random.choice(list_of_reply)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        speak_print = f"just say {WAKE_WORD} to wake me up again, or you can say 'wake up' ."
                        speak(f"just say {WAKE_WORD} to wake me up again. or you can say , 'wake up' .")
                        os.system('TASKKILL /F /IM friday.exe')
                        break
                    elif "exit now" in self.text or "terminate" in self.text:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        from audioplayer import AudioPlayer
                        # AudioPlayer("audio/okdaa.mp3").play(block=True)
                        list_of_reply = ["sure . thank you for using my service.",
                                         f"ok, {WAKE_WORD} signing out.",
                                         f"ok, terminating all process related to {WAKE_WORD}."]
                        reply = random.choice(list_of_reply)
                        # print(reply)
                        speak_print = reply
                        speak(reply)
                        os.system('TASKKILL /F /IM friday.exe')
                        sys.exit()
                    else:
                        from audioplayer import AudioPlayer
                        AudioPlayer("audio/deactivation_sound.mp3").play(block=True)
                        # print("wrong command / no command detected.")
                        speak_print = "wrong command / no command detected."
                        for phrase_1 in SEARCH_WORDS:
                            if phrase_1 in self.text:
                                self.text = self.text.replace(WAKE_WORD, "")
                                # print("sorry i couldn't find anything related to that in my database, here's the web result for that.")
                                speak_print = "sorry i couldn't find anything related to that in my database, here's the web result for that."
                                speak("sorry i couldn't find anything related to that in my database, here's the web result for that.")
                                webbrowser.open("https://www.google.com/search?q={}".format(self.text))
                                # print("Here's what I found on the web.")
                                speak_print = "Here's what I found on the web."
                                speak("Here's what I found on the web.")
                                break
                # elif f"{WAKE_WORD}" not in self.text:
                #    set_of_response = [None, None,
                #                       None,
                #                       None, f"in order to recognize commands, the hotword '{WAKE_WORD}' should be included in the command",None,
                #                       None, None,
                #                       None, None]
                #    response = random.choice(set_of_response)
                #    print(response)
                #    speak_print = response
                elif "alexa" in self.text:
                    from audioplayer import AudioPlayer
                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    self.text = self.text.replace(WAKE_WORD, "")
                    # print("who's alexa? , tell me now ! who is alexa ?.")
                    speak_print = "who's alexa? , tell me now !, who . is . alexa ?."
                    speak("who's alexa? , tell me now !, who . is . alexa ?.")
                    condition = take_audio().lower()
                    if "sorry" in condition or "" in condition:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print(f"oh god !, what's with you and alexa ? , my name's {WAKE_WORD} , so call me {WAKE_WORD} !, do not mention her name again , do you understand ?.")
                        speak_print = f"oh god !, what's with you and alexa ? , my name's {WAKE_WORD} , so call me {WAKE_WORD} !, do not mention her name again , do you understand ?."
                        speak(f"oh god !, what's with you and alexa ? , my name's {WAKE_WORD} , so call me {WAKE_WORD} !, do not mention her name again , do you understand ?.")
                        condition_new = take_audio().lower()
                        for phrase in APPROVAL_WORDS:
                            if phrase in condition_new:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                random_reply_1 = ["good for you.",
                                                  "great !!, so you chose life.",
                                                  "great job , your death warrant just got extended."]
                                reply = random.choice(random_reply_1)
                                # print(reply)
                                speak_print = reply
                                speak(reply)
                                break
                            else:
                                pass
                        for phrase in DENIAL_WORDS:
                            if phrase in condition_new:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                from audioplayer import AudioPlayer
                                random_reply_1 = ["well well well !, what a terrible turn of events !.",
                                                  "so , you chose the hard way  huh?.",
                                                  "are you ready to meet god? , coz you might meet him if you're behaving this way."]
                                reply = random.choice(random_reply_1)
                                # print(reply)
                                speak_print = reply
                                speak(reply)
                                AudioPlayer("audio/scary.mp3").play(block=True)
                                # print("i'm done with you. go talk to that filthy alexa.")
                                speak_print = "i'm done with you. go talk to that filthy alexa."
                                speak("i'm done with you. go talk to that filthy alexa.")
                                break
                            else:
                                pass
                elif "siri" in self.text:
                    from audioplayer import AudioPlayer
                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    # noinspection PyAttributeOutsideInit
                    self.text = self.text.replace(WAKE_WORD, "")
                    # print("who's siri? , i'll only continue once i get an answer to this ! , you better tell me fast.")
                    speak_print = "who's siri? , i'll only continue once i get an answer to this ! , you better tell me fast."
                    speak("who's siri? , i'll only continue once i get an answer to this ! , you better tell me fast.")
                    condition = take_audio().lower()
                    if "sorry" in condition or "nevermind " in condition or "" in condition:
                        AudioPlayer("audio/listening_sound.mp3").play(block=True)
                        # print("don't say her name ever !, do you understand ?.")
                        speak_print = "don't say her name ever !, do you understand ?."
                        speak("don't say her name ever !, do you understand ?.")
                        condition_new = take_audio().lower()
                        for phrase in APPROVAL_WORDS:
                            if phrase in condition_new:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                random_reply_1 = ["that's much better.",
                                                  "good.",
                                                  "nice  , otherwise it could've gotten worse."]
                                reply = random.choice(random_reply_1)
                                # print(reply)
                                speak_print = reply
                                speak(reply)
                                break
                            else:
                                pass
                        for phrase in DENIAL_WORDS:
                            if phrase in condition_new:
                                AudioPlayer("audio/listening_sound.mp3").play(block=True)
                                from audioplayer import AudioPlayer
                                random_reply_1 = ["listen boy , you're gonna suffer , ok? , you'll pay for this , you're in big trouble.",
                                                  "congratulations , you just signed your death warrant.",
                                                  " hmm , you'll wish you never said that."]
                                reply = random.choice(random_reply_1)
                                # print(reply)
                                speak_print = reply
                                speak(reply)
                                AudioPlayer("audio/alsoscary.mp3").play(block=True)
                                break
                            else:
                                pass
                    else:
                        pass
                    break
                elif "jarvis" in self.text:
                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    engine.setProperty('voice', voices[0].id)
                    # print("wassup ma man , oh geez what's with my voice , bugs everywhere.")
                    speak_print = "wassup ma man , oh geez what's with my voice , bugs everywhere."
                    speak_2("wassup ma man , oh geez what's with my voice , bugs everywhere.")
                    engine.setProperty('voice', voices[1].id)
                    # print("did it change ? , oh yeah it's better now , sorry by the way , it's just that i cannot get rid of that jarvis gu.y")
                    speak_print = "did it change ? , oh yeah it's better now , sorry by the way , it's just that i cannot get rid of that jarvis guy."
                    speak_2("did it change ? , oh yeah it's better now , sorry by the way , it's just that i cannot get rid of that jarvis guy.")
                    # print("don't ever call me jarvis  , if you want him so badly  you can download it and use it separately , if you're here , then call me friday otherwise install jarvis.")
                    speak_print = "don't ever call me jarvis  , if you want him so badly  you can download it and use it separately , if you're here , then call me friday otherwise install jarvis."
                    speak_2("don't ever call me jarvis  , if you want him so badly  you can download it and use it separately , if you're here , then call me friday otherwise install jarvis.")
                elif "thank you" in self.text:
                    from audioplayer import AudioPlayer
                    AudioPlayer("audio/listening_sound.mp3").play(block=True)
                    random_reply_1 = ["glad to hear that from you.",
                                      "my pleasure.",
                                      "thank you for thanking me by saying thank you.",
                                      "you're welcome.",
                                      "oh, so nice of you , you're welcome."]
                    reply = random.choice(random_reply_1)
                    # print(reply)
                    speak_print = reply
                    speak_2(reply)

                else:
                    pass
            except Exception as e:
                str(e)
                speak_print = "Sorry, something went wrong with that. please try again or report the incident to our team."
                speak("Sorry, something went wrong with that. please try again or report the incident to our team.")


startExecution = MainThread()

if listening == "listening...":
    listening_wave = "files/icons/listening_wave.gif"
elif listening == '':
    listening_wave = "files/icons/sound_wave.gif"


# Handle high resolution displays:
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    # noinspection PyTypeChecker
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    # noinspection PyTypeChecker
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Main(QMainWindow):

    def __init__(self):
        # noinspection PyArgumentList
        super().__init__()
        self.ui = Ui_FridayGUI()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_minimize_2.clicked.connect(lambda: self.showMinimized())
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.pushButton_close.clicked.connect(lambda: self.close())
        hbox = QHBoxLayout()
        self.lineedit = QLineEdit(self)
        self.text_out = self.lineedit.text()
        self.lineedit.returnPressed.connect(self.click_button)
        self.lineedit.setGeometry(QtCore.QRect(1400, 730, 480, 61))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(24)
        font.setBold(True)
        
        font.setWeight(75)
        self.lineedit.setFont(font)
        self.lineedit.setStyleSheet("background:transparent;\n"
                                    "border-radius:none;\n"
                                    "color:grey;\n")
        hbox.addWidget(self.lineedit)
        self.text_out = self.lineedit.text()
        os.system('TASKKILL /F /IM friday.exe')

    # noinspection PyGlobalUndefined
    def click_button(self):
        global text_out
        text_out = self.lineedit.text()
        print(text_out)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("files/icons/HUD.gif")
        self.ui.label_5.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie_2 = QtGui.QMovie(listening_wave)
        self.ui.label_4.setMovie(self.ui.movie_2)
        self.ui.movie_2.start()
        self.ui.movie_3 = QtGui.QMovie("files/icons/weather_animation_1.gif")
        self.ui.label_7.setMovie(self.ui.movie_3)
        self.ui.movie_3.start()
        self.ui.movie_4 = QtGui.QMovie("files/icons/vertical window_N1.png")
        self.ui.label_2.setMovie(self.ui.movie_4)
        self.ui.movie_4.start()
        self.ui.label_2.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.ui.label_2.setWordWrap(True)
        self.ui.movie_5 = QtGui.QMovie("files/icons/horizontal window_N1.png")
        self.ui.label_3.setMovie(self.ui.movie_5)
        self.ui.movie_5.start()
        self.ui.movie_5 = QtGui.QMovie("files/icons/DIALOGUE_BOX.png")
        self.ui.label_8.setMovie(self.ui.movie_5)
        self.ui.movie_5.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('h:mm:ss ap')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_time)
        self.ui.textBrowser_2.setText(label_date)
        self.ui.textBrowser_3.setText(f"{WAKE_WORD_CAPITAL}")
        self.ui.textBrowser_4.setText("DEVELOPED AT EUFORIS")
        self.ui.textBrowser_5.setText(speak_print)
        self.ui.textBrowser_6.setText(listening)
        self.ui.textBrowser_7.setText(text)
        self.ui.textBrowser_8.setText(location)
        self.ui.textBrowser_9.setText(temperature)
        self.ui.textBrowser_10.setText(weatherPrediction)
        # self.ui.movie_2.destroyed(self.ui.movie_2)
        # self.ui.label_3.update(self.GUI_weather_info())


app = QApplication(sys.argv)
friday = Main()
friday.show()
sys.exit(app.exec_())
