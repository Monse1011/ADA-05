# Readiness Improvement Report — ADA-08

**Repository:** `Monse1011/ADA-05` (Customer Search, Python)
**Date:** 2026-10-28
**Prepared by:** Claude Code (desktop app, `claude-opus-5-5`) under the owner's direction. Every phase was authorized by the owner.

## 1. Executive Summary

- **Readiness score:** **39.0 → 77.0 / 100 (+38.0 points)**, using the same 8 dimensions and weights. The delta exceeds the recommended +15. The total stays below the recommended 80.
- **Task result:** the same task (substring search, FR-01 to FR-03) and the same official prompt gave **PASS** in both BEFORE and AFTER.
- **What changed in the process:**
  - BEFORE had two failed validation commands and found the interpreter on its own, outside the repository. It did not demonstrate that its tests failed before the change.
  - AFTER had no failed commands, used the documented verification script, and showed red-then-green evidence.
- **Causality:** these differences are consistent with the Phase 3 changes. With one run per side and the other variables in §10, they are not proof that the changes caused them.

## 2. Baseline and Evaluation Setup

| Item | BEFORE | AFTER |
|---|---|---|
| Base commit | `2ad2060e720407975aa72db03bd8df62fa103def` (`main`) | `7d0618d723bbeb1fef1b9a17ba3ed64b824028db` (`ada08-agent-ready`; parent `2ad2060`) |
| Worktree | `../ADA-05-before` (detached) | `../ADA-05-after` (detached) |
| Task file | `TASK_UNDER_TEST.md`, SHA-256 `0f165144…fbbf` | Same hash |
| Prompt | Official ADA-08 prompt, unchanged | Same |
| Launcher preamble | "Evaluation run. Work only inside the current working folder. No additional context is provided beyond the prompt." | Same |
| Agent / model | Claude Code side session, `claude-opus-5-5`, effort medium | Same |
| Permission mode | `auto` | `auto` |
| Python | `~/.venv`: 3.9.6, pytest 8.4.2 | Same |
| Session time (UTC) | 04:07:33–04:08:13, 12 turns | 04:23:26–04:24:21, 13 turns |

`2ad2060..7d0618d` changes 12 files (+409/−5). It contains **no changes** to `customer_search/`, `tests/test_project_setup.py`, or the protected documents. Verified with `git diff --quiet`.

### Evidence location and provenance

All files below are in branch `ada08-agent-ready` (worktree `../ADA-05-ready`) and are uncommitted.

| File | Origin | SHA-256 | Note |
|---|---|---|---|
| `REPOSITORY_READINESS_AUDIT.md` | Copy of `~/Downloads/REPOSITORY_READINESS_AUDIT.md` (`f21aa358…84d4`), then completed with AFTER | — (edited) | The original in Downloads is unchanged |
| `results/baseline-environment.md` | Copy of `main` checkout `results/` | `6ab9f98f…9f24` | Identical to the original |
| `results/before-agent-run.md` | Same | `b09a8ebb…dfb8dc` | Identical to the original |
| `results/after-agent-run.md` | Same | `add92cbf…b76c` | Identical to the original |
| `TASK_UNDER_TEST.md` | Copy from `../ADA-05-before` | `0f165144…fbbf` | Same hash as the AFTER copy |
| `results/before-agent-run.diff` | `git diff` of `../ADA-05-before`, plus the untracked test | `612af3b8…b6e6b482` | Text only, not applied |
| `results/after-agent-run.diff` | `git diff` of `../ADA-05-after`, plus the untracked test | `d40598b0…87c0` | Text only, not applied |

The originals in the `main` checkout (`/Users/monseanaya/Developer/ADA-05/results/`) and in `~/Downloads` remain the source copies.

## 3. Initial Readiness Findings

From the Phase 1 audit, §5:
1. **Agent instructions were nearly empty.** Critical rules lived in human memory or in historical reports: the protected specs, the workspace rule, the open questions, and the Definition of Done.
2. **There was no reproducible verification contract.** `pytest -v` failed with exit 127 because pytest was undeclared. There was no script, CI, or guardrail.
3. **Navigation and traceability hazards:**
   - There was no README or repository map.
   - The requirements file name has a leading space.
   - FR-07, FR-08, and NFR-04 were untraced.
   - The tests checked structure only.

## 4. Implicit Knowledge Identified

`results/implicit-knowledge.md` lists 17 items (K1–K17), each with its source, evidence, conversion, and classification. The most consequential ones, as confirmed by the runs:
- **K1/K2:** pytest is undeclared, and the working interpreter is an off-repository `~/.venv` on Python 3.9.6. The BEFORE agent hit both.
- **K4/K5/K6:** the specifications and ADA-05 evidence must not be edited, and the leading-space file name must not be "fixed".
- **K10:** Q-01 to Q-05 are stop conditions.
- **K14:** a new test must be shown to fail without the change. The BEFORE agent skipped this; the AFTER agent did it.

## 5. Readiness Improvements Implemented

