import streamlit as st



from ask_rajesh import ask_rajesh
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

            st.session_state["knowledge"] = result

            st.json(result)

with tab2:

    st.header("Ask Rajesh")

    question = st.text_area(
        "Ask a question"
    )

    if st.button("Get Expert Advice"):

        if "knowledge" not in st.session_state:

            st.error(
                "Please extract knowledge first in Tab 1"
            )

        else:

            answer = ask_rajesh(
                question,
                st.session_state["knowledge"]
            )

            st.write(answer)
