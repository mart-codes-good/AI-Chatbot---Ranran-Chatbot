from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtCore import QUrl
import speech_recognition as sr

class RrbSoundManager:
    def __init__(self):
        # Load sounds
        self.msg_sound = self.load_sound("assets/rrb_message_sound.wav")
        self.open_sound = self.load_sound("assets/rrb_bootup_sound.wav")
        self.close_sound = self.load_sound("assets/rrb_on_close_sound.wav")

    # Intializing sound components, in a reusable manner
    def load_sound(self, path):
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(path))
        sound.setVolume(0.5)
        return sound

    def play_msg(self):
        self.msg_sound.play()

    def play_open(self):
        self.open_sound.play()

    def play_close(self):
        self.close_sound.play()

# Methods for speech recognition
class RrbSpeechRecognizer:
    def __init__(self):
        self.r = sr.Recognizer() # Interacts with microphone

    def listen(self):
        with sr.Microphone() as source:
            audio = self.r.listen(source) # start listening and captures user speech
        try:
            return self.r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I did not hear you!" # Error handling to avoid crashes
        except sr.RequestError:
            return "Speech recongnition service error!"

# Wrapping methods for cleaner use
class rrb_logic:
    def __init__(self):
        self.sounds = RrbSoundManager()
        self.speech = RrbSpeechRecognizer()

    def play_msg_sound(self):
        self.sounds.play_msg()

    def play_open_sound(self):
        self.sounds.play_open()

    def play_close_sound(self):
        self.sounds.play_close()
    def listen_for_input(self):
        return self.speech.listen()

