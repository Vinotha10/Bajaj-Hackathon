import threading
import os
from webhook_server import app as flask_app

def run_streamlit():
    os.system("streamlit run main_app.py --server.port=8501 --server.address=0.0.0.0")

def run_flask():
    from waitress import serve
    serve(flask_app, host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_streamlit).start()
    threading.Thread(target=run_flask).start()
