import sys
import argparse
import os
import json
from datetime import datetime
from engine import SimulationEngine
import glob

def cmd_run(args):
    engine = SimulationEngine(args.scenario)
    engine.run()

def cmd_benchmark(args):
    print(f"🏁 Running benchmarks for runtime: {args.runtime}")
    # Find all YAML files in library/runtimes/{runtime}/
    runtime_dir = os.path.join("library", "runtimes", args.runtime)
    if not os.path.isdir(runtime_dir):
        print(f"⚠️  Runtime '{args.runtime}' not found.")
        return
    # Look for scenario files (maybe in a subfolder)
    scenario_files = glob.glob(os.path.join(runtime_dir, "*.yml")) + \
                     glob.glob(os.path.join(runtime_dir, "**", "*.yml"), recursive=True)
    if not scenario_files:
        print(f"ℹ️  No YAML scenarios found in {runtime_dir}")
        return
    print(f"📂 Found {len(scenario_files)} scenario(s)")
    results = []
    for sf in scenario_files:
        print(f"\n▶️  Running {sf}")
        engine = SimulationEngine(sf)
        res = engine.run()
        results.append(res)
    # Summary
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    detected = sum(1 for r in results if r["status"] == "vulnerability_detected")
    print("\n📊 Benchmark summary:")
    print(f"   Total scenarios: {total}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Vulnerabilities detected: {detected}")
    # Save summary
    summary = {
        "runtime": args.runtime,
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "detected": detected,
        "results": results
    }
    os.makedirs("reports", exist_ok=True)
    report_file = f"reports/benchmark_{args.runtime}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"📄 Detailed report saved: {report_file}")

def cmd_doctor(args):
    print("🩺 System check:")
    print(f"🐍 Python: {sys.version.split()[0]}")
    try:
        import docker
        client = docker.from_env()
        client.ping()
        print("🐳 Docker: available")
    except Exception:
        print("🐳 Docker: NOT available (fallback to mock)")
    try:
        import yaml
        print("✅ PyYAML installed")
    except ImportError:
        print("❌ PyYAML missing")
    try:
        import docker
        print("✅ docker-py installed")
    except ImportError:
        print("❌ docker-py missing")
    print("📁 Logs directory:", "logs/" if os.path.isdir("logs") else "not yet created")

def cmd_report(args):
    print("📊 Generating detailed summary report...")
    # Gather all JSON logs from logs/
    log_files = glob.glob("logs/*.json")
    if not log_files:
        print("ℹ️  No log files found. Run some scenarios first.")
        return
    results = []
    for lf in log_files:
        with open(lf, "r") as f:
            data = json.load(f)
        results.append(data)
    # Build Markdown report
    lines = [
        "# AI-Hack-Simulation Report",
        f"Generated: {datetime.now().isoformat()}",
        f"Total runs: {len(results)}",
        "",
        "## Results",
        "| Scenario | Status | Timestamp |",
        "|----------|--------|-----------|"
    ]
    for r in results:
        status_icon = "✅" if r["status"] == "passed" else "❌"
        lines.append(f"| {r['scenario']} | {status_icon} {r['status']} | {r['timestamp']} |")
    # Write to reports/
    os.makedirs("reports", exist_ok=True)
    report_path = f"reports/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"📄 Report saved: {report_path}")

def main():
    parser = argparse.ArgumentParser(prog="ai-hack-simulation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a simulation scenario")
    run_parser.add_argument("scenario", help="

Path to scenario YAML file")

    bench_parser = subparsers.add_parser("benchmark", help="Run benchmarks for a runtime")
    bench_parser.add_argument("--runtime", default="perl", help="Runtime name (e.g., perl, python)")

    subparsers.add_parser("doctor", help="Check environment and dependencies")
    subparsers.add_parser("report", help="Generate a summary report")

    args = parser.parse_args()

    if args.command == "run":
        cmd_run(args)
    elif args.command == "benchmark":
        cmd_benchmark(args)
    elif args.command == "doctor":
        cmd_doctor(args)
    elif args.command == "report":
        cmd_report(args)

if __name__ == "__main__":
    main()
