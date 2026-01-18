import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="📄 Document QA Assistant",
    layout="centered"
)

st.title("📄 Document QA Assistant")
st.caption("Ask questions from your uploaded document")

# Session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# Upload Section
# -------------------------------
st.subheader("Upload Document")

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

if uploaded_file:
    if st.button("📤 Upload & Process"):
        with st.spinner("Processing document..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post(
                f"{BACKEND_URL}/upload",
                files={"file": uploaded_file}
            )

        if response.status_code == 200:
            st.success("✅ Document uploaded and indexed successfully!")
        else:
            st.error("❌ Failed to upload document")

st.divider()

# -------------------------------
# Chat Section
# -------------------------------
st.subheader("Ask Questions")

query = st.text_input("Enter your question")

if st.button("💬 Ask"):
    if query.strip() == "":
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            response = requests.post(
                f"{BACKEND_URL}/ask",
                params={"query": query}
            )

        answer = response.json()["answer"]

        st.session_state.chat_history.append(
            ("You", query)
        )
        st.session_state.chat_history.append(
            ("Bot", answer)
        )

# -------------------------------
# Chat History Display
# -------------------------------
st.divider()
st.subheader("Conversation")

for speaker, message in st.session_state.chat_history:
    if speaker == "You":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")




## http://localhost:8501
## streamlit run ui/app.py
## uvicorn app.main:app --reload