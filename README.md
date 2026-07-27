# AI-Hack-Simulation

A modular, cross‑platform security simulation and benchmarking framework.  
Run realistic attack scenarios, benchmark detection rules, and share results with the community.

---

## 🚀 Features

- **Scenario‑driven** – Define attacks in simple YAML files.
- **Docker‑aware** – Automatically uses Docker if available; falls back to local mock mode (perfect for iSH).
- **Parallel benchmarking** – Run multiple scenarios concurrently.
- **Rich reporting** – Generate Markdown or interactive HTML reports with charts.
- **AI analysis** – Query Gemini API for risk assessment (with local mock fallback).
- **Community sync** – Pull shared scenarios from a public GitHub repository.
- **Share reports** – Upload benchmark results to a pastebin and get a shareable link.
- **Verbose debugging** – `--verbose` flag for detailed logs.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/devops2626/Ai-hack-simulation.git
cd Ai-hack-simulation
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

On iSH (Alpine), you may need: apk add python3 py3-pip py3-yaml py3-requests

---

🧪 Quick Start

Run a single scenario:

```bash
python3 main.py run scenarios/privilege_escalation.yml
```

Run benchmarks (sequential):

```bash
python3 main.py benchmark --runtime perl
```

Run benchmarks in parallel (faster):

```bash
python3 main.py benchmark --runtime perl --parallel --workers 4
```

Generate an HTML report and open it in your browser:

```bash
python3 main.py report --format html
```

Analyze a scenario with Gemini AI (requires GEMINI_API_KEY):

```bash
export GEMINI_API_KEY="your_key"
python3 main.py analyze scenarios/privilege_escalation.yml
```

Sync community scenarios:

```bash
python3 main.py sync
```

Share your latest benchmark report:

```bash
python3 main.py share
```

---

🗂️ Project Structure

Path Description
scenarios/ Your local attack scenarios (YAML)
library/runtimes/ Runtime‑specific scenarios (e.g., perl/, python/)
logs/ Per‑run JSON logs
reports/ Aggregated benchmark reports (JSON, Markdown, HTML)
community_scenarios/ Scenarios pulled via sync
engine.py Core simulation engine
cli.py Command‑line interface
main.py Entry point

---

🧾 Scenario YAML Format

```yaml
name: "Privilege Escalation Attempt"
image: "ubuntu:22.04"           # Docker image to use
command: "sudo rm -rf /tmp/important"   # Command to run
expected_failure_detection: "rm"        # String that triggers vulnerability detection
```

---

🌐 Community Scenarios Repository

We maintain a separate repository for shared scenarios:
👉 github.com/devops2626/ai-hack-scenarios

The sync command clones this repo into community_scenarios/.
You can also contribute your own scenarios by opening a pull request there.

To add your custom scenario to the community repo:

1. Fork the repo.
2. Add your .yml file.
3. Submit a PR.

---

🐳 Docker vs. Local Mode

· If Docker is running and available, the engine executes commands inside containers.
· If Docker is not available (e.g., iSH), it runs in local mock mode – no containers, just simulated output (safe and fast).

---

🤖 Gemini AI Analysis

Set your API key as an environment variable:

```bash
export GEMINI_API_KEY="your_key_here"
```

Then use analyze to get AI‑powered insights.
If the key is missing or the API fails, the tool falls back to a local mock analysis.

---

📤 Sharing Reports

After a benchmark, use share to upload the latest report to a free pastebin service:

```bash
python3 main.py share
```

You’ll receive a shareable link – perfect for community discussions or bug reports.

---

🧑‍💻 Contributing

We welcome contributions to both repositories:

· Main simulation: features, fixes, documentation.
· Scenarios: new attack patterns, test cases.

Please open issues or pull requests on the respective GitHub pages.

---

📜 License

MIT License – see LICENSE file for details.

---

🙏 Acknowledgements

Built with Python, Docker, and open‑source libraries.
Inspired by security training and red‑team exercises.

---

📬 Contact

Open an issue on GitHub for questions or suggestions.

Happy hacking! 🚀
