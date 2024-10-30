import torch
from TTS.api import TTS

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

# List available 🐸TTS models
print(TTS().list_models())

# Init TTS
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

# Run TTS
# ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
# Korean
# # Text to speech list of amplitude values as output
# wav = tts.tts(text="나는 커피 마시는 것을 좋아해. 너는 뭘 좋아해?", speaker_wav="/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/kss_all/1_0093.wav", language="ko")
# # Text to speech to a file
# tts.tts_to_file(text="나는 커피 마시는 것을 좋아해. 너는 뭘 좋아해?", language="ko", speaker_wav="/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/kss_all/1_0093.wav", file_path="output.wav")

# Japanese
# Text to speech list of amplitude values as output
wav = tts.tts(text="あなたと一緒にいて、とても幸せです。ありがとうございます。", speaker_wav="/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/japanese_all/wavs/audio_0.wav", language="ja")
# Text to speech to a file
tts.tts_to_file(text="あなたと一緒にいて、とても幸せです。ありがとうございます。", language="ja", speaker_wav="/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/japanese_all/wavs/audio_0.wav", file_path="output.wav")
