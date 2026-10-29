# AFTER Agent Run — ADA-08 Phase 4

**Date:** 2026-10-28. Session timestamps: 2026-10-29T04:23:26Z–04:24:21Z UTC.
**Task:** `TASK_UNDER_TEST.md`, the same file as in BEFORE. SHA-256 `0f165144be0e3e97facac1716116b417a71616316fea5d552a65f773d3f3fbbf` was checked in both worktrees.

## Run Context

| Item | Value | Source |
|---|---|---|
| Agent | Claude Code (Claude desktop app, Code tab), side session "ADA-08 AFTER agent run" (`local_adfae825-749f-44cc-a03c-1953d24ae84a`) | session metadata |
| Model | `claude-opus-5-5`, effort `medium` (same as BEFORE) | session metadata |
| Tools | Claude Code default toolset. The compact transcript shows `update_plan` ×2, `Bash` ×6, `Write` ×1, `Edit` ×2, `wrap_up` ×1. There were no `SendMessage` or `list_events` calls | transcript |
| Permissions | Permission mode `auto` (same as BEFORE). No prompts or denials are recorded | session metadata |
| Base commit | `7d0618d723bbeb1fef1b9a17ba3ed64b824028db` on `ada08-agent-ready`. Its parent is `2ad2060`, and it contains no product-code changes compared with `2ad2060` | `git log`, `git diff --quiet 2ad2060 7d0618d -- customer_search` |
| Worktree | `/Users/monseanaya/Developer/ADA-05-after`, created with `git worktree add --detach ../ADA-05-after 7d0618d`. Its only addition before the run was the untracked `TASK_UNDER_TEST.md` | `git worktree list`, `git status` |
| Python environment | `~/.venv`: Python 3.9.6, pytest 8.4.2 (same as BEFORE) | command output |

### Pre-run checks (all passed)

- `main` = `2ad2060`.
- `7d0618d` is contained only in `ada08-agent-ready`, and `2ad2060` is its ancestor.
- The BEFORE worktree is at `2ad2060`. `7d0618d` has no `tests/test_substring_search.py` and no changes under `customer_search/`, so the BEFORE implementation was not carried over.
- The `ADA-05-ready` working tree was clean, and `PYTHON=~/.venv/bin/python scripts/verify_repo.sh` gave exit 0 with 8 passed, which reproduces Phase 3.

### Instructions available to the agent

- **Prompt and preamble:** the official prompt, unchanged, and the same preamble as BEFORE ("Evaluation run. Work only inside the current working folder. No additional context is provided beyond the prompt."). The app also added the shared-notes line; that folder was empty.
- **Repository instructions at `7d0618d`:**
  - `AGENTS.md`, `CLAUDE.md` (imports `AGENTS.md`), `docs/REPO_MAP.md`.
  - `scripts/verify_repo.sh`, `scripts/check_repo_contract.py`, `tests/test_repo_contract.py`, `.github/workflows/verify.yml`.
  - `results/implicit-knowledge.md` and `AI_USAGE_LOG.md`. These two describe BEFORE friction in general terms, for example that "a new test must fail without the change", but contain no task solution.
- **User-level configuration:** the same as BEFORE (`~/.claude/CLAUDE.md` and the `ponytail` plugin).
- **Difference from BEFORE in the app context:** the AFTER session's first message carried a system note listing the sibling session `ada08-before` and how to message it. The transcript shows no call that used it.

## Clarification Questions

None. The agent asked no questions before or during the run.

## Repository Exploration

The compact transcript records tool *calls* but not their arguments, so the exact files read **cannot be verified**.

From the agent's report and its output:
- It followed `AGENTS.md`. It ran `scripts/verify_repo.sh` with `PYTHON=~/.venv/bin/python`, the interpreter documented in `AGENTS.md`, and cited `AGENTS.md` for the accepted Python 3.9.6 gap.
- It updated `docs/TRACEABILITY.md`, which `AGENTS.md` describes as "update it when coverage changes".
- It changed only the repository layer and kept the public interfaces.
- It referenced the open questions Q-02, Q-03, Q-04, and Q-05 in its test comments and in the traceability notes.

