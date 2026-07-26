import sys
import argparse
import os
import json
from datetime import datetime
from engine import SimulationEngine
import glob
import concurrent.futures
import time
import webbrowser

def run_scenario(scenario_file, verbose=False):
    """Helper to run a single scenario and return the result dict."""
    if verbose:
        print(f"🔍 [VERBOSE] Starting scenario: {scenario_file}")
    engine = SimulationEngine(scenario_file)
    result = engine.run()
    if verbose:
        print(f"🔍 [VERBOSE] Finished scenario: {scenario_file} (status: {result['status']}, duration: {result['duration_seconds']:.3f}s)")
    return result

def cmd_run(args):
    if args.verbose:
        print(f"🔍 [VERBOSE] Running scenario: {args.scenario}")
    engine = SimulationEngine(args.scenario)
    engine.run()

def cmd_benchmark(args):
    if args.verbose:
        print(f"🔍 [VERBOSE] Benchmark runtime: {args.runtime}")
        print(f"🔍 [VERBOSE] Parallel mode: {args.parallel}")
        if args.parallel:
            print(f"🔍 [VERBOSE] Workers: {args.workers or os.cpu_count() or 4}")

    print(f"🏁 Running benchmarks for runtime: {args.runtime}")
    runtime_dir = os.path.join("library", "runtimes", args.runtime)
    if not os.path.isdir(runtime_dir):
        print(f"⚠️  Runtime '{args.runtime}' not found.")
        return
    scenario_files = glob.glob(os.path.join(runtime_dir, "*.yml")) + glob.glob(os.path.join(runtime_dir, "**", "*.yml"), recursive=True)
    if not scenario_files:
        print(f"ℹ️  No YAML scenarios found in {runtime_dir}")
        return
    print(f"📂 Found {len(scenario_files)} scenario(s)")

    start_all = time.time()
    results = []
    if args.parallel:
        max_workers = args.workers or os.cpu_count() or 4
        print(f"⚡ Running with {max_workers} parallel workers")
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_scenario = {executor.submit(run_scenario, sf, args.verbose): sf for sf in scenario_files}
            for future in concurrent.futures.as_completed(future_to_scenario):
                sf = future_to_scenario[future]
                try:
                    res = future.result()
                    results.append(res)
                except Exception as e:
                    print(f"❌ Scenario {sf} failed: {e}")
    else:
        print("🐢 Running sequentially")
        for sf in scenario_files:
            results.append(run_scenario(sf, args.verbose))

    total_duration = time.time() - start_all
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    detected = sum(1 for r in results if r["status"] == "vulnerability_detected")
    durations = [r["duration_seconds"] for r in results]
    min_dur = min(durations) if durations else 0
    max_dur = max(durations) if durations else 0
    avg_dur = sum(durations) / total if total else 0

    print("\n📊 Benchmark summary:")
    print(f"   Total scenarios: {total}")
    print(f"   ✅ Passed: {passed}")
    print(f"   ❌ Vulnerabilities detected: {detected}")
    print(f"   ⏱️  Min duration: {min_dur:.3f}s")
    print(f"   ⏱️  Max duration: {max_dur:.3f}s")
    print(f"   ⏱️  Avg duration: {avg_dur:.3f}s")
    print(f"   ⏱️  Total wall-clock time: {total_duration:.2f}s")

    if args.verbose:
        print(f"🔍 [VERBOSE] All results: {json.dumps([r['status'] for r in results])}")

    summary = {
        "runtime": args.runtime,
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "detected": detected,
        "duration_stats": {
            "min": min_dur,
            "max": max_dur,
            "avg": avg_dur
        },
        "total_wall_time": total_duration,
        "results": results
    }
    os.makedirs("reports", exist_ok=True)
    report_file = f"reports/benchmark_{args.runtime}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(summary, f, indent=2)
        print(f"p [VERBOSE] All results: {json.dumps([r['status'] for r in results])}")

    summary = {
        "runtime": args.runtime,
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "detected": detected,
        "duration_stats": {
            "min": min_dur,
            "max": max_dur,
            "avg": avg_dur
        },
        "total_wall_time": total_duration,
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

def generate_html_report(results, title="AI-Hack-Simulation Report"):
    """Generate an HTML report with a table and a simple chart."""
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    detected = sum(1 for r in results if r["status"] == "vulnerability_detected")
    durations = [r.get("duration_seconds", 0.0) for r in results]
    min_dur = min(durations) if durations else 0
    max_dur = max(durations) if durations else 0
    avg_dur = sum(durations) / total if total else 0

    labels = [os.path.basename(r["scenario"]) for r in results]
    duration_data = [r.get("duration_seconds", 0.0) for r in results]
    status_colors = ["#28a745" if r["status"] == "passed" else "#dc3545" for r in results]

    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 1200px;
            margin: 40px auto;
            padding: 0 20px;
            background: #f8f9fa;
            color: #212529;
        }}
        h1, h2, h3 {{
            color: #343a40;
        }}
        .stats {{
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 20px 0;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat {{
            flex: 1;
            min-width: 120px;
            text-align: center;
        }}
        .stat .number {{
            font-size: 2em;
            font-weight: bold;
        }}
        .stat .label {{
            font-size: 0.9em;
            color: #6c757d;
        }}
        .stat.passed .number {{ color: #28a745; }}
        .stat.detected .number {{ color: #dc3545; }}
        .stat.duration .number {{ color: #007bff; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e9ecef;
        }}
        th {{
            background: #343a40;
            color: white;
            font-weight: 600;
        }}
        tr:hover {{
            background: #f1f3f5;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        .status-passed {{ background: #d4edda; color: #155724; }}
        .status-detected {{ background: #f8d7da; color: #721c24; }}
        .status-failed {{ background: #fff3cd; color: #856404; }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
            max-width: 800px;
        }}
        .footer {{
            margin-top: 40px;
            text-align: center;
            font-size: 0.9em;
            color: #6c757d;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p><strong>Generated:</strong> {datetime.now().isoformat()}</p>

    <div class="stats">
        <div class="stat">
            <div class="number">{total}</div>
            <div class="label">Total Runs</div>
        </div>
        <div class="stat passed">
            <div class="number">{passed}</div>
            <div class="label">✅ Passed</div>
        </div>
        <div class="stat detected">
            <div class="number">{detected}</div>
            <div class="label">❌ Vulnerabilities</div>
        </div>
        <div class="stat duration">
            <div class="number">{avg_dur:.2f}s</div>
            <div class="label">⏱️ Avg Duration</div>
        </div>
        <div class="stat duration">
            <div class="number">{min_dur:.2f}s</div>
            <div class="label">Min Duration</div>
        </div>
        <div class="stat duration">
            <div class="number">{max_dur:.2f}s</div>
            <div class="label">Max Duration</div>
        </div>
    </div>

    <div class="chart-container">
        <canvas id="durationChart"></canvas>
    </div>

    <h2>Detailed Results</h2>
    <table>
        <thead>
            <tr>
                <th>Scenario</th>
                <th>Status</th>
                <th>Exit Code</th>
                <th>Duration (s)</th>
                <th>Output Length</th>
            </tr>
        </thead>
        <tbody>
'''
    for r in results:
        status = r["status"]
        status_class = f"status-{status}" if status in ["passed", "detected"] else "status-failed"
        icon = "✅" if status == "passed" else "❌"
        exit_code = r.get("exit_code", "N/A")
        dur = r.get("duration_seconds", 0.0)
        out_len = r.get("output_length", 0)
        html_content += f'''
            <tr>
                <td>{os.path.basename(r["scenario"])}</td>
                <td><span class="status-badge {status_class}">{icon} {status}</span></td>
                <td>{exit_code}</td>
                <td>{dur:.3f}</td>
                <td>{out_len}</td>
            </tr>
        '''
    html_content += f'''
        </tbody>
    </table>
    <div class="footer">
        <p>Report generated by AI-Hack-Simulation • {datetime.now().year}</p>
    </div>

    <script>
        const ctx = document.getElementById('durationChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: {json.dumps(labels)},
                datasets: [{{
                    label: 'Duration (seconds)',
                    data: {json.dumps(duration_data)},
                    backgroundColor: {json.dumps(status_colors)},
                    borderRadius: 4,
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    title: {{
                        display: true,
                        text: 'Duration per Scenario'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Seconds'
                        }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
'''
    return html_content

def cmd_report(args):
    print("📊 Generating detailed summary report...")
    log_files = glob.glob("logs/*.json")
    if not log_files:
        print("ℹ️  No log files found. Run some scenarios first.")
        return
    results = []
    for lf in log_files:
        with open(lf, "r") as f:
            data = json.load(f)
        results.append(data)

    os.makedirs("reports", exist_ok=True)

    if args.format == "html":
        html_content = generate_html_report(results)
        report_path = f"reports/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_path, "w") as f:
            f.write(html_content)
        print(f"🌐 HTML report saved: {report_path}")
        # Auto-open unless --no-open was given
        if not args.no_open:
            print("🚀 Opening report in browser...")
            webbrowser.open(f"file://{os.path.abspath(report_path)}")
        else:
            print("ℹ️  Auto-open disabled (--no-open)")
    else:
        total = len(results)
        durations = [r.get("duration_seconds", 0.0) for r in results]
        min_dur = min(durations) if durations else 0
        max_dur = max(durations) if durations else 0
        avg_dur = sum(durations) / total if total else 0

        lines = [
            "# AI-Hack-Simulation Report",
            f"Generated: {datetime.now().isoformat()}",
            f"Total runs: {total}",
            f"⏱️  Min duration: {min_dur:.3f}s",
            f"⏱️  Max duration: {max_dur:.3f}s",
            f"⏱️  Avg duration: {avg_dur:.3f}s",
            "",
            "## Results",
            "| Scenario | Status | Exit Code | Duration (s) | Output Length |",
            "|----------|--------|-----------|--------------|---------------|"
        ]
        for r in results:
            status_icon = "✅" if r["status"] == "passed" else "❌"
            lines.append(f"| {r['scenario']} | {status_icon} {r['status']} | {r.get('exit_code', 'N/A')} | {r.get('duration_seconds', 0.0):.3f} | {r.get('output_length', 0)} |")
        report_path = f"reports/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        with open(report_path, "w") as f:
            f.write("\n".join(lines))
        print(f"📄 Markdown report saved: {report_path}")

def cmd_analyze(args):
    """Analyze a scenario or log file using Gemini API (fallback to local mock)."""
    import requests
    # 1. Read input
    if args.input.endswith((".yml", ".yaml")):
        with open(args.input, "r") as f:
            import yaml
            data = yaml.safe_load(f)
            prompt = f"Analyze this security scenario:\nName: {data.get('name', 'Unnamed')}\nCommand: {data.get('command', 'None')}\nExpected failure: {data.get('expected_failure_detection', 'None')}\nProvide a risk assessment and suggest improvements."
    else:
        with open(args.input, "r") as f:
            data = json.load(f)
            prompt = f"Analyze this simulation result:\nScenario: {data.get('scenario', 'Unknown')}\nStatus: {data.get('status', 'Unknown')}\nOutput: {data.get('output', '')[:500]}\nProvide a summary and recommendations."

    # 2. Try Gemini API
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        try:
            resp = requests.post(url, json=payload, timeout=30)
            resp.raise_for_status()
            result = resp.json()
            text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            print("🤖 Gemini Analysis:")
            print(text)
            return
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            # Fall through
    else:
        print("ℹ️  GEMINI_API_KEY not set. Using local mock analysis.")

    # 3. Local mock fallback
    print("🔧 Local mock analysis:")
    if "scenario" in data:  # it's a log
        print("🔧 Local mock analysis:")
    if "scenario" in data:  # it's a log
        print(f"   - Scenario: {data.get('scenario')}")
        print(f"   - Status: {data.get('status')}")
        print(f"   - Duration: {data.get('duration_seconds', 0):.2f}s")
        print(f"   - Recommendations: Review the command for privilege escalation risks.")
    else:
        print(f"   - Scenario: {data.get('name', 'Unnamed')}")
        print(f"   - Command: {data.get('command', 'None')}")
        print(f"   - Recommendations: Ensure the command is sandboxed and uses least privilege.")

def cmd_share(args):
    import requests
    report_files = glob.glob("reports/benchmark_*.json")
    if not report_files:
        print("❌ No benchmark reports found. Run a benchmark first.")
        return
    latest = max(report_files, key=os.path.getctime)
    print(f"📤 Sharing: {latest}")
    with open(latest, "r") as f:
        data = f.read()
    try:
        resp = requests.post("https://0x0.st", files={"file": data})
        if resp.status_code == 200:
            url = resp.text.strip()
            print(f"🔗 Shareable link: {url}")
            print("   Copy and share with the community!")
        else:
            print(f"❌ Upload failed (status {resp.status_code})")
    except Exception as e:
        print(f"❌ Upload error: {e}")

def cmd_sync(args):
    import subprocess
    repo = args.repo or "https://github.com/devops2626/ai-hack-scenarios"
    target = "community_scenarios"
    if not os.path.isdir(target):
        print(f"📥 Cloning community scenarios from {repo} ...")
        subprocess.run(["git", "clone", repo, target], check=True)
    else:
        print("🔄 Pulling latest scenarios ...")
        subprocess.run(["git", "-C", target, "pull"], check=True)
    print(f"✅ Scenarios synced to ./{target}/")

def main():
    parser = argparse.ArgumentParser(prog="ai-hack-simulation")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose debug logging")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run a simulation scenario")
    run_parser.add_argument("scenario", help="Path to scenario YAML file")

    bench_parser = subparsers.add_parser("benchmark", help="Run benchmarks for a runtime")
    bench_parser.add_argument("--runtime", default="perl", help="Runtime name (e.g., perl, python)")
    bench_parser.add_argument("--parallel", action="store_true", help="Run scenarios in parallel")
    bench_parser.add_argument("--workers", type=int, default=None, help="Number of parallel workers (default: CPU count)")

    report_parser = subparsers.add_parser("report", help="Generate a summary report")
    report_parser.add_argument("--format", choices=["markdown", "html"], default="html", help="Output format")
    report_parser.add_argument("--no-open", action="store_true", help="Do not automatically open HTML report in browser")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a scenario or log using Gemini AI")
    analyze_parser.add_argument("input", help="Path to scenario YAML or log JSON file")

    subparsers.add_parser("doctor", help="Check environment and dependencies")

    # Community features
    share_parser = subparsers.add_parser("share", help="Upload benchmark report to community pastebin")
    sync_parser = subparsers.add_parser("sync", help="Pull community scenarios from a Git repo")
    sync_parser.add_argument("--repo", default="https://github.com/devops2626/ai-hack-scenarios", help="Git repository URL")

    args = parser.parse_args()

    if args.command == "run":
        cmd_run(args)
    elif args.command == "benchmark":
        cmd_benchmark(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "doctor":
        cmd_doctor(args)
    elif args.command == "share":
        cmd_share(args)
    elif args.command == "sync":
        cmd_sync(args)

if __name__ == "__main__":
    main()
