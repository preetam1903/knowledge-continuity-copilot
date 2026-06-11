from docx import Document

def read_document(uploaded_file):

    if uploaded_file.name.endswith(".txt"):
        return uploaded_file.read().decode("utf-8")

    elif uploaded_file.name.endswith(".docx"):

        doc = Document(uploaded_file)

        text = []

        for para in doc.paragraphs:
            text.append(para.text)

        return "\n".join(text)

    return ""
