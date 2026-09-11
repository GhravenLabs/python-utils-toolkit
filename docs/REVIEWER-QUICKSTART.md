# Reviewer Quickstart

This toolkit is a small standard-library utility collection for automation and agent-workflow projects.

## What to inspect first

1. `README.md` for the module list and short examples.
2. `utils/` for implementation style.
3. `tests/` for behavior coverage.
4. `CHANGELOG.md` for release history.

## Local verification

```bash
python -m pytest
```

The project is intentionally dependency-light. If a future utility needs an external package, document why the standard library was not enough.

