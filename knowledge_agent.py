import streamlit as st
from openai import OpenAI
import json

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)


KNOWLEDGE_PROMPT = """
You are a Manufacturing Knowledge Extraction Agent.

Analyze the manufacturing document and return ONLY valid JSON.

{
  "asset":"",
  "failure_modes":[],
  "symptoms":[],
  "root_causes":[],
  "corrective_actions":[],
  "preventive_actions":[],
  "operating_limits":[],
  "spare_parts":[],
  "inventory_rules":[],
  "expert_insights":[],
  "procedures":[],
  "safety_warnings":[]
}

Rules:

1. Extract equipment or asset names.
2. Extract failure modes.
3. Extract symptoms.
4. Extract root causes.
5. Extract corrective actions.
6. Extract preventive actions.
7. Extract operating limits and thresholds.
8. Extract spare parts.
9. Extract inventory rules.
10. Extract expert insights.
11. Extract procedures.
12. Extract safety warnings.
13. Do not invent values.
14. If information is missing return [].
15. Return ONLY JSON.
16. No markdown.
17. No explanations.

Examples:

Expert Insights:
- Always inspect lubrication first.
- 90 percent of vibration above 8 mm/s is caused by lubrication issues.
- Never replace roller before checking alignment.

Operating Limits:
- Vibration > 8 mm/s
- Temperature > 80°C

Symptoms:
- High vibration
- Abnormal noise
- Bearing temperature rise

Root Causes:
- Lubrication failure
- Bearing wear
- Misalignment

Corrective Actions:
- Inspect lubrication
- Replace bearing
- Verify alignment

Preventive Actions:
- Weekly lubrication inspection
- Monthly alignment check

Document:

{document}
"""



def extract_knowledge(document_text):

    prompt = KNOWLEDGE_PROMPT.replace(
        "{document}",
        document_text
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
            "asset": "",
            "failure_modes": [],
            "symptoms": [],
            "root_causes": [],
            "corrective_actions": [],
            "preventive_actions": [],
            "operating_limits": [],
            "spare_parts": [],
            "inventory_rules": [],
            "expert_insights": [],
            "procedures": [],
            "safety_warnings": [],
            "raw_response": result
        }

