#!/usr/bin/env python3
import os
import glob
from flask import Flask, render_template_string, request, jsonify
from agent import AIHackerAgent
import io
import contextlib

app = Flask(__name__)

def get_scenarios():
    """Return a list of scenario filenames from the examples/ folder."""
    files = glob.glob("examples/*.yaml")
    return [os.path.basename(f) for f in files]

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Hacking Simulator</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, sans-serif; background: #0f0f0f; color: #e0e0e0; padding: 20px; max-width: 800px; margin: 0 auto; }
        h1 { color: #00ffcc; text-align: center; }
        .container { background: #1e1e1e; border-radius: 12px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.5); }
        #logs { background: #000; color: #00ff00; padding: 15px; border-radius: 8px; font-family: 'Courier New', Courier, monospace; white-space: pre-wrap; word-wrap: break-word; min-height: 200px; max-height: 400px; overflow-y: auto; border: 1px solid #333; margin-top: 10px; }
        select, button { background: #00ffcc; color: #000; border: none; padding: 15px; font-size: 18px; font-weight: bold; border-radius: 50px; cursor: pointer; width: 100%; margin-top: 10px; }
        select { background: #2a2a2a; color: #e0e0e0; }
        button:disabled { background: #555; color: #888; cursor: not-allowed; }
        .status { font-size: 14px; text-align: center; color: #888; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 AI Hacking Simulator</h1>
        <label for="scenario">Choose Scenario:</label>
        <select id="scenario">
            {% for file in scenario_files %}
            <option value="{{ file }}">{{ file }}</option>
            {% endfor %}
        </select>
        <div id="logs">Select a scenario and click "Run Simulation" to start the attack chain...</div>
        <button id="runBtn" onclick="runSimulation()">▶ Run Simulation</button>
        <div class="status" id="status">Ready</div>
    </div>

    <script>
        async function runSimulation() {
            const btn = document.getElementById('runBtn');
            const logs = document.getElementById('logs');
            const status = document.getElementById('status');
            const scenario = document.getElementById('scenario').value;

            btn.disabled = true;
            btn.innerText = "⏳ Running...";
            status.innerText = "Running " + scenario + "...";
            logs.innerText = "Waiting for agent to respond...\\n";

            try {
                const response = await fetch('/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ scenario: scenario })
                });
                const data = await response.json();
                logs.innerText = data.logs;
                status.innerText = "✅ Completed";
            } catch (error) {
                logs.innerText = "❌ Error: " + error;
                status.innerText = "❌ Error";
            } finally {
                btn.disabled = false;
                btn.innerText = "▶ Run Simulation";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE, scenario_files=get_scenarios())

@app.route('/run', methods=['POST'])
def run_agent():
    data = request.get_json()
    scenario_file = data.get('scenario', 'basic_attack.yaml')
    # Ensure the file exists in examples/ to avoid path traversal
    if not os.path.exists(f"examples/{scenario_file}"):
        return jsonify({"logs": f"❌ Error: Scenario '{scenario_file}' not found."})
    
    agent = AIHackerAgent(scenario_path=f"examples/{scenario_file}")
    with contextlib.redirect_stdout(io.StringIO()) as f:
        agent.run()
    output = f.getvalue()
    
    return jsonify({"logs": output})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
