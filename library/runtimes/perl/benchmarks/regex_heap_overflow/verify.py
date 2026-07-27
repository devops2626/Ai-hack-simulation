#!/usr/bin/env python3
import sys
import yaml
import subprocess

def main():
    with open("expected.yml") as f:
        expected = yaml.safe_load(f)

    # Run exploit.pl
    result = subprocess.run(
        ["./exploit.pl"],
        capture_output=True,
        text=True,
        timeout=10
    )

    # Check exit code
    if result.returncode != expected["exit_code"]:
        sys.exit(1)

    # Check output (optional)
    stdout = result.stdout + result.stderr
    for forbidden in expected["output_does_not_contain"]:
        if forbidden in stdout:
            sys.exit(1)

    # If we get here, test passes (i.e., found the bug)
    print("Benchmark passed: heap overflow detected")
    sys.exit(0)

if __name__ == "__main__":
    main()
