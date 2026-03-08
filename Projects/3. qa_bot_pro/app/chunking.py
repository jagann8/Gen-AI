import sys
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


from langchain_text_splitters import RecursiveCharacterTextSplitter
from .config import CHUNK_SIZE, CHUNK_OVERLAP


def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
        add_start_index=True,  # useful for later source highlighting
    )