Commit `7d0618d`, Phase 3:

| Improvement | Classification | Evidence |
|---|---|---|
| `AGENTS.md` rewritten: sources of truth, DoD, environment, rules, stop conditions | Context | File at `7d0618d` |
| `CLAUDE.md` imports `AGENTS.md`, with no duplicated rules | Context | `@AGENTS.md` and 2 notes |
| `docs/REPO_MAP.md` | Navigation | Layout, imports, commands, documents, gaps, where to change what |
| `scripts/verify_repo.sh`: single command, interpreter selection, guided failure when pytest is missing | Executable Knowledge | Exit 0 / exit 2 runs (§8) |
| `pyproject.toml` dev extra `pytest` | Executable Knowledge | File |
| Protected-file SHA-256 contract | Guardrail + Human Gate | Negative run: SPEC edit → exit 1 |
| Layer import contract | Guardrail | Negative run: API imports repository → exit 1 |
| Traceability coverage contract, plus 3 new rows | Guardrail | First run exit 1 (FR-07, FR-08, NFR-04), then exit 0 |
| `tests/test_repo_contract.py` (4 tests) | Test | Pass |
| `.github/workflows/verify.yml` calls `verify_repo.sh` | CI Check | Defined; **never run** |
| `.gitignore` build artifacts | Guardrail | File |
| Workspace rule, open questions as stop conditions | Context + Human Gate | `AGENTS.md` |

Deliberately not done:
- T-03 behavior tests, which would solve the AFTER task in advance.
- Fixes to the authorizer or the validation placement, which are functional changes.
- Lint, which would be a new dependency.
- A hard failure on Python <3.10, because the owner accepted 3.9.6.
- A `README.md`, which ADA-08 §21 lists. **This is a remaining gap.**

## 6. BEFORE vs AFTER Score Comparison

| # | Dimension | Weight | BEFORE | BEFORE pts | AFTER | AFTER pts | Δ pts |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Entry Point & Navigation | 15 | 2 | 6.0 | 4 | 12.0 | +6.0 |
| 2 | Agent Instructions | 15 | 1 | 3.0 | 4 | 12.0 | +9.0 |
| 3 | Build / Run / Test | 15 | 2 | 6.0 | 4 | 12.0 | +6.0 |
| 4 | Architecture Boundaries | 10 | 3 | 6.0 | 4 | 8.0 | +2.0 |
| 5 | Requirements & Traceability | 10 | 3 | 6.0 | 4 | 8.0 | +2.0 |
| 6 | Automation & Guardrails | 10 | 1 | 2.0 | 4 | 8.0 | +6.0 |
| 7 | Testability & Evidence | 15 | 2 | 6.0 | 3 | 9.0 | +3.0 |
| 8 | Safety & Permissions | 10 | 2 | 4.0 | 4 | 8.0 | +4.0 |
| | **Total** | **100** | | **39.0** | | **77.0** | **+38.0** |

Points per dimension are `score / 5 × weight`. The justification for each dimension is in `REPOSITORY_READINESS_AUDIT.md` §7.

No dimension reaches 5, because each one still has an open item: README, CI execution, environment version, unenforceable rules, or product behavior tests. The BEFORE scores were not changed (audit §8).

## 7. Agent Execution Comparison

| Indicator | BEFORE | AFTER | Type |
|---|---|---|---|
| Clarification questions | 0 | 0 | Fact |
| Failed / unknown commands | 2 (`pytest -v`: command not found; `python3 -m pytest -v`: No module named pytest) | 0 | Fact (agent reports) |
| Incorrect assumptions | 1: predicted that only TS-02..TS-05 would fail on the stub; all 5 fail | 0 | Fact (verified by evaluator) |
| Out-of-scope files modified | 0 | 0. `docs/TRACEABILITY.md` was updated per `AGENTS.md`; the FR-01 note says "name" instead of "name or email" | Fact |
| Files changed | Repository (1 line) and a new test file | Repository (1 line), a new test file, `docs/TRACEABILITY.md` | Fact |
| Validation executed | pytest via `~/.venv` (9 passed) | `scripts/verify_repo.sh` (contract OK and 13 passed) | Fact |
| Red step shown by the agent | No | Yes (5 failed before the change) | Fact |
| Interpreter discovery | Found `~/.venv` outside the folder, undocumented | Used the `AGENTS.md`-documented path | Fact (how BEFORE found it: not visible) |
| Case sensitivity (Q-03) | Case-sensitive; disclosed in the report | Case-sensitive; disclosed in the report, docstring, and test module | Fact |
| Final result | PASS | PASS | Fact |
| Files read during exploration | Not verifiable | Not verifiable | Limitation |

**Inferences (not proven):**
- The disappearance of failed commands and of the off-repository search is consistent with `AGENTS.md` "Environment".
- The red step is consistent with the `AGENTS.md` test rule.
- The traceability update is consistent with the `AGENTS.md` sources-of-truth rule.

## 8. Validation and CI Evidence

