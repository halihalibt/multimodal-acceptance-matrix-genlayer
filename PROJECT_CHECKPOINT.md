# PROJECT CHECKPOINT — Multimodal Acceptance Matrix — Phase 4 closure

## Overall goal

Complete the frozen Intelligent Contract primitive and its BriefProof application
using the same canonical source and Stable Studionet only.

## Current phase and goal

**PHASE 4 CLOSURE — real onchain evidence and frontend integration.**
Record the user's successful deployment/create/evaluate, independently verify
read-only persistence and provenance, enable the existing real frontend, and
prepare a separate draft PR. Stop; do not merge or enter Phase 5.

## Confirmed completed

- Original RPC transactions confirm FINALIZED / Leader SUCCESS / MAJORITY_AGREE.
- Evaluate: Normal, 5 initial validators, 0 rotations, 3 AGREE / 2 DISAGREE.
- Public Explorer evaluation overview and Consensus tab independently inspected.
- Review #1: EVALUATED / ACCEPTED, actual C1–C5 all PASS; exact hashes and brief.
- Source commit `6fed5915a839b9b4336cd4723a69fd80df37fb25`; source SHA256 `563ac0b7c429f571acb45ff427840555105401155aebe2d906e0a8960c56daf2`.
- Canonical A source, complete B copy and deployment transaction code byte identity PASS.
- Real SDK count/review readback and mounted React first-load/remount verified
  without signing wallet. Full Chromium/CORS validation remains limited.

## Validation

Repository A: **219 PASS / 0 FAIL / 0 SKIPPED**, full approved pytest suite.
Repository B final results: see the validation section in README.md.
Live frontend read-only check: **1 PASS**, actual SDK/native fetch, JSDOM mount
and fresh gateway/remount. Never describe this as full Chromium reload evidence.

## Frozen decisions

All architecture/specification/prompt/equivalence decisions remain unchanged.
Canonical production contract source remains unchanged. No alternate network,
backend, mock production review, verdict recomputation or automatic write retry.

## Limitations and unresolved questions

See REAL_NETWORK_EVIDENCE.md. Full browser preview/hosted-origin CORS and frontend
wallet signing are not claimed. Broad negative live-model/error cases remain
unverified. These do not invalidate the independently verified successful
onchain example or the actual local React read/reconstruction test.

## Real network actions / transactions / hosting

Work: existing transaction reads and view calls only. User: three already completed
manual transactions. **No new blockchain transactions sent.** No faucet, contract
deploy/upgrade, hosting, Portal submission, merge or Phase 5 action.

## Rejected options

Inventing five AGREE votes, copying the older brief/spec hash, hard-coding a detail
matrix, broadly refactoring passing integration, changing deployed contract source,
and treating a canceled Validator run as failed Leader execution were rejected.

## Files changed in Phase 4 closure

- `DEPLOYMENT_MANIFEST_STUDIONET.md`
- `PROJECT_CHECKPOINT.md`
- `README.md`
- `REAL_NETWORK_EVIDENCE.md`

## Scope deviations / stop condition

NONE. Prepare draft PRs and stop for authorization. No automatic Phase 5.

---

## Historical checkpoint (superseded phase status and authorization)

The following records the earlier completed stage. Its earlier network-disabled
scope/status/stop statements are historical; the current Phase 4 instruction and
checkpoint above supersede them. Frozen protocol decisions still apply.

# PROJECT CHECKPOINT

## Overall Goal

Build Multimodal Acceptance Matrix as a reusable GenLayer Intelligent Contract
primitive according to the authoritative FROZEN V1 documents. Repository A is the
only implementation scope of this run.

## Current Phase

PHASE 2 — Nondeterministic Leader / Validator: **PASS / LOCAL COMPLETE**.
Real GenVM/network/model verification is explicitly deferred to authorized Phase 4.
STOP at Phase 2; do not merge, deploy, create Repository B, or begin Phase 3.

Baseline main: `ec65b616b8a7a70211ccc163dc3c20657037d4a6`.
Phase 1 was already merged and authoritative: 143 passing deterministic tests.
All 15 baseline files were verified byte-for-byte by Git blob hash before edits.

## Phase Goal

Replace the intentional evaluate placeholder with the supported custom
nondeterministic pipeline: independent byte fetching and SHA256, complete
multimodal Leader classification, complete independent Validator classification,
frozen deterministic material comparison, and accepted-result persistence.

## Confirmed Completed

- Read the required README, frozen plans/specifications/prompt/equivalence/rules,
  prior checkpoint, complete contract, and existing tests before changing code.
- Inspected actual hash-pinned GenVM v0.2.16 SDK source and current official
  documentation; no unsupported or obsolete API name was assumed.
- Implemented actual `gl.nondet.web.get` response-body access, HTTPS requirement,
  byte-based PNG/JPEG/WEBP container checks, and exact 2,000,000-byte maximum.
