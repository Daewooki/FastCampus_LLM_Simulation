from flask import Flask, request, send_file
import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.tts.layers.xtts.tokenizer import Tokenizer
import urllib.parse
 
app = Flask(__name__)

# 모델 로드 및 초기화
print("Loading model...")
config = XttsConfig()
# LANGUAGE = "ko"
LANGUAGE = "ja"

## 216342 kss best
## /workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/GPT_XTTS_v2.0_KSS_FT-October-12-2024_04+34AM-dbf1a08a/best_model_216342.pth
## 139840 japanese best
## /workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/XTTS_v2.0_Japanese_FT-October-13-2024_06+18AM-dbf1a08a/best_model_139840.pth

config.load_json("/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/XTTS_v2.0_Japanese_FT-October-13-2024_06+18AM-dbf1a08a/config.json")
model = Xtts.init_from_config(config)
model.load_checkpoint(config, checkpoint_dir="/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/XTTS_v2.0_Japanese_FT-October-13-2024_06+18AM-dbf1a08a/", use_deepspeed=False)
model.cuda()

# 토크나이저 수동 초기화
if model.tokenizer is None:
    print("Tokenizer was not initialized. Manually loading tokenizer...")
    model.tokenizer = Tokenizer(config.model_args['tokenizer_file'])

print("Tokenizer after initialization:", model.tokenizer)

# Speaker latents 계산
print("Computing speaker latents...")
# gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/kss_all/4_0017.wav"])
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/japanese_all/wavs/audio_0.wav"])

@app.route('/tts', methods=['GET'])
def generate_tts():
    # URL 인코딩된 텍스트를 디코딩
    encoded_text = request.args.get('text', default='愛してください。久しぶりに一緒に行こう', type=str)
    text = urllib.parse.unquote(encoded_text)
    print(f"Decoded text to synthesize: {text}")

    print("Inference...")
    out = model.inference(
        text,
        LANGUAGE,  # 언어를 일본어로 설정
        gpt_cond_latent,
        speaker_embedding,
        temperature=0.7,
    )

    # 생성된 음성을 저장
    output_wav_path = "xtts.wav"
    torchaudio.save(output_wav_path, torch.tensor(out["wav"]).unsqueeze(0), 24000)

    return send_file(output_wav_path, mimetype='audio/wav')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
