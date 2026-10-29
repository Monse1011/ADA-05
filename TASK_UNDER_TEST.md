# Task Under Test — Substring search by name and email

## Goal

Make customer search return only the customers whose name or email contains the search query, instead of returning every customer. This implements the matching part of task T-03 for full and partial names and email addresses.

## Requirements Covered

- **FR-01**: search by full or partial name.
- **FR-02**: search by full or partial email address.
- **FR-03**: return customers whose name or email contains the search term.
- `SPEC.md` Search Rules 1–5 and 10 (empty result set when nothing matches).
- Acceptance criteria AC-01, AC-02, AC-03, and the result-set part of AC-05.
- Test scenarios TS-01, TS-02, TS-03, TS-04, and the result-set part of TS-05.

## Verification

- Automated tests cover TS-01 to TS-04 and show that non-matching customers are excluded. For TS-05, `xyz123` returns an empty result set.
- When a test expects more than one match (TS-02), it compares the results as a set and does not assert their order.
- The full existing test suite still passes, with no test removed or weakened.
- The final report states the exact validation commands and their output.

## Constraints

- Do not modify ` REQUIREMENTS.md`, `SPEC.md`, `ARCHITECTURE.md`, or `TASKS.md`.
- **Out of scope:**
  - FR-04 relevance ordering, which is open under Q-02.
  - FR-05 no-results message text (Q-04).
  - FR-06 and NFR-02 authorization.
  - Empty-query behavior (Q-05).
  - Validation and special-character handling (T-04).
  - UI, performance, and FR-07 and FR-08.
- **Case sensitivity is unresolved (Q-03).**
  - Tests must use queries whose letter case matches the stored data.
  - Do not add tests or documentation that assert either case-sensitive or case-insensitive behavior.
  - Report whatever case behavior the implementation ends up with as an assumption.
- Keep the existing layered architecture and public interfaces. Do not add dependencies.
- Do not commit, push, or modify files outside this repository.
