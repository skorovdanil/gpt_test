import os
from openai import Client
from config import key
import time

client = Client(api_key=key)

def get_pdf_files(directory):
    pdf_files = []
    for file in os.listdir(directory):
        if file.endswith(".pdf"):
            pdf_files.append(os.path.join(directory, file))
    return pdf_files

def upload_pdf_files(files):
    file_ids = []
    for file_path in files:
        with open(file_path, "rb") as f:
            uploaded_file = client.files.create(
                file=f,
                purpose='assistants'
            )
            file_ids.append(uploaded_file.id)
    return file_ids

def create_assistant(name, description, instructions, model, tools, file_ids):
    assistant = client.beta.assistants.create(
        name=name,
        description=description,
        instructions=instructions,
        model=model,
        tools=tools,
        file_ids=file_ids
    )
    return assistant

def create_thread(messages, file_ids):
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": "Посмотри ответ в файле",
                "file_ids": file_ids
            }
        ]
    )
    return thread

# Определите директорию, в которой находятся ваши PDF-файлы
pdf_directory = "instructions/"

# Получите список всех PDF-файлов в указанной директории
pdf_files = get_pdf_files(pdf_directory)

# Загрузите все PDF-файлы и получите их идентификаторы
file_ids = upload_pdf_files(pdf_files)

print(file_ids)
# Создайте ассистента, передав список идентификаторов файлов
assistant = create_assistant(
    name="Ассистент по битрикс в стоительной компании",
    description="Ты ассистент строительной компании и должен консультировать пользователей, пиши ответы кратко и четко, нужно выбирать информацию (подкрепля картинками, если они есть и нужны) только из файлов, которые загружены",
    instructions="Ты должен помогать разобраться в функционале шахматки и битрикса, пиши ответы кратко и четко",
    model="gpt-3.5-turbo-1106",
    tools=[{"type": "retrieval"}],
    file_ids=file_ids
)

# Создайте новую ветку для ассистента с сообщением пользователя и прикрепленными файлами
thread = create_thread(
    messages=[
        {
            "role": "user",
            "content": "Посмотри ответ в файлах",
            "file_ids": file_ids
        }
    ],
    file_ids=file_ids
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
