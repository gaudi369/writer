# Pre Set Up
GOOGLE_API_KEY='AIzaSyDQzKErcqZncO59-jAQSeLmyUQl6VNhb1Y'

from google import genai
from google.genai import types
from google.genai.errors import ServerError

client = genai.Client(api_key=GOOGLE_API_KEY)

MODEL_ID = "gemini-2.0-flash-exp" 
THINKING = 'gemini-2.0-flash-thinking-exp-01-21'

for i, m in zip(range(5), genai.list_tuned_models()):
  print(m.name)

# name = ""
# genai.delete_tuned_model(f'tunedModels/{name}')