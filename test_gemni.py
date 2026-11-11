import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not api_key:
    print("ERROR: API key not loaded")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=model,
            contents="Say hello to CAREERVERSE in one sentence."
        )

        print("GEMINI CONNECTED!")
        print(response.text)

    except Exception as error:
        print("GEMINI ERROR:", type(error).__name__)
        print(error)