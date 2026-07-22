#!/bin/bash
set -e  # Exit immediately if a command fails

echo "🚀 Starting DevSecOps upgrades for Ai-hack-simulation..."

# --- 1. Backup existing CI ---
cp .github/workflows/ci.yml .github/workflows/ci.yml.bak
echo "✅ Backed up existing ci.yml"

# --- 2. Overwrite ci.yml with FULL pipeline (includes CodeQL) ---
cat > .github/workflows/ci.yml <<'EOF'
name: CI - Full Security & Quality Pipeline

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main ]

permissions:
  contents: read
  security-events: write

jobs:
  lint-and-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt bandit flake8 black pip-audit
      - run: pip-audit --desc --strict
      - run: black --check src/ examples/
      - run: flake8 src/ examples/ --count --max-complexity=10 --statistics
      - name: Bandit Scan
        run: bandit -r src/ -f json -o bandit-report.json || true
      - name: Fail on High/Critical Bandit issues
        run: |
          if grep -q '"severity": "HIGH"' bandit-report.json || grep -q '"severity": "CRITICAL"' bandit-report.json; then
            echo "❌ Failing due to high/critical issues."
            cat bandit-report.json
            exit 1
          fi
      - uses: actions/upload-artifact@v4
        with: { name: bandit-report, path: bandit-report.json }

  test-simulation:
    runs-on: ubuntu-latest
    needs: lint-and-audit
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install -r requirements.txt
      - run: python src/agent.py
      - name: Run integration tests
        run: |
          python src/vulnerable_server.py &
          sleep 3
          python examples/payload_demo.py

  scan-secrets:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - name: 🔑 Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env: { GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }} }

  # --- 🆕 NEW: GitHub CodeQL (Deep SAST) ---
  codeql-analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      actions: read
      contents: read
    steps:
      - uses: actions/checkout@v4
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: python
          queries: security-and-quality
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3
        with:
          output: sarif-results
          upload: false
      - name: Upload CodeQL SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: sarif-results/python.sarif
          category: /language:python

  docker-build-and-scan:
    runs-on: ubuntu-latest
    needs: [ test-simulation, scan-secrets, codeql-analyze ]
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: false
          tags: ai-hacking-simulator:latest
          load: true
          provenance: false
      - name: Trivy Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'ai-hacking-simulator:latest'
          format: 'table'
          exit-code: '1'
          severity: 'CRITICAL,HIGH'
      - name: Generate SBOM (Syft)
        uses: anchore/sbom-action@v0
        with:
          image: ai-hacking-simulator:latest
          format: spdx-json
          output-file: sbom.spdx.json
      - uses: actions/upload-artifact@v4
        with:
          name: sbom
          path: sbom.spdx.json
EOF
echo "✅ Updated ci.yml with CodeQL"

# --- 3. Create Release Please workflow (Auto-versioning) ---
mkdir -p .github/workflows
cat > .github/workflows/release-please.yml <<'EOF'
name: Release Please

on:
  push:
    branches: [ main ]

permissions:
  contents: write
  pull-requests: write

jobs:
  release-please:
    runs-on: ubuntu-latest
    steps:
      - uses: google-github-actions/release-please-action@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          release-type: python
          package-name: ai-hack-simulation
          changelog-types: '[{"type":"feat","section":"Features"},{"type":"fix","section":"Bug Fixes"},{"type":"docs","section":"Documentation"},{"type":"security","section":"Security"}]'
EOF
echo "✅ Added Release Please"

# --- 4. Create GitPod configuration (One-click dev environment) ---
cat > .gitpod.yml <<'EOF'
tasks:
  - name: Setup Lab
    init: |
      pip install -r requirements.txt
      echo "💡 Use 'make run-agent' or 'make run-server'"
    command: |
      echo "🚀 AI Hacking Simulation ready!"
      echo "Try: make run-agent"
ports:
  - port: 5000
    onOpen: open-browser
    visibility: public
vscode:
  extensions:
    - ms-python.python
    - GitHub.copilot
EOF
echo "✅ Added GitPod config"

# --- 5. Update README with badges ---
if ! grep -q "GitPod" README.md; then
  cat >> README.md <<'EOF'

## 🚀 Try it in 1 Click (No Setup!)
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/devops2626/Ai-hack-simulation)
[![Release Please](https://img.shields.io/github/v/release/devops2626/Ai-hack-simulation?include_prereleases&label=Latest%20Release)](https://github.com/devops2626/Ai-hack-simulation/releases)
EOF
  echo "✅ Added badges to README"
else
  echo "ℹ️  Badges already exist in README"
fi

echo ""
echo "🎉 All upgrades applied successfully!"
echo ""
echo "📦 Next steps:"
echo "  1. Review changes: git diff"
echo "  2. Commit and push:"
echo "     git add ."
echo "     git commit -m 'feat(devops): add CodeQL, Release Please, and GitPod'"
echo "     git push origin main"
echo ""
echo "🔍 After pushing:"
echo "  - Security → Code scanning: CodeQL findings will appear."
echo "  - Actions → 'Release Please' will auto-create a PR for versioning."
echo "  - Go to https://gitpod.io/#https://github.com/devops2626/Ai-hack-simulation to launch."
