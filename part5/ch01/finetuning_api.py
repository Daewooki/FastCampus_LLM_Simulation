from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="ft:gpt-4o-mini-2024-07-18:personal:girlfriend:ACwApKL6:ckpt-step-76",
  messages=[
    {"role": "system", "content": "츤데레 성격의 여자친구"},
    {"role": "user", "content": "안녕? 오늘 산책갈까?"}
  ]
)
print(completion.choices[0].message.content)