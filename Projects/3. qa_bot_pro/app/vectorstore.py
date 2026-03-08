import sys
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


from langchain_community.vectorstores import FAISS
from .embeddings import get_embeddings
from .config import INDEX_DIR, DOCUMENTS_DIR
from .document_loaders import load_all_documents
from .chunking import get_text_splitter


def load_or_build_vectorstore(force_rebuild: bool = False):
    embeddings = get_embeddings()

    if INDEX_DIR.exists() and not force_rebuild:
        vs = FAISS.load_local(
            str(INDEX_DIR),
            embeddings,
            allow_dangerous_deserialization=True
        )
        return vs

    # Build new index
    raw_docs = load_all_documents(DOCUMENTS_DIR)
    if not raw_docs:
        raise ValueError(f"No documents found in {DOCUMENTS_DIR}")

    splitter = get_text_splitter()
    chunks = splitter.split_documents(raw_docs)

    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local(str(INDEX_DIR))

    return vectorstore