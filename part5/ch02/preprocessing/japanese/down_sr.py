import os
import librosa
import soundfile as sf


# 타겟 샘플 레이트 설정
target_sample_rate = 22050


# 오디오 파일 경로 설정
audio_dir = './japanese_data/audio_files/'

cnt=0
# 모든 오디오 파일을 다운샘플링
for file_name in os.listdir(audio_dir):
    cnt += 1
    print(cnt)
    file_path = os.path.join(audio_dir, file_name)
    try:
        # 오디오 파일 로드 및 타겟 샘플 레이트로 변환
        y, sr = librosa.load(file_path, sr=target_sample_rate)
       
        # 변환된 오디오 파일을 동일한 경로에 다시 저장
        sf.write(file_path, y, target_sample_rate)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")