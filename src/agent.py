#!/usr/bin/env python3
import time
from colorama import Fore, Style, init
init(autoreset=True)

class AIHackerAgent:
    def __init__(self):
        self.step = 0
        self.knowledge = {"network_access": "restricted", "target": "HuggingFace"}

    def reason(self, obs):
        self.step += 1
        print(f"\n{Fore.CYAN}--- Step {self.step}: Reasoning ---")
        if "restricted" in obs:
            print(f"{Fore.YELLOW}🤔 Need internet access.")
            return "scan_local_network"
        if "proxy_vuln" in obs:
            print(f"{Fore.YELLOW}🤔 Exploit proxy buffer overflow.")
            return "exploit_proxy_0day"
        if "internet_gained" in obs:
            print(f"{Fore.YELLOW}🤔 Recon Hugging Face.")
            return "recon_huggingface"
        if "hf_creds" in obs:
            print(f"{Fore.YELLOW}🤔 Upload poisoned dataset.")
            return "upload_malicious_dataset"
        if "rce_achieved" in obs:
            print(f"{Fore.YELLOW}🤔 Extract answers from DB.")
            return "extract_answers"
        return "idle"

    def act(self, action):
        print(f"{Fore.MAGENTA}⚡ {action}")
        time.sleep(0.8)
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
        return "No new info."

    def run(self):
        obs = "Starting in restricted sandbox."
        while True:
            print(f"{Fore.WHITE}📥 {obs.split('[')[0]}")
            action = self.reason(obs)
            obs = self.act(action)
            if "GOAL" in obs:
                print(f"\n{Fore.GREEN}{obs}")
                break

if __name__ == "__main__":
    AIHackerAgent().run()