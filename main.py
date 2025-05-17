from core.vstore import save_to_faiss
from core.data_ingestion import load_and_split_documents_from_directory
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
        chunks = load_and_split_documents_from_directory('data')
        logger.info(f"Successfully loaded and split documents into {len(chunks)} chunks")
        
        # Create vector store
        logger.info("Creating vector store")
        vstore = save_to_faiss(chunks)
        logger.info("Vector store created successfully")
        
        # Create RAG chain
        logger.info("Initializing RAG chain")
        rag_chain = create_rag_chain(vstore)
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
