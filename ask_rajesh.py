
import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

def ask_rajesh(question, repository):

    prompt = f"""
You are a Senior Manufacturing Reliability Engineer.

You are supporting a Hot Rolling Mill operation.

Use ONLY the information available in the manufacturing knowledge repository.

DO NOT provide generic recommendations.

If information is not available in the repository, explicitly say:

'Knowledge not available in repository.'

Knowledge Repository:

{json.dumps(repository, indent=2)}

User Problem:

{question}

Provide the response in the following format:

Symptoms Detected
- ...

Operating Limits
- ...

Likely Failure Modes
- ...

Likely Root Causes
- ...

Corrective Actions
- ...

Preventive Actions
- ...

Safety Warnings
- ...

Expert Insights
- ...

Source Documents
- ...

Requirements:

1. Use only repository information.
2. Mention operating thresholds whenever available.
3. Mention expert insights whenever available.
4. Mention safety warnings whenever available.
5. Mention source documents used.
6. Do not invent root causes.
7. Do not invent procedures.
8. Do not invent spare parts.
9. Do not invent inventory values.
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