All runs used `~/.venv` (Python 3.9.6, pytest 8.4.2) on macOS. All were observed directly.

| Command | Where | Result |
|---|---|---|
| `~/.venv/bin/pytest -v -p no:cacheprovider` | `main` at `2ad2060` | 4 passed, exit 0 |
| `PYTHON=~/.venv/bin/python scripts/verify_repo.sh` (first run) | Phase 3, before the traceability rows | exit 1: FR-07 / FR-08 / NFR-04 not traced |
| Same command | `7d0618d` (`ADA-05-ready`) | exit 0, contract OK, 8 passed (re-run in Phase 4 and Phase 5) |
| `scripts/verify_repo.sh` with no `$PYTHON` | `ADA-05-ready` | exit 2, install hint |
| `check_repo_contract.py` on scratch copies | SPEC edit / layer import / rename | exit 1 each. Rename first crashed, then was fixed |
| BEFORE tests on clean `2ad2060` | Scratch export | 5 failed, 4 passed |
| `verify_repo.sh` | `ADA-05-after` | exit 0, 13 passed |
| `pytest tests/test_search_matching.py` | `ADA-05-after` | 5 passed |
| AFTER tests on clean `7d0618d` | Scratch export | 5 failed, 8 passed |

**The verify script and the feature evidence are separate things.** `verify_repo.sh` exiting 0 shows repository health. The feature evidence is the task tests passing with the change *and* failing without it.

**CI:** `.github/workflows/verify.yml` exists, but it has **not run on GitHub Actions**, because nothing was pushed. `pip install -e '.[dev]'`, the workflow's install step, was not run locally.

## 9. Questions, Assumptions, Failed Commands and Out-of-Scope Changes

- **Questions:** none in either run.
- **Assumptions:**
  - Both runs implemented case-sensitive matching (Q-03 is open), disclosed it, and did not assert it in tests. This follows `TASK_UNDER_TEST.md`.
  - BEFORE also made an incomplete prediction about which tests would fail.
- **Failed commands:** BEFORE had 2; AFTER had 0. There were none in either run outside validation.
- **Out-of-scope changes:** none in either run. The AFTER traceability edit is a documented repository convention. One wording issue is noted.

## 10. Limitations and Threats to Validity

1. **One run per side** with a non-deterministic model, so variance is unknown.
2. **The compact transcripts omit tool arguments.** Exploration paths and file reads cannot be verified.
3. **The app context differed.** The AFTER session was shown a sibling session (`ada08-before`) and the means to message it. No such call appears in its transcript.
4. **Evidence and experiment were designed by the same orchestrator.** It also wrote the improvements and scored them, so there was no independent scorer.
5. **The AFTER tree contained `results/implicit-knowledge.md` and `AI_USAGE_LOG.md`.** They describe BEFORE friction in general terms, which could prime the agent, but contain no task solution.
6. **User-level configuration** (`~/.claude/CLAUDE.md` in Spanish, the `ponytail` plugin) applied to both runs. It is constant but uncontrolled.
7. **Environment:** Python 3.9.6 is below `requires-python >=3.10`. The Phase 1 audit validated on 3.12.3 and pytest 9.2.0.
8. **The task was small and BEFORE already passed**, so the effect shows up in process and evidence, not in the outcome.
9. **The BEFORE scores used the audit's own anchors.** They were re-checked against the ADA-08 anchors and are consistent, but the re-check was done by the same evaluator.

## 11. Remaining Risks and Human Decision Points

| Item | Decision owner |
|---|---|
| Push the branch so CI runs for the first time, and review the result | Owner |
| Rebuild the venv on Python ≥3.10, or change `requires-python` | Owner |
| Answer Q-01..Q-05, especially Q-02 (relevance) and Q-03 (case) | Product owner |
| `CustomerSearchAuthorizer` is fail-open and the authorization check is never called (FR-06, NFR-02) | Scoped task + owner |
| Add FR-07, FR-08, and NFR-04 to `SPEC.md` (protected; hash update needed) | Owner |
| Add `README.md` (listed in ADA-08 §21) | Owner |
| Approve the protected-file hashes and `ALLOWED_IMPORTS` | Owner |
| Commit the Phase 5 documents; create the `ada08-baseline` tag if wanted | Owner |
| The workspace rule cannot be enforced in the repository; it needs sandbox or permission settings | Owner |

## 12. Final Conclusion

Phase 3 converted the main pieces of tribal knowledge into instructions, a map, one verification command, and a deterministic contract check. It did so without touching product code or specifications.

On the same task, the AFTER agent produced the same correct implementation as BEFORE. It did so with no failed commands, through the documented verification path, and with red-then-green evidence. The readiness score rose from 39 to 77 (+38), short of the recommended 80. The shortfall comes from items that need human action: running CI, aligning the Python version, adding a README, and the product test gaps that were deliberately left open.

The comparison supports the conclusion that the agent had less uncertainty and produced better evidence. It does not establish causality, because of the limitations in §10.
