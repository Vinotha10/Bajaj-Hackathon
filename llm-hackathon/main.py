import streamlit as st
import tempfile
import os
from qa_engine import answer_question

st.set_page_config(page_title="📄 Document Q&A", layout="centered")

st.title("📄 Document Query Retrieval System")
st.write("Upload a PDF and ask questions about it.")

# File upload
uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])

# Question input
question = st.text_input("Ask a question about the document")

if st.button("Get Answer"):
    if uploaded_file is None:
        st.warning("Please upload a document first.")
    elif question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        
        try:
            # Call your existing backend logic
            result = answer_question(tmp_path, question)
            st.success("Answer:")
            st.write(result["answers"][0])
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            os.remove(tmp_path)
