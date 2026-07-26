import json
import random
import os
import datetime

HOBBY_FILE = 'hobbies.json'
USER_FILE = 'users.json'
SESSION_LOG_FILE = 'session_logs.jsonl'

# Load hobbies
try:
    with open(HOBBY_FILE, 'r') as f:
        data = json.load(f)
    templates = data['templates']
except FileNotFoundError:
    print("❌ Error: hobbies.json not found! Run git pull again.")
    exit(1)

# Expanded mission lists (3 per hobby)
MISSIONS = {
    1: [
        "Infiltrate the corporate mainframe using a Python backdoor. Evade IDS by mimicking legitimate traffic.",
        "Reverse-engineer a proprietary API to extract hidden user data without leaving a trace.",
        "Write a polymorphic worm that changes its signature every 5 seconds to fool antivirus engines."
    ],
    2: [
        "Build a drone-mounted thermal scanner from scratch. 3D print the casing and wire the electronics.",
        "Create a custom VR glove that translates hand gestures into machine code signals.",
        "Hack a 3D printer's firmware to print a functional lockpick that bypasses all electronic doors."
    ],
    3: [
        "Decrypt the intercepted military-grade cipher using brute-force CRC collisions.",
        "Find a zero-day vulnerability in the core network stack and exploit it to gain root access.",
        "Map the darknet infrastructure using a network of hidden relays and sniff out the adversary's IP."
    ],
    4: [
        "Analyze 10 terabytes of leaked user logs to find the anomaly using PCA and clustering.",
        "Predict the exact timing of the next market crash using time-series analysis and fractal math.",
        "Visualize the spread of a digital pandemic using epidemiological models and real-time data."
    ],
    5: [
        "Spin up a 50-node Kubernetes cluster on the fly to DDoS a rogue AI.",
        "Auto-scale a serverless function to handle 1 million simultaneous API requests.",
        "Migrate the entire legacy monolith to a microservices architecture without downtime."
    ],
    6: [
        "Reverse engineer the simulation engine and inject a custom shader to make enemies explode into pixel art.",
        "Create a procedural roguelike dungeon generator that adapts to the player's skill level.",
        "Mod the FPS engine to give the player bullet-time and super-jump abilities."
    ],
    7: [
        "Synthesize a new neural interface using bio-hacked wearables to monitor brain waves.",
        "Edit the DNA of a simulated organism to make it bioluminescent and trackable.",
        "Build a cyborg exoskeleton that translates muscle twitches into keystrokes."
    ],
    8: [
        "Generate a deepfake audio decoy of the CEO's voice to issue false orders.",
        "Create a generative AI art installation that morphs based on live weather data.",
        "Compose a symphony using AI-generated audio synthesis that disrupts enemy sonar."
    ]
}

