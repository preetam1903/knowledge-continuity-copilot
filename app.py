import streamlit as st



from ask_rajesh import ask_rajesh
from document_reader import read_document
from knowledge_agent import extract_knowledge
from rag_agent import ask_rag

st.set_page_config(
    page_title="Knowledge Continuity Copilot",
    layout="wide"
)

st.title("🧠 Knowledge Continuity Copilot")

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Knowledge Repository",
        "Knowledge Dashboard",
        "Ask Expert",
        "Ask RAG"
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
            raw_documents=[]

            with st.spinner(
                "Extracting knowledge from documents..."
            ):

                for uploaded_file in uploaded_files:

                    document_text = read_document(
                        uploaded_file
                    )
                    raw_documents.append(
                        document_text
                    )
                    knowledge = extract_knowledge(
                        document_text
                    )

                    repository.append({
                        "source_file": uploaded_file.name,
                        "knowledge": knowledge
                    })

            st.session_state["repository"] = repository
            st.session_state["raw_documents"] = raw_documents

            st.success(
                f"Repository built from {len(repository)} documents"
            )

            # Summary Metrics

            
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

with tab3:

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


with tab2:

    st.header("Knowledge Dashboard")

    if "repository" not in st.session_state:

        st.warning(
            "Build repository first"
        )

    else:

        repository = st.session_state["repository"]

        assets = set()
        failure_modes = set()
        root_causes = set()
        expert_insights = set()

        for item in repository:

            k = item["knowledge"]

            asset = k.get(
                "asset",
                ""
            )

            if asset:
                assets.add(asset)

            failure_modes.update(
                k.get(
                    "failure_modes",
                    []
                )
            )

            root_causes.update(
                k.get(
                    "root_causes",
                    []
                )
            )

            expert_insights.update(
                k.get(
                    "expert_insights",
                    []
                )
            )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Assets",
                len(assets)
            )

        with col2:
            st.metric(
                "Failure Modes",
                len(failure_modes)
            )

        with col3:
            st.metric(
                "Root Causes",
                len(root_causes)
            )

        with col4:
            st.metric(
                "Expert Insights",
                len(expert_insights)
            )

        st.subheader(
            "Assets"
        )

        for x in assets:
            st.write(
                "-",
                x
            )

        st.subheader(
            "Failure Modes"
        )

        for x in failure_modes:
            st.write(
                "-",
                x
            )

        st.subheader(
            "Root Causes"
        )

        for x in root_causes:
            st.write(
                "-",
                x
            )

        st.subheader(
            "Expert Insights"
        )

        for x in expert_insights:
            st.write(
                "-",
                x
            )

with tab4:

    st.header("Ask RAG")

    question = st.text_input(
        "Ask a question",
        key="rag_question"
    )

    if st.button(
        "Ask RAG"
    ):

        docs = st.session_state.get(
            "raw_documents",
            []
        )

        answer = ask_rag(
            question,
            docs
        )

        st.write(answer)



