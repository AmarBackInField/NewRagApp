from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from utils.logging import get_logger
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
logger = get_logger("vstore")

def store_documents_in_vectorstore(chunks, index_path="faiss_index"):
    """Embed chunks and store them in FAISS vector store."""
    try:
        logger.info("Creating vector store with OpenAIEmbeddings")
        embeddings = OpenAIEmbeddings(api_key=api_key)
        vectorstore = FAISS.from_documents(chunks, embeddings)

        logger.info(f"Saving vector store to path: {index_path}")
        
        # Create or clear the index path
        os.makedirs(index_path, exist_ok=True)
        for filename in os.listdir(index_path):
            file_path = os.path.join(index_path, filename)
            try:
                os.remove(file_path)
                logger.info(f"Removed existing file: {file_path}")
            except Exception as e:
                logger.error(f"Error removing file {file_path}: {str(e)}")

        # Save vectorstore to disk
        vectorstore.save_local(index_path)
        logger.info("Vector store saved successfully")

    except Exception as e:
        logger.error(f"Error saving vector store: {str(e)}")
        raise

def load_vectorstore(index_path="faiss_index"):
    """Load the vector store from disk."""
    try:
        logger.info("Loading vector store from disk")
        embeddings = OpenAIEmbeddings()
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        logger.error(f"Error loading vector store: {str(e)}")
        raise