- Hash exact fetched bytes in deterministic code using lowercase SHA256.
  Model text, filename, URL, and MIME claims never supply the hash or image.
- Frozen canonical classification semantics implemented as a fixed protocol and
  escaped untrusted specification JSON; visible image text is explicitly untrusted.
- Both roles supply actual image bytes through the SDK's plural `images=[body]`
  multimodal parameter with `response_format="json"`.
- Complete matrix parsing/validation rejects malformed JSON, missing/duplicate/
  wrong/reordered criteria, invalid mode/status combinations, extra prose fields,
  and model-generated verdict/hash fields. Code injects the real artifact hash.
- Supported custom `gl.vm.run_nondet_unsafe` block wired to evaluate.
- Validator fully fetches, hashes, and classifies again before inspecting Leader
  matrix. No shared answer, cached classification, comparison model, or convenience
  equivalence function is used.
- Existing Phase 1 comparison helpers and deterministic business semantics remain
  unchanged: exact hashes, frozen non-transitive neighboring SHOULD tolerance,
  and exact independently derived verdict equality.
- EXPECTED / EXTERNAL / TRANSIENT / MODEL_ERROR separation implemented. Transient
  and model failures never become UNKNOWN or accepted business matrices.
- Independently reproduced matching EXTERNAL errors can agree only as raised
  errors; the SDK propagates them without entering persistence.
- Both callbacks are state-free. Only a successfully returned consensus evaluation
  reaches the existing atomic complete-record commit boundary. The authoritative
  verdict is derived from MUST criteria in deterministic code.
- Creator-only evaluation, one-time transition, immutable specification, unchanged
  state on failed execution, and exactly four public application methods verified.
- Added 76 Phase 2 local cases, including actual SDK request-payload inspection,
  independent captured Validator execution, hard closure serialization roundtrips,
  and the exact pinned SDK RunNondet serialized result/error transport with an
  offline WASI/consensus stand-in.

## Tests

PASS: **219**
FAIL: **0**
SKIPPED: **0**

| Suite | Passed | Failed | Skipped |
| --- | ---: | ---: | ---: |
| Retained Phase 1 | 143 | 0 | 0 |
| Added Phase 2 | 76 | 0 | 0 |
| Total | 219 | 0 | 0 |

Final verification command:
`python -m pytest -q --tb=short -W error::RuntimeWarning`.
Final successful full-suite run: `219 passed in 5.29s`.

All Phase 1 test cases remain present. Exactly one obsolete placeholder expectation
was updated: test_evaluate_shell_fails_without_writing now injects failure at the
actual consensus boundary and asserts the same unchanged-state invariant. Its old
PHASE_NOT_IMPLEMENTED result necessarily disappeared with Phase 2 authorization.
No deterministic coverage was deleted or skipped.

Initial added-test runs revealed an incorrectly copied JPEG fixture and a harness
omission of cloudpickle. Corrected the fixture to exact valid generated JPEG bytes
and made the test fixture load the runner's own dependency after each Direct Mode
reset. Callback serialization is now enforced as a hard roundtrip, not a warning.
The full suite passed after these fixes and subsequent stronger transport tests.

See PHASE2_LOCAL_VERIFICATION.md for the complete 26-requirement evidence mapping.

## Evidence Boundaries

**Tested locally:** SDK web/model request payloads with exact image bytes;
independent Leader/Validator calls under different responses; byte/hash behavior;
complete matrix and error validation; frozen comparison; authorization and ABI;
PENDING preservation under failure; one-time deterministic persistence after an
offline agreement gate; closure serialization using the pinned runner dependency;
real SDK RunNondet result/error encoding at a mocked WASI boundary.

**Structurally verified:** callbacks capture only specification JSON, not contract
state or Leader output; no nondeterministic storage writes; comparison occurs after
independent re-derivation; actual plural images parameter; SDK return/error behavior;
no forbidden equivalence wrapper; no frozen deterministic semantic changes.

**Not claimed:** live model accuracy/injection resistance, full image-codec support,
real GenVM sandbox execution, real Validator quorum, blockchain acceptance or finality.
Direct Mode's default unsafe hook executes only Leader. Tests explicitly execute
captured Validator callbacks; offline gates supplement, not replace, Phase 4.

## Frozen Decisions

- Logical state schema, public ABI, immutable Review specifications and results,
  PENDING/EVALUATED lifecycle, successful one-time evaluation.
- 1–6 fixed sequential criteria, at least one MUST, frozen enums.
- UNKNOWN is evidence insufficiency only, never a system-error fallback.
- MUST-only deterministic verdict; model cannot choose verdict or artifact hash.
- Exact BINARY and GRADED MUST status agreement.
- GRADED SHOULD tolerance only PASS/PARTIAL or PARTIAL/FAIL in either direction;
  no PASS/FAIL tolerance, no UNKNOWN/known tolerance, no transitive broadening.
