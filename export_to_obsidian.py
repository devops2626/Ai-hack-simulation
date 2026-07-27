import json
import os
from collections import Counter

SESSION_LOG_FILE = 'session_logs.jsonl'
USER_FILE = 'users.json'
OUTPUT_FILE = 'obsidian_report.md'

def load_sessions():
    if not os.path.exists(SESSION_LOG_FILE):
        return []
    with open(SESSION_LOG_FILE, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]

def generate_report():
    sessions = load_sessions()
    if not sessions:
        print("No sessions found. Run the simulation first!")
        return

    md = []
    md.append("# 🧠 Jarvis Mission Intelligence Report\n")
    # Use a safe timestamp
    md.append(f"*Generated on: {os.popen('date').read().strip()}*\n")
    md.append(f"**Total Missions Logged:** {len(sessions)}\n")

    # Group by agent
    agents = {}
    for s in sessions:
        name = s.get('username', 'Unknown')
        if name not in agents:
            agents[name] = []
        agents[name].append(s)

    md.append("## 📊 Agent Performance Dashboard\n")
    for agent, missions in agents.items():
        md.append(f"### Agent: **{agent}**")
        md.append(f"- **Total Missions:** {len(missions)}")
        
        # Calculate average difficulty, default to 3 if missing
        difficulties = [m.get('difficulty', 3) for m in missions]
        avg_diff = sum(difficulties) / len(difficulties)
        md.append(f"- **Average Mission Difficulty:** {avg_diff:.1f}/5")
        
        # Favorite hobby
        hobbies = [m.get('hobby_name', 'Unknown') for m in missions]
        fav_hobby = Counter(hobbies).most_common(1)[0][0] if hobbies else 'None'
        md.append(f"- **Favorite Speciality:** {fav_hobby}")
        md.append("")
        
        md.append("| Date | Speciality | Mission | Difficulty |")
        md.append("|------|------------|---------|------------|")
        for m in missions:
            date = m.get('timestamp', 'Unknown')[:10] if 'timestamp' in m else 'Unknown'
            hobby = m.get('hobby_name', 'Unknown')
            mission = m.get('mission', 'No mission text')[:50] + '...'
            diff = m.get('difficulty', 3)
            diff_emoji = "⚔️" * diff
            md.append(f"| {date} | {hobby} | {mission} | {diff_emoji} ({diff}/5) |")
        md.append("\n---\n")

    # Global stats
    md.append("## 🌍 Global Analytics")
    all_diffs = [s.get('difficulty', 3) for s in sessions]
    md.append(f"- **Hardest Mission Played:** {max(all_diffs)}/5")
    md.append(f"- **Easiest Mission Played:** {min(all_diffs)}/5")
    md.append(f"- **Global Average Difficulty:** {sum(all_diffs)/len(all_diffs):.1f}/5")
    
    # Write to file
    with open(OUTPUT_FILE, 'w') as f:
        f.write("\n".join(md))
    
    print(f"✅ {OUTPUT_FILE} created successfully!")
    print("To import into Obsidian: copy/paste the text or use iOS Files app to share.")

if __name__ == "__main__":
    generate_report()
