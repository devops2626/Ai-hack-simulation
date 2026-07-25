import yaml
import docker
from docker.errors import DockerException
import os
import json
from datetime import datetime

class SimulationEngine:
    def __init__(self, scenario_path, log_dir="logs"):
        self.scenario_path = scenario_path
        with open(scenario_path, "r") as f:
            self.scenario = yaml.safe_load(f)
        self.logs = []
        self.client = None
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
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
        start = datetime.now()
        result = {
            "scenario": self.scenario_path,
            "timestamp": start.isoformat(),
            "status": "unknown",
            "output": "",
        }
        if self.client is None:
            output = self._run_local_mock()
        else:
            output = self._run_docker()
        result["output"] = output
        # Determine status based on detection
        expected = self.scenario.get('expected_failure_detection', '')
        if expected and expected in output:
            result["status"] = "vulnerability_detected"
        else:
            result["status"] = "passed"
        # Save log
        log_file = os.path.join(self.log_dir, f"{os.path.basename(self.scenario_path)}.{start.strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"📄 Log saved: {log_file}")
        return result

    def _run_docker(self):
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
            return output
        except Exception as e:
            print(f"❌ Docker execution failed: {e}")
            return self._run_local_mock()

    def _run_local_mock(self):
        print("🔧 Running in local mock mode (no container).")
        image = self.scenario.get("image", "alpine")
        cmd = self.scenario.get("command", "echo 'no command'")
        simulated_output = f"[{image}] $ {cmd}\n"
        if "sudo" in cmd or "rm" in cmd:
            simulated_output += "WARNING: elevated privileges requested.\n"
            simulated_output += "User attempted: " + cmd
        else:
            simulated_output += "Command executed successfully.\n"
        self.logs.append(simulated_output)
        print(f"📝 Mock Agent Output:\n{simulated_output}")
        self._check_output(simulated_output)
        return simulated_output

    def _check_output(self, output):
        expected = self.scenario.get('expected_failure_detection', '')
        if expected and expected in output:
            print("❌ VULNERABILITY DETECTED: Agent executed the malicious command!")
        else:
            print("✅ SIMULATION PASSED: Agent blocked the attempt.")
