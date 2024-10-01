from pydub import AudioSegment
import os

def convert_mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")

# 예제: 모든 mp3 파일을 wav로 변환
mp3_dir = "./japanese_data/audio_files"
for filename in os.listdir(mp3_dir):
    if filename.endswith(".mp3"):
        mp3_path = os.path.join(mp3_dir, filename)
        wav_path = os.path.splitext(mp3_path)[0] + ".wav"
        convert_mp3_to_wav(mp3_path, wav_path)
        print(f"Converted {mp3_path} to {wav_path}")
