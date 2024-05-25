from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()




client = OpenAI(
  api_key=os.getenv("API_KEY"),
  organization=os.getenv("ORG_ID"),
  project=os.getenv("PROJECT_ID"),
  
)

# model = "gpt-4o"

# test_assistant = client.beta.assistants.create(
#     name="Test assistant",
#     instructions="""You are standart gpt""",
#     model=model
# )
# print(assistant_id := test_assistant.id)

# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user", 
#             "content": "How do i get started working out to found out something iteresting"
#         }
#     ]
# )
# print(thred_id := thread.id)

asistant_id = "asst_2He8epGZ4PHaTCPlOL3lPDG0"
thread_id = "thread_SC8r0FWbkD4xAY6zBRQqZtYw" 

message = "What's the hottest news in the world"