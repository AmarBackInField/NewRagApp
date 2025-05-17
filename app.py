import streamlit as st
from core.rag import create_rag_chain
from core.data_ingestion import ingest_documents, load_vectorstore
import os
import time
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from config.prompt import intro_prompt
from pypdf.errors import EmptyFileError

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

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

st.set_page_config(page_title="Chat with Documents", layout="wide")

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

# Sidebar
with st.sidebar:
    st.title("📚 Doc Chatbot")

    uploaded_files = st.file_uploader("Upload PDFs or TXT files", type=["pdf", "txt"], accept_multiple_files=True)

    if st.button("Ingest & Index"):
        if uploaded_files:
            # Validate files before processing
            is_valid, message = validate_files(uploaded_files)
            if not is_valid:
                st.error(message)
            else:
                with st.spinner("Processing documents..."):
                    try:
                        chunks = ingest_documents(uploaded_files)  # Save & Index
                        # llm = ChatOpenAI(temperature=0.7, model="gpt-4", api_key=api_key)
                        llm = ChatOpenAI(temperature=0.7, model="gpt-4o-mini", api_key=api_key)
                        top_chunks = chunks[:5]
                        chunk_text = "\n\n".join([c.page_content for c in top_chunks])

                        # Format prompt
                        intro_promp=intro_prompt()
                        prompt = intro_promp.format(chunks=chunk_text)

                        # Generate intro message
                        intro_message = llm.invoke(prompt).content
                        st.success(intro_message)
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

# Main Chat Interface
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
