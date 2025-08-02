# @author: Martin Tejada
# @version: 2.0
# @since 8/01/2025

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtGui import QFont, QMovie
from PyQt6.QtCore import QSize, QTimer
import time
import random
import sys
from ranbotapi import get_llm_response
from rrb_logic import rrb_logic

welcome_msg = [
    "Hello, I'm RanRan, wassup?", 
    "Tell me about your favourite movie!", 
    "How was your day today?", 
    "Tell me about your favourite food!", 
    "Any great ideas you want to explore?"
    ]

suggested_msg = {
    0 : ["I am good, how are you!", "Not much you?"],
    1 : ["I don't have a favourite movie!", "I like the movie fantastic 4!"],
    2 : ["My day was good! :)", "I had a rough day today :("],
    3 : ["I love pizza!", "Sushi sounds rlly good right now!"],
    4 : ["I want to find a new hobby!", "I want to learn something new!"]
}

random_number = random.randint(0, len(welcome_msg) - 1)

class ChatBotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RanRan ChatBot")
        self.setGeometry(100, 100, 650, 450)
        
        # Intialize buttons, labels, and widgets etc
        self.chat_log = QTextEdit()
        self.input_line = QLineEdit()
        self.send_button = QPushButton("Send")
        self.mic_button = QPushButton("MIC")
        self.name_label = QLabel("RanRan:")
        self.idle_label = QLabel()
        self.idle_animation = QMovie("assets/idlerrb.gif")

        self.suggest_value = suggested_msg.get(random_number)
        self.suggest_msg1 = QPushButton(self.suggest_value[0])
        self.suggest_msg2 = QPushButton(self.suggest_value[1])

        self.main_layout = QVBoxLayout()
        self.input_layout = QHBoxLayout()
        self.suggest_layout = QHBoxLayout()
        
        # Using rrb_logic class
        self.logic = rrb_logic()
        self.logic.play_open_sound()

        # Flag for closeEvent method
        self._force_close_flag = False

        # To remove suggested messages after first message
        self._message_counter = 0

        self.initUI()
        
    # Layout, styling, and connecting signals  
    def initUI(self):

        self.chat_log.setReadOnly(True)
        self.chat_log.setFont(QFont("Arial", 12))
        self.chat_log.setStyleSheet("background-color: #F1EAE4; padding: 5px; border-radius: 10px;")

        self.input_line.setFont(QFont("Arial", 12))
        self.input_line.setStyleSheet("background-color: #F1EAE4")
        self.input_line.setPlaceholderText("Type your message here...")

        self.send_button.setFont(QFont("Arial", 12))
        self.send_button.clicked.connect(self.send_message)
        self.send_button.setStyleSheet("background-color: #C1292E; color: white; padding: 6px 12px;") # Alternate color #6a5acd blue

        self.mic_button.setFont(QFont("Arial", 12))
        self.mic_button.clicked.connect(self.listen_to_user)
        self.mic_button.setStyleSheet("background-color: #C1292E; color: white; padding: 6px 12px;") 
        
        self.name_label.setFont(QFont("Arial", 11))
        self.name_label.setStyleSheet("background-color: #C1292E; color: white; font-weight: bold; padding: 5px; border-radius: 10px;")

        self.suggest_msg1.setFont(QFont("Arial", 12))
        self.suggest_msg1.clicked.connect(self.write_suggested)
        self.suggest_msg1.setStyleSheet("background-color: #C1292E; color: white; padding: 6px 12px;") 

        self.suggest_msg2.setFont(QFont("Arial", 12))
        self.suggest_msg2.clicked.connect(self.write_suggested)
        self.suggest_msg2.setStyleSheet("background-color: #C1292E; color: white; padding: 6px 12px;") 

        self.idle_label.setMovie(self.idle_animation)
        self.idle_animation.setScaledSize(QSize(160,160))
        self.idle_animation.start()
        
        self.input_layout.addWidget(self.input_line)
        self.input_layout.addWidget(self.send_button)
        self.input_layout.addWidget(self.mic_button)

        self.suggest_layout.addWidget(self.suggest_msg1)
        self.suggest_layout.addWidget(self.suggest_msg2)

        self.main_layout.addWidget(self.name_label)
        self.main_layout.addWidget(self.idle_label)
        self.main_layout.addWidget(self.chat_log)
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.suggest_layout)

        self.setStyleSheet("background-color: #313638")
        self.setLayout(self.main_layout)

        # Initial greeting
        self.chat_log.append(f'RanRan Bot: {welcome_msg[random_number]}')

    # Get chatbot reply from user input, and add both messages to chatlog
    def send_message(self):
        user_text = self.input_line.text()

        # Ignore empty/white-space input
        if not user_text.strip():
            return
        
        self.chat_log.append("")
        self.chat_log.append(f'<div style="color: blue; font-weight: bold;"> You: {user_text}</div>')

        response = get_llm_response(user_text)

        self.logic.play_msg_sound()
        self.chat_log.append("")
        self.chat_log.append(f'RanRan Bot: {response}')

        # Clear text field for new input
        self.input_line.clear()

        self._message_counter += 1

        if self._message_counter != 0:
            self.suggest_msg1.setDisabled(True)
            self.suggest_msg2.setDisabled(True)
            self.suggest_msg1.hide()
            self.suggest_msg2.hide()

    # Handling suggested messages, and removing from UI after use
    def write_suggested(self):
        self.button = self.sender()
        self.user_text = self.button.text()
        self.input_line.setText(self.user_text)
        self.send_message()

        self.suggest_msg1.setDisabled(True)
        self.suggest_msg2.setDisabled(True)
        self.suggest_msg1.hide()
        self.suggest_msg2.hide()

    # Get microphone input, and set it to the user's text field
    def listen_to_user(self):
        self.user_speech = self.logic.listen_for_input()
        self.input_line.setText(self.user_speech)

    # Play audio on program close, overides orginal built-in closeEvent method, requires flagging and extra method to avoid loops and errors
    def closeEvent(self, event):
        if self._force_close_flag:
            event.accept()
        else:
            event.ignore()
            self.logic.play_close_sound()
            QTimer.singleShot(2000, self.force_close)

    def force_close(self):
        self._force_close_flag = True
        self.close() # calls closeEvent again
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatBotApp()
    window.show()
    sys.exit(app.exec())
