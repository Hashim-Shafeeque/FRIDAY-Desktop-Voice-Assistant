import speech_recognition as sr


def take_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            global listening
            listening = "listening..."
            print(listening)
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
            text = r.recognize_google(audio, language="en")
            # print(f"user said: {text}")

        except Exception as e:
            print(str(e))
            return "none"
    text = text.lower()
    print(text)
    return text


while True:
    take_audio()
