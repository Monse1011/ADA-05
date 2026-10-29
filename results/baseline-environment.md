# Baseline Environment — ADA-08 (BEFORE)

**Date:** 2026-10-28
**Repository state:** `main` @ `2ad2060e720407975aa72db03bd8df62fa103def`, working tree clean before this file was added. Tag `ada08-baseline` not created yet.

## Environment accepted for BEFORE

| Item | Value |
|---|---|
| OS | macOS (Darwin 27.0.0, arm64) |
| Virtualenv | `~/.venv` (outside the repository, prepared by the owner) |
| Python in venv | 3.9.6 (`/usr/bin/python3` base) |
| pytest | 8.4.2 (pluggy 1.6.0) |
| Other interpreter available | Python 3.15.2 (`/opt/homebrew/bin/python3`, no pytest) |

## Known discrepancy (accepted by the owner)

`pyproject.toml` declares `requires-python = ">=3.10"`, but the BEFORE venv uses Python 3.9.6. pytest does not enforce `requires-python`, so the suite runs. This environment is accepted as-is for BEFORE; the same environment should be used for AFTER so results are comparable.

## Observed validation

The venv is not activated in the shell, so the literal `pytest -v` from `AGENTS.md` fails (`command not found`, exit 127). It was run with the venv path:

```bash
~/.venv/bin/pytest -v -p no:cacheprovider
```

```
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
configfile: pyproject.toml
testpaths: tests
collected 4 items
tests/test_project_setup.py::test_models_instantiation PASSED
tests/test_project_setup.py::test_repository_interface_and_implementation PASSED
tests/test_project_setup.py::test_validation_and_auth_components PASSED
tests/test_project_setup.py::test_layers_wiring_and_controller_reference PASSED
4 passed in 0.01s — exit 0
```

`-p no:cacheprovider` was used only to avoid creating `.pytest_cache/`; it does not change test selection or results.
