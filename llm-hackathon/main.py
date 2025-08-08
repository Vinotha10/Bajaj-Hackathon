import threading
import os
import tempfile
import streamlit as st
from webhook_server import app as flask_app
from qa_engine import answer_question

# ----------- Streamlit Function -----------
def run_streamlit():
    # Define the Streamlit interface
    st.set_page_config(page_title="📄 Document Q&A", layout="centered")
    st.title("📄 Document Query Retrieval System")
    st.write("Upload a PDF and ask questions about it.")

    uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"])
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
                result = answer_question(tmp_path, question)
                st.success("Answer:")
                st.write(result["answers"][0])
            except Exception as e:
                st.error(f"Error: {str(e)}")
            finally:
                os.remove(tmp_path)

# ----------- Flask Server Function -----------
def run_flask():
    from waitress import serve
    serve(flask_app, host="0.0.0.0", port=5000)

# ----------- Start Both Threads -----------
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    streamlit_thread = threading.Thread(target=lambda: os.system("streamlit run main.py --server.port=8501 --server.address=0.0.0.0"))

    flask_thread.start()
    streamlit_thread.start()

    flask_thread.join()
    streamlit_thread.join()
