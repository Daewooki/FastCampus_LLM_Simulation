import os
import csv


# 경로 설정
audio_directory = r"C:/Users/daewook/Desktop/python/FastCampus_LLM_Simulation/part5/ch02/preprocessing/japanese/japanese_data/audio_files"
text_directory = r"C:/Users/daewook/Desktop/python/FastCampus_LLM_Simulation/part5/ch02/preprocessing/japanese/japanese_data/texts"
output_csv = "output.csv"


# CSV 파일 작성
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter='|')


    # 0부터 9999까지 파일 읽기(file 1만개)
    for i in range(10000):
        print(i)
        text_filename = f"transcription_{i}.txt"


        # 텍스트 파일 경로
        text_filepath = os.path.join(text_directory, text_filename)


        # 텍스트 파일이 존재하는지 확인하고, 존재하면 읽기
        if os.path.exists(text_filepath):
            with open(text_filepath, 'r', encoding='utf-8') as file:
                text = file.read().strip()
                writer.writerow([f"audio_{i}", text, text])


print(f"CSV 파일이 {output_csv}로 저장되었습니다.")