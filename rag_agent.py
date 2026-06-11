
import streamlit as st
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def ask_rag(question, documents):

    context = "\n\n".join(documents)

    prompt = f"""
You are a manufacturing assistant.

Use ONLY the document content below.

Documents:

{context}

Question:

{question}

Answer using only the document information.
Mention document references when possible.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
