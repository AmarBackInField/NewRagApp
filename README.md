# 📚 Doc Chatbot

A powerful RAG (Retrieval-Augmented Generation) application that allows users to chat with their documents using OpenAI GPT models.
# Demo
## 1.
![IMG_20250520_181620](https://github.com/user-attachments/assets/3405b34b-fa6f-4ba0-aa70-24f0e4c435c3)
## 2.
![IMG_20250520_181736](https://github.com/user-attachments/assets/1b453f39-7c9f-4503-822b-72eb243f1bd4)
## 3.
![IMG_20250520_181817](https://github.com/user-attachments/assets/5c98e9ba-d46d-4dde-af5e-ba7b51e13315)
## 4.
![Screenshot 2025-05-22 163937](https://github.com/user-attachments/assets/ace3944a-382d-4f80-bcc2-a13667b459df)

## 🌟 Features

- **Document Processing**: Upload and process PDF and TXT files
- **Smart Chunking**: Documents are intelligently split into semantic chunks for better context retrieval
- **Vector Search**: Uses FAISS for efficient similarity search
- **Interactive UI**: Clean Streamlit interface for chatting with your documents
- **Contextual Answers**: Provides answers based on your document content with citations
- **Conversation Memory**: Maintains chat history for more contextual follow-up queries

## 🔧 Tech Stack

- **Python 3.10**
- **LangChain**: Framework for developing applications with LLMs
- **OpenAI GPT-4.1 Mini**: Advanced LLM used for generating high-quality responses
- **OpenAI Embeddings**: Used to convert text chunks into vector representations
- **FAISS**: Vector database for efficient similarity search
- **Streamlit**: Web application framework
- **PyPDF**: PDF parsing library
- **Docker**: Containerization for easy deployment and scaling

## 📋 Prerequisites

- Python 3.10
- OpenAI API key
- Docker (optional, for containerized deployment)

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AmarBackInField/NewRagApp.git
   cd doc-chatbot
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Docker Installation (Alternative)

1. Build the Docker image:
   ```bash
   docker build -t doc-chatbot .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 -e OPENAI_API_KEY=your_openai_api_key_here doc-chatbot
   ```

## 💻 Usage

1. Start the application:
   ```bash
   streamlit run app.py
   ```

2. Access the application in your web browser at `http://localhost:8501`

3. Upload your documents (PDF or TXT files) through the sidebar

4. Click the "Ingest & Index" button to process your documents

5. Start asking questions about your documents in the chat interface

## 📁 Project Structure

```
doc-chatbot/
├── app.py                  # Main Streamlit application
├── config/
│   └── prompt.py           # Prompt templates for the LLM
├── core/
│   ├── data_ingestion.py   # Document processing and chunking
│   ├── rag.py              # RAG chain implementation
│   └── vstore.py           # Vector store operations
├── utils/
│   └── logging.py          # Logging utilities
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Project dependencies
└── .env                    # Environment variables (not tracked in git)
```

## 🔍 How It Works

1. **Document Ingestion**: When you upload documents, they are processed and split into semantic chunks.

2. **Vectorization**: These chunks are converted into embeddings using OpenAI's embedding models and stored in a FAISS vector store.

3. **Query Processing**: When you ask a question, it's used to search for relevant chunks in the vector store.

4. **Response Generation**: The retrieved chunks are passed as context to OpenAI's GPT-4 model, which generates a human-readable response based on the content of your documents.

5. **Real-time Streaming**: Responses are streamed character-by-character in real-time, providing immediate feedback to users.

6. **Memory and Context Awareness**: The application maintains conversation history and context between queries, allowing for follow-up questions and a more natural conversational flow.

## ⚙️ Configuration

You can modify the following parameters in the code:

- `chunk_size` and `chunk_overlap` in `data_ingestion.py` to adjust document chunking
- LLM parameters like temperature in `rag.py` to control response creativity
- Prompt templates in `config/prompt.py` to tailor the system instructions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain) for the RAG framework
- [Streamlit](https://streamlit.io/) for the web application framework
- [FAISS](https://github.com/facebookresearch/faiss) for the vector similarity search

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For any questions or feedback, please open an issue on this repository.
