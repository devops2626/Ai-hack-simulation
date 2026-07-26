import json
import os
import datetime

SESSION_LOG_FILE = 'session_logs.jsonl'
USER_FILE = 'users.json'

# --- Core Analysis Engine (Reusing logic) ---
def load_sessions():
    if not os.path.exists(SESSION_LOG_FILE):
        return []
    with open(SESSION_LOG_FILE, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def analyze_user(username):
    sessions = load_sessions()
    user_sessions = [s for s in sessions if s['username'].lower() == username.lower()]
    if not user_sessions:
        return f"I have no data on {username}, sir."
    
    total = len(user_sessions)
    hobbies = [s['hobby_name'] for s in user_sessions]
    fav_hobby = max(set(hobbies), key=hobbies.count) if hobbies else "None"
    
    return f"Profile for {username}: {total} tracked sessions. Favorite speciality: {fav_hobby}."

# --- Execution Loop (The "Voice" Interface) ---
def jarvis_loop():
    print("\n" + "=" * 50)
    print("   🧠 JARVIS TEXT COMMAND CENTER   ")
    print("=" * 50)
    print("Type 'profile <name>' to get agent stats.")
    print("Type 'stats' for overall system analytics.")
    print("Type 'exit' to leave the command center.")
    print("=" * 50)

    while True:
        try:
            command = input("\n🎙️ [Jarvis] Listening... ").strip().lower()
            
            if command == "exit":
                print("\n👋 Shutting down the command center, sir.")
                break
            
            elif command.startswith("profile "):
                agent = command.split(" ", 1)[1].strip()
                response = analyze_user(agent)
                print(f"\n🤖 {response}")
            
            elif command == "stats":
                sessions = load_sessions()
                if not sessions:
                    print("\n🤖 No mission logs found yet, sir. Run 'make start' first.")
                else:
                    agents = list(set(s['username'] for s in sessions))
                    print(f"\n🤖 System Report: {len(sessions)} total missions logged across {len(agents)} active agents.")
                    print(f"   Active roster: {', '.join(agents)}")
            
            else:
                print("\n🤖 I'm sorry, sir. I didn't catch that. Try 'profile Jarvis' or 'stats'.")
                
        except KeyboardInterrupt:
            print("\n\n🤖 Aborting mission. See you next time, sir.")
            break

if __name__ == "__main__":
    jarvis_loop()
