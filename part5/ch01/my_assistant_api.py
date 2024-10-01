from openai import OpenAI
client = OpenAI()

# 코난
# assistant = client.beta.assistants.retrieve("asst_KdsXRdHmtsSspZv6oDw7rTnM")
# 츤데레 여자친구
assistant = client.beta.assistants.retrieve("asst_jNYK9t3xtMvSwEmLhBEUxhru")

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
  thread_id=thread.id,
  role="user",
  content="안녕? 오늘 산책갈까?"
)

run = client.beta.threads.runs.create_and_poll(
  thread_id=thread.id,
  assistant_id=assistant.id,
)

if run.status == 'completed': 
  messages = client.beta.threads.messages.list(
    thread_id=thread.id
  )
  print(messages.data[0].content[0].text.value)
else:
  print(run.status)