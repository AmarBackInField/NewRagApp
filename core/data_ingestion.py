from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.logging import get_logger
import tempfile
import os

logger = get_logger("data_ingestion")


def ingest_documents(file_paths):
    """Process and chunk documents from file paths."""
    logger.info("Starting document ingestion process")
    documents = []

    for path in file_paths:
        try:
            logger.debug(f"Processing file: {path}")
            ext = os.path.splitext(path)[1].lower()
            
            if ext == ".pdf":
                loader = PyPDFLoader(path)
            elif ext == ".txt":
                loader = TextLoader(path)
            else:
                logger.warning(f"Unsupported file type: {ext}")
                continue

            documents.extend(loader.load())
            logger.info(f"Successfully loaded {path}")

        except Exception as e:
            logger.error(f"Error processing {path}: {str(e)}")
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


