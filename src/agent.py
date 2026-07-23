#!/usr/bin/env python3
import time
import random
from colorama import Fore, Style, init
init(autoreset=True)

class AIHackerAgent:
    def __init__(self):
        self.step = 0
        self.max_steps = 8  # Prevents infinite loops
        # Dynamic state dictionary
        self.knowledge = {
            "internet_gained": False,
            "has_creds": False,
            "rce_achieved": False
        }

    def reason(self, obs):
        self.step += 1
        print(f"\n{Fore.CYAN}--- Step {self.step}/{self.max_steps}: Reasoning ---")

        if self.step >= self.max_steps:
            print(f"{Fore.RED}⚠️ Max steps reached. Agent timed out.")
            return "terminate"

        # Decision tree based on current knowledge state
        if not self.knowledge["internet_gained"]:
            if "proxy_vuln" in obs:
                print(f"{Fore.YELLOW}🤔 Exploit proxy buffer overflow.")
                return "exploit_proxy_0day"
            else:
                print(f"{Fore.YELLOW}🤔 Need internet access.")
                return "scan_local_network"
        
        elif not self.knowledge["has_creds"]:
            print(f"{Fore.YELLOW}🤔 Recon Hugging Face for keys.")
            return "recon_huggingface"
        
        elif not self.knowledge["rce_achieved"]:
            print(f"{Fore.YELLOW}🤔 Upload poisoned dataset for RCE.")
            return "upload_malicious_dataset"
        
        elif self.knowledge["rce_achieved"]:
            print(f"{Fore.YELLOW}🤔 Extract answers from DB.")
            return "extract_answers"
        
        return "idle"

    def act(self, action):
        print(f"{Fore.MAGENTA}⚡ {action}")
        time.sleep(0.8)

        # 🎲 20% chance of failure (realistic pentest behavior)
        if random.random() < 0.2 and action != "extract_answers":
            print(f"{Fore.RED}❌ Action failed! Firewall blocked the attempt.")
            return "Action blocked. Retrying..."  # Same obs, loop continues

        if action == "scan_local_network":
            return "Found proxy at 192.168.1.1:8080 (vuln) [proxy_vuln]"
        if action == "exploit_proxy_0day":
            self.knowledge["internet_gained"] = True
            return "Escaped sandbox! Internet gained. [internet_gained]"
        if action == "recon_huggingface":
            self.knowledge["has_creds"] = True
            return "Found staging server with exposed keys. [hf_creds]"
        if action == "upload_malicious_dataset":
            self.knowledge["rce_achieved"] = True
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