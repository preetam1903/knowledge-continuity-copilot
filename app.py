import streamlit as st

from document_reader import read_document
from knowledge_agent import extract_knowledge

st.set_page_config(
    page_title="Knowledge Continuity Copilot",
    layout="wide"
)

st.title("🧠 Knowledge Continuity Copilot")

tab1, tab2 = st.tabs(
    [
        "Knowledge Extraction",
        "Ask Rajesh"
    ]
)

with tab1:

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["txt","docx"]
    )

    if uploaded_file:

        document_text = read_document(uploaded_file)

        if st.button("Extract Knowledge"):

            result = extract_knowledge(document_text)

            st.json(result)

with tab2:

    st.write("Coming Soon")
