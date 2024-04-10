from openai import OpenAI, AsyncOpenAI
import config
client = AsyncOpenAI(api_key=config.key)




completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "Вы - поэтический помощник, умеющий объяснять сложные программные концепции с творческим размахом."},
    {"role": "user", "content": "Составьте стихотворение, которое объясняет концепцию рекурсии в программировании."}
  ]
)

print(completion.choices[0].message)