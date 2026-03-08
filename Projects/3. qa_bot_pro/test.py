# test.py — Correct version for google-genai SDK

import os
from dotenv import load_dotenv

from google import genai
from google.genai import types  # for generation config if needed

# Load .env file (if you're using one)
load_dotenv()

# The new SDK automatically uses GEMINI_API_KEY or GOOGLE_API_KEY from env
# No configure() call needed

# Create a client (this is the main entry point now)
client = genai.Client()

# Create the model using the client
model = client.models.generate_model(
    model="gemini-2.5-flash"          # or "gemini-2.5-flash-001", "gemini-2.5-pro", etc.
    # Optional: generation_config=types.GenerationConfig(temperature=0.7, max_output_tokens=500)
)

# Generate content
response = model.generate_content("Say hello world")

print("Response:")
print(response.text.strip())