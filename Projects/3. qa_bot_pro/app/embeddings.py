import sys
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


from langchain_community.embeddings import HuggingFaceEmbeddings
from .config import EMBEDDING_MODEL_NAME


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},          # change to "cuda" if GPU available
        encode_kwargs={"normalize_embeddings": True},
    )