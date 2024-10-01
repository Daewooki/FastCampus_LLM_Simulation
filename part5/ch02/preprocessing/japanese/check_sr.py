import librosa
import os


# 오디오 파일
# 경로 설정
audio_dir = 'japanese_data/audio_files/'


# 모든 오디오 파일의 샘플 레이트 확인
sample_rates = []
for file_name in os.listdir(audio_dir):
    file_path = os.path.join(audio_dir, file_name)
    try:
        y, sr = librosa.load(file_path, sr=None)
        print(sr)
        sample_rates.append(sr)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")


# 고유한 샘플 레이트 출력
unique_sample_rates = set(sample_rates)
print(f"Unique sample rates in the dataset: {unique_sample_rates}")