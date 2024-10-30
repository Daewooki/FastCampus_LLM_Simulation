import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QScrollArea
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie, QFont, QLinearGradient, QBrush, QPalette, QColor
import requests
from pygame import mixer
from PyQt5 import QtCore
import time

NAME = "호시노 아이"
JOB = "최애의 아이"

class TypingEffect(QThread):
    update_text = pyqtSignal(str)

    def __init__(self, full_text):
        super().__init__()
        self.full_text = full_text

    def run(self):
        displayed_text = ''
        for char in self.full_text:
            displayed_text += char
            self.update_text.emit(displayed_text)
            self.msleep(50)

class AudioPlayer(QThread):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def run(self):
        try:
            mixer.init()
            mixer.music.load(self.file_path)
            mixer.music.play()
            while mixer.music.get_busy():
                QtCore.QThread.msleep(100)
            mixer.music.unload()
            os.remove(self.file_path)
        except Exception as e:
            print(f"Error playing sound: {str(e)}")

class CustomUI(QWidget):
    def __init__(self):
        super().__init__()

        self.GIF_PATHS = ["ai_hoshino1.png", "ai_hoshino2.png", "ai_hoshino3.png"]
        self.image_index = 0

        self.setWindowTitle("Chat Simulation")
        self.background = QLabel(self)
        
        self.movie = QMovie(self.GIF_PATHS[self.image_index])
        self.background.setMovie(self.movie)
        self.movie.start()

        self.background.setScaledContents(True)
        self.background.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        self.overlay = QWidget(self)
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, 1)
        gradient.setCoordinateMode(QLinearGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QColor(0, 0, 0, 80))
        gradient.setColorAt(1.0, QColor(0, 0, 0, 80))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.overlay.setPalette(palette)
        self.overlay.setAutoFillBackground(True)

        self.title_area = QWidget(self.overlay)
        self.title_area.setStyleSheet("background-color: transparent; padding-left: 20px; padding-right: 20px;")

        self.title = QLabel(f"{NAME}", self.title_area)
        self.title.setStyleSheet("color: white; font-weight: bold;")
        title_font = QFont("Arial", 20, QFont.Bold)
        self.title.setFont(title_font)

        self.subtitle = QLabel(f"{JOB}", self.title_area)
        subtitle_font = QFont("Arial", 14)
        self.subtitle.setFont(subtitle_font)
        self.subtitle.setStyleSheet("color: #89CFF0;")

        title_layout = QHBoxLayout(self.title_area)
        title_layout.addWidget(self.title)
        title_layout.addWidget(self.subtitle)
        title_layout.addStretch()

        self.line = QLabel(self.title_area)
        self.line.setFixedHeight(2)
        self.line.setStyleSheet("background-color: white; margin-top: 10px;")
        title_layout.addWidget(self.line)

        self.scroll_area = QScrollArea(self.overlay)
        self.scroll_area.setWidgetResizable(True)
        self.chat_area = QLabel()
        self.chat_area.setStyleSheet("color: white; font-size: 16px; padding: 10px; background-color: transparent;")
        self.chat_area.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.chat_area.setWordWrap(True)
        self.scroll_area.setWidget(self.chat_area)
        self.scroll_area.setStyleSheet("background-color: rgba(0, 0, 0, 150); border: none;")

        chat_layout = QVBoxLayout(self.overlay)
        chat_layout.addWidget(self.title_area)
        chat_layout.addWidget(self.line)
        chat_layout.addWidget(self.scroll_area)

        self.input_box = QLineEdit(self.overlay)
        self.input_box.setStyleSheet("background-color: white; font-size: 18px; padding: 10px; margin: 10px; border-radius: 15px;")
        self.input_box.returnPressed.connect(self.on_enter_pressed)

        self.send_button = QPushButton("➤", self.overlay)
        self.send_button.setFixedSize(50, 40)
        self.send_button.setStyleSheet("background-color: #1a73e8; color: white; font-size: 18px; margin: 10px; border-radius: 20px;")
        self.send_button.clicked.connect(self.on_enter_pressed)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        chat_layout.addLayout(input_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(self.background)
        self.setLayout(layout)

        self.overlay.setGeometry(0, self.height() - 300, self.width(), 300)
        self.title_area.setGeometry(20, 20, self.width() - 40, 60)

        self.setMinimumSize(800, 600)
        self.setGeometry(100, 100, 1024, 768)

        self.show()

    def display_typing_effect_dual(self, message_ko, message_ja):
        combined_message = f"{message_ja}\n{message_ko}"
        self.typing_thread = TypingEffect(combined_message)
        self.typing_thread.update_text.connect(self.chat_area.setText)
        self.typing_thread.start()

    def resizeEvent(self, event):
        self.overlay.setGeometry(0, self.height() - 300, self.width(), 300)
        self.title_area.setGeometry(20, 20, self.width() - 40, 60)
        self.background.resize(self.size())
        event.accept()

    def on_enter_pressed(self):
        user_input = self.input_box.text().strip()
        if user_input:
            # Request response from GPT Assistant API
            response_ko, response_ja = self.request_gpt_response(user_input)
            if response_ko and response_ja:
                # Send Japanese part of GPT response to TTS API
                audio_path = self.request_tts(response_ja)
                
                if audio_path:
                    self.audio_thread = AudioPlayer(audio_path)
                    self.audio_thread.start()

                # Display typing effect with both Korean and Japanese responses
                self.display_typing_effect_dual(response_ko, response_ja)
                # Update the background image to the next one in the list
                self.update_background_image()

            else:
                print("No response from GPT assistant.")
            
        self.input_box.clear()

    def update_background_image(self):
        # Cycle through the images
        self.image_index = (self.image_index + 1) % len(self.GIF_PATHS)
        self.movie = QMovie(self.GIF_PATHS[self.image_index])
        self.background.setMovie(self.movie)
        self.movie.start()

    def request_gpt_response(self, user_input, max_retries=5):
        retries = 0

        while retries < max_retries:
            try:
                # Call GPT Assistant API
                url = 'http://127.0.0.1:5000/chat'
                headers = {'Content-Type': 'application/json'}
                data = {'message': user_input}
                response = requests.post(url, json=data, headers=headers)
                
                if response.status_code == 200:
                    response_data = response.json().get('response', "")
                    
                    if "일본어:" in response_data and "한국어:" in response_data:
                        # Safely extract the Japanese and Korean parts
                        japanese_part = response_data.split("일본어:")[1].split("한국어:")[0].strip()
                        korean_part = response_data.split("한국어:")[1].strip()
                        return korean_part, japanese_part
                    else:
                        print(f"Error: The response doesn't contain the expected '일본어:' or '한국어:' markers. Retrying... ({retries+1}/{max_retries})")
                        retries += 1
                        time.sleep(1)
                else:
                    print(f"Error: GPT Assistant API returned status {response.status_code}. Retrying... ({retries+1}/{max_retries})")
                    retries += 1
                    time.sleep(1)
            except Exception as e:
                print(f"Error during GPT request: {str(e)}. Retrying... ({retries+1}/{max_retries})")
                retries += 1
                time.sleep(1)

        print("Max retries reached. No valid response from GPT Assistant.")
        return None, None

    def request_tts(self, text):
        try:
            timestamp = int(time.time())
            output_wav_path = f'output_{timestamp}.wav'
            response = requests.get(f'http://172.81.127.6:10752/tts', params={'text': text}, stream=True)
            with open(output_wav_path, 'wb') as f:
                f.write(response.content)
            return output_wav_path
        except Exception as e:
            print(f"Error during TTS request: {str(e)}")
            return None
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = CustomUI()
    sys.exit(app.exec_())