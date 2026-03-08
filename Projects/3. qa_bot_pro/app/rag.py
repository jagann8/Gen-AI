import sys
import os
from pathlib import Path
from dotenv import load_dotenv  # Needed to load .env variables
from google import genai

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

# Load configurations from your local config file
from .config import GEMINI_MODEL, GENERATION_MAX_TOKENS, GENERATION_TEMPERATURE

# 1. Load the .env file
load_dotenv()

# 2. Get the API key and handle the missing key error gracefully
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Ensure it is defined in your .env file.")

# 3. Initialize the Client (Modern SDK 2.0 approach)
client = genai.Client(api_key=api_key)

def build_prompt(query: str, context: str) -> str:
    """Constructs the grounding prompt for the RAG system."""
    return f"""You are a precise, factual assistant that answers questions using **only** the provided context.
Do NOT use external knowledge.
Do NOT make up information.
If the context does not contain enough information, reply exactly: "I don't have sufficient information in the documents to answer this."

Context:
{context}

Question: {query}

Answer concisely and directly:"""


def generate_answer(query: str, context: str) -> str:
    """Generates a response from Gemini based on the provided context."""
    prompt = build_prompt(query, context)

    # 4. Use the updated generate_content method
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            'temperature': GENERATION_TEMPERATURE,
            'max_output_tokens': GENERATION_MAX_TOKENS,
        }
    )

    return response.text.strip()