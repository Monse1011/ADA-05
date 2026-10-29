# Implicit Knowledge → Explicit Artifacts (ADA-08 Phase 3)

**Branch:** `ada08-agent-ready` (worktree `../ADA-05-ready`), created from baseline `2ad2060`.
**Inputs:**
- `REPOSITORY_READINESS_AUDIT.md` (Phase 1). It is kept outside the repository, at `~/Downloads`.
- `results/before-agent-run.md` and `results/baseline-environment.md` (Phase 2). They are kept untracked in the main checkout and were not copied here; see "Deviations".

## Knowledge inventory

| # | Implicit knowledge | Where it lived before | Evidence | Converted into | Classification |
|---|---|---|---|---|---|
| K1 | pytest is needed but not declared, so bare `pytest -v` fails | Owner's memory | Audit §1 (exit 127); BEFORE run (`command not found`) | `[project.optional-dependencies] dev` in `pyproject.toml`; `verify_repo.sh` detects a missing pytest and prints the install command | Executable Knowledge |
| K2 | The working interpreter is `~/.venv` (Python 3.9.6), which does not meet `requires-python >=3.10` | Owner's machine only | BEFORE run: the agent found `~/.venv` outside the repo; `baseline-environment.md` | `AGENTS.md` "Environment" section; `$PYTHON` selection in `verify_repo.sh`; a warning when the interpreter is older than 3.10 | Context + Executable Knowledge |
| K3 | There is no single "done" command | — | Audit §4.3, §5 | `scripts/verify_repo.sh` (contract check, then tests) as the Definition of Done | Executable Knowledge |
| K4 | ` REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, and `TASKS.md` must not be edited to fit code | `docs/AGENT_REPORT.md` "Human Interventions" | Audit §4.2 | SHA-256 contract in `check_repo_contract.py`; rule in `AGENTS.md`. A legitimate change requires the owner to approve and update the hash | Guardrail + Human Gate |
| K5 | The ADA-05 historical evidence in `docs/` must not be rewritten | Unstated | Audit §4.1, §4.8 | Same hash contract; labeled "historical" in `AGENTS.md` and `REPO_MAP.md` | Guardrail + Context |
| K6 | The requirements file name has a leading space and must not be renamed | `docs/AGENT_REPORT.md` problem 3 | Audit §4.1 | Rule in `AGENTS.md` and `CLAUDE.md`. The hash check fails if the file is renamed, because its expected path no longer exists | Context + Guardrail |
| K7 | Layer direction: the API never touches the repository, and dependencies point down | Only in `ARCHITECTURE.md` prose | Audit §4.4 | `ALLOWED_IMPORTS` check plus 3 unit tests that prove it rejects violations (`tests/test_repo_contract.py`) | Guardrail + Test |
| K8 | FR-07, FR-08, and NFR-04 were missing from traceability | Unnoticed | Audit §4.5 (grep) | 3 honest rows (Missing / Not verified) in `docs/TRACEABILITY.md`; a contract check that every FR/NFR has a row | Guardrail |
| K9 | Agents must stay inside the repository | `docs/AGENT_REPORT.md` problem 1; repeated in the BEFORE run | Audit §4.2; BEFORE run | Rule in `AGENTS.md`. **Not enforceable from inside the repository**; it depends on the agent's sandbox or permission settings | Context + Human Gate |
| K10 | Q-01..Q-05 are open and must not be decided by inference. Q-03..Q-05 appear only in SPEC.md | `SPEC.md` | Audit §4.5; BEFORE run (case-sensitivity choice) | A stop-condition rule in `AGENTS.md` (ask, or disclose as an assumption without asserting it in tests); listed in `REPO_MAP.md` | Context + Human Gate |
| K11 | Known stubs: the repository returns everything, the authorizer is fail-open, and the authorization check is never called | Code docstrings, `TRACEABILITY.md` | Audit §4.4, §4.8 | Listed in `AGENTS.md` and `REPO_MAP.md` as "change only within a scoped task" | Context |
| K12 | ARCHITECTURE.md describes the API validating and authorizing, an HTTP endpoint, and a UI, but the code differs | Unstated | Audit §4.1, §4.4 | "Known gaps" section in `REPO_MAP.md` | Navigation |
| K13 | There is no repository map or starting point | — | Audit §4.1 | `docs/REPO_MAP.md` (layout, imports, commands, documents, where to change what), linked from `AGENTS.md` | Navigation |
| K14 | A new test must fail without the change | Not stated | BEFORE run: the agent did not show its tests failing, and its prediction was incomplete | Rule in `AGENTS.md` "Tests" | Context |
| K15 | The same check should run in CI | — | Audit §4.6 (no CI) | `.github/workflows/verify.yml` calls `scripts/verify_repo.sh` and contains no duplicated logic | CI Check |
| K16 | Build artifacts (`*.egg-info/` and others) were not ignored | — | Audit §1 (egg-info produced) | `.gitignore` entries for `*.egg-info/`, `.venv/`, `build/`, `dist/` | Guardrail |
| K17 | Commits ended up with a non-collectable test suite (`e97dd36`) | — | Audit §4.6 | Not fully covered. CI catches it on push, but there is no pre-commit hook (it would need a dependency or a local hook install) | CI Check (partial) |

## Deliberately not done

- **No behavior tests for T-03 (TS-01..TS-05).** They would leak the Phase 4 task solution into the AFTER tree.
- **No fix for the fail-open authorizer or the validation placement.** These are functional changes and need a scoped task.
- **No lint or type checker.** None is configured, and adding one means a new dependency the project does not use.
- **No hard failure on Python <3.10.** The owner accepted the 3.9.6 environment for BEFORE and AFTER comparability, so the script warns instead. Rebuilding the venv on 3.10+ is a Human Gate.

## Deviations from the ADA-08 expected structure

- **Two AI usage logs.** `AI_USAGE_LOG.md` at the root is the ADA-08 log. `docs/AI_USAGE_LOG.md` is kept unchanged as protected ADA-05 evidence. The root file links to it.
- **Phase 1 and 2 evidence is not in this branch.**
  - The audit stays in `~/Downloads`.
  - The BEFORE evidence stays untracked in the main checkout (`/Users/monseanaya/Developer/ADA-05/results/`).
  - This keeps it intact and keeps the BEFORE observations from being visible to the AFTER agent. Consolidating them is a decision for the owner.
  - **Update (Phase 5):** with the owner's approval, the evidence was copied into this branch after the AFTER run: the audit, the `results/*-agent-run.md` files, `baseline-environment.md`, `TASK_UNDER_TEST.md`, and the agent diffs. The originals were left in place. Provenance and hashes are in `results/readiness-improvement-report.md` §2.
