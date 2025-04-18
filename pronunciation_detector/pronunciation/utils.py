import pyttsx3

def speak_text(word):
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()
