```markdown
# Ai-hack-simulation Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill introduces the core development patterns, coding conventions, and operational workflows used in the `Ai-hack-simulation` Python repository. It covers file organization, code style, commit practices, and step-by-step instructions for key maintenance workflows such as funding updates and Dockerfile security hardening. This guide is designed to help contributors quickly align with the project's standards and automation.

## Coding Conventions

### File Naming
- **Convention:** camelCase
- **Example:**  
  ```plaintext
  aiAgent.py
  dataProcessor.py
  ```

### Import Style
- **Convention:** Relative imports are preferred.
- **Example:**
  ```python
  from .utils import helperFunction
  from .models import SimulationModel
  ```

### Export Style
- **Convention:** Named exports (explicitly listing exported classes/functions).
- **Example:**
  ```python
  __all__ = ['SimulationModel', 'runSimulation']
  ```

### Commit Patterns
- **Types:** Mixed (features, fixes, chores, docs, security)
- **Prefixes:** `chore`, `security`, `docs`, `fix`, `feat`
- **Example:**
  ```
  feat: add support for multi-agent simulation
  fix: correct agent movement logic
  docs: update README with usage examples
  ```

## Workflows

### Update Funding Configuration
**Trigger:** When someone wants to change or add funding sources or sponsorship information.  
**Command:** `/update-funding`

1. Edit `.github/FUNDING.yml` with new or updated funding entries.
2. Commit and push the changes.

**Example:**
```yaml
# .github/FUNDING.yml
github: [your-github-username]
patreon: your-patreon-id
```

---

### Dockerfile Security Hardening
**Trigger:** When someone wants to address security vulnerabilities or optimize Docker builds.  
**Command:** `/harden-dockerfile`

1. Edit `Dockerfile` to improve security or optimize the build process.
2. Optionally update `.trivyignore` to suppress known CVEs.
3. Commit and push the changes.

**Example:**
```dockerfile
# Dockerfile
FROM python:3.11-slim
RUN pip install --no-cache-dir -r requirements.txt
USER nobody
```
```plaintext
# .trivyignore
CVE-2023-12345
```

---

### Suppress CVE in Trivyignore
**Trigger:** When someone wants to temporarily ignore specific CVEs during security scans.  
**Command:** `/suppress-cve`

1. Edit `.trivyignore` to add or update CVE entries.
2. Commit and push the changes.

**Example:**
```plaintext
# .trivyignore
CVE-2023-12345
CVE-2024-67890
```

---

## Testing Patterns

- **Framework:** Unknown (not explicitly detected)
- **File Pattern:** Test files are named using the pattern `*.test.*`
- **Example:**
  ```plaintext
  agentLogic.test.py
  simulationRunner.test.py
  ```
- **Note:** Ensure new tests follow this naming convention for consistency.

## Commands

| Command             | Purpose                                                      |
|---------------------|--------------------------------------------------------------|
| /update-funding     | Update project funding and sponsorship configuration         |
| /harden-dockerfile  | Apply security improvements or optimizations to Dockerfile   |
| /suppress-cve       | Suppress specific CVEs in vulnerability scans via Trivyignore|
```
