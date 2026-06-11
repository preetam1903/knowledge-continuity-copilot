import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def ask_rajesh(question, repository):

    prompt = f"""
You are Rajesh, a senior SAP, MES and Production Reporting expert.

Use ONLY the knowledge repository provided.

Knowledge Repository:

{json.dumps(repository, indent=2)}

Question:

{question}

Provide:

1. Recommended Approach
2. Likely Root Causes
3. Expert Insights
4. Relevant Business Rules

Answer like an experienced support expert.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
