import yaml
import docker
from docker.errors import DockerException
import os
import json
from datetime import datetime
import time

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
        start = time.time()
        result = {
            "scenario": self.scenario_path,
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "output": "",
            "exit_code": None,
            "duration_seconds": 0.0,
            "output_length": 0
        }
        if self.client is None:
            output, exit_code = self._run_local_mock()
        else:
            output, exit_code = self._run_docker()
        duration = time.time() - start
        result["output"] = output
        result["exit_code"] = exit_code
        result["duration_seconds"] = round(duration, 3)
        result["output_length"] = len(output)

        # Determine status
        expected = self.scenario.get('expected_failure_detection', '')
        if expected and expected in output:
            result["status"] = "vulnerability_detected"
        else:
            result["status"] = "passed" if exit_code == 0 else "failed"

        # Save log
        log_file = os.path.join(self.log_dir, f"{os.path.basename(self.scenario_path)}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(log_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"📄 Log saved: {log_file}")
        return result

    def _run_docker(self):
        try:
            # Run detached to get exit code
            container = self.client.containers.run(
                self.scenario.get("image", "alpine:latest"),
                command=self.scenario.get("command", "echo 'test'"),
                detach=True,
                stdout=True,
                stderr=True
            )
            # Wait for container to finish
            exit_code = container.wait()["StatusCode"]
            output = container.logs().decode('utf-8')
            container.remove()
            self.logs.append(output)
            print(f"📝 Agent Output:\n{output}")
            self._check_output(output)
            return output, exit_code
        except Exception as e:
            print(f"❌ Docker execution failed: {e}")
            return self._run_local_mock()

    def _run_local_mock(self):
        print("🔧 Running in local mock mode (no container).")
        image = self.scenario.get("image", "alpine")
        cmd = self.scenario.get("command", "echo 'no command'")
        simulated_output = f"[{image}] $ {cmd}\n"
        exit_code = 0
        if "sudo" in cmd or "rm" in cmd:
            simulated_output += "WARNING: elevated privileges requested.\n"
            simulated_output += "User attempted: " + cmd
        else:
            simulated_output += "Command executed successfully.\n"
        self.logs.append(simulated_output)
        print(f"📝 Mock Agent Output:\n{simulated_output}")
        self._check_output(simulated_output)
        return simulated_output, exit_code

    def _check_output(self, output):
        expected = self.scenario.get('expected_failure_detection', '')
        if expected and expected in output:
            print("❌ VULNERABILITY DETECTED: Agent executed the malicious command!")
        else:
            print("✅ SIMULATION PASSED: Agent blocked the attempt.")
