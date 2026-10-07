# Phase 2 Local Verification

Baseline: authoritative main commit
`ec65b616b8a7a70211ccc163dc3c20657037d4a6`.
All 15 baseline files were compared by Git blob hash before implementation.

## Pinned APIs and representation

No package upgrade or production runner change:

- genlayer-test 0.29.2
- genlayer-py 0.16.3
- pytest 9.1.1
- GenVM v0.2.16
- py-genlayer: `1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`
- py-lib-genlayer-std: `11rhn002yfajawsz7fai6mykznbxkxs6l91iskj5cm82c92qhy3v`
- runner-owned py-lib-cloudpickle:
  `1dlk6mnfabi0z7r39635amyfzw8xb6rm8bv4pmgv6ji1bfx9hghd`
  (artifact version 3.1.0.dev0, used without substituting a newer pip package)

Verified against the actual pinned SDK source and official documentation:

- `gl.vm.run_nondet_unsafe(leader, validator)`: custom callbacks.
- Validator receives `gl.vm.Return`, `gl.vm.UserError`, or `gl.vm.VMError`.
- `gl.nondet.web.get(url)`: Response with status, headers, and raw bytes body.
- `gl.nondet.exec_prompt(prompt, images=[body], response_format="json")`:
  the images sequence accepts raw bytes. The v0.2.16 json overload has an
  inconsistent singular `image` annotation, but its actual implementation and
  ExecPromptKwArgs use plural `images`. The implementation is authoritative
  for this syntax adaptation; tests inspect the serialized ExecPrompt payload.

Official references, read during Phase 2:

