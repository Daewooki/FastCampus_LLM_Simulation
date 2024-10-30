from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app) # cors 이슈 없도록 설정


client = OpenAI()
apikey = os.getenv('OPENAI_API_KEY')

ASSISTANT_ID = "asst_3omFSZgzfxvTfnp7YEgc23VF"

# http://127.0.0.1:5000/chat

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')

    if not user_input:
        return jsonify({'error': 'No message.'}), 400
    
    # 스레드 생성
    thread = client.beta.threads.create()

    # 사용자 메시지 추가
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_input
    )

    # assistant 실행
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=ASSISTANT_ID
    )

    # 응답 메시지 가져오기
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    assistant_response = None
    for msg in messages.data:
        if msg.role == 'assistant':
            assistant_response = msg.content[0].text.value
            break

    if assistant_response:
        return jsonify({'response': assistant_response}), 200
    else:
        return jsonify({'error': 'No response from assistant.'}), 500
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)