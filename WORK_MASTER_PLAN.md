# WORK MASTER PLAN V1

## Objective

Build Submission A: **Multimodal Acceptance Matrix**, a reusable GenLayer Intelligent Contract primitive.

The contract evaluates a visual artifact against natural-language acceptance criteria using independent Leader / Validator multimodal reasoning and deterministic material-consequence equivalence.

## Core Flow

Natural-language brief + 1–6 criteria + public HTTPS image
→ Leader independently evaluates all criteria
→ Validator independently re-evaluates all criteria
→ deterministic matrix comparison
→ GenLayer consensus
→ persistent acceptance matrix + deterministic verdict

## Non-Negotiable Architecture

1. Leader performs a complete independent evaluation.
2. Validator performs the same complete evaluation independently.
3. Validator must not merely judge whether Leader output looks reasonable.
4. Real image bytes must be supplied to multimodal model execution.
5. Artifact bytes must be SHA256 hashed.
6. Artifact hash mismatch causes disagreement.
7. Overall verdict is derived deterministically from MUST criteria.
8. Review specification is immutable after creation.
9. Successful evaluation is one-time only.
10. Failed consensus must not partially persist results.
11. No backend.
12. No database.
13. No paid API.
14. No secondary blockchain.
15. No token or escrow.
16. No cross-chain system.
17. V1 supports images only.
18. Scope expansion is prohibited.

## Development Phases

### PHASE 1 — Repository A Skeleton + Deterministic Core

Implement:
- contract state types
- criterion schema
- review schema
- input validation
- specification hash
- deterministic verdict derivation
- deterministic equivalence helpers
- public methods needed for deterministic core
- direct unit tests

Acceptance gate:
- deterministic tests pass
- state transitions pass
- verdict logic passes
- equivalence matrix passes

**STOP after Phase 1. Do not begin Phase 2 unless explicitly authorized.**

### PHASE 2 — Nondeterministic Leader / Validator

Implement:
- artifact fetching
- supported-image validation
- size validation where safely supported
- image hashing
- canonical prompt
- Leader full-matrix classification
- Validator independent full-matrix reclassification
- deterministic comparison
- consensus execution
- malformed-output handling
- transient/external error handling

**STOP after Phase 2.**

### PHASE 3+ 

Frontend, real-network E2E, and submission packaging are separate later phases and are not authorized by this repository's first Work run.

## Resource Discipline

Target total project budget: 3 five-hour Work usage windows.
Hard ceiling: 4.

Keep each Work run strictly phase-scoped.
