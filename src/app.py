from flask import Flask, jsonify
from src.agent import AIHackerAgent
import io
import contextlib

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "project": "AI Hacking Simulator",
        "status": "ready",
        "endpoints": {
            "/api/run-simulation": "POST - Executes the agentic CTF simulation"
        }
    })

@app.route('/api/run-simulation', methods=['POST'])
def run_simulation():
    agent = AIHackerAgent()
    
    # Capture the print() outputs from your agent into a string
    with contextlib.redirect_stdout(io.StringIO()) as f:
        agent.run()
        output = f.getvalue()
    
    return jsonify({
        "status": "completed",
        "logs": output
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)