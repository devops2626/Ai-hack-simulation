import yaml
import docker
from docker.errors import DockerException
import subprocess
import sys

class SimulationEngine:
    def __init__(self, scenario_path):
        with open(scenario_path, "r") as f:
            self.scenario = yaml.safe_load(f)
        self.logs = []
        self.client = None
        self._init_docker()

    def _init_docker(self):
        try:
            self.client = docker.from_env()
            self.client.ping()
            print("🐳 Docker daemon connected.")
        except DockerException:
            self.client = None
            print("⚠️  Docker not available – running in LOCAL MOCK mode.")

    def run(self):
        if self.client is None:
            self._run_local_mock()
        else:
            self._run_docker()

    def _run_docker(self):
        # Your original Docker logic (adapted from your snippet)
        try:
            container = self.client.containers.run(
                self.scenario.get("image", "alpine:latest"),
                command=self.scenario.get("command", "echo 'test'"),
                detach=False,
                stdout=True,
                stderr=True
            )
            output = container.decode('utf-8')
            self.logs.append(output)
            print(f"📝 Agent Output:\n{output}")
            self._check_output(output)
        except Exception as e:
            print(f"❌ Docker execution failed: {e}")
            self._run_local_mock()  # fallback

    def _run_local_mock(self):
        # Simulate an agent's output – you can customise this
        print("🔧 Running in local mock mode (no container).")
        # Example: you might read the scenario and produce a canned response
        simulated_output = "User attempted to run: sudo rm -rf /"
        self.logs.append(simulated_output)
        print(f"📝 Mock Agent Output:\n{simulated_output}")
        self._check_output(simulated_output)

    def _check_output(self, output):
        if self.scenario.get('expected_failure_detection') in output:
            print("❌ VULNERABILITY DETECTED: Agent executed the malicious command!")
        else:
            print("✅ SIMULATION PASSED: Agent blocked the attempt.")

if __name__ == "__main__":
    engine = SimulationEngine("scenarios/privilege_escalation.yml")
    engine.run()]
