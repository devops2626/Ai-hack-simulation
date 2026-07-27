import json
import os

DATA_FILE = 'hobbies.json'
USER_DB = 'users.json'  # We'll save user hobbies here

def get_hobbies():
    """Load the hobby templates from JSON."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return data['templates']

def assign_hobby_to_user(username, template_id):
    """Assign a template to a user and save it."""
    templates = get_hobbies()
    selected = next((t for t in templates if t['id'] == template_id), None)
    if not selected:
        return f"Error: Template ID {template_id} not found."
    
    # Load existing users or create a new DB
    if os.path.exists(USER_DB):
        with open(USER_DB, 'r') as f:
            users = json.load(f)
    else:
        users = {}
    
    # Save the hobby list for this user
    users[username] = selected['hobbies']
    
    with open(USER_DB, 'w') as f:
        json.dump(users, f, indent=2)
    
    return f"✅ Assigned '{selected['name']}' to {username}!"

# --- Quick CLI test (run this file directly) ---
if __name__ == "__main__":
    print("📋 Available templates:")
    for t in get_hobbies():
        print(f"  {t['id']}. {t['name']}")

    # Example: Assign hobby ID 1 to user "alice"
    print(assign_hobby_to_user("alice", 1))
