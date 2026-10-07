# Multimodal Acceptance Matrix

A reusable GenLayer Intelligent Contract primitive for consensus-based multimodal acceptance evaluation.

## Status

- Architecture: **FROZEN V1**
- Development: **PHASE 1 COMPLETE — deterministic core only**
- Deployment: **NOT STARTED**
- Scope: **FROZEN**

## Core Idea

Given a natural-language brief, 1–6 acceptance criteria, and a public HTTPS image, GenLayer independently evaluates the same visual deliverable through Leader and Validator reasoning, compares the resulting criterion matrices with deterministic Material Consequence Equivalence, and persists the accepted matrix and deterministic final verdict onchain.

## Authoritative Documents

Read these before implementation:

1. `WORK_MASTER_PLAN.md`
2. `IMPLEMENTATION_SPEC_A.md`
3. `CANONICAL_CLASSIFICATION_PROMPT_V1.md`
4. `EQUIVALENCE_AND_ACCEPTANCE_V1.md`
5. `TEST_AND_ACCEPTANCE_PLAN.md`
6. `WORK_EXECUTION_RULES.md`
7. `WORK_PROGRESS_TEMPLATE.md`

Do not redesign the product or expand scope without explicit authorization.

## Phase 1 Implementation

Canonical source: `contracts/multimodal_acceptance_matrix.py`.

Public interface:

- `create_review(title, brief, artifact_url, criteria) -> review_id`
- `evaluate(review_id)` — precondition checks and an explicit Phase 2 unavailable error only
- `get_review(review_id) -> complete Review`
- `get_review_count() -> int`

`criteria` is an array of objects with `id`, `text`, `importance`, and
`assessment_mode`. IDs must be exactly `C1` through `Cn` in order (1–6).
Duplicate IDs are rejected. Review IDs start at 1. Specification strings are
preserved exactly; title, brief, and criterion text must be nonblank.
HTTPS validation checks URL syntax only; image fetching, actual format/size
validation, and image-byte hashing belong to Phase 2.

Persistent state uses `TreeMap[u256, str]` with canonical JSON Review records and
a `u256` count. Criteria are nested objects within the immutable specification.
Views decode detached memory copies. `spec_hash` is lowercase SHA256 of UTF-8
JSON with sorted object keys, compact separators, and `ensure_ascii=False`;
criterion array order is preserved. Creator and result fields are excluded.
New reviews contain empty artifact hash/verdict strings and an empty matrix.

Pure helpers validate matrices, derive MUST-only verdicts, and compare complete
outputs under frozen Material Consequence Equivalence. Malformed classifications
raise `MODEL_ERROR` and never become `UNKNOWN`. Business errors raise `EXPECTED`.
The private `_commit_evaluation` boundary validates everything before writing a
single complete record. It is exercised directly in local lifecycle tests and is
excluded from the public ABI. It is not connected to `evaluate` in this phase.

## Local Deterministic Tests

Use Python 3.12+:

```bash
python -m venv .venv
# Activate .venv for your operating system, then:
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

The official `genlayer-test` Direct Mode loads the hash-pinned SDK from GenVM
`v0.2.16`. Its first run downloads development artifacts from GitHub; contract
tests run in memory without RPC, wallets, Docker, deployment, or transactions.
`pytest.ini` disables the separate Studio plugin, avoiding its default Localnet
configuration. This does not select or use another blockchain.

Phase 1 result: **143 passed, 0 failed, 0 skipped**. See `PROJECT_CHECKPOINT.md`
for the exact scope, tooling details, and acceptance evidence.

**STOP: Phase 2 requires explicit authorization.** No multimodal execution,
Leader, Validator, consensus, frontend, or Repository B is implemented.
