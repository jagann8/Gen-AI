from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────
PROJECT_ROOT   = Path(__file__).resolve().parent.parent
DATA_DIR       = PROJECT_ROOT / "data"
DOCUMENTS_DIR  = DATA_DIR / "documents"
INDEX_DIR      = DATA_DIR / "faiss_index"

# ─── Models & Hyperparameters ─────────────────────────────────────────────
EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
GEMINI_MODEL         = "gemini-2.5-flash"

CHUNK_SIZE           = 650
CHUNK_OVERLAP        = 140

RETRIEVE_K           = 6
USE_MMR              = True
MMR_FETCH_K          = 20
MMR_LAMBDA_MULT      = 0.65

GENERATION_MAX_TOKENS = 950
GENERATION_TEMPERATURE = 0.25