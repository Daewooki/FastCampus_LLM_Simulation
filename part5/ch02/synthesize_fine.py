# ## Korean
# import os
# import torch
# import torchaudio
# from TTS.tts.configs.xtts_config import XttsConfig
# from TTS.tts.models.xtts import Xtts
# from TTS.tts.layers.xtts.tokenizer import Tokenizer

# print("Loading model...")
# config = XttsConfig()

# config.load_json("/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/GPT_XTTS_v2.0_KSS_FT-October-01-2024_04+36PM-dbf1a08a/config.json")
# model = Xtts.init_from_config(config)
# # model.pth
# model.load_checkpoint(config, checkpoint_dir="/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/GPT_XTTS_v2.0_KSS_FT-October-01-2024_04+36PM-dbf1a08a", use_deepspeed=False)
# model.cuda()

# # Manually initialize tokenizer if it wasn't loaded correctly
# if model.tokenizer is None:
#     print("Tokenizer was not initialized. Manually loading tokenizer...")
#     model.tokenizer = Tokenizer(config.model_args['tokenizer_file'])

# print("Tokenizer after initialization:", model.tokenizer)

# print("Computing speaker latents...")
# gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/kss_all/1_0093.wav"])

# print("Inference...")
# out = model.inference(
#     "나는 커피 마시는 것을 좋아해. 너는 뭘 좋아해?",
#     "ko",
#     gpt_cond_latent,
#     speaker_embedding,
#     temperature=0.7,
# )
# torchaudio.save("xtts.wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)

## Japanese
import os
import torch
import torchaudio
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import Xtts
from TTS.tts.layers.xtts.tokenizer import Tokenizer

print("Loading model...")
config = XttsConfig()

config.load_json("/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/XTTS_v2.0_Japanese_FT-October-13-2024_06+18AM-dbf1a08a/config.json")
model = Xtts.init_from_config(config)
# model.pth
model.load_checkpoint(config, checkpoint_dir="/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/run/training/XTTS_v2.0_Japanese_FT-October-13-2024_06+18AM-dbf1a08a", use_deepspeed=False)
model.cuda()

# Manually initialize tokenizer if it wasn't loaded correctly
if model.tokenizer is None:
    print("Tokenizer was not initialized. Manually loading tokenizer...")
    model.tokenizer = Tokenizer(config.model_args['tokenizer_file'])

print("Tokenizer after initialization:", model.tokenizer)

print("Computing speaker latents...")
gpt_cond_latent, speaker_embedding = model.get_conditioning_latents(audio_path=["/workspace/FastCampus_TTS/TTS/recipes/ljspeech/xtts_v2/japanese_all/wavs/audio_0.wav"])

print("Inference...")
out = model.inference(
    "あなたと一緒にいて、とても幸せです。ありがとうございます。",
    "ja",
    gpt_cond_latent,
    speaker_embedding,
    temperature=0.7,
)
torchaudio.save("xtts.wav", torch.tensor(out["wav"]).unsqueeze(0), 24000)
