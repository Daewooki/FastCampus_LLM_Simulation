init python:
    import requests
    import re
    import uuid
    import os
    import random


    # 서버 URL 설정
    # 서버 IP 입력 혹은 DNS
    IP = ""
    chat_url = f"http://{IP}/chat"
    tts_url = f"http://{IP}/tts"


    # 배경 이미지 폴더 경로 설정
    bg_folder = os.path.join(renpy.config.basedir, 'game', 'images', 'backgrounds')


    # 폴더 내의 모든 파일을 리스트로 가져옴
    background_images = [f for f in os.listdir(bg_folder) if f.endswith(('.jpg', '.png'))]


    def get_random_background():
        # 랜덤으로 이미지 파일 하나 선택
        selected_bg = random.choice(background_images)
        return os.path.join(bg_folder, selected_bg).replace("\\", "/")  # 경로를 슬래시로 변경


    def send_message_to_assistant(message):
        while True:
            # 메시지를 보내고 응답을 받아오는 함수
            data = {"message": message}
            chat_response = requests.post(chat_url, json=data)

            if chat_response.status_code == 200:
                response_json = chat_response.json()
                response_text = response_json.get("response_text", "")

                # 정규식 패턴 설정
                pattern = r'(?:\d\.\s*)?Dialogue:\s*"(.*?)"\s*(?:\n|\\n)?(?:\d\.\s*)?Choices:\s*(?:"1\.\s*(.*?)"\s*"2\.\s*(.*?)")'

                match = re.search(pattern, response_text, re.DOTALL)
                if match:
                    dialogue = match.group(1).strip()
                    choice_1 = match.group(2).strip()
                    choice_2 = match.group(3).strip()


                # 유효한 선택지가 있을 때만 반환
                if choice_1 and choice_2:
                    # 짧은 UUID 생성 (앞 8자리만 사용) 음성 합성된 파일을 저장하기 위해서.
                    short_uuid = str(uuid.uuid4())[:8]

                    # 대화를 TTS로 변환
                    tts_data = {"text": dialogue}
                    tts_response = requests.post(tts_url, json=tts_data)


                    if tts_response.status_code == 200:
                        # Ren'Py 기본 디렉토리에 파일 저장
                        wav_file = f"{short_uuid}.wav"
                        audio_file_path = os.path.join(renpy.config.basedir, 'game', 'audio', wav_file).replace("\\", "/")
                        with open(audio_file_path, "wb") as f:
                            f.write(tts_response.content)
                        renpy.log(f"Audio file saved as {audio_file_path}")
                        return dialogue, choice_1, choice_2, wav_file

            # 유효하지 않은 경우 반복문을 통해 재시도
            renpy.log("Warning: Invalid response received, retrying...")


# 메인 이미지 
image main_image = "main.png"


define e = Character('최수연', color="#c8ffc8")


label start:
    show main_image at Transform(xalign=0.5, yalign=0.5, zoom=1.0)
   
    window show
    e "시작해볼까?"
    window auto

    menu:
        "시작하기":
            $ random_bg_path = get_random_background()  # 랜덤 배경 이미지 경로 얻기
            show expression random_bg_path at Transform(xalign=0.5, yalign=0.5, zoom=1.0)


            $ dialogue, choice_1, choice_2, wav_file = send_message_to_assistant("시작하기")


            # 대화 출력
            $ renpy.pause(0.3)
            
            # 오디오 재생
            play audio wav_file
            e "[dialogue]"  # 변수명으로 대화 삽입

            # 오디오 재생 후 다음 선택지로
            jump show_choices


label show_choices:
    menu:
        "[choice_1]":
            $ random_bg_path = get_random_background()
            show expression random_bg_path at Transform(xalign=0.5, yalign=0.5, zoom=1.0)


            $ dialogue, choice_1, choice_2, wav_file = send_message_to_assistant(choice_1)


    
            $ renpy.pause(0.3)
            play audio wav_file
            e "[dialogue]"  # 변수명으로 대화 삽입

            jump show_choices


        "[choice_2]":
            $ random_bg_path = get_random_background()
            show expression random_bg_path at Transform(xalign=0.5, yalign=0.5, zoom=1.0)


            $ dialogue, choice_1, choice_2, wav_file = send_message_to_assistant(choice_2)


            $ renpy.pause(0.3)
            play audio wav_file
            e "[dialogue]"  # 선택에 따라 대화 삽입

            jump show_choices