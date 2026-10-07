# PROJECT CHECKPOINT

## Overall Goal

Build Multimodal Acceptance Matrix as a reusable GenLayer Intelligent Contract
submission, according to the repository's authoritative FROZEN V1 documents.

## Current Phase

PHASE 1 — Repository A Skeleton + Deterministic Core: **PASS / COMPLETE**.
Stopped at the Phase 1 acceptance gate. PHASE 2 is not started.

## Phase Goal

Make all deterministic protocol semantics independently testable before adding
artifact access or nondeterministic execution. Implement only Repository A.

## Confirmed Completed

- Read README and all seven required frozen specification/execution documents
  in full before changing code; inspected the originally documents-only tree.
- Single-file SDK contract skeleton with complete Review JSON representation,
  nested Criterion representation, sized count, and typed persistent map.
- Input validation: nonblank title/brief/criterion text, syntactically valid HTTPS
  URL, 1–6 criteria, unique sequential C1–Cn IDs, frozen enums, and at least one MUST.
- Permissionless creation, creator-only evaluation preconditions, public reads,
  count, deterministic unknown-review and already-evaluated errors.
- Immutable specification and detached views; deterministic canonical JSON and
  SHA256 spec hash covering every specification field and ordered criterion IDs.
- Complete matrix validation: exact expected IDs/order/count/fields, no duplicate
  cells, legal statuses by assessment mode. BINARY/PARTIAL is rejected.
- Deterministic MUST-only verdict derivation with frozen precedence; SHOULD
  FAIL/PARTIAL never changes ACCEPTED.
- Exact artifact-hash comparison, independent deterministic verdict derivation,
  and per-cell Material Consequence Equivalence, including symmetric SHOULD
  GRADED neighboring tolerance without transitive PASS/FAIL tolerance.
- Internal one-time PENDING → EVALUATED persistence boundary; result validation
  and verdict derivation occur before the single storage-record write. Failed
  deterministic operations leave complete existing state unchanged.
- Public evaluate shell checks existence, creator, and PENDING, then explicitly
  raises PHASE_NOT_IMPLEMENTED:EVALUATION_REQUIRES_PHASE_2. It cannot persist
  results or accept caller-supplied classifications.
- Official Direct Mode tests and SDK ABI generation confirm the four frozen
  public methods; the internal persistence boundary is not public.
- Repository structure inspected: no frontend, Repository B, deployment scripts,
  backend, generated artifacts, or unused application dependencies added.

## Tests

PASS: **143**
FAIL: **0**
SKIPPED: **0**

Final command: `python -m pytest -q` in the repository with the isolated
development environment. Final output: `143 passed in 2.72s`.

| Coverage group | Passed cases |
| --- | ---: |
| Creation, criterion/enum/URL validation, count and multiple creators | 27 |
| Unknown reviews, authorization, evaluate shell, lifecycle and immutability | 25 |
| Stable canonical spec hash and sensitivity to specification fields | 7 |
| Verdict derivation and internal persistence | 10 |
| Invalid matrix/output rejection and unchanged state | 19 |
| Equivalence: all 50 legal cell pairs plus complete-output checks | 54 |
| SDK-generated public ABI and calldata-compatible criteria parameter | 1 |
| Total | 143 |

All deterministic acceptance cases A1–A28 in TEST_AND_ACCEPTANCE_PLAN.md are
covered. Double evaluation, immutable specification, and successful lifecycle
tests use the private deterministic commit boundary, not a fake public evaluate
implementation. The 50-pair equivalence table covers every ordered legal status
pair for BINARY/GRADED × MUST/SHOULD, including both tolerance directions.
Every contract fixture asserts that no nondeterministic validator execution was
captured. Public calls roundtrip arguments through the official calldata codec.

The first complete run had 142 PASS / 1 FAIL: a test counted the SDK's inherited
system error hook as an application method. Replaced that introspection with
the SDK's official ABI schema generation; the full rerun passed. No core semantic
change was needed.

## Frozen Decisions Relevant to This Phase

- Exactly PENDING / EVALUATED, one successful evaluation, immutable specifications
  and accepted results; changed specifications require a new Review.
- 1–6 criteria, at least one MUST, sequential criterion IDs, frozen enums.
- UNKNOWN is an evidence classification, not a model/system-error fallback.
- MUST-only deterministic verdict; the model cannot set the final verdict.
- BINARY and MUST GRADED use exact status agreement. SHOULD GRADED tolerates
  PASS/PARTIAL and PARTIAL/FAIL, but not PASS/FAIL or UNKNOWN/known-state pairs.
- Artifact hashes and independently derived verdicts must exactly match.
- Independent complete Leader/Validator evaluations remain required in Phase 2;
  deterministic comparison helpers do not implement either execution role.
- Images only, no other chain, no backend/database, no payments/token/escrow.

## Files Changed

- `README.md` — implementation status, interface/storage semantics, local test command.
- `contracts/multimodal_acceptance_matrix.py` — canonical deterministic source.
- `tests/conftest.py` — official SDK Direct Mode fixtures with fixed release.
- `tests/test_phase1.py` — complete deterministic acceptance suite.
- `requirements-dev.txt` — stable testing-suite/client and tested pytest pins.
- `pytest.ini` — Phase 1 tests only; Studio plugin disabled.
- `.gitignore` — exclude local environments, caches, bytecode.
- `PROJECT_CHECKPOINT.md` — this phase report.

The seven frozen specifications/plans/rules/template files remain unchanged.

## SDK / Tooling Adaptations

- No SDK/testing packages were initially installed. Used an isolated Python
  3.12.14 environment with genlayer-test 0.29.2 (current non-prerelease), its
  genlayer-py 0.16.3 dependency, and pytest 9.1.1.
- Loaded official GenVM v0.2.16 artifacts through the testing suite and fixed the
  contract's documented py-genlayer runner hash:
  `1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`.
  Resolved standard-library hash:
  `11rhn002yfajawsz7fai6mykznbxkxs6l91iskj5cm82c92qhy3v`.
- Used supported `from genlayer import *`, `gl.Contract`, public write/view
  decorators, `gl.message.sender_address`, and `gl.vm.UserError`.
- Adapted logical Review/Criteria storage to canonical JSON in
  `TreeMap[u256, str]` and a `u256` counter rather than unsupported persistent
  Python dict/list/int annotations. In-memory calldata remains list/dict/int,
  verified by the official SDK schema and calldata codec.
- Used official in-memory Direct Mode only. Disabled the independent Studio
  pytest plugin to avoid its unrelated default Localnet configuration.
- No semantic conflict with installed tooling was found.

## Real Network Actions

NONE.

This means blockchain/RPC actions: no chain was contacted. Development-only
GitHub repository access, official documentation lookup, and package/SDK artifact
downloads were performed. Direct Mode's local instance construction is not an
onchain deployment.

## Transactions Sent

NONE.

## Unresolved Issues

- No Phase 1 blockers. Direct Mode validates actual SDK storage/calldata and
  deterministic behavior; full GenVM/network execution has not been attempted.
- evaluate remains intentionally unavailable pending explicit Phase 2 authorization.
  Real-byte fetching/hash, supported-image/size checks, multimodal model access,
  independent Leader/Validator execution, consensus, and external/transient error
  handling are deferred exactly as specified, not claimed as complete.

## Rejected Alternatives

- Persistent native Python dict/list fields: replaced with supported typed map
  plus canonical JSON records, preserving the frozen logical representation.
- Public test-only result setter or fabricated successful evaluate: rejected;
  lifecycle tests use a private deterministic boundary excluded from the ABI.
- Automatic latest SDK artifact selection: rejected in favor of a fixed stable
  release and runner hash for reproducible deterministic testing.

## Scope Deviations

NONE.

## Next Recommended Phase

PHASE 2 — Nondeterministic Leader / Validator, only after explicit authorization.
Do not enter automatically. No deployment or transaction authorization is implied.
