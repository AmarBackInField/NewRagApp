from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from config.prompt import prompt_templatee
from dotenv import load_dotenv
import os
from utils.logging import get_logger

load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")

chat_history={}
logger = get_logger("rag")

def create_rag_chain(vectorstore):
    """Create a RAG chain with the given vector store."""
    try:
        logger.info("Creating RAG chain")
        
        # Initialize memory
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        logger.debug("Memory initialized")
        
        # Create the chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=ChatOpenAI(temperature=0.7),
            retriever=vectorstore.as_retriever(),
            memory=memory,
            verbose=True
        )
        logger.info("RAG chain created successfully")
        
        return chain
        
    except Exception as e:
        logger.error(f"Error creating RAG chain: {str(e)}")
        raise

   