- Exact hash and independently derived verdict matching.
- Independent full-matrix multimodal Leader and Validator derivation.
- HTTPS PNG/JPEG/WEBP only; no backend, secondary chain, paid API, payments, or token.

The seven frozen specification/plan/rules/template documents were not rewritten.
The original runner header, package pins, and pytest configuration remain unchanged.

## Exact Files Changed

1. `contracts/multimodal_acceptance_matrix.py` — independent evaluation, prompt,
   image byte/container validation/hash, errors, custom Validator, evaluate wiring.
2. `tests/conftest.py` — expose the exact runner-owned cloudpickle dependency in
   local Direct Mode after its per-test SDK cleanup; preserve Phase 1 fixtures.
3. `tests/test_phase1.py` — update only the obsolete placeholder failure assertion.
4. `tests/test_phase2.py` — 76 focused offline SDK/direct/serialized-transport cases.
5. `README.md` — current Phase 2 behavior, local evidence and limitations.
6. `PHASE2_LOCAL_VERIFICATION.md` — API/error/image details, acceptance evidence,
   harness limitations and deferred real-network questions.
7. `PROJECT_CHECKPOINT.md` — this completed-stage checkpoint.

## SDK / API Adaptations

No package upgrade. No runner change. Pinned versions remain genlayer-test 0.29.2,
genlayer-py 0.16.3, pytest 9.1.1, GenVM v0.2.16.

- Nondeterministic mechanism: `gl.vm.run_nondet_unsafe(leader, validator)`.
  Validator UserError/VMError handling is custom; no default error-message equality
  can accidentally validate model/transient failure as a business result.
- Actual multimodal representation: raw byte sequence via `images=[body]`.
  The SDK's json overload annotation uses singular image, but actual implementation
  and typed kwargs use plural images; the executable API was inspected and tested.
- Temporary model output omits artifact_hash. Code adds the independently computed
  byte hash, preserving canonical artifact_hash + criteria output.
- Test tooling adaptation only: extract the exact py-lib-cloudpickle dependency
  `1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd` from the same pinned release.
  Direct Mode's path loader otherwise omits it and its unsafe hook ignores the
  check_pickling setting. This changes no production dependencies or semantics.

## Independence Guarantees

**Leader:** independent_evaluation receives only immutable specification JSON,
then obtains its own Response.body, validates/hash-calculates those exact bytes,
and executes a complete criterion classification with the fixed prompt.

**Validator:** independent_evaluation is invoked again with that specification,
with no Leader answer argument. It fetches/hashes/classifies independently before
validate_independently reads Leader classification for deterministic comparison.
Tests inspect two separate SDK fetches and two multimodal request payloads, then
change Validator image/model responses to establish hash and judgment disagreement.

## Unresolved Real-Network-Only Questions

- Live image decoding, uncommon PNG/JPEG/WEBP variants and corrupt compressed data
  beyond bounded container checks, plus provider classification quality.
- Live OCR/model behavior for visibly rendered prompt-injection text. Local tests
  prove prompt/data separation and structural rejection, not universal resistance.
- Node-runtime sandbox/cloudpickle compatibility, resource limits, error detail,
  consensus rotations/retries/quorum/finality, and real atomic rollback.
- Real independent node artifact availability and mutable-byte/hash disagreement.
- Hidden redirects: pinned Response has no final URL or redirect-control option.
  Submitted URL is HTTPS; exposed redirects abort. Executor behavior is deferred.
- The body limit is post-fetch because the stable API materializes Response.body;
  it cannot bound upstream download/allocation before bytes arrive.

No local Phase 2 blocker remains. These limitations are documented and must be
verified only in an explicitly authorized later real-network phase.

## Rejected Options

- Schema-only or Leader plausibility checking: violates independent re-derivation.
- strict_eq, prompt_comparative/non_comparative or generic equivalence substitution:
  would change the frozen material consequences.
- Model-generated hash/verdict: replaced with authoritative deterministic code.
- UNKNOWN as catch-all error fallback: violates business/system separation.
- Broad package upgrades or adding a codec dependency: unnecessary for the pinned
  SDK byte representation; bounded container checks preserve original image bytes.
- Claiming real consensus from Leader-only Direct Mode: explicitly prohibited;
  local Validator and transport evidence is labeled, real execution deferred.

## Key Assumptions and Constraints

Only Phase 2 is authorized. Stable Studionet remains the later intended network;
no network is used now. SDK-provided raw body/image representation is used directly.
A successful custom nondeterministic return precedes persistence; actual protocol
finality and failure rollback require later network evidence.

## Real Network Actions

NONE.
Development-only GitHub and official documentation/artifact inspection occurred.
No blockchain/RPC endpoint was contacted.

## Transactions Sent

NONE.

## Scope Deviations

NONE.
No frontend, Repository B, backend, deployment, wallet, faucet, hosting, or Phase 3.

## Stop Condition

Phase 2 implementation and local acceptance gate are complete. Create a draft PR
against main and stop. Do not merge automatically. Wait for explicit authorization.
