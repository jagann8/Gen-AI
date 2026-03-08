import sys
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


from langchain_community.vectorstores import FAISS
from .config import RETRIEVE_K, USE_MMR, MMR_FETCH_K, MMR_LAMBDA_MULT


def get_retriever(vectorstore: FAISS, k: int = None):
    k = k or RETRIEVE_K

    if USE_MMR:
        return vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": k,
                "fetch_k": MMR_FETCH_K,
                "lambda_mult": MMR_LAMBDA_MULT,
            }
        )
    else:
        return vectorstore.as_retriever(search_kwargs={"k": k})