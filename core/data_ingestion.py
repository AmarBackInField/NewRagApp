from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.logging import get_logger
import tempfile
import os

logger = get_logger("data_ingestion")

def ingest_documents(files):
    """Process and chunk uploaded documents."""
    logger.info("Starting document ingestion process")
    documents = []
    
    for file in files:
        try:
            logger.debug(f"Processing file: {file.name}")
            if file.type == "application/pdf":
                loader = PyPDFLoader(file)
            elif file.type == "text/plain":
                loader = TextLoader(file)
            else:
                logger.warning(f"Unsupported file type: {file.type}")
                continue
                
            documents.extend(loader.load())
            logger.info(f"Successfully loaded {file.name}")
            
        except Exception as e:
            logger.error(f"Error processing {file.name}: {str(e)}")
            raise
    
    logger.info(f"Total documents loaded: {len(documents)}")
    
    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Documents split into {len(chunks)} chunks")
    
    return chunks

def load_vectorstore(index_path="faiss_index"):
    """Load the vector store from disk."""
    try:
        logger.info("Loading vector store from disk")
        embeddings = OpenAIEmbeddings()
        return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        logger.error(f"Error loading vector store: {str(e)}")
        raise
