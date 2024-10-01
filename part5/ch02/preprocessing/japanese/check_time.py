import os
from pydub import AudioSegment

# 오디오 파일이 저장된 디렉토리 경로
audio_dir = './japanese_data/audio_files'

# 총 길이를 저장할 변수
total_duration = 0.0
# 파일 경로를 확인하고 접근 가능한지 테스트
audio_dir = os.path.abspath('japanese_data/audio_files')


# 디렉토리 내의 모든 오디오 파일에 대해
for audio_filename in os.listdir(audio_dir):
    audio_path = os.path.join(audio_dir, audio_filename)
    
    try:
        # 오디오 파일 불러오기
        audio = AudioSegment.from_file(audio_path)
        
        # 파일 길이를 초 단위로 계산
        duration_seconds = len(audio) / 1000.0  # 길이는 밀리초로 반환되므로 초로 변환
        
        # 총 길이에 추가
        total_duration += duration_seconds
        
        print(f"{audio_filename}: {duration_seconds} seconds")
    except Exception as e:
        print(f"Error processing {audio_filename}: {e}")

# 총 길이 출력
print(f"Total duration of all audio files: {total_duration} seconds")
