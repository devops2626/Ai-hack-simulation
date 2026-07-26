import json
import os
from collections import Counter

SESSION_LOG_FILE = 'session_logs.jsonl'
USER_FILE = 'users.json'

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
    hobbies = Counter([s['hobby_name'] for s in user_sessions])
    fav_hobby = hobbies.most_common(1)[0][0] if hobbies else "None"
    
    user_missions = 0
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            users = json.load(f)
            if username in users:
                user_missions = users[username].get('missions_completed', 0)
    
    return f"Profile for {username}: {total} tracked sessions. Favorite speciality: {fav_hobby}. Total missions: {user_missions}."

def main():
    print("=" * 45)
    print("   🧠 JARVIS ANALYTICS ENGINE   ")
    print("=" * 45)
    if not os.path.exists(SESSION_LOG_FILE):
        print("No session logs found. Run a simulation first!")
        return
    
    sessions = load_sessions()
    print(f"Jarvis Report: {len(sessions)} total recorded sessions across all agents.")
    
    unique_agents = list(set(s['username'] for s in sessions))
    print(f"Active agents observed: {', '.join(unique_agents)}")
    
    print("\n--- Detailed Jarvis Analysis ---")
    for agent in unique_agents:
        print(analyze_user(agent))
    print("=" * 45)

if __name__ == "__main__":
    main()
