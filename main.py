from core.data_ingestion import ingest_documents
from core.vstore import store_documents_in_vectorstore, load_vectorstore
from core.rag import create_rag_chain
from utils.logging import get_logger
import sys

# Initialize logger
logger = get_logger("main")

def main():
    try:
        logger.info("Starting document processing")
        
        # Load and split documents
        logger.info("Loading documents from 'data' directory")
        chunks = ingest_documents('data')
        logger.info(f"Successfully loaded and split documents into {len(chunks)} chunks")
        
        # Create vector store
        logger.info("Creating vector store")
        store_documents_in_vectorstore(chunks, index_path="faiss_index")
        logger.info("Vector store created successfully")
        
        # Create RAG chain
        logger.info("Initializing RAG chain")
        vectorstore = load_vectorstore()
        rag_chain = create_rag_chain(vectorstore)
        logger.info("RAG chain initialized successfully")
        
        # Interactive query loop
        logger.info("Starting interactive query session")
        while True:
            try:
                query = input("\nAsk a question (or type 'exit'): ")
                if query.lower() == "exit":
                    logger.info("User requested exit")
                    break
                
                logger.debug(f"Processing query: {query}")
                response = rag_chain(query)
                print("\nResponse:\n", response['answer'])
                logger.debug("Response generated successfully")
                
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}")
                print("\nAn error occurred while processing your question. Please try again.")
                
    except Exception as e:
        logger.critical(f"Critical error in main execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
