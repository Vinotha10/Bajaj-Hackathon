from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/v1/hackrx/run', methods=['POST'])
def webhook():
    data = request.get_json()
    prompt = data.get("prompt", "")
    
    # Replace with actual LLM call if needed
    return jsonify({"response": f"You sent: {prompt}"})
