import os
import pandas as pd
import binascii


# Parquet 파일 경로 리스트
parquet_files = ['C:/Users/daewook/Desktop/download_model/TTS Data/train-00001-of-00003.parquet',
                 'C:/Users/daewook/Desktop/download_model/TTS Data/train-00002-of-00003.parquet',
                 'C:/Users/daewook/Desktop/download_model/TTS Data/train-00000-of-00003.parquet']


# 각 Parquet 파일을 읽어서 데이터프레임으로 저장
dfs = [pd.read_parquet(file) for file in parquet_files]


# 데이터프레임 병합
combined_df = pd.concat(dfs, ignore_index=True)


# 저장할 디렉토리 설정
output_dir = 'japanese_data'
audio_dir = os.path.join(output_dir, 'audio_files')
text_dir = os.path.join(output_dir, 'texts')


# 디렉토리 생성
os.makedirs(audio_dir, exist_ok=True)
os.makedirs(text_dir, exist_ok=True)


# 데이터 저장
for index, row in combined_df.iterrows():
    audio_data_dict = row['audio']
    transcription = row['transcription']


    # 오디오 데이터가 딕셔너리 형태일 경우
    if isinstance(audio_data_dict, dict):
        audio_data = audio_data_dict.get('bytes', None)  # 'bytes' 키를 통해 데이터에 접근


        if audio_data:  # 데이터가 존재할 경우
            try:
                # 데이터의 첫 몇 바이트를 확인하여 파일 포맷 추정
                print(f"Audio data type: {type(audio_data)}, First 20 bytes: {binascii.hexlify(audio_data[:20])}")


                file_extension = '.mp3'  # 기본값으로 mp3 설정


                if audio_data[:3] == b'ID3':
                    file_extension = '.mp3'
                elif audio_data[:4] == b'RIFF':
                    file_extension = '.wav'
                elif audio_data[:4] == b'OggS':
                    file_extension = '.ogg'
                # 필요에 따라 추가 포맷을 여기에 추가


                audio_filename = f'audio_{index}{file_extension}'
                audio_output_path = os.path.join(audio_dir, audio_filename)
               
                # 바이너리 데이터를 파일로 저장
                with open(audio_output_path, 'wb') as f:
                    f.write(audio_data)
                   
                print(f"Saved {audio_output_path}")
            except Exception as e:
                print(f"Error processing audio data at index {index}: {e}")
   
    # 트랜스크립트만 텍스트 파일로 저장
    text_filename = f'transcription_{index}.txt'
    text_output_path = os.path.join(text_dir, text_filename)
   
    with open(text_output_path, 'w', encoding='utf-8') as f:
        f.write(transcription)
   
    print(f"Saved transcription to {text_output_path}")


