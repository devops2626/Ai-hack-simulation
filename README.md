# 🤖 AI Hack Simulation

A lightweight, interactive CLI game built in Python that runs perfectly on iSH (Alpine Linux). 
Choose your hacker specialty, receive a unique random mission, and track your agent's stats on the leaderboard!

## 🚀 Quick Start

Make sure you have Python 3 installed:
```bash
apk add python3
```

Run the game:

```bash
python3 ai_hack_cli.py
```

Or use the shortcut:

```bash
make start
```

🎮 Features

· 8 unique hacker specialties (from Tech Enthusiast to AI Artist)
· Dynamic mission generator with 3 random scenarios per specialty
· Persistent user database (users.json) tracking mission counts
· Built-in leaderboard to rank agents

📂 File Structure

· ai_hack_cli.py – Main game logic
· hobbies.json – Template definitions
· hobby_manager.py – Standalone backend helper
· Makefile – Launch shortcut
· users.json – Local user stats (gitignored)

🐧 Running on iSH (iPhone)

Since iSH uses Alpine Linux, packages are installed via apk.
No JIT required — this script runs fast on pure Python.

---

Built with ❤️ by devops2626


## 🎙️ Easter Egg: Jarvis Voice
Type **`Jarvis`** as your agent codename to unlock a special voice greeting. 
The AI will acknowledge your presence and activate **VOICE MODE**, giving you a tactical analysis before the mission begins. 
