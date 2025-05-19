import streamlit as st
from core.rag import create_rag_chain
from core.data_ingestion import ingest_documents
from core.vstore import store_documents_in_vectorstore, load_vectorstore
import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from config.prompt import intro_prompt
from pypdf.errors import EmptyFileError
import shutil

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# --- Helper Functions ---

def stream_output(text, container, delay=0.005):
    """Stream text output character by character in Streamlit."""
    streamed_text = ""
    for char in text:
        streamed_text += char
        container.markdown(streamed_text)
        time.sleep(delay)

def validate_files(files):
    """Validate uploaded files."""
    if not files:
        return False, "Please upload at least one file."
    
    for file in files:
        if file.size == 0:
            return False, f"Error: {file.name} is empty. Please upload a valid file."
        if file.type not in ["application/pdf", "text/plain"]:
            return False, f"Error: {file.name} is not a supported file type. Please upload PDF or TXT files only."
    
    return True, "Files validated successfully."

def save_uploaded_files(uploaded_files, upload_folder="uploaded_files"):
    """Save uploaded files and return their paths."""
    os.makedirs(upload_folder, exist_ok=True)

    # Clear folder if it has old files
    if os.listdir(upload_folder):
        for filename in os.listdir(upload_folder):
            file_path = os.path.join(upload_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    saved_paths = []
    for file in uploaded_files:
        file_path = os.path.join(upload_folder, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        saved_paths.append(file_path)

    return saved_paths


# --- Streamlit Setup ---

st.set_page_config(page_title="Chat with Documents", layout="wide")

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# --- Sidebar ---

with st.sidebar:
    st.title("📚 Doc Chatbot")
    uploaded_files = st.file_uploader("Upload PDFs or TXT files", type=["pdf", "txt"], accept_multiple_files=True)

    if st.button("Ingest & Index"):
        if uploaded_files:
            is_valid, message = validate_files(uploaded_files)
            if not is_valid:
                st.error(message)
            else:
                with st.spinner("Processing documents..."):
                    try:
                        saved_file_paths = save_uploaded_files(uploaded_files)
                        chunks = ingest_documents(saved_file_paths)

                        # Embed and store in vector DB
                        store_documents_in_vectorstore(chunks, index_path="faiss_index")

                        # Show example response
                        llm = ChatOpenAI(temperature=0.2, model="gpt-4", api_key=api_key)
                        chunk_text = "\n\n".join([c.page_content for c in chunks[:5]])
                        prompt = intro_prompt().format(chunks=chunk_text)
                        intro_message = llm.invoke(prompt).content
                        st.success(intro_message)

                        # Setup RAG Chain
                        st.session_state.vectorstore = load_vectorstore()
                        st.session_state.rag_chain = create_rag_chain(st.session_state.vectorstore)
                        st.success("Documents successfully indexed and ready for querying!")
                    
                    except EmptyFileError:
                        st.error("Error: One or more files are empty. Please check your files and try again.")
                    except Exception as e:
                        st.error(f"An error occurred while processing the documents: {str(e)}")
        else:
            st.warning("Please upload a file first.")

    st.markdown("---")
    st.markdown("**Instructions:**\n- Upload your docs\n- Ask questions\n- Get AI answers")


# --- Main Chat Interface ---

st.title("🤖 Ask Questions from Your Docs")

if not st.session_state.rag_chain:
    st.info("👉 Upload and ingest documents from the sidebar to start chatting.")
else:
    user_input = st.chat_input("Ask something about your document...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        
        with st.chat_message("assistant"):
            response_box = st.empty()
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.rag_chain.invoke({"question": user_input})
                    answer = response["answer"]
                    stream_output(answer, response_box)
                except Exception as e:
                    st.error(f"An error occurred while processing your question: {str(e)}")

        st.session_state.chat_history.append({"role": "assistant", "text": answer})

    # Display chat history
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            with st.chat_message("user"):
                st.markdown(entry["text"])
        else:
            with st.chat_message("assistant"):
                st.markdown(entry["text"])
