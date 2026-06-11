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

    st.header("Build Knowledge Repository")

    uploaded_files = st.file_uploader(
        "Upload Knowledge Documents",
        type=["txt", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.write(
            f"{len(uploaded_files)} document(s) selected"
        )

        if st.button("Build Knowledge Repository"):

            repository = []

            with st.spinner(
                "Extracting knowledge from documents..."
            ):

                for uploaded_file in uploaded_files:

                    document_text = read_document(
                        uploaded_file
                    )

                    knowledge = extract_knowledge(
                        document_text
                    )

                    repository.append({
                        "source_file": uploaded_file.name,
                        "knowledge": knowledge
                    })

            st.session_state["repository"] = repository

            st.success(
                f"Repository built from {len(repository)} documents"
            )

            # Summary Metrics

            systems = 0
            rules = 0
            insights = 0
            root_causes = 0

            for item in repository:

                k = item["knowledge"]

                systems += len(
                    k.get("systems", [])
                )

                rules += len(
                    k.get("business_rules", [])
                )

                insights += len(
                    k.get("expert_insights", [])
                )

                root_causes += len(
                    k.get("root_causes", [])
                )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Documents",
                    len(repository)
                )

            with col2:
                st.metric(
                    "Systems",
                    systems
                )

            with col3:
                st.metric(
                    "Business Rules",
                    rules
                )

            with col4:
                st.metric(
                    "Expert Insights",
                    insights
                )

            st.metric(
                "Root Causes",
                root_causes
            )

            st.subheader(
                "Knowledge Repository"
            )

            st.json(repository)

with tab2:

    st.header("Ask Rajesh")

    question = st.text_area(
        "Ask a question"
    )

    if st.button("Get Expert Advice"):

        if "repository" not in st.session_state:

            st.error(
                "Please build repository first"
            )

        else:

            answer = ask_rajesh(
                question,
                st.session_state["repository"]
            )

            st.write(answer)
