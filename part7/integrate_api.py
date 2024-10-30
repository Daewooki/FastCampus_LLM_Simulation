from flask import Flask, request, jsonify, send_file
import requests
import os
import time
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.tts.layers.xtts.tokenizer import Tokenizer
import urllib.parse

app = Flask(__name__)

# OpenAI API Settings
API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID = "asst_UHWGpegS06cbtXyjGmfXZe4a"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}",
    "OpenAI-Beta": "assistants=v2"
}
BASE_URL = "https://api.openai.com/v1"
thread_id = None  # Thread ID storage

# TTS Model Settings
print("Loading TTS model...")
config = XttsConfig()
# LANGUAGE = "ko"
LANGUAGE = "ja"

## 216342 kss best
## /workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/GPT_XTTS_v2.0_KSS_FT-October-01-2024_04+36PM-dbf1a08a/best_model_216342.pth
## 139840 japanese best
## /workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/XTTS_v2.0_Japanese_FT-October-13-2024_06+18AM-dbf1a08a/best_model_139840.pth

config.load_json("/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/XTTS_v2.0_Japanese_FT-October-13-2024_06+18AM-dbf1a08a/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/XTTS_v2.0_Japanese_FT-October-13-2024_06+18AM-dbf1a08a/", use_deepspeed=False)
model.cuda()

if model.tokenizer is None:
    model.tokenizer = Tokenizer(config.model_args['tokenizer_file'])

# Speaker latents computation
# gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/kss_all/4_0017.wav"])
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/japanese_all/wavs/audio_0.wav"])

# Chat API Functionality
def get_assistant_response(message_content):
    global thread_id

    # Initialize or use existing thread
    if thread_id is None:
        response = requests.post(f"{BASE_URL}/threads", headers=HEADERS)
        response.raise_for_status()
        thread = response.json()
        thread_id = thread['id']
    else:
        pass  # Reuse thread_id

    # Add message to thread
    data = {"role": "user", "content": message_content}
    response = requests.post(f"{BASE_URL}/threads/{thread_id}/messages", headers=HEADERS, json=data)
    response.raise_for_status()

    # Execute assistant response
    data = {
        "assistant_id": ASSISTANT_ID
    }
    response = requests.post(f"{BASE_URL}/threads/{thread_id}/runs", headers=HEADERS, json=data)
    response.raise_for_status()
    run_id = response.json()['id']

    # Poll for completion
    while True:
        response = requests.get(f"{BASE_URL}/threads/{thread_id}/runs/{run_id}", headers=HEADERS)
        response.raise_for_status()
        if response.json()['status'] == 'completed':
            break
        time.sleep(1)

    # Retrieve final assistant response
    response = requests.get(f"{BASE_URL}/threads/{thread_id}/messages", headers=HEADERS)
    response.raise_for_status()
    for msg in response.json()['data']:
        if msg['role'] == 'assistant':
            for content in msg['content']:
                if content['type'] == 'text':
                    return content['text']['value'], content.get('choices', [])
    return "No response found.", []

# TTS Functionality
def generate_tts(text):
    print(f"Generating TTS for text: {text}")
    out = model.inference(text, LANGUAGE, gpt_cond_latent, speaker_embedding, temperature=0.1)
    output_wav_path = "xtts.wav"
    torchaudio.save(output_wav_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)
    return output_wav_path

# Chat Route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message_content = data.get("message")
    if not message_content:
        return jsonify({"error": "No message content provided"}), 400
    response_text, choices = get_assistant_response(message_content)
    return jsonify({"response_text": response_text, "choices": choices})

# TTS Route
@app.route('/tts', methods=['POST'])
def tts():
    data = request.json
    text = data.get("text")
    text = text.replace("Choices", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400
    audio_file_path = generate_tts(text)
    return send_file(audio_file_path, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
