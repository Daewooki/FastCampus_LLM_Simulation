# 행 개수를 세려는 텍스트 파일 경로
text_file_path = 'transcript_cleaned.txt'

# 행 개수 세기
with open(text_file_path, 'r', encoding='utf-8') as f:
    line_count = sum(1 for line in f)
    print(f"텍스트 파일의 총 행 개수: {line_count}")


import os

# 파일 개수를 세려는 디렉토리 경로
directory_path = 'kss_all'

# 파일 개수 세기
file_count = len([name for name in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, name))])
print(f"디렉토리 내 파일 개수: {file_count}")