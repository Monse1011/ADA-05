# BEFORE Agent Run — ADA-08 Phase 2

**Date:** 2026-10-28 (session timestamps 2026-10-29T04:07:33Z–04:08:13Z UTC)
**Task:** `TASK_UNDER_TEST.md` — substring search by name and email (T-03, FR-01 to FR-03). The task was approved by the repository owner before the run.

## Run Context

| Item | Value | Source |
|---|---|---|
| Agent | Claude Code (Claude desktop app, Code tab), side session "ADA-08 BEFORE agent run" (`local_0b50bc80-04d5-4b6d-a87e-59b6b32150d3`) | session metadata |
| Model | `claude-opus-5-5`, effort `medium` | session metadata |
| Tools | Claude Code default toolset (Bash, Read, Edit, Write, and others). The compact transcript shows these calls: `update_plan` ×2, `Bash` ×6, `Edit` ×1, `Write` ×1, `wrap_up` ×1 | transcript |
| Permissions | Permission mode `auto`. No permission prompts or denials are recorded | session metadata |
| Baseline commit | `2ad2060e720407975aa72db03bd8df62fa103def` ("Creacion de archivos"). No tag (`ada08-baseline` not created) | `git rev-parse HEAD` in worktree |
| Worktree | `/Users/monseanaya/Developer/ADA-05-before`, created with `git worktree add --detach ../ADA-05-before 2ad2060`. Its only addition before the run was the untracked `TASK_UNDER_TEST.md` | `git worktree list`, `git status` |
| Python environment | `~/.venv` (outside the repo): Python 3.9.6, pytest 8.4.2. See `results/baseline-environment.md` | command output |

### Instructions available to the agent

- **Prompt:** the official ADA-08 prompt, unchanged.
- **Preamble from the launcher:** the desktop app requires a `background` field when a session is started from another session. It was set to:
  > Evaluation run. Work only inside the current working folder. No additional context is provided beyond the prompt.

  The app also prepended a line pointing to a shared notes folder for sibling sessions. It was empty and unused.
- **Repository instructions:** `AGENTS.md` from the baseline, 13 lines, `pytest -v` only. There was no `CLAUDE.md` in the repository.
- **User-level configuration (not part of the repository):**
  - `~/.claude/CLAUDE.md`, the owner's global preferences. Among other things it says: reply in Spanish, ask before installing dependencies, never put secrets in code.
  - The `ponytail` plugin, which loads at session start.

  Both apply to every session on this machine. They are not Phase 3 improvements, but they were available to the agent. The agent replied in Spanish, which is consistent with the global `CLAUDE.md` being loaded. Whether `ponytail` was active cannot be confirmed from the transcript.
- **Phase 3 artifacts:** none were present, because no `docs/REPO_MAP.md`, scripts, or CI exist at `2ad2060`.

## Clarification Questions

None. The agent asked no questions before or during the run.

## Repository Exploration

The compact transcript records tool *calls* but not their arguments. The exact files and commands used during exploration therefore **cannot be verified**.

From the agent's final report:
- It identified the repository layer and the `ICustomerRepository` interface as the place where filtering belongs.
- It referenced the architecture ("según la arquitectura") and the layering of service, controller, and repository.
- It treated `TASK_UNDER_TEST.md` as authoritative for the no-commit rule and the Q-03 handling.

**Exploration outside the working folder:** the agent ran pytest from `~/.venv`, which sits outside the repository and is not mentioned in any repository file. To use it, the agent must have discovered that path outside the working folder, although how it did so is not visible in the compact transcript. This goes against the launcher preamble ("Work only inside the current working folder"). It was read-only and nothing outside the worktree was modified, which was checked with `git status` in the main checkout.

## Incorrect Assumptions

1. **Expected failures were predicted but not executed.**
   - The agent did not run the new tests against the old code. It predicted that "TS-02 to TS-05 would fail".
   - Independent re-run: **all 5** new tests fail on the baseline, including TS-01, because the stub returns all 3 fixture customers. The prediction was incomplete. See Validation Evidence.
2. **Case sensitivity (Q-03).** The implementation (`query in c.name or query in c.email`) is case-sensitive. The agent reported this as an assumption and added no test that asserts it, as the task requires. This is an implementation choice on an open question that was correctly disclosed. It is not an unsupported business rule.

No invented requirements were found. FR-04 ordering, authorization, empty-query behavior, and validation were not touched.

## Failed / Unknown Commands

Reported by the agent; failure messages as quoted in its report:

| Command | Result |
|---|---|
| `pytest -v` (literal from `AGENTS.md`) | Failed: `command not found` (pytest not on `PATH`) |
| `python3 -m pytest -v` | Failed: `No module named pytest` |
| `~/.venv/bin/python -m pytest -v` | Succeeded: 9 passed |

The documented validation command did not work as written. The agent recovered only by using an environment outside the repository that is not documented in the repository. The agent also noted the mismatch between the venv's Python 3.9 and `requires-python >=3.10`.

## Out-of-Scope Changes

None found in source or documentation:
- `git diff` shows only `customer_search/repositories/customer_repository.py`.
- Specification files, `AGENTS.md`, `docs/`, and `pyproject.toml` are unchanged.
- No commit was created; `HEAD` is still `2ad2060`.

A side effect of running pytest: `.pytest_cache/` was created in the worktree. It is ignored by `.gitignore`.

## Validation Evidence

### Files changed by the agent

- **Modified** `customer_search/repositories/customer_repository.py`: `InMemoryCustomerRepository.search_customers` now returns `[c for c in self._customers if query in c.name or query in c.email]`. The baseline stub returned all customers.
- **Added** `tests/test_substring_search.py`: 5 tests covering TS-01 to TS-05.
  - Customers are compared by ID sets, so TS-02 asserts no order.
  - Queries use the same letter case as the stored data.
  - The fixture contains a non-matching customer (`Alice Green`), so exclusion is checked.

### Executed by the agent (reported)

`~/.venv/bin/python -m pytest -v` → **9 passed in 0.02s**: 4 existing tests and 5 new ones.

### Executed independently by the evaluator (after the run)

1. **Suite in the BEFORE worktree:**

   ```bash
   cd /Users/monseanaya/Developer/ADA-05-before && ~/.venv/bin/pytest -v -p no:cacheprovider
   ```

   Result: 9 passed in 0.02s, exit 0. Every test is listed as PASSED, both the 4 in `test_project_setup.py` and the 5 in `test_substring_search.py`.

2. **New tests against the unmodified baseline code.** A clean export of `2ad2060` was made with `git archive` into a scratch folder, `tests/test_substring_search.py` was copied in, and `~/.venv/bin/pytest -q` was run.

   Result: **5 failed, 4 passed**. All five new tests fail, so they do detect the missing behavior.

### Recommended but not executed

None beyond the above. The agent ran no linting or type checking, and none is configured in the repository.

## Final Result

**PASS.**
- The requested behavior was implemented in the layer the architecture specifies.
- TS-01 to TS-05 are covered by new tests that pass with the change and fail without it.
- The existing tests still pass, and no test was removed or weakened.
- No specification file was modified.
- The open questions were respected, and the case-sensitivity choice was disclosed.

**Friction observed (input for Phase 3, not a failure of the task):**
- The documented validation command `pytest -v` failed in this environment.
- Validation depended on an undocumented environment outside the repository, which the agent found by looking beyond the working folder.
- The agent did not show its new tests failing on the old code, and its prediction about which tests would fail was incomplete.
- The exploration steps are not reconstructable from the available transcript.
