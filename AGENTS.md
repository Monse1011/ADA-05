# Agent Guidelines

Customer Search is a Python library implementing a layered customer search. It has no HTTP server and no UI. For the map of files and layers, see [`docs/REPO_MAP.md`](docs/REPO_MAP.md).

## Sources of truth (read first)

1. ` REQUIREMENTS.md`: requirements FR-01..FR-08 and NFR-01..NFR-04, plus open questions.
   - **The file name starts with a space.** Always quote it (`" REQUIREMENTS.md"`), and do not rename it.
2. `SPEC.md`: acceptance criteria AC-01..AC-09, test scenarios TS-01..TS-12, and open questions Q-01..Q-05.
3. `ARCHITECTURE.md`: layers and data flow.
4. `TASKS.md`: tasks T-01..T-06.
5. `docs/TRACEABILITY.md`: the current status of each requirement. This is a living document; update it when coverage changes.

`docs/AGENT_REPORT.md` and `docs/AI_USAGE_LOG.md` are historical ADA-05 evidence, not instructions.

## Verify (Definition of Done)

```bash
scripts/verify_repo.sh
```

The script runs two things:
- the repository contract check, `scripts/check_repo_contract.py`;
- the full pytest suite.

A change is done only when the script exits 0 and you report the command and its output. CI runs the same script in `.github/workflows/verify.yml`.

### Environment

- `pytest` is a dev dependency and is not installed globally. A bare `pytest -v` fails with `command not found` unless an environment is active.
- The script uses the first interpreter it finds, in this order: `$PYTHON`, then `./.venv/bin/python`, then `python3`.
- On the owner's machine, run `PYTHON=~/.venv/bin/python scripts/verify_repo.sh`.
  - That environment is Python 3.9.6 with pytest.
  - The script warns that `pyproject.toml` asks for Python >=3.10. This is a known, accepted gap.
- If pytest is missing, the script exits with code 2 and prints the install command. **Do not install dependencies or create environments without the owner's approval.**

## Rules

- **Stay inside this repository.** Do not read or modify sibling directories or the home folder. The only exception is the interpreter named above.
- **Protected files:**
  - ` REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md`, `docs/AGENT_REPORT.md`, `docs/AI_USAGE_LOG.md`.
  - The contract check fails if any of them changes.
  - Never edit a specification to fit an implementation. If one looks wrong, stop and report it.
- **Layers:** keep the dependency direction that the contract check enforces (see `docs/REPO_MAP.md`). The API never imports the repository.
- **Open questions are stop conditions.**
  - Do not decide Q-01..Q-05: displayed fields, relevance order, case sensitivity, the no-results message, and the empty query.
  - If a task depends on one of them, ask.
  - If the code must pick a behavior anyway, do not assert it in tests, and report it as an assumption.
- **Known stubs.** Change these only within a scoped task:
  - `InMemoryCustomerRepository.search_customers` returns all customers.
  - `CustomerSearchAuthorizer` allows everything (fail-open).
  - Production code never calls `is_user_authorized_for_search`.
- **Tests:**
  - Never delete or weaken existing tests.
  - A new behavior test must fail without your change. Show that it does.
- **No commits, pushes, tags, or deletions** unless the owner asks.
