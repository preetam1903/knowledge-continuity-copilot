import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

KNOWLEDGE_PROMPT = """
You are an Enterprise Knowledge Extraction Agent.

Analyze the document and return ONLY valid JSON.

{{
  "artifact_type":"",
  "summary":"",
  "systems":[],
  "tables":[],
  "business_rules":[],
  "issues":[],
  "root_causes":[],
  "troubleshooting_steps":[],
  "expert_insights":[],
  "lessons_learned":[],
  "corrective_actions":[]
}}

Rules:

1. Extract systems explicitly mentioned.
2. Extract table names explicitly mentioned.
3. Extract business rules.
4. Extract issues and root causes.
5. Extract troubleshooting steps.
6. Extract lessons learned.
7. Do not invent values.
8. If information is missing return [].

Expert Insights include:
- Rules of thumb
- Experience-based observations
- Lessons learned
- Statements such as:
  - "90% of incidents are caused by..."
  - "Always check..."
  - "The first thing I check..."
  - "In my experience..."
  - "Never compare..."
- Recommendations from senior experts

Return ONLY JSON.
Do not include markdown.
Do not include explanations.

Document:

{document}
"""

def extract_knowledge(document_text):

    prompt = KNOWLEDGE_PROMPT.format(
        document=document_text
    )

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

    result = response.choices[0].message.content

    try:
        return json.loads(result)

    except Exception:

        return {
            "artifact_type": "",
            "summary": "JSON Parsing Error",
            "systems": [],
            "tables": [],
            "business_rules": [],
            "issues": [],
            "root_causes": [],
            "troubleshooting_steps": [],
            "expert_insights": [],
            "lessons_learned": [],
            "corrective_actions": [],
            "raw_response": result
        }
