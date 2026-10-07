# MATERIAL CONSEQUENCE EQUIVALENCE V1

## First Check

Leader and Validator artifact hashes must match exactly.

Otherwise:
MATERIAL_CONFLICT.

## BINARY Criteria

Exact status agreement only.

- PASS vs PASS → AGREEMENT
- FAIL vs FAIL → AGREEMENT
- UNKNOWN vs UNKNOWN → AGREEMENT

All other combinations → MATERIAL_CONFLICT.

## GRADED + MUST

Exact status agreement only.

Any different state → MATERIAL_CONFLICT.

Reason: MUST states can change the authoritative final verdict.

## GRADED + SHOULD

Exact matching agrees.

Allowed neighboring tolerance:
- PASS ↔ PARTIAL
- PARTIAL ↔ FAIL

Forbidden:
- PASS ↔ FAIL
- UNKNOWN ↔ PASS
- UNKNOWN ↔ PARTIAL
- UNKNOWN ↔ FAIL

Forbidden combinations are MATERIAL_CONFLICT.

## Overall Verdict Check

Derive an overall verdict independently from each complete matrix using deterministic code.

Leader-derived verdict must exactly equal Validator-derived verdict.

Otherwise → MATERIAL_CONFLICT.

## Validator Acceptance

Return AGREE only if:

artifact hash exact match
AND all criteria are materially equivalent
AND derived overall verdict exact match.

Otherwise return DISAGREE.

## Frozen Principle

Validator must independently re-run the complete multimodal classification.

Do not replace this with:
- Leader-output plausibility checking
- strict equality over free-form model text
- a convenience equivalence wrapper that changes these semantics
