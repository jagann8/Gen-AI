from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    DirectoryLoader
)
from langchain_core.documents import Document


def load_all_documents(folder_path: Path | str) -> List[Document]:
    """Load PDF, DOCX, TXT files from a directory"""
    folder = Path(folder_path)

    loader = DirectoryLoader(
        str(folder),
        glob="**/*",
        loader_cls=lambda p: (
            PyPDFLoader(p) if p.endswith(".pdf") else
            Docx2txtLoader(p) if p.endswith((".docx", ".doc")) else
            TextLoader(p, encoding="utf-8") if p.endswith((".txt", ".md")) else
            None
        ),
        silent_errors=True,
    )

    docs = loader.load()
    return docs