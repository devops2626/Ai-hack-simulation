---
name: dockerfile-security-hardening
description: Workflow command scaffold for dockerfile-security-hardening in Ai-hack-simulation.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /dockerfile-security-hardening

Use this workflow when working on **dockerfile-security-hardening** in `Ai-hack-simulation`.

## Goal

Improves Dockerfile security or optimizes build process, often in response to CVEs.

## Common Files

- `Dockerfile`
- `.trivyignore`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit Dockerfile to improve security or build process.
- Optionally update .trivyignore to suppress known CVEs.
- Commit and push the changes.

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.