# AI Usage Log — ADA-08

ADA-08 AI usage only. The ADA-05 log is kept unchanged in [`docs/AI_USAGE_LOG.md`](docs/AI_USAGE_LOG.md).

## Entry 1: Phase 1, readiness audit

- **Tool:** Claude Opus 5.5 (claude.ai chat, Linux container).
- **Output:** `REPOSITORY_READINESS_AUDIT.md`. It was produced read-only and is stored outside the repository.

## Entry 2: Phase 2, BEFORE run

- **Orchestrator:** Claude Code (desktop app), `claude-opus-5-5`.
- **Preparation:**
  - Proposed `TASK_UNDER_TEST.md`, which the owner approved.
  - Created a detached worktree `../ADA-05-before` at `2ad2060`.
- **Agent under test:** a fresh Claude Code side session (`claude-opus-5-5`, effort medium, permission mode `auto`) given the official prompt.
- **Evidence:** `results/before-agent-run.md` and `results/baseline-environment.md` in the main checkout. Result: **PASS**, with friction around validation.

## Entry 3: Phase 3, readiness improvements

- **Tool:** Claude Code (desktop app), `claude-opus-5-5`.
- **Branch / worktree:** `ada08-agent-ready` at `../ADA-05-ready`, from `2ad2060`. No commits.
- **Human decisions:**
  - The owner told the agent to reuse the Phase 3 instructions, and to start from the original baseline in a separate branch.
  - The owner accepted the Python 3.9.6 venv in Phase 2.
- **AI-generated:**
  - `AGENTS.md` (rewritten), `CLAUDE.md`, `docs/REPO_MAP.md`.
  - `scripts/verify_repo.sh`, `scripts/check_repo_contract.py`, `tests/test_repo_contract.py`.
  - `.github/workflows/verify.yml`.
  - `results/implicit-knowledge.md` and this log.
  - Edits to `pyproject.toml` (dev extra), `.gitignore`, and `docs/TRACEABILITY.md` (3 rows).
- **Human review needed:**
  - The protected-file list and its hashes.
  - The `ALLOWED_IMPORTS` map.
  - The wording of the three new traceability rows.

### Commands and results

1. `PYTHON=~/.venv/bin/python scripts/verify_repo.sh`, before the traceability rows were added.
   - **exit 1**: `CONTRACT FAIL: requirement FR-07 / FR-08 / NFR-04 not traced in docs/TRACEABILITY.md`.
   - This is a real gap found by the new guardrail.
2. The same command after adding the rows: **exit 0**. The contract check passed, and **8 passed** (4 original + 4 contract tests). The Python <3.10 warning was printed.
3. `scripts/verify_repo.sh` with no `$PYTHON` set (it falls back to `python3` = Homebrew 3.15.2, which has no pytest).
   - **exit 2**, with the install hint printed. This is the expected guided failure.
4. Negative guardrail cases, each run on a scratch copy with `check_repo_contract.py`:
   - A line appended to `SPEC.md` → exit 1, "protected file modified".
   - The API importing the repository → exit 1, "layer violation".
   - ` REQUIREMENTS.md` renamed: the first run **crashed with a `FileNotFoundError` traceback**. The script was fixed to skip the traceability check when the file is missing. On re-run → exit 1, "protected file missing".
5. Final `PYTHON=~/.venv/bin/python scripts/verify_repo.sh` → exit 0, 8 passed.
6. Baseline preserved:
   - `git diff --quiet 2ad2060 -- customer_search tests/test_project_setup.py <protected files>` → identical.
   - The main checkout is still at `2ad2060`.
   - The BEFORE worktree and its evidence files are untouched.
7. **Not verified:**
   - The GitHub Actions workflow was not run, because nothing was pushed.
   - `pip install -e '.[dev]'` was not run locally, because it requires installing dependencies.
