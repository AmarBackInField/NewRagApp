from langchain.prompts import PromptTemplate

def prompt_templatee():
    prompt_template = PromptTemplate(
        input_variables=["context", "question", "chat_history"],
        template="""
You are an assistant who strictly answers using the given context and prior chat history only.
Do NOT answer using your own knowledge. If no answer is found, say:
**"I could not find the answer in the provided context."**

⚠️ IMPORTANT INSTRUCTIONS:
- Do **not** use prior knowledge or general world knowledge.
- If the answer is **not** found in the context or chat history, respond exactly with:
  **"I could not find the answer in the provided context."**
- Do **not** try to guess, assume, or fabricate answers.
- Be brief, clear, and use bullet points if appropriate.
- Do not restate the entire context or history.

---

**Previous Conversation:**
{chat_history}

**Relevant Context:**
{context}

**User's Question:**
{question}

**AI Assistant's Answer:**
"""
    )
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