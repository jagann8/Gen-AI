
import sys
from pathlib import Path

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))


import streamlit as st
from app.vectorstore import load_or_build_vectorstore
from app.retrieval import get_retriever
from app.rag import generate_answer
from app.config import RETRIEVE_K

st.set_page_config(page_title="QA Bot • Gemini Flash", layout="wide")

st.title("Document Q&A")
st.caption("gemini-2.5-flash • FAISS • BAAI/bge-small-en-v1.5")

# Load once
if "vectorstore" not in st.session_state:
    with st.spinner("Loading / building vector store..."):
        st.session_state.vectorstore = load_or_build_vectorstore()

retriever = get_retriever(st.session_state.vectorstore, k=RETRIEVE_K)

query = st.chat_input("Ask anything about the documents...")

if query:
    st.chat_message("user").markdown(query)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            docs = retriever.invoke(query)

        context = "\n\n".join([d.page_content for d in docs])
        sources = [d.metadata.get("source", "unknown") for d in docs]

        with st.spinner("Thinking..."):
            answer = generate_answer(query, context)

        st.markdown(answer)

        with st.expander("Sources"):
            for i, src in enumerate(sources, 1):
                st.markdown(f"{i}. {src}")