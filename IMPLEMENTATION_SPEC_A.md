# IMPLEMENTATION SPEC A — Multimodal Acceptance Matrix

## Primary Entity

A Review logically contains:

- review_id
- creator
- title
- brief
- artifact_url
- criteria
- status
- spec_hash
- artifact_hash
- matrix
- verdict

Exact storage representation may adapt to currently supported GenVM storage types. Semantic meaning may not change.

## Review Status

Exactly:

- PENDING
- EVALUATED

No other lifecycle state in V1.

## Criterion Schema

Each criterion contains:

- id
- text
- importance
- assessment_mode

### Importance

Exactly:
- MUST
- SHOULD

### Assessment Mode

Exactly:
- BINARY
- GRADED

### Criterion IDs

C1 through C6, sequentially normalized or validated.

Minimum criteria: 1  
Maximum criteria: 6  
At least one criterion must be MUST.

## Allowed Classification States

BINARY:
- PASS
- FAIL
- UNKNOWN

GRADED:
- PASS
- PARTIAL
- FAIL
- UNKNOWN

PARTIAL is invalid for BINARY.

## Overall Verdicts

Exactly:
- ACCEPTED
- NEEDS_REVISION
- REJECTED
- UNDETERMINED

The model never sets the authoritative overall verdict.

## Deterministic Verdict Algorithm

Evaluate MUST criteria only.

1. If every MUST result is UNKNOWN → UNDETERMINED.
2. Else if any MUST result is FAIL → REJECTED.
3. Else if any MUST result is PARTIAL → NEEDS_REVISION.
4. Else if any MUST result is UNKNOWN → NEEDS_REVISION.
5. Else → ACCEPTED.

SHOULD criteria never change the overall verdict in V1.

## Specification Hash

Compute a deterministic hash over the immutable review specification, including at minimum:

- title
- brief
- artifact_url
- criterion IDs
- criterion text
- importance
- assessment_mode

Canonical serialization must use deterministic field ordering.

## Artifact Hash

During nondeterministic evaluation:

1. fetch the actual artifact_url
2. obtain raw image bytes
3. validate supported image availability
4. compute SHA256 over exact bytes

Leader and Validator independently calculate the hash.

Hash mismatch → disagreement.

## Image Policy

V1 supports only:
- HTTPS
- PNG
- JPEG/JPG
- WEBP

Target maximum: 2 MB.

Do not silently add GIF, SVG, PDF, video, base64 calldata, or IPFS.

## Public Methods

Required public methods:

### create_review(...)

Creates immutable PENDING review.

Must validate:
- title
- brief
- HTTPS artifact_url
- 1–6 criteria
- valid enums
- sequential/normalized criterion IDs
- at least one MUST

Writes the immutable specification, creator, PENDING state, spec_hash, and empty result fields.

### evaluate(review_id)

Requires:
- review exists
- caller == creator
- status == PENDING

Performs nondeterministic adjudication and atomically persists accepted result.

On success:
- status = EVALUATED
- artifact_hash = accepted hash
- matrix = accepted canonical matrix
- verdict = deterministic verdict

On failed consensus/system error, review must remain logically PENDING.

### get_review(review_id)

Returns complete Review representation.

### get_review_count()

Returns total review count.

## Authorization

- create_review: any wallet
- evaluate: original creator only
- view methods: public

## Immutability

No method may edit or reset an existing review specification or accepted result.

Changed artifact/specification = new Review.

## Idempotency

PENDING → evaluate → EVALUATED

Successful evaluation cannot be repeated.

Failed execution must not partially persist matrix/verdict.

## Error Taxonomy

### EXPECTED
Deterministic business/input errors.

Examples:
- unknown review
- wrong caller
- invalid criterion
- invalid enum
- already evaluated
- no MUST criterion

### EXTERNAL
Stable external evidence errors such as 404 or unsupported image resource.

### TRANSIENT
Timeouts, upstream 5xx, temporary runtime failures.

Must not become a business classification.

### MODEL_ERROR
Malformed structured output, missing/duplicate criterion, illegal status, wrong type.

Must not become UNKNOWN.
