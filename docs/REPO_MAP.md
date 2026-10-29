# Repository Map

## What this is

Customer Search is implemented as an importable Python package, `customer_search`. There is **no runnable entry point**:
- There is no HTTP server. `ARCHITECTURE.md` describes `GET /api/customers/search`, but `CustomerSearchController` is a plain class that takes a dict of query parameters.
- There is no UI, although ARCHITECTURE.md lists a Customer Search UI.

The tests are the way to exercise the code.

## Layout

| Path | Role | May import (internal) |
|---|---|---|
| `customer_search/api/controller.py` | `CustomerSearchController.handle_search_request(query_params, user_context)` → `{"results": [...]}` | services, models, validation, auth |
| `customer_search/services/search_service.py` | `CustomerSearchService.search(query, user_context)`: orchestrates validation, repository, and authorization | models, repositories, validation, auth |
| `customer_search/validation/validator.py` | `SearchInputValidator.sanitize_query`: strips whitespace (stub for T-04) | — |
| `customer_search/auth/authorizer.py` | `CustomerSearchAuthorizer`: **fail-open stub** (FR-06 not implemented) | models |
| `customer_search/repositories/customer_repository.py` | `ICustomerRepository` (abstract) and `InMemoryCustomerRepository`: **returns all customers** (stub for T-03) | models |
| `customer_search/models/customer.py` | `Customer`, `CustomerSearchResult` dataclasses | — |
| `tests/test_project_setup.py` | Structure and wiring tests (T-01) | |
| `tests/test_repo_contract.py` | Tests for the repository guardrail | |
| `scripts/verify_repo.sh` | Single verification command (local and CI) | |
| `scripts/check_repo_contract.py` | Checks protected-file hashes, layer imports, and traceability coverage | |
| `.github/workflows/verify.yml` | CI: installs `.[dev]` and runs `scripts/verify_repo.sh` | |

The "May import" column is enforced by `scripts/check_repo_contract.py`. Dependencies point down: api → services → repositories/validation/auth → models.

## Commands

| Purpose | Command |
|---|---|
| Verify everything | `scripts/verify_repo.sh`; on the owner's machine, `PYTHON=~/.venv/bin/python scripts/verify_repo.sh` |
| Tests only | `<python> -m pytest -v` |
| Contract only | `<python> scripts/check_repo_contract.py` |
| Install dev dependencies (needs owner approval) | `<python> -m pip install -e '.[dev]'` |

## Documents

| Document | Status |
|---|---|
| ` REQUIREMENTS.md` (leading space), `SPEC.md`, `ARCHITECTURE.md`, `TASKS.md` | Source of truth. **Protected.** |
| `docs/TRACEABILITY.md` | Living. Every FR/NFR must have a row (enforced) |
| `docs/AGENT_REPORT.md`, `docs/AI_USAGE_LOG.md` | Historical ADA-05 evidence. **Protected.** |
| `AGENTS.md` (`CLAUDE.md` imports it) | Agent instructions |
| `AI_USAGE_LOG.md` (root), `results/` | ADA-08 evidence |

## Known gaps between documents and code

These are recorded here so nobody "fixes" them outside a scoped task:
- **Validation and authorization placement.** ARCHITECTURE.md says the API validates and authorizes. In the code, the service validates, and the API does neither.
- **Authorization.** `is_user_authorized_for_search` is not called by production code, and `filter_authorized_customers` returns its input unchanged (FR-06 and NFR-02).
- **Requirements without a spec.** FR-07, FR-08, and NFR-04 exist only in ` REQUIREMENTS.md`; SPEC.md does not cover them.
- **Open questions.** Q-01..Q-05 are open. Only Q-01 and Q-02 appear in ` REQUIREMENTS.md`; Q-03..Q-05 appear only in `SPEC.md`.

## Where to change what

| Change | Touch | Also update |
|---|---|---|
| Matching logic (T-03) | `repositories/customer_repository.py`; service, if ordering or orchestration changes | tests, `docs/TRACEABILITY.md` |
| Input rules (T-04) | `validation/validator.py` | tests, traceability |
| Authorization (FR-06) | `auth/authorizer.py`, and service wiring | tests, traceability |
| A new layer or package | Needs an `ARCHITECTURE.md` change, so **owner approval first** | `ALLOWED_IMPORTS` in `scripts/check_repo_contract.py` |
| A protected document | **Owner approval first** | Its hash in `scripts/check_repo_contract.py` |
