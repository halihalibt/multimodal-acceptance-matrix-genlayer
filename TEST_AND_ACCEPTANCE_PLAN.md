# TEST AND ACCEPTANCE PLAN

## A. Deterministic Contract Tests

Must cover:

1. create valid Review
2. reject zero criteria
3. reject >6 criteria
4. reject no MUST criteria
5. reject invalid enum
6. reject BINARY/PARTIAL
7. reject nonexistent Review
8. reject non-creator evaluation
9. reject double evaluation
10. preserve immutable Review specification
11. stable specification hash

### Verdict Derivation

12. all MUST PASS → ACCEPTED
13. one MUST FAIL → REJECTED
14. MUST PARTIAL → NEEDS_REVISION
15. MUST UNKNOWN with another PASS → NEEDS_REVISION
16. all MUST UNKNOWN → UNDETERMINED
17. SHOULD FAIL does not change ACCEPTED
18. SHOULD PARTIAL does not change ACCEPTED

### Equivalence

19. BINARY PASS/PASS agrees
20. BINARY PASS/FAIL conflicts
21. UNKNOWN/UNKNOWN agrees
22. MUST GRADED PASS/PARTIAL conflicts
23. SHOULD GRADED PASS/PARTIAL agrees
24. SHOULD GRADED PARTIAL/FAIL agrees
25. SHOULD GRADED PASS/FAIL conflicts
26. SHOULD UNKNOWN/PARTIAL conflicts
27. artifact hash mismatch conflicts
28. derived verdict mismatch conflicts

## B. Nondeterministic Tests — Phase 2

Must later demonstrate:
- Leader receives real image bytes
- Validator independently receives real image bytes
- Validator independently re-runs full classification
- malformed result is rejected
- missing criterion is rejected
- duplicate criterion is rejected
- illegal status is rejected
- image fetch failure does not become UNKNOWN
- transient network failure does not persist EVALUATED

## Phase 1 Acceptance Gate

PHASE 1 passes only when:
- deterministic core exists
- deterministic tests pass
- state transitions pass
- verdict derivation passes
- equivalence rules pass

Then STOP.

Do not begin nondeterministic implementation without explicit authorization.
