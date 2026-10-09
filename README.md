# Multimodal Acceptance Matrix

A reusable GenLayer Intelligent Contract primitive for consensus-based multimodal acceptance evaluation.

## Status

- Architecture: **FROZEN V1**
- Development: **PHASE 5 — public demo available; pre-submission review**
- Deployment: **Stable Studionet — `0xFE36de515cD28269E1347faD4f583319e9111312`**
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

## Implementation

Canonical source: `contracts/multimodal_acceptance_matrix.py`.

Public interface:

- `create_review(title, brief, artifact_url, criteria) -> review_id`
- `evaluate(review_id)` — creator-only independent multimodal evaluation and atomic persistence
- `get_review(review_id) -> complete Review`
- `get_review_count() -> int`

`criteria` is an array of objects with `id`, `text`, `importance`, and
`assessment_mode`. IDs must be exactly `C1` through `Cn` in order (1–6).
Duplicate IDs are rejected. Review IDs start at 1. Specification strings are
preserved exactly; title, brief, and criterion text must be nonblank.
Creation validates HTTPS URL syntax. Evaluation independently fetches exact bytes
on Leader and Validator, validates PNG/JPEG/WEBP containers, enforces a 2,000,000-byte
body limit, and calculates lowercase SHA256. Neither URL text nor MIME claims
substitute for image content.

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
excluded from the public ABI. Phase 2 connects it to `evaluate` only after the
custom nondeterministic block successfully returns.

The pinned SDK's `gl.vm.run_nondet_unsafe` receives two specification-only
closures. Both run the same independent full classification pipeline, supplying
the fetched bytes through `gl.nondet.exec_prompt(images=[body], response_format="json")`.
Validator never supplies Leader output to its model. Only after re-derivation does
deterministic code compare exact hashes, every frozen material-consequence cell,
and independently derived MUST-only verdicts.

The model returns only `criteria`; code adds the artifact hash and derives the
verdict. Malformed classifications raise MODEL_ERROR. Temporary fetch/model
failures raise TRANSIENT. Neither becomes UNKNOWN. Matching independently
reproduced EXTERNAL errors can agree only as errors, which the SDK propagates
without returning a matrix or persisting EVALUATED.

## Local Tests

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

The fixture also loads the exact runner-owned cloudpickle artifact for strong
callback serialization checks; no package pins or runner hashes were upgraded.

Current result: **219 passed, 0 failed, 0 skipped** (143 retained Phase 1 cases
and 76 new Phase 2 cases). The obsolete placeholder expectation is updated to
assert unchanged state when the actual consensus boundary raises.

Direct Mode does not execute real consensus. Tests explicitly run captured
Validator callbacks, enforce an offline pre-persistence consensus gate, and
exercise the pinned SDK's serialized RunNondet interface with an offline WASI
stand-in. The Phase 4 example now verifies actual image evaluation and multi-Validator
acceptance; broader decoder/injection/negative-path claims remain limited. See `PHASE2_LOCAL_VERIFICATION.md` and
`PROJECT_CHECKPOINT.md` for evidence and limitations.

## Public product demonstration

The companion BriefProof product is publicly hosted at
https://halihalibt.github.io/briefproof-genlayer/ . Its verified Review #1
(https://halihalibt.github.io/briefproof-genlayer/#/review/1) reads the
contract's persisted EVALUATED / ACCEPTED result and C1–C5 PASS matrix.
The project owner also confirmed a successful reload in a real Chrome browser.
This read-only browser success is not proof of successful public-site write signing;
those writes were executed manually in GenLayer Studio.

## Real onchain evidence

Review #1 is EVALUATED / ACCEPTED, with actual C1–C5 all PASS. Work independently
read the deployed state and original three transactions. Evaluation has 3 AGREE /
2 DISAGREE, 5 initial validators and 0 rotations. Deployment source bytes match
this canonical source and Repository B's complete copy exactly.

See [deployment manifest](DEPLOYMENT_MANIFEST_STUDIONET.md),
[real evidence](REAL_NETWORK_EVIDENCE.md) and [checkpoint](PROJECT_CHECKPOINT.md)
for exact source commit/hash, address, transactions, immutable brief/criteria,
artifact/spec hashes, actual execution semantics and verification limitations.

## Licensing and submission status

Licensed under the [MIT License](LICENSE). The deployed canonical source is
unchanged; its complete byte-identical copy is present in the BriefProof project.
Phase 4 closure PR was merged and the companion project's GitHub Pages site is
published. **Portal submission has not occurred as part of this patch.**
No new contract deployment, upgrade, or chain transaction was required.
