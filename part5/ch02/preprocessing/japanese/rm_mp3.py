import os

# mp3 파일들을 삭제할 디렉터리 경로 설정
directory = r'C:/Users/daewook/Desktop/python/FastCampus_LLM_Simulation/part5/ch02/preprocessing/japanese/audio_files'

# 디렉터리 내의 .mp3 파일 삭제
for filename in os.listdir(directory):
    if filename.endswith(".mp3"):
        file_path = os.path.join(directory, filename)
        os.remove(file_path)
        print(f"Deleted: {file_path}")