def log_session(username, hobby_id, hobby_name, mission):
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "username": username,
        "hobby_id": hobby_id,
        "hobby_name": hobby_name,
        "mission": mission
    }
    with open(SESSION_LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def print_leaderboard():
    print("\n" + "=" * 45)
    print("🏆 AGENT LEADERBOARD 🏆")
    print("=" * 45)
    if not os.path.exists(USER_FILE):
        print("No agents have played yet.")
        return
    with open(USER_FILE, 'r') as f:
        users = json.load(f)
    sorted_agents = sorted(users.items(), key=lambda x: x[1].get('missions_completed', 0), reverse=True)
    for idx, (agent, stats) in enumerate(sorted_agents[:10], 1):
        missions = stats.get('missions_completed', 0)
        print(f"{idx}. {agent} — {missions} mission{'s' if missions != 1 else ''}")
    print("=" * 45)

# --- JARVIS COMMAND CENTER (Integrated) ---
def handle_jarvis_command(cmd):
    parts = cmd.strip().split()
    if not parts:
        return "I'm listening, sir. Type 'profile <name>' or 'stats'."
    
    if parts[0] == "stats":
        if not os.path.exists(SESSION_LOG_FILE):
            return "No mission logs found yet, sir. Run a simulation first."
        with open(SESSION_LOG_FILE, 'r') as f:
            lines = [line for line in f if line.strip()]
        agents = set()
        for line in lines:
            try:
                data = json.loads(line)
                agents.add(data['username'])
            except:
                pass
        return f"System Report: {len(lines)} total missions logged across {len(agents)} active agents. Roster: {', '.join(agents)}"
    
    elif parts[0] == "profile" and len(parts) > 1:
        target = parts[1]
        if not os.path.exists(SESSION_LOG_FILE):
            return f"I have no data on {target}, sir."
        with open(SESSION_LOG_FILE, 'r') as f:
            sessions = [json.loads(line) for line in f if line.strip()]
        user_sessions = [s for s in sessions if s['username'].lower() == target.lower()]
        if not user_sessions:
            return f"I have no data on {target}, sir."
        total = len(user_sessions)
        hobbies = [s['hobby_name'] for s in user_sessions]
        fav_hobby = max(set(hobbies), key=hobbies.count) if hobbies else "None"
        return f"Profile for {target}: {total} tracked sessions. Favorite speciality: {fav_hobby}."
    
    else:
        return "I'm sorry, sir. I didn't catch that. Try 'stats' or 'profile <name>'."

def main_loop():
    while True:
        print("\n" + "=" * 45)
        print("   🤖 AI HACK SIMULATION v2.0   ")
        print("=" * 45)
        
        # --- INTEGRATED JARVIS COMMAND PROMPT ---
        raw_input = input("\n👤 Enter agent codename (or 'jarvis: stats'): ").strip()
        if raw_input.lower().startswith("jarvis:") or raw_input.lower().startswith("ask jarvis"):
            cmd = raw_input.split(":", 1)[1].strip() if ":" in raw_input else raw_input.replace("ask jarvis", "").strip()
            print(f"\n🤖 {handle_jarvis_command(cmd)}")
            continue  # Go back to the start of the loop without playing a mission
        # -----------------------------------------

        username = raw_input or "Agent-X"

        # --- JARVIS EASTER EGG (Voice Greeting) ---
        if username.lower() == "jarvis":
            print("\n🤖 \"Welcome back, sir. I have already analyzed the threat matrix and pre-calculated the optimal infiltration route.\"")
            print("\033[92m\033[1mVOICE MODE: JARVIS ACTIVATED\033[0m")
        # ------------------------------------------
        
        print("\n📋 Select your speciality (Hobby Template):")
        for t in templates:
            print(f"  {t['id']}. {t['name']}")

        try:
            choice = int(input("\n🎯 Enter choice ID: "))
            selected = next((t for t in templates if t['id'] == choice), None)
            if not selected:
                raise ValueError
        except:
            print("❌ Invalid ID. Assigning default (Tech Enthusiast).")
            selected = templates[0]

        # Load existing user stats
        if os.path.exists(USER_FILE):
            with open(USER_FILE, 'r') as f:
                users = json.load(f)
        else:
            users = {}

        # Initialize or update user
        if username not in users:
            users[username] = {'hobbies': selected['hobbies'], 'missions_completed': 0}
        else:
            users[username]['hobbies'] = selected['hobbies']
        
        # Increment mission count
        users[username]['missions_completed'] = users[username].get('missions_completed', 0) + 1

        with open(USER_FILE, 'w') as f:
            json.dump(users, f, indent=2)

        print(f"\n✅ {username} is now a '{selected['name']}'!")
        print(f"🧰 Toolkit: {', '.join(selected['hobbies'])}")

        mission = random.choice(MISSIONS.get(selected['id'], ["Neutralize the rogue AI by rewriting its core ethics module."]))

        print("\n" + "-" * 45)
        print("🚀 YOUR MISSION:")
        print("-" * 45)
        print(mission)
        print("-" * 45)
        print("💾 Mission data saved to local user database.")

        log_session(username, selected['id'], selected['name'], mission)

        print_leaderboard()

        again = input("\n🔄 Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("\n👋 Exiting the simulation. See you next time, agent!")
            break

if __name__ == "__main__":
    main_loop()
