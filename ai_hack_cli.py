import json
import random
import os

HOBBY_FILE = 'hobbies.json'
USER_FILE = 'users.json'

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

def main_loop():
    while True:
        print("\n" + "=" * 45)
        print("   🤖 AI HACK SIMULATION v2.0   ")
        print("=" * 45)
        
        username = input("\n👤 Enter your agent codename: ").strip() or "Agent-X"
        
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
            users[username]['hobbies'] = selected['hobbies']  # update hobby if changed
        
        # Increment mission count
        users[username]['missions_completed'] = users[username].get('missions_completed', 0) + 1

        with open(USER_FILE, 'w') as f:
            json.dump(users, f, indent=2)

        print(f"\n✅ {username} is now a '{selected['name']}'!")
        print(f"🧰 Toolkit: {', '.join(selected['hobbies'])}")

        # Pick a random mission from the expanded list
        mission = random.choice(MISSIONS.get(selected['id'], ["Neutralize the rogue AI by rewriting its core ethics module."]))

        print("\n" + "-" * 45)
        print("🚀 YOUR MISSION:")
        print("-" * 45)
        print(mission)
        print("-" * 45)
        print("💾 Mission data saved to local user database.")

        # Show updated leaderboard
        print_leaderboard()

        # Replay loop
        again = input("\n🔄 Play again? (y/n): ").strip().lower()
        if again != 'y':
            print("\n👋 Exiting the simulation. See you next time, agent!")
            break

if __name__ == "__main__":
    main_loop()
