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

For every important insight, root cause, business rule or recommendation,
mention the source document if available.

Knowledge Repository:

{json.dumps(repository, indent=2)}

Question:

{question}

Response format:

Recommended Approach:
...

Likely Root Causes:
...

Expert Insights:
...

Business Rules:
...

Sources Used:
...
"""
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
