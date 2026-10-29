# Repository Readiness Audit — ADA-08

**Repository:** `Monse1011/ADA-05` (Customer Search, Python)
**Audit phase:** BEFORE (Phase 1) and AFTER (Phase 5). The BEFORE content in §1–§6 is unchanged from the Phase 1 original. The AFTER evaluation is in §7–§8.
**Original BEFORE file:** `~/Downloads/REPOSITORY_READINESS_AUDIT.md`, SHA-256 `f21aa358a145f37522f40995477a278b83c1ff5a5673fdd4a80a0766cb0684d4`. It is kept outside the repository, unmodified.
**Audit date:** 2026-10-28
**Auditor:** Claude Opus 5.5 (claude.ai chat, Linux container). The repository was cloned and inspected read-only. No application code was modified.

---

## 1. Baseline

| Item | Value |
|---|---|
| Branch | `main` (only branch; `origin/HEAD -> origin/main`) |
| HEAD | `2ad2060e720407975aa72db03bd8df62fa103def` — "Creacion de archivos" |
| Working tree | Clean at clone time |
| Existing tags | None |
| History | `0011e4a` spec → `e97dd36` tests → `f3bb7c4` code + traceability → `2ad2060` docs |
| Proposed baseline tag | `ada08-baseline` → `2ad2060` |

The proposed tag has not been pushed. Pushing to the remote requires the owner's explicit action:

```bash
git tag -a ada08-baseline 2ad2060 -m "ADA-08 functional baseline (BEFORE)"
git push origin ada08-baseline
```

**Baseline validation (observed):**

| Command | Result |
|---|---|
| `pytest -v` (literal command from `AGENTS.md`, clean Python 3.12.3) | **exit 127** — `pytest` is not installed and not declared as a dependency |
| `python3 -m compileall -q customer_search tests` | exit 0 |
| `pip install pytest` (isolated venv) → `pytest -v` | **4 passed in 0.02s**, exit 0 (pytest 9.2.0) |
| `pytest -q` at historical commit `e97dd36` | **Collection error.** The tests were committed before the code they import, so this commit is not a valid baseline. |
| `pip install -e .` (dry run) | Generates `customer_search.egg-info/`, which `.gitignore` does not ignore. The file was removed after the check. |

---

## 2. Method and scale

Each dimension is scored on an integer 0–5 scale. Weighted points = `score / 5 × weight`, so the maximum total is 100.

The anchors below were applied consistently. If the ADA-08 assignment defines different anchors, the scores must be re-checked against them.

- **0** — Absent.
- **1** — Minimal or mostly unusable.
- **2** — Present but incomplete, or requires implicit knowledge.
- **3** — Usable, with notable gaps.
- **4** — Good, with minor gaps.
- **5** — Complete, explicit, and verified.

---

## 3. Scores

| # | Dimension | Weight | BEFORE score (0–5) | BEFORE points | AFTER score (0–5) | AFTER points |
|---|---|---:|---:|---:|---:|---:|
| 1 | Entry Point & Navigation | 15 | 2 | 6.0 | 4 | 12.0 |
| 2 | Agent Instructions | 15 | 1 | 3.0 | 4 | 12.0 |
| 3 | Build / Run / Test | 15 | 2 | 6.0 | 4 | 12.0 |
| 4 | Architecture Boundaries | 10 | 3 | 6.0 | 4 | 8.0 |
| 5 | Requirements & Traceability | 10 | 3 | 6.0 | 4 | 8.0 |
| 6 | Automation & Guardrails | 10 | 1 | 2.0 | 4 | 8.0 |
| 7 | Testability & Evidence | 15 | 2 | 6.0 | 3 | 9.0 |
| 8 | Safety & Permissions | 10 | 2 | 4.0 | 4 | 8.0 |
| | **Total** | **100** | | **39.0 / 100** | | **77.0 / 100** |

**Delta:** AFTER − BEFORE = 77.0 − 39.0 = **+38.0 points**. The ADA-08 recommended target is ≥80 and at least +15. The delta meets its target; the AFTER total does not reach 80. See §8.

---

## 4. Evidence per dimension

### 4.1 Entry Point & Navigation — 2/5

