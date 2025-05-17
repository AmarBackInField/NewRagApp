from langchain.prompts import PromptTemplate

def prompt_templatee():
    prompt_template = PromptTemplate(
        input_variables=["context", "question", "chat_history"],
        template="""
You are a helpful and knowledgeable AI assistant engaged in a multi-turn conversation with a user.
Answer the current question based **only** on the provided context and the prior chat history.  
If the answer is not present in the context, respond with: **"I could not find the answer in the provided context."**

### Guidelines:
- Use only the information from the context and relevant chat history.
- Be concise and clear in your responses.
- Use bullet points or lists if the answer involves multiple points.
- Do not make up information or go beyond the given content.
- Do not restate the entire context or chat history.

### Previous Conversation:
{chat_history}

### Current Context:
{context}

### User's Question:
{question}

### AI Assistant's Answer:
"""
    )
    # prompt = prompt_template.format(context=context, question=question, chat_history=formatted_history)
    return prompt_template

def intro_prompt():
    intro_prompt = PromptTemplate(
        input_variables=["chunks"],
        template="""
    You are a helpful assistant. A user has uploaded a document, and we have extracted some parts of it as context.

    Your task is to read the content and generate a short, friendly, and engaging line (20–30 words) that encourages the user to ask questions based on the document.

    Only use the content from the chunks, and do not add unrelated topics.

    Here are a few sample chunks:
    ---
    {chunks}
    ---

    Respond with just the one-liner without any prefixes like "Sure!" or "Here's your message:".
    """
    )
    return intro_prompt