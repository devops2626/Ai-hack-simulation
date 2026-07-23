Title: chore: suppress CVE-2026-8376 and force linux/amd64 to avoid 32-bit perl issue

This PR:

- Adds .trivyignore to suppress CVE-2026-8376 until Debian upstream provides a fix.
- Forces --platform=linux/amd64 on both Dockerfile stages to avoid the 32-bit perl build affected by the CVE.

Rationale:
The perl-base package in the python:3.11-slim base image contains CVE-2026-8376 with no fixed Debian package yet; suppressing the Trivy alert prevents CI failures while forcing the AMD64 platform avoids the 32-bit-only impact of the vulnerability.

No functional code changes beyond the Docker platform pinning and Trivy ignore of the known-but-unfixed base image CVE.
