from pathlib import Path
from openai import OpenAI
import pygame

client = OpenAI()

def text_to_speech(text, voice="nova", output_file="output.mp3"):
    response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
                )
    response.stream_to_file(output_file)

def play_audio(file_path):
    # 초기화
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()


if __name__ == '__main__':
    while True:
        text = input("음성 합성을 위한 텍스트를 입력하세요: ")
        if text.lower() == 'exit':
            print("프로그램을 종료합니다.")
            break
        voice_option = input("사용할 목소리 선택하세요. (alloy, echo, fable, onyx, nova, shimmer): ")
        file_path = "output2.mp3"
        text_to_speech(text, voice=voice_option, output_file=file_path)
        print("오디오 파일이 생성되었습니다.")
        play_audio(file_path)