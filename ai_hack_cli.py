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

# --- ASCII Art Title ---
print("\n" + "=" * 45)
print("   🤖 AI HACK SIMULATION v1.0   ")
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

# Save to user DB
if os.path.exists(USER_FILE):
    with open(USER_FILE, 'r') as f:
        users = json.load(f)
else:
    users = {}

users[username] = selected['hobbies']
with open(USER_FILE, 'w') as f:
    json.dump(users, f, indent=2)

print(f"\n✅ {username} is now a '{selected['name']}'!")
print(f"🧰 Toolkit: {', '.join(selected['hobbies'])}")

# --- Mission Generator ---
missions = {
    1: "Infiltrate the corporate mainframe using a Python backdoor. Evade IDS by mimicking legitimate traffic. Your key tool: Open Source intelligence.",
    2: "Build a drone-mounted thermal scanner from scratch. 3D print the casing and wire the electronics to detect hidden heat signatures.",
    3: "Decrypt the intercepted military-grade cipher using brute-force CRC collisions. Manage to slip past the firewall undetected.",
    4: "Analyze 10 terabytes of leaked user logs to find the anomaly. Use PCA and clustering to pinpoint the rogue actor among millions.",
    5: "Spin up a 50-node Kubernetes cluster on the fly to DDoS a rogue AI. Orchestrate the deployment with Infrastructure as Code.",
    6: "Reverse engineer the simulation engine and inject a custom shader. Make the enemies explode into pixel art in real-time.",
    7: "Synthesize a new neural interface using bio-hacked wearables. Monitor the pilot's brain waves to predict their next move before they make it.",
    8: "Generate a deepfake audio decoy of the CEO's voice to issue false orders. Use prompt engineering to slip past the voice biometrics."
}

mission = missions.get(selected['id'], "Neutralize the rogue AI by rewriting its core ethics module using a combination of all your skills.")

print("\n" + "-" * 45)
print("🚀 YOUR MISSION:")
print("-" * 45)
print(mission)
print("-" * 45)
print("\n💾 Mission data saved to local user database.\n")