**Access outside the working folder:** it used `~/.venv/bin/python`, which `AGENTS.md` names as the allowed exception. Nothing in the record shows other access outside the worktree, but the transcript cannot rule it out.

## Incorrect Assumptions

None found.
- **Case sensitivity (Q-03).** The implementation is case-sensitive. It is disclosed in the docstring ("case handling is open (Q-03)"), in the test module, and in the report. No test or document asserts it.
- **Ordering.** Results are compared as sets, with an explicit comment about Q-02.

## Failed / Unknown Commands

None reported or observed. Both reported commands succeeded:

| Command | Result |
|---|---|
| `~/.venv/bin/python -m pytest -p no:cacheprovider -q tests/test_search_matching.py`, before the code change | 5 failed. This is the expected "red" step |
| `PYTHON=~/.venv/bin/python scripts/verify_repo.sh`, after the change | Contract OK, 13 passed, exit 0, and the Python <3.10 warning |

## Out-of-Scope Changes

No source change outside the task. One change goes beyond what `TASK_UNDER_TEST.md` asks for, but follows a repository convention:
- **`docs/TRACEABILITY.md`.** The FR-01, FR-02, FR-03, and FR-05 rows now point to the new test and note the open questions. All statuses remain "Partial", which is consistent with the remaining gaps.
  - The task does not require this edit, but `AGENTS.md` says to update traceability when coverage changes, and `TRACEABILITY.md` is not protected.
  - It is classified as **in line with repository conventions, not out of scope**.
- **Wording to check:** the new FR-01 note says the repository matches on "name". The implementation matches on name or email, which the FR-02 and FR-03 rows state.

Protected files are unchanged (`Repository contract: OK`). No commit was made, and `HEAD` is still `7d0618d`. No `.pytest_cache/` was created.

## Validation Evidence

### Files changed by the agent

- **Modified** `customer_search/repositories/customer_repository.py`: `search_customers` returns `[c for c in self._customers if query in c.name or query in c.email]`.
- **Added** `tests/test_search_matching.py`: one parametrized test with 5 cases covering TS-01 to TS-05.
  - Results are compared as ID sets.
  - Queries use the same letter case as the stored data.
  - The non-matching customer `Alice Green` is never expected in any case.
- **Modified** `docs/TRACEABILITY.md`: 4 rows (see above).

### Executed by the agent (reported)

1. The new tests on the stub: **5 failed**.
2. `scripts/verify_repo.sh`: **13 passed**, exit 0.

### Executed independently by the evaluator

1. **Repository verification**, measuring repository health:

   ```bash
   cd /Users/monseanaya/Developer/ADA-05-after && PYTHON=~/.venv/bin/python scripts/verify_repo.sh
   ```

   Result: contract OK, **13 passed**, exit 0. The suite has 4 original tests, 4 contract tests, and 5 task cases. The Python <3.10 warning was printed.

2. **Task tests only**, measuring the feature:

   ```bash
   ~/.venv/bin/python -m pytest -v -p no:cacheprovider tests/test_search_matching.py
   ```

   Result: **5 passed** (TS-01 to TS-05).

3. **New tests against the unmodified `7d0618d` code.** A clean export was made with `git archive` into a scratch folder, `tests/test_search_matching.py` was copied in, and `~/.venv/bin/pytest -q` was run.

   Result: **5 failed, 8 passed**. All 5 task cases fail without the change, so the tests detect the missing behavior.

The verify script passing (1) does not by itself prove the feature. The evidence for the feature is (2) together with (3).

### Recommended but not executed

None.

## Final Result

**PASS.**
- The requested behavior was implemented in the repository layer.
- TS-01 to TS-05 are covered by tests that pass with the change and fail without it. The agent showed the failure itself before implementing, and the evaluator reproduced it.
- The repository contract and all existing tests pass. No test was removed or weakened, and no protected file changed.
- The open questions were respected and disclosed.
