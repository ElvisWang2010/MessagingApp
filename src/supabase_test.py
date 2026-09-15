import os

from dotenv import load_dotenv
from supabase import create_client


load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

print("URL:", url)
print("Key loaded:", key is not None)

supabase = create_client(url, key)

print("Connected to Supabase!")


message = {
    "sender": "Elvis",
    "content": "Hello from Python!"
}

response = supabase.table("messages").insert(message).execute()

print("Message sent!")
print(response.data)