import os
import shutil

# 소스 폴더 목록
source_folders = ['kss/1', 'kss/2', 'kss/3', 'kss/4']
# 타겟 폴더 경로
target_folder = 'kss_all/'

# 타겟 폴더가 없으면 생성
os.makedirs(target_folder, exist_ok=True)

# 각 소스 폴더에서 타겟 폴더로 파일 복사
for folder in source_folders:
    if os.path.exists(folder):
        for file_name in os.listdir(folder):
            source_file = os.path.join(folder, file_name)
            target_file = os.path.join(target_folder, file_name)
            # 파일 복사
            shutil.copy(source_file, target_file)
            print(f"Copied: {source_file} to {target_file}")
    else:
        print(f"Source folder not found: {folder}")

print("모든 파일이 성공적으로 복사되었습니다.")