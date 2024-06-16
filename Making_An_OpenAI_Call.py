import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("local.env")

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Set the model to use
model_engine = "gpt-3.5-turbo"

# Set the prompt to generate text for
text = input("Topic: ")
prompt = text

print("The AI BOT is trying now to generate a new text for you...")

response = client.chat.completions.create(
  model=model_engine,
  #max_tokens=1024,
  messages=[
    {"role": "system", "content": "You are a helpful assistant.Provide details about the topic in 2 lines"},
    {"role": "user", "content": f'{prompt}'},
    {"role": "system", "content": '{response}'}
  ]
)

# Print the generated text
generated_text = response.choices[0].message.content
print(response.choices[0].message.content)

# Save the text in a file
with open("generated_text.txt", "w") as file:
    file.write(generated_text.strip())

print("The Text Has Been Generated Successfully!")