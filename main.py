from openai import Client
from config import key
import time

client = Client(api_key=key)

file = client.files.create(
    file=open("data.txt", "rb"),
    purpose='assistants'
)

assistant = client.beta.assistants.create(
    name="Повар",
    description="Ты гениальный повар, используешь рецепты из файла data.txt",
    instructions="Ты должен помогать по вопросам приготовления блюд. Рецепты бери из файла",
    model="gpt-3.5-turbo-1106",
    tools=[{"type": "retrieval"}],
    file_ids=[file.id_])


thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Посмотри рецепты из файла",
            "file_ids": [file.id]
        }
    ]
)

assistant_id = assistant.id
thread_id = thread.id

def create_msg(user_msg):
    message_creates = client.beta.threads.messages.create(
        role="user",
        thread_id=thread_id,
        content=f"{user_msg}"
    )


def thread_running():
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    return run.id

def refresh_thread(run_id):
    run_info = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id,
    )

def get_last_msgs():
    messages = client.beta.threads.messages.list(
        thread_id=thread_id,
    )
    return messages


def ask_assistant(user_msg):
    create_msg(user_msg)
    run_id = thread_running()
    time.sleep(10)

    refresh_thread(run_id)

    messages = get_last_msgs()

    print(messages.data[0].content[0].text.value)


while True:
    print("Введите вопрос ассистенту:.....")
    user_msg = input()
    ask_assistant(f"{user_msg}")