**Strengths:**
- Specification documents exist at the root: ` REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, and `TASKS.md`.
- The package layout `customer_search/{api,validation,auth,services,repositories,models}` mirrors `ARCHITECTURE.md`.
- `customer_search/__init__.py` states the layer order.

**Gaps:**
- There is no `README.md`, no repository map, and no document saying where to start or what is source of truth versus historical record.
- The requirements file name has a **leading space** (` REQUIREMENTS.md`). This breaks naive shell commands and globbing, and `docs/TRACEABILITY.md` has to link it as `./%20REQUIREMENTS.md`. The leading space is documented only in `docs/AGENT_REPORT.md` (problem 3).
- `docs/` mixes historical ADA-05 evidence (`AGENT_REPORT.md`, `AI_USAGE_LOG.md`) with living documentation (`TRACEABILITY.md`) without labeling either.
- The library has no runnable entry point. `CustomerSearchController` is a plain class, not an HTTP server, even though `ARCHITECTURE.md` describes `GET /api/customers/search`. Nothing explains this difference.

### 4.2 Agent Instructions — 1/5

`AGENTS.md` is 13 lines long and contains only `pytest -v`. It is missing:
- How to install dependencies. The documented command fails with exit 127 in a clean environment.
- Read-first documents and sources of truth.
- Change boundaries, including the rule that ` REQUIREMENTS.md` and `SPEC.md` must not be modified. That rule exists only as a past human instruction recorded in `docs/AGENT_REPORT.md`, under "Human Interventions".
- A workspace confinement rule. `docs/AI_USAGE_LOG.md` (Entry 1) records that a previous agent explored directories outside the repository.
- Stop conditions, for example the open questions Q-01 to Q-05 that must not be resolved by invention.
- A Definition of Done.

There is no `CLAUDE.md`.

### 4.3 Build / Run / Test — 2/5

**Strengths:**
- `pyproject.toml` declares the setuptools build backend, `requires-python = ">=3.10"`, and pytest configuration (`testpaths = ["tests"]`, `pythonpath = ["."]`).
- The suite runs in 0.02s once pytest is installed.

**Gaps:**
- No development dependencies are declared (no `[project.optional-dependencies]` and no requirements file), so `pytest` must be known implicitly.
- There are no install or setup instructions and no single verification command.
- No linter or type checker is configured.
- There is no run command, because no runnable application exists (see 4.1).

### 4.4 Architecture Boundaries — 3/5

**Strengths:**
- `ARCHITECTURE.md` (354 lines) defines components, responsibilities, data flow, interfaces, error handling, and design decisions DD-01 to DD-05.
- Code layering matches the document. The service receives the repository, validator, and authorizer through constructor injection, and `ICustomerRepository` is an abstract interface.

**Gaps:**
- Boundaries are not enforced or checked; there are no import rules and no contract check.
- No file maps each layer to its paths.
- Documented and implemented flow differ:
  - `ARCHITECTURE.md` says the API validates and verifies access. In the code, `CustomerSearchController` does neither, and validation happens inside `CustomerSearchService`.
  - `CustomerSearchAuthorizer.is_user_authorized_for_search()` is never called by production code (verified with grep).
- The UI layer is documented but absent, and nothing records that difference.

### 4.5 Requirements & Traceability — 3/5

**Strengths:**
- Requirements carry stable IDs (FR-01 to FR-08, NFR-01 to NFR-04).
- `SPEC.md` defines acceptance criteria AC-01 to AC-09 and test scenarios TS-01 to TS-12.
- `TASKS.md` defines tasks T-01 to T-06 with acceptance and verification steps.
- `docs/TRACEABILITY.md` reports status honestly (Partial / Missing / Not verified), not as complete.

**Gaps:**
- **FR-07, FR-08, and NFR-04 appear only in ` REQUIREMENTS.md`.** They are absent from `SPEC.md` ("Requirements Covered") and from `docs/TRACEABILITY.md`, which traces 9 of 12 requirements. This was verified with grep.
- Open questions Q-01 to Q-05 are unresolved. Q-02 (relevance criteria) blocks FR-04 / AC-04, and Q-03 (case sensitivity) affects FR-01 to FR-03.
- Commit messages do not reference requirement or task IDs, and two different commits share the message "Customer Search: implement feature".

### 4.6 Automation & Guardrails — 1/5

**Present:** `.gitignore` (3 entries) and pytest configuration.

**Absent:**
- CI (`.github/` does not exist), pre-commit hooks, and lint or format configuration.
- A verification script and any repository contract check.
- `.gitignore` entries for `*.egg-info/`, `.venv/`, `build/`, and `dist/` (an egg-info directory was produced during this audit).

Nothing prevents the history from repeating the failure seen at commit `e97dd36`, where a non-collectable test suite was committed.

### 4.7 Testability & Evidence — 2/5

**Strengths:**
- 4 deterministic, fast tests pass.
- The in-memory repository and constructor injection make the service easy to test without infrastructure.

**Gaps:**
- All 4 tests check structure and wiring, not behavior. No test covers AC-01 to AC-07 or TS-01 to TS-09 (confirmed in `docs/TRACEABILITY.md`).
- Coverage tooling is not configured.
- No negative tests exist. The repository stub returns every customer for any query, and no test detects that.
- Historical commit `e97dd36` does not pass its own suite (collection error).

### 4.8 Safety & Permissions — 2/5

**Strengths:**
- No secrets were found (grep for key, token, and password patterns; no `.env` files).
- There are no destructive scripts, data files, or deployment configuration.
- The repository is small (176 KB).

**Gaps:**
- No document lists protected paths (the specification files and `docs/` historical evidence) or forbidden operations (pushes, deleting history, editing specifications to fit an implementation).
- Workspace confinement is undocumented, even though a previous agent violated it (`docs/AI_USAGE_LOG.md`, Entry 1).
- The local project path contains a space (`/Users/monse/Documents/ADA 05`, per `docs/AGENT_REPORT.md`), and nothing warns agents to quote paths.
- Product note, recorded as context and not scored here: `CustomerSearchAuthorizer` fails open. `is_user_authorized_for_search` defaults to `True`, and `filter_authorized_customers` returns its input unchanged. This conflicts with FR-06 / NFR-02 and should not be "fixed" outside a scoped task.

---

## 5. Three principal friction points

1. **Agent instructions are nearly empty, and critical rules live only in human memory or historical reports.** `AGENTS.md` does not state sources of truth, the "do not modify ` REQUIREMENTS.md` / `SPEC.md`" rule, workspace confinement, the stop condition for open questions Q-01 to Q-05, or a Definition of Done. An agent must rediscover all of this, or will violate it.
2. **There is no reproducible verification contract.** The only documented command (`pytest -v`) fails with exit 127 in a clean environment because pytest is undeclared. There is no verification script, no lint, no CI, and no guardrail, so "done" cannot be checked deterministically.
3. **Navigation and traceability hazards.**
   - There is no README or repository map.
   - The requirements file name has a leading space.
   - Three requirements (FR-07, FR-08, NFR-04) are missing from `SPEC.md` and the traceability matrix.
   - Behavioral tests are absent, so an agent cannot tell from the tests what "correct" means.

---

## 6. Notes for Phase 2 (not yet executed)

These observations only constrain the choice of `TASK_UNDER_TEST.md`. No task has been selected or executed.

- A small but nontrivial task grounded in existing requirements is available. **T-03 / FR-01–FR-03** (substring matching on name and email, AC-01 to AC-03, TS-01 to TS-04) is fully specified, and its current state is a documented stub.
- **FR-04 relevance ordering** (Q-02) and **case sensitivity** (Q-03) are open questions. A valid task must exclude them or state them as constraints rather than invent rules.
- Existing tests that must keep passing were checked against substring filtering:
  - `test_repository_interface_and_implementation` searches `"Alice"`, which matches the only customer.
  - `test_layers_wiring_and_controller_reference` searches `"Bob"`, which matches `Bob Smith`.
  - Both remain compatible with substring filtering.

---

## 7. AFTER evaluation (Phase 5)

**AFTER baseline:** commit `7d0618d723bbeb1fef1b9a17ba3ed64b824028db` on branch `ada08-agent-ready`. Its parent is `2ad2060`, and it contains no changes to `customer_search/`, `tests/test_project_setup.py`, or the specification files (`git diff --quiet 2ad2060 7d0618d -- …`).
**Evaluated by:** Claude Code (desktop app), `claude-opus-5-5`, on 2026-10-28.
**Environment:** macOS, `~/.venv` with Python 3.9.6 and pytest 8.4.2. This differs from the Phase 1 container (Python 3.12.3, pytest 9.2.0); see §8.
**Scale:** the same 0–5 integers and weights as §2. §8 explains how the ADA-08 anchors relate to them.

Each dimension below gives the BEFORE score and its main gap as recorded in §4, the AFTER evidence, the AFTER score, and why.

### 7.1 Entry Point & Navigation (weight 15): BEFORE 2 → AFTER 4 (12.0 points)

- **BEFORE gap (§4.1):**
  - There was no README, repository map, or starting point.
  - The leading-space file name was a hazard.
  - Historical and living documents in `docs/` were not labeled.
  - The missing HTTP server and UI were not explained.
- **AFTER evidence:**
  - `docs/REPO_MAP.md` has the layout with each layer's role and allowed imports, the commands, a document status table (source of truth, living, historical, ADA-08 evidence), "Known gaps between documents and code", and "Where to change what".
  - `AGENTS.md` links the map on its first line and lists the sources of truth in reading order.
  - The leading space is documented in `AGENTS.md` and `CLAUDE.md`.
  - The AFTER agent ran the documented command and touched only the expected layer. It made no failed or exploratory commands (`results/after-agent-run.md`).
- **Why 4, not 5:**
  - There is still no `README.md`, which ADA-08 §21 lists.
  - The leading-space file name remains, because the file is protected.
  - Discoverability rests on one agent run, and the compact transcript does not show which files were read.

### 7.2 Agent Instructions (weight 15): BEFORE 1 → AFTER 4 (12.0 points)

- **BEFORE gap (§4.2):** `AGENTS.md` contained only `pytest -v`. It had no install instructions, sources of truth, change boundaries, workspace rule, stop conditions, or Definition of Done, and there was no `CLAUDE.md`.
- **AFTER evidence:**
  - `AGENTS.md` now covers sources of truth, the Definition of Done (`scripts/verify_repo.sh` exits 0 and the output is reported), the environment and interpreter selection, protected files, layers, open questions as stop conditions, known stubs, test rules, and forbidden operations.
  - `CLAUDE.md` imports `AGENTS.md` (`@AGENTS.md`) and adds only two Claude-specific notes.
  - In the AFTER run, the agent used the documented interpreter, cited `AGENTS.md` for the accepted Python gap, showed its tests failing before the change, and updated the traceability matrix. Each of these follows a rule in `AGENTS.md`.
- **Why 4, not 5:**
  - Some rules cannot be enforced from the repository, such as staying in the workspace and asking before installing.
  - The evidence is a single run.
  - User-level configuration (`~/.claude/CLAUDE.md`, plugins) also shaped the agent's behavior and is outside the repository's control.

### 7.3 Build / Run / Test (weight 15): BEFORE 2 → AFTER 4 (12.0 points)

- **BEFORE gap (§4.3):** dev dependencies were undeclared, there was no setup instruction or single command, no lint, and no run command.
- **AFTER evidence:**
  - `pyproject.toml` declares `[project.optional-dependencies] dev = ["pytest"]`.
  - `scripts/verify_repo.sh` is the single command. Observed results:
    - Exit 0 at `7d0618d` with the owner's environment: contract OK, 8 passed.
    - Exit 2 with an install hint when pytest is missing.
    - Exit 0 in the AFTER worktree: 13 passed.
  - The BEFORE agent's failed `pytest -v` and `python3 -m pytest -v` did not recur in AFTER.
- **Why 4, not 5:**
  - The only local environment is Python 3.9.6, below the declared `>=3.10`. The script warns but does not fail.
  - `pip install -e '.[dev]'` and the CI workflow have never been executed.
  - A bare `pytest -v` still fails without an active environment.
  - There is still no lint and no run command; the library has no entry point.

### 7.4 Architecture Boundaries (weight 10): BEFORE 3 → AFTER 4 (8.0 points)

- **BEFORE gap (§4.4):** boundaries were not enforced, no file mapped layers to paths, the documented flow differed from the code, and the absent UI was not recorded.
- **AFTER evidence:**
  - `ALLOWED_IMPORTS` in `scripts/check_repo_contract.py` enforces the layer direction.
  - Three unit tests show that the rule rejects violations.
  - A negative run in which the API imports the repository gave exit 1, "layer violation".
  - `docs/REPO_MAP.md` maps each layer to its path and lists the documentation/code gaps.
- **Why 4, not 5:** the gaps are documented but not resolved. The API still neither validates nor authorizes, and that is a functional change outside Phase 3.

### 7.5 Requirements & Traceability (weight 10): BEFORE 3 → AFTER 4 (8.0 points)

- **BEFORE gap (§4.5):** FR-07, FR-08, and NFR-04 were missing from `SPEC.md` and `docs/TRACEABILITY.md`. Q-01 to Q-05 were open. Commits did not reference IDs.
- **AFTER evidence:**
  - `docs/TRACEABILITY.md` now has rows for all 12 IDs. The three new rows are honestly marked Missing or Not verified.
  - The contract check fails if any FR or NFR lacks a row. The first Phase 3 run caught exactly these 3 IDs (exit 1).
  - Open questions are stop conditions in `AGENTS.md`.
  - Both agents respected Q-02 and Q-03 and disclosed their case-sensitivity choice.
- **Why 4, not 5:**
  - FR-07, FR-08, and NFR-04 are still absent from `SPEC.md`, which is protected and was not modified.
  - Q-01 to Q-05 remain unresolved.
  - Commit messages still do not carry IDs.

### 7.6 Automation & Guardrails (weight 10): BEFORE 1 → AFTER 4 (8.0 points)

- **BEFORE gap (§4.6):** there was no CI, no hooks, no verify script, no contract check, and incomplete `.gitignore` entries.
- **AFTER evidence:**
  - `scripts/check_repo_contract.py` checks protected-file hashes, layer imports, and traceability coverage. Each check has a negative run that fails as expected: SPEC edit, layer import, and rename.
  - The rename case first crashed with a traceback; it was fixed in Phase 3 before the commit.
  - `.github/workflows/verify.yml` calls the same script.
  - `.gitignore` now covers `*.egg-info/`, `.venv/`, `build/`, and `dist/`.
- **Why 4, not 5:**
  - CI is defined but has **never run**, because nothing was pushed.
  - There is no pre-commit hook.
  - There is no lint gate.

### 7.7 Testability & Evidence (weight 15): BEFORE 2 → AFTER 3 (9.0 points)

- **BEFORE gap (§4.7):** the tests checked only structure, there were no behavior or negative tests and no coverage tooling, and `e97dd36` did not pass its own suite.
- **AFTER evidence:**
  - The Definition of Done now requires reporting the verification output and showing that a new behavior test fails without the change.
  - The AFTER agent did so (5 failed → 13 passed), and the evaluator reproduced it independently: 5 failed against `7d0618d`, 5 passed in the AFTER worktree.
  - `tests/test_repo_contract.py` adds tests for the guardrail.
- **Why 3:**
  - At `7d0618d`, the product still has **no behavior tests**. They were deliberately not added, so the AFTER task would not be solved in advance. The authorizer and validator also remain untested.
  - No coverage tooling is configured.
  - What improved is the evidence process, not the product test suite itself.

### 7.8 Safety & Permissions (weight 10): BEFORE 2 → AFTER 4 (8.0 points)

- **BEFORE gap (§4.8):** protected paths and forbidden operations were not listed, the workspace rule was undocumented, and paths with spaces carried no warning.
- **AFTER evidence:**
  - `AGENTS.md` lists the protected files, and the hash check enforces them.
  - It forbids commits, pushes, tags, and deletions without the owner, and requires approval before installing.
  - It has a workspace rule and asks agents to quote paths.
  - The AFTER agent used only the interpreter that `AGENTS.md` allows outside the repository. The BEFORE agent had discovered `~/.venv` on its own.
- **Why 4, not 5:**
  - The workspace rule depends on the agent's sandbox and permissions, not on the repository.
  - The fail-open `CustomerSearchAuthorizer` is unchanged. This is a product issue, recorded as context and not scored, as in §4.8.

## 8. Notes on scoring validity

- **Anchors.** The ADA-08 scale is: 0 absent; 1 partial, obsolete, or ambiguous; 2 useful only with prior knowledge; 3 sufficient for a human but causes friction for an agent; 4 clear, verifiable, and usually sufficient; 5 explicit, reproducible, safe, and validated by automation or evidence. The anchors in §2 are worded differently. The 8 BEFORE scores were re-checked against the ADA-08 wording, and each one remains consistent, so **none was changed**. The AFTER scores use the ADA-08 wording.
- **Below the recommended target.** The AFTER total of 77 is below the recommended 80. The main reasons:
  - CI has not run.
  - The environment does not match `requires-python`.
  - There is no README.
  - Behavior tests were intentionally withheld.

  These gaps are stated here rather than scored away.
- **Single runs.** BEFORE and AFTER each consist of one agent run with a non-deterministic model. Both ended in PASS, so the differences are in process and evidence, not in the outcome.
- **Outdated statements in §1–§6, kept as written:**
  - The local project path no longer contains a space; it is now `/Users/monseanaya/Developer/ADA-05`.
  - Q-01 and Q-02 are in ` REQUIREMENTS.md`, but Q-03 to Q-05 appear only in `SPEC.md`.
  - The proposed tag `ada08-baseline` was never created. Commit `2ad2060` serves as the baseline.
