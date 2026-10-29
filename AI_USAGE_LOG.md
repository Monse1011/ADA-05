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
  - *Correction (Phase 5):* this was true when written. Afterwards, at the owner's explicit instruction, the Phase 3 changes were committed as `7d0618d`. They were not pushed.
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

## Decision log (Phase 5 consolidation)

Each entry records the decision, why it was made, and its status. The statuses reflect the owner's choices recorded in this session. No alternatives are claimed beyond those actually presented.

### D1: Initial audit and its validation

- **Decision:** accept the Phase 1 audit (39.0/100) as the BEFORE baseline. Keep it unchanged.
- **Justification:** several of its claims were re-observed locally:
  - `pytest -v` fails because pytest is not installed.
  - `main` is at `2ad2060`.
  - FR-07, FR-08, and NFR-04 were untraced; the first contract run caught exactly these.
- **Differences found:**
  - The audit ran in a container with Python 3.12.3 and pytest 9.2.0; the local runs used 3.9.6 and 8.4.2.
  - The path-with-space claim is outdated.
  - Q-03 to Q-05 appear only in `SPEC.md`.
  - These are recorded in audit §8. No BEFORE score was changed.
- **Status:** accepted.

### D2: Environment for BEFORE and AFTER

- **Decision:** use the owner-prepared `~/.venv` (Python 3.9.6, pytest 8.4.2), even though it does not meet `requires-python >=3.10`.
- **Justification:** the owner chose "Aceptar y documentar" when offered the choice between this and rebuilding the venv with 3.15. Using one environment for both runs keeps them comparable.
- **Status:** accepted by the owner. Rebuilding on 3.10 or later is pending.

### D3: Design of `AGENTS.md`

- **Decision:** make `AGENTS.md` the single source of agent instructions.
  - It contains sources of truth, the Definition of Done, the environment, rules, stop conditions, and known stubs.
  - `CLAUDE.md` only imports it with `@AGENTS.md` and adds 2 Claude-specific notes.
  - Product requirements are not copied into either file.
- **Justification:** avoid duplicate sources of truth (ADA-08 §21). Every rule traces to an audit finding or a BEFORE observation (`results/implicit-knowledge.md`).
- **Excluded on purpose:** solution hints for the T-03 task.
- **Status:** accepted. It was committed in `7d0618d` on the owner's instruction. The owner has not yet reviewed it line by line.

### D4: Selection of guardrails

- **Decision:** automate three checks in `scripts/check_repo_contract.py`:
  - SHA-256 of the protected specification and history files;
  - the layer import direction from `ARCHITECTURE.md`;
  - an FR/NFR row in `docs/TRACEABILITY.md` for every requirement.
- **Justification:** each check targets a rule that was previously only human memory or prose, and that an agent could break without noticing.
- **Rejected in Phase 3, by the agent with reasons stated to the owner:**
  - Lint, because it would be a new dependency.
  - A pre-commit hook, because it needs a local install step.
  - A hard failure on Python <3.10, because it conflicts with D2.
  - T-03 behavior tests, because they would leak the AFTER solution.
- **Status:** accepted. The hashes and `ALLOWED_IMPORTS` are pending the owner's review.

### D5: Discoverability and implicit knowledge

- **Decision:** convert the hidden knowledge into executable or checked form where possible, and into instructions only where it cannot be enforced (`results/implicit-knowledge.md`).
  - Executable or checked: the interpreter selection, the missing-pytest message, the protected files, layers, and traceability.
  - Instructions only: the workspace rule and the open questions.
- **Justification:** the ADA-08 instruction not to solve everything with documentation.
- **Status:** accepted. Workspace confinement remains a human gate.

### D6: CI

- **Decision:** `.github/workflows/verify.yml` installs `.[dev]` and calls `scripts/verify_repo.sh`, with no duplicated logic. The agent, the human, and CI share the same contract and test run.
- **Justification:** one verification definition for everyone.
- **Status:** accepted. It has **never been executed on GitHub**, because nothing was pushed. That run is pending the owner's push.

### D7: Changes observed during AFTER

- **Observation:** on the same task, prompt, model, and environment (only the commit differs: `7d0618d` vs `2ad2060`), the AFTER agent:
  - had 0 failed commands, against 2 in BEFORE;
  - used `scripts/verify_repo.sh` with the documented interpreter;
  - showed its new tests failing before the change;
  - updated the traceability matrix.
- **Result:** both runs gave PASS.
- **Interpretation:** consistent with `AGENTS.md`, but not proof of causation (report §10).
- **Status:** recorded in `results/after-agent-run.md`.

### D8: Final evaluation and remaining human intervention

- **Decision:** score AFTER at 77.0/100 (+38.0). Report it below the recommended 80 without adjusting any score.
- **Justification:** each dimension keeps an open item that needs a human:
  - running CI;
  - aligning the Python version;
  - adding a README;
  - answering Q-01..Q-05;
  - fixing the fail-open authorizer in a scoped task;
  - enforcing the workspace rule through sandbox settings.
- **Status:** submitted for the owner's review.

### D9: Documentation consolidation

- **Decision:** copy the audit, the BEFORE/AFTER evidence, `TASK_UNDER_TEST.md`, and the agent diffs into `ada08-agent-ready`, uncommitted. The originals stay in `~/Downloads` and in the `main` checkout. Hashes are listed in report §2.
- **Justification:** ADA-08 §21 expects them in the repository, and the copies keep a verifiable link to the originals.
- **Status:** approved by the owner ("Aprobar plan", including the diffs). Committing them is pending.
