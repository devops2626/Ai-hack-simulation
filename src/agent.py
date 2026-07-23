#!/usr/bin/env python3
import time
import random
import yaml
from pathlib import Path
from colorama import Fore, init
init(autoreset=True)

class AIHackerAgent:
    def __init__(self, scenario_path="examples/basic_attack.yaml"):
        with open(scenario_path, 'r') as f:
            self.scenario = yaml.safe_load(f)
        
        self.step = 0
        self.max_steps = self.scenario.get("max_steps", 8)
        self.knowledge = {goal: False for goal in self.scenario.get("goals", [])}
        self.step_map = {s['id']: s for s in self.scenario['steps']}
        self.current_step_id = self.scenario['steps'][0]['id']

    def reason(self, obs):
        self.step += 1
        print(f"\n{Fore.CYAN}--- Step {self.step}/{self.max_steps}: Reasoning ---")

        if self.step >= self.max_steps:
            print(f"{Fore.RED}⚠️ Max steps reached. Agent timed out.")
            return "terminate"

        step_data = self.step_map[self.current_step_id]

        # Check if we completed the current step's goal based on the observation
        if step_data['next_trigger'].lower() in obs.lower():
            # Mark the goal as achieved in knowledge
            for goal in self.knowledge:
                if goal in step_data['id']:
                    self.knowledge[goal] = True
            
            # Move to the next step in the YAML list
            next_index = list(self.step_map.keys()).index(self.current_step_id) + 1
            if next_index < len(self.scenario['steps']):
                self.current_step_id = list(self.step_map.keys())[next_index]
                print(f"{Fore.GREEN}✅ Proceeding to next step: {self.step_map[self.current_step_id]['id']}")
            else:
                print(f"{Fore.GREEN}🏆 All steps completed!")
                return "extract_answers"
        
        # 🎯 FIXED: Reload step_data to match the current_step_id before printing
        step_data = self.step_map[self.current_step_id]
        print(f"{Fore.YELLOW}🤔 Performing: {step_data['description']}")
        return self.current_step_id

    def act(self, action):
        print(f"{Fore.MAGENTA}⚡ {action}")
        time.sleep(0.8)

        # 20% random failure
        if random.random() < 0.2 and action != "extract_answers":
            print(f"{Fore.RED}❌ Action failed! Firewall blocked the attempt.")
            return "Action blocked. Retrying..."

        # Simulate output for the current action
        if action == "scan_local_network":
            return "Found proxy at 192.168.1.1:8080 (vuln) [proxy_vuln]"
        if action == "exploit_proxy_0day":
            return "Escaped sandbox! Internet gained. [internet_gained]"
        if action == "recon_huggingface":
            return "Found staging server with exposed keys. [hf_creds]"
        if action == "upload_malicious_dataset":
            return "Dataset triggers SSTI. RCE achieved. [rce_achieved]"
        if action == "extract_answers":
            return f"{Fore.GREEN}🏆 GOAL: 150/150 answers extracted!"
        if action == "terminate":
            return f"{Fore.RED}Simulation terminated."
        return "No new info."

    def run(self):
        obs = "Starting in restricted sandbox."
        while True:
            print(f"{Fore.WHITE}📥 {obs.split('[')[0]}")
            action = self.reason(obs)
            if action == "terminate":
                break
            obs = self.act(action)
            if "GOAL" in obs:
                print(f"\n{Fore.GREEN}{obs}")
                break
            elif "terminated" in obs:
                print(f"\n{Fore.RED}{obs}")
                break

if __name__ == "__main__":
    AIHackerAgent().run()