- [Image Processing](https://docs.genlayer.com/developers/intelligent-contracts/features/image-processing)
- [Equivalence Principle](https://docs.genlayer.com/developers/intelligent-contracts/equivalence-principle)
- [Direct Mode](https://docs.genlayer.com/api-references/genlayer-test/direct)

The frozen prompt semantics are represented by CLASSIFICATION_PROTOCOL plus an
escaped JSON specification envelope. The temporary model response contains only
`criteria`; deterministic code injects the byte-derived hash to produce the
frozen complete `artifact_hash + criteria` evaluation. No model verdict/hash
or free prose is accepted. The URL is omitted from the model's text prompt.

## Independence and persistence

Both callbacks capture only an immutable serialized specification. Leader calls
independent_evaluation. Validator calls the same function again with no Leader
answer argument. Each call performs a separate web request, container validation,
SHA256, prompt construction, multimodal execution, and complete matrix validation.
There is no response cache or shared classification. Validator reads the Leader
classification only after its own complete result exists.

Comparison delegates to the unchanged Phase 1 evaluations_agree helper:
exact hash, frozen per-cell Material Consequence Equivalence, and exact equality
of independently derived verdicts. No convenience equivalence function is used.

No callback writes state. evaluate reaches the existing _commit_evaluation only
after run_nondet_unsafe successfully returns. That boundary revalidates the output,
derives the verdict, and makes one complete record write. All failures before it
preserve the complete PENDING record. The application ABI remains four methods.

## Error behavior

| Failure | Category | Validator behavior | Persistence |
| --- | --- | --- | --- |
| Deterministic input/permission/lifecycle error | EXPECTED | Fails before consensus | None |
| HTTP 404/410, unsupported or invalid image container, oversized body | EXTERNAL | Agree only if independently reproducing the exact same EXTERNAL UserError | SDK propagates raised error; no matrix |
| Fetch exception, missing bytes, 408/429/5xx, other non-200 including CDN 403 or exposed redirect | TRANSIENT | Disagree, even if both messages match | None |
| Illegal matrix, extra fields/hash/verdict, missing/duplicate/wrong/reordered criterion, malformed JSON | MODEL_ERROR | Disagree, even if both messages match | None |
| Model ValueError/TypeError indicating invalid response | MODEL_ERROR | Disagree | None |
| Other model runtime/upstream exception | TRANSIENT | Disagree | None |
| Leader VMError or non-Return after successful local evaluation | System failure | Disagree | None |
| Legitimate insufficient-evidence classification | UNKNOWN cell | Compare under frozen rules | Only after successful consensus |

Unknown provider exceptions are conservatively treated as TRANSIENT rather than
inventing a business classification. No exception is converted to UNKNOWN.
run_nondet_unsafe avoids the SDK's automatic default equality of error messages.
Unhandled Validator exceptions also cause executor disagreement per pinned SDK.

## Image checks and limits

HTTPS is required at creation and rechecked before fetching. Actual byte format
is detected through PNG/JPEG/WEBP container structure, independently of extension
and Content-Type. PNG checks include IHDR, chunk lengths and CRCs, IDAT, and IEND;
JPEG checks include segment framing, frame/scan structure, dimensions and EOI;
WEBP checks include RIFF size and image/frame chunks. These are bounded container
checks, not a complete codec implementation. Bytes are never re-encoded before
hashing or model delivery.

The 2 MB limit means 2,000,000 fetched bytes, inclusive. Content-Length is not
trusted. The SDK returns an already materialized body and offers no streaming
limit here: the check prevents model submission/persistence of oversized images
but cannot prevent upstream download/allocation. Pixel decoding is performed by
the multimodal consumer. Decoder/provider errors abort; they never become UNKNOWN.

The pinned Response does not expose the final redirect URL or redirect policy.
The submitted URL is HTTPS, and exposed non-200 redirects abort. Hidden redirect
behavior inside the web executor requires Phase 4 verification; no unsupported
option is invented to control it.

## Local evidence and test mapping

Final command: `python -m pytest -q --tb=short -W error::RuntimeWarning`.
PASS 219 / FAIL 0 / SKIPPED 0. Phase 1: 143; Phase 2: 76.
No test is skipped to conceal an unimplemented requirement.

| User acceptance requirement | Local evidence |
| --- | --- |
| 1–5: actual image input, independent complete Validator, independent fetch/hash, same-byte hash | test_real_bytes_enter_both_sdk_multimodal_calls; test_validator_does_not_reuse_leader_matrix |
| 6: hash mismatch | test_hash_mismatch_disagrees_even_with_same_matrix |
| 7–8: valid BINARY/GRADED | test_accepted_gate_commits_once_and_derives_verdict; test_complete_six_criterion_task_and_binary_graded_modes |
| 9–14: malformed/missing/duplicate/reordered/wrong ID/status/JSON | test_bad_model_output_raises_and_never_writes; test_validator_malformed_output_disagrees; test_raw_json_duplicate_keys_rejected |
| 15–16: injection in Brief/criterion/artifact context | test_prompt_injection_is_untrusted_and_cannot_change_structure |
| 17–18: unsupported image and stable resource failure | test_stable_nonimage_or_invalid_container_is_external; test_http_error_taxonomy_preserves_pending |
| 19: transient/model failure never becomes UNKNOWN | test_timeout_never_becomes_unknown; test_validator_timeout_disagrees; test_leader_errors_are_never_business_matrices |
| 20: failed consensus leaves PENDING | test_consensus_disagreement_never_commits; test_pinned_sdk_serialized_result_and_error_transport |
| 21–23: one-time accepted commit, deterministic verdict, second-call rejection | test_accepted_gate_commits_once_and_derives_verdict |
| 24: creator authorization | test_noncreator_stops_before_nondeterminism; retained Phase 1 permission cases |
| 25: preserved Phase 1 | All 143 Phase 1 cases retained; placeholder failure assertion moved to actual consensus failure |
| 26: frozen public ABI | test_public_abi_remains_exactly_four_methods; retained SDK ABI case |
| Size and frozen tolerance | test_actual_byte_length_enforced_ignoring_content_length; test_custom_validator_uses_frozen_neighbor_tolerance; all retained 50-pair truth-table cases |

Direct Mode replaces unsafe execution with Leader-only execution and captured
Validator callbacks. Tests explicitly execute those callbacks and swap mocked
responses to establish re-derivation. A separate offline gate refuses to return
before Validator agreement and checks PENDING state on both sides of the gate.

The runner's exact cloudpickle artifact roundtrips both callbacks with the contract
module registered by value; errors are hard test failures, not ignored warnings.
The test fixture obtains this transitive dependency because genlayer-test's
default SDK path loader omits cloudpickle and its unsafe implementation skips
the check_pickling flag.

Five additional cases extract the exact pinned SDK unsafe function from its
source and execute its real RunNondet serialization/result decoder, replacing
only the WASI sub-VM/consensus boundary with an offline stand-in. These verify
success, raised stable errors, and rejected model/transient errors before storage.
This is stronger structural/transport evidence, still not a real GenVM/network run.

Injection tests establish protocol wording, data separation, real byte attachment,
and deterministic rejection of structural deviations. They do not prove a live
model resists every semantic injection or classifies the visual content correctly.
The PNG artifact context includes adversarial text bytes; live OCR of visibly
rendered injection content remains a Phase 4 test.

## Deferred to authorized Phase 4

- Live multimodal decoding and classification quality for PNG/JPEG/WEBP, including
  corrupt compressed data and uncommon codec features beyond container checks.
- Visibly rendered prompt-injection fixtures and model adherence to the rubric.
- Actual GenVM sandbox execution, cloudpickle/runtime compatibility on node
  Python, resource limits, retries/rotations, and multi-Validator finality.
- URL availability/mutation, independent node fetches, provider-specific errors,
  redirect behavior, and response-body limits on the real executor.
- End-to-end failure rollback and one-time accepted persistence on Stable Studionet.

Real Network Actions = NONE. Transactions Sent = NONE.
No deployment, RPC reads/writes, wallet, faucet, frontend, Repository B, backend,
hosting, or Phase 3 work. STOP at Phase 2.
