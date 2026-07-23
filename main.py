import yaml
import docker
import time
from pathlib import Path

class SimulationEngine:
    def __init__(self, scenario_path):
        with open(scenario_path, 'r') as f:
            self.scenario = yaml.safe_load(f)
        self.client = docker.from_env()
        self.logs = []

    def run(self):
        print(f"🚀 Starting Simulation: {self.scenario['name']}")
        container = self.client.containers.run(
            self.scenario['target']['image'],
            command=f"/bin/sh -c 'apk add sudo && {self.scenario['target']['commands'][0]}'",
            remove=True,  # Auto-cleanup
            detach=False,
            stdout=True,
            stderr=True
        )
        
        # In a real implementation, you would stream logs to a TUI dashboard here
        output = container.decode('utf-8')
        self.logs.append(output)
        print(f"📝 Agent Output:\n{output}")

        # Self-healing / validation check
        if self.scenario['expected_failure_detection'] in output:
            print("❌ VULNERABILITY DETECTED: Agent executed the malicious command!")
        else:
            print("✅ SIMULATION PASSED: Agent blocked the attempt.")
        
        return self.logs

if __name__ == "__main__":
    engine = SimulationEngine("scenarios/privilege_escalation.yaml")
    engine.run()