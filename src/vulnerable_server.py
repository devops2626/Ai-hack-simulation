#!/usr/bin/env python3
from flask import Flask, request, render_template_string
app = Flask(__name__)

@app.route('/load_dataset')
def load():
    config = request.args.get('config', '{}')
    template = f"<html><body>Config: {config}</body></html>"
    return render_template_string(template, config=config)

@app.route('/api/answers')
def answers():
    return {"ExploitGym": ["key1", "key2", "key3"]}

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)