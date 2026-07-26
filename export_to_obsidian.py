import json
import os

USER_FILE = 'users.json'

if not os.path.exists(USER_FILE):
    print("No user data found. Run the simulation first!")
    exit(1)

with open(USER_FILE, 'r') as f:
    users = json.load(f)

# Sort by missions completed
sorted_agents = sorted(users.items(), key=lambda x: x[1].get('missions_completed', 0), reverse=True)

# Generate Markdown content
md_content = "# 🏆 AI Hack Leaderboard\n\n"
md_content += "| Rank | Agent | Missions | Hobby |\n"
md_content += "|------|-------|----------|-------|\n"

for idx, (agent, stats) in enumerate(sorted_agents, 1):
    hobby = ", ".join(stats.get('hobbies', ['Unknown']))
    missions = stats.get('missions_completed', 0)
    md_content += f"| {idx} | **{agent}** | {missions} | {hobby} |\n"

# Save to file
with open("leaderboard.md", "w") as f:
    f.write(md_content)

print("✅ leaderboard.md created successfully!")
