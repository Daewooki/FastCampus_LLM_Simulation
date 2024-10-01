# 기존 파일 경로
input_file_path = 'transcript.v.1.4.txt'
# 새로 생성할 파일 경로
output_file_path = 'transcript_cleaned.txt'

# 파일 읽기
with open(input_file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 파일 쓰기
with open(output_file_path, 'w', encoding='utf-8') as f:
    for line in lines:
        # 기존 형식: 1/1_0000.wav|그는 괜찮은 척하려고 애쓰는 것 같았다.|그는 괜찮은 척하려고 애쓰는 것 같았다.|발음|점수|번역
        parts = line.strip().split('|')
        
        if len(parts) >= 3:
            # '1/1_0000.wav'에서 '/' 이후의 파일명만 추출
            wav_file = parts[0].split('/')[-1]
            
            # original_text와 spoken_text 가져오기
            original_text, spoken_text = parts[1], parts[2]
            
            # 새로운 형식으로 변환: wav_file|original_text|spoken_text
            new_format_line = f"{wav_file}|{spoken_text}|{spoken_text}\n"
            
            f.write(new_format_line)

print(f"파일이 성공적으로 변환되어 저장되었습니다: {output_file_path}")