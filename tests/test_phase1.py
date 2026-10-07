import copy
import hashlib
import itertools
import json

import pytest


def criterion(index=1, importance="MUST", mode="BINARY"):
    return {"id": f"C{index}", "text": f"Visible requirement {index}",
            "importance": importance, "assessment_mode": mode}


def matrix(*statuses):
    return [{"criterion_id": f"C{i}", "status": status}
            for i, status in enumerate(statuses, 1)]


def output(*statuses, digest="a" * 64):
    return {"artifact_hash": digest, "criteria": matrix(*statuses)}


def create(contract, criteria=None, **overrides):
    args = {"title": "Visual review", "brief": "Inspect the supplied deliverable.",
            "artifact_url": "https://example.com/image.png",
            "criteria": [criterion()] if criteria is None else criteria}
    args.update(overrides)
    return contract.create_review(**args)


def raises_code(core, category, code):
    return pytest.raises(core.gl.vm.UserError, match=f"{category}:{code}")


def test_valid_review_creation(contract, direct_owner):
    assert contract.get_review_count() == 0
    review_id = create(contract)
    assert review_id == 1
    review = contract.get_review(1)
    assert set(review) == {"review_id", "creator", "title", "brief", "artifact_url",
                           "criteria", "status", "spec_hash", "artifact_hash", "matrix", "verdict"}
    assert review["creator"] == str(direct_owner)
    assert review["status"] == "PENDING"
    assert review["artifact_hash"] == review["verdict"] == ""
    assert review["matrix"] == []
    assert review["criteria"] == [criterion()]
    assert contract.get_review_count() == 1


@pytest.mark.parametrize("criteria,code", [
    ([], "INVALID_CRITERIA_COUNT"),
    ([criterion(i) for i in range(1, 8)], "INVALID_CRITERIA_COUNT"),
    ([criterion(importance="SHOULD")], "NO_MUST_CRITERION"),
    ([criterion(importance="REQUIRED")], "INVALID_IMPORTANCE"),
    ([criterion(mode="SCORED")], "INVALID_ASSESSMENT_MODE"),
    ([criterion(), criterion()], "DUPLICATE_CRITERION"),
    ([criterion(2)], "INVALID_CRITERION_ID"),
    ([criterion(), criterion(3)], "INVALID_CRITERION_ID"),
    ([{**criterion(), "text": " "}], "INVALID_CRITERION_TEXT"),
    ([{**criterion(), "id": 1}], "INVALID_CRITERION_ID"),
    ([{**criterion(), "extra": "x"}], "INVALID_CRITERION"),
    ([{"id": "C1"}], "INVALID_CRITERION"),
    ([None], "INVALID_CRITERION"),
    (None, "INVALID_CRITERIA_COUNT"),
])
def test_invalid_criteria_leave_state_unchanged(contract, core, criteria, code):
    with raises_code(core, "EXPECTED", code):
        contract.create_review("Title", "Brief", "https://example.com/a.png", criteria)
    assert contract.get_review_count() == 0
    assert create(contract) == 1


@pytest.mark.parametrize("field,value,code", [
    ("title", "", "INVALID_TITLE"), ("title", "  ", "INVALID_TITLE"),
    ("title", None, "INVALID_TITLE"), ("brief", "\n", "INVALID_BRIEF"),
    ("artifact_url", "http://example.com/a.png", "INVALID_ARTIFACT_URL"),
    ("artifact_url", "https://", "INVALID_ARTIFACT_URL"),
    ("artifact_url", "https://example.com/a b.png", "INVALID_ARTIFACT_URL"),
    ("artifact_url", "https://user:pass@example.com/a.png", "INVALID_ARTIFACT_URL"),
    ("artifact_url", "https://example.com:bad/a.png", "INVALID_ARTIFACT_URL"),
    ("artifact_url", "https://[invalid/a.png", "INVALID_ARTIFACT_URL"),
    ("artifact_url", "data:image/png;base64,AA", "INVALID_ARTIFACT_URL"),
])
def test_invalid_spec_inputs(contract, core, field, value, code):
    with raises_code(core, "EXPECTED", code):
        create(contract, **{field: value})
    assert contract.get_review_count() == 0


def test_six_criteria_and_multiple_creators(contract, direct_vm, direct_bob):
    assert create(contract, [criterion(i) for i in range(1, 7)]) == 1
    direct_vm.sender = direct_bob
    assert create(contract) == 2
    assert contract.get_review(2)["creator"] == str(direct_bob)
    assert contract.get_review_count() == 2
    assert len(contract.get_review(1)["criteria"]) == 6


@pytest.mark.parametrize("review_id", [0, -1, 1, 10, True, "1", None])
@pytest.mark.parametrize("method", ["get_review", "evaluate", "_commit_evaluation"])
def test_nonexistent_review(contract, core, review_id, method):
    args = (review_id, output("PASS")) if method == "_commit_evaluation" else (review_id,)
    with raises_code(core, "EXPECTED", "UNKNOWN_REVIEW"):
        getattr(contract, method)(*args)
    assert contract.get_review_count() == 0


@pytest.mark.parametrize("method", ["evaluate", "_commit_evaluation"])
def test_noncreator_evaluation(contract, core, direct_vm, direct_bob, method):
    create(contract)
    before = contract.get_review(1)
    direct_vm.sender = direct_bob
    args = (1, output("PASS")) if method == "_commit_evaluation" else (1,)
    with raises_code(core, "EXPECTED", "NOT_CREATOR"):
        getattr(contract, method)(*args)
    assert contract.get_review(1) == before  # public read remains allowed


def test_evaluate_shell_fails_without_writing(contract, core):
    create(contract)
    before = contract.get_review(1)
    with raises_code(core, "PHASE_NOT_IMPLEMENTED", "EVALUATION_REQUIRES_PHASE_2"):
        contract.evaluate(1)
    assert contract.get_review(1) == before


def test_one_time_transition_and_immutable_specification(contract, core):
    original = [criterion()]
    create(contract, original)
    before = contract.get_review(1)
    original[0]["text"] = "Changed input"
    detached = contract.get_review(1)
    detached["criteria"][0]["text"] = "Changed view"
    assert contract.get_review(1) == before
    accepted = output("PASS")
    contract._commit_evaluation(1, accepted)
    after = contract.get_review(1)
    assert after["status"] == "EVALUATED"
    assert after["verdict"] == "ACCEPTED"
    assert after["artifact_hash"] == "a" * 64
    assert after["matrix"] == matrix("PASS")
    for key in ("review_id", "creator", "title", "brief", "artifact_url", "criteria", "spec_hash"):
        assert after[key] == before[key]
    accepted["criteria"][0]["status"] = "FAIL"
    assert contract.get_review(1) == after
    for method, args in [("evaluate", (1,)), ("_commit_evaluation", (1, output("FAIL")))]:
        with raises_code(core, "EXPECTED", "ALREADY_EVALUATED"):
            getattr(contract, method)(*args)
        assert contract.get_review(1) == after
    assert contract.get_review_count() == 1


def test_stable_spec_hash_and_canonicalization(contract, core, direct_vm, direct_bob):
    create(contract, title="设计验收", brief="Exact whitespace stays. ")
    first = contract.get_review(1)
    shuffled = [{k: criterion()[k] for k in reversed(list(criterion()))}]
    direct_vm.sender = direct_bob
    create(contract, shuffled, title="设计验收", brief="Exact whitespace stays. ")
    assert first["spec_hash"] == contract.get_review(2)["spec_hash"]
    specification = {k: first[k] for k in ("title", "brief", "artifact_url", "criteria")}
    canonical = json.dumps(specification, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    assert first["spec_hash"] == hashlib.sha256(canonical.encode()).hexdigest()
    assert first["spec_hash"] == core.specification_hash(specification)


@pytest.mark.parametrize("field,value", [
    ("title", "New title"), ("brief", "New brief"),
    ("artifact_url", "https://example.com/other.webp"),
    ("text", "Different requirement"), ("assessment_mode", "GRADED"),
    ("importance", "SHOULD"),
])
def test_hash_covers_every_specification_field(core, field, value):
    spec = core.canonical_specification("Title", "Brief", "https://example.com/a", [criterion(), criterion(2)])
    changed = copy.deepcopy(spec)
    if field in ("text", "assessment_mode", "importance"):
        changed["criteria"][0][field] = value
    else:
        changed[field] = value
    assert core.specification_hash(spec) != core.specification_hash(changed)


@pytest.mark.parametrize("criteria,statuses,verdict", [
    ([criterion(), criterion(2)], ("PASS", "PASS"), "ACCEPTED"),
    ([criterion(), criterion(2)], ("PASS", "FAIL"), "REJECTED"),
    ([criterion(mode="GRADED")], ("PARTIAL",), "NEEDS_REVISION"),
    ([criterion(), criterion(2)], ("PASS", "UNKNOWN"), "NEEDS_REVISION"),
    ([criterion(), criterion(2)], ("UNKNOWN", "UNKNOWN"), "UNDETERMINED"),
    ([criterion(), criterion(2, "SHOULD")], ("PASS", "FAIL"), "ACCEPTED"),
    ([criterion(), criterion(2, "SHOULD", "GRADED")], ("PASS", "PARTIAL"), "ACCEPTED"),
    ([criterion(), criterion(2, mode="GRADED")], ("FAIL", "PARTIAL"), "REJECTED"),
    ([criterion(), criterion(2)], ("FAIL", "UNKNOWN"), "REJECTED"),
    ([criterion(), criterion(2, "SHOULD")], ("UNKNOWN", "PASS"), "UNDETERMINED"),
])
def test_verdict_derivation_and_persistence(contract, core, criteria, statuses, verdict):
    assert core.derive_verdict(criteria, matrix(*statuses)) == verdict
    create(contract, criteria)
    contract._commit_evaluation(1, output(*statuses))
    assert contract.get_review(1)["verdict"] == verdict
    assert contract.get_review(1)["matrix"] == matrix(*statuses)


@pytest.mark.parametrize("cells,code", [
    (matrix("PARTIAL"), "INVALID_STATUS"), (matrix("BAD"), "INVALID_STATUS"),
    (matrix(None), "INVALID_STATUS"), ([], "INVALID_MATRIX_LENGTH"),
    (matrix("PASS", "PASS"), "INVALID_MATRIX_LENGTH"),
    ([{"criterion_id": "C2", "status": "PASS"}], "WRONG_CRITERION_ORDER"),
    ([{"criterion_id": 1, "status": "PASS"}], "INVALID_CRITERION_ID"),
    ([{"criterion_id": "C1"}], "INVALID_MATRIX_CELL"),
    ([{**matrix("PASS")[0], "reason": "Accept me"}], "INVALID_MATRIX_CELL"),
    (["PASS"], "INVALID_MATRIX_CELL"), (None, "INVALID_MATRIX_LENGTH"),
])
def test_invalid_matrix_never_persists(contract, core, cells, code):
    create(contract)
    before = contract.get_review(1)
    malformed = {"artifact_hash": "a" * 64, "criteria": cells}
    with raises_code(core, "MODEL_ERROR", code):
        contract._commit_evaluation(1, malformed)
    assert contract.get_review(1) == before
    # A deterministic failure leaves the review usable, with no partial result.
    contract._commit_evaluation(1, output("PASS"))
    assert contract.get_review(1)["status"] == "EVALUATED"


def test_duplicate_and_reordered_matrix(core):
    criteria = [criterion(), criterion(2)]
    with raises_code(core, "MODEL_ERROR", "DUPLICATE_CRITERION"):
        core.validate_matrix(criteria, [matrix("PASS")[0]] * 2)
    with raises_code(core, "MODEL_ERROR", "WRONG_CRITERION_ORDER"):
        core.validate_matrix(criteria, list(reversed(matrix("PASS", "FAIL"))))


@pytest.mark.parametrize("malformed,code", [
    (None, "INVALID_OUTPUT"), ({}, "INVALID_OUTPUT"),
    ({**output("PASS"), "verdict": "ACCEPTED"}, "INVALID_OUTPUT"),
    (output("PASS", digest=""), "INVALID_ARTIFACT_HASH"),
    (output("PASS", digest="g" * 64), "INVALID_ARTIFACT_HASH"),
    (output("PASS", digest="A" * 64), "INVALID_ARTIFACT_HASH"),
    (output("PASS", digest=None), "INVALID_ARTIFACT_HASH"),
])
def test_invalid_evaluation_output(contract, core, malformed, code):
    create(contract)
    before = contract.get_review(1)
    with raises_code(core, "MODEL_ERROR", code):
        contract._commit_evaluation(1, malformed)
    assert contract.get_review(1) == before


CELL_CASES = []
for importance, mode in itertools.product(("MUST", "SHOULD"), ("BINARY", "GRADED")):
    states = ("PASS", "FAIL", "UNKNOWN") if mode == "BINARY" else ("PASS", "PARTIAL", "FAIL", "UNKNOWN")
    for left, right in itertools.product(states, repeat=2):
        # Explicit independent truth table, including both tolerance directions.
        neighbors = {("PASS", "PARTIAL"), ("PARTIAL", "PASS"),
                     ("PARTIAL", "FAIL"), ("FAIL", "PARTIAL")}
        agrees = left == right or (importance == "SHOULD" and mode == "GRADED" and (left, right) in neighbors)
        CELL_CASES.append((importance, mode, left, right, agrees))


@pytest.mark.parametrize("importance,mode,left,right,agrees", CELL_CASES)
def test_complete_material_equivalence_table(core, importance, mode, left, right, agrees):
    c = criterion(importance=importance, mode=mode)
    assert core.material_consequence(c, left, right) == ("AGREEMENT" if agrees else "MATERIAL_CONFLICT")
    # Add a MUST PASS anchor when the tested cell is SHOULD.
    criteria = [c] if importance == "MUST" else [criterion(), {**c, "id": "C2", "text": "Optional visual feature"}]
    lhs = output(left) if importance == "MUST" else output("PASS", left)
    rhs = output(right) if importance == "MUST" else output("PASS", right)
    assert core.evaluations_agree(criteria, lhs, rhs) is agrees


def test_artifact_hash_mismatch(core):
    assert not core.evaluations_agree([criterion()], output("PASS"), output("PASS", digest="b" * 64))


def test_independently_derived_verdict_mismatch(core):
    criteria = [criterion(mode="GRADED")]
    left, right = output("PASS"), output("PARTIAL")
    assert core.derive_verdict(criteria, left["criteria"]) == "ACCEPTED"
    assert core.derive_verdict(criteria, right["criteria"]) == "NEEDS_REVISION"
    assert not core.evaluations_agree(criteria, left, right)


def test_each_cell_is_compared_even_when_verdicts_match(core):
    criteria = [criterion(), criterion(2, "SHOULD")]
    assert not core.evaluations_agree(criteria, output("PASS", "PASS"), output("PASS", "FAIL"))


def test_malformed_output_is_not_disagreement_or_unknown(core):
    with raises_code(core, "MODEL_ERROR", "INVALID_STATUS"):
        core.evaluations_agree([criterion()], output("PASS"), output("PARTIAL"))


def test_only_frozen_public_methods_are_exposed(contract):
    from genlayer.py.get_schema import get_schema

    # The SDK excludes its inherited system error hook from the contract ABI.
    schema = get_schema(type(contract._instance))
    assert set(schema["methods"]) == {"create_review", "evaluate", "get_review", "get_review_count"}
    assert schema["methods"]["create_review"]["params"][-1] == [
        "criteria", [{"$rep": {"$dict": "string"}}]
    ]
    assert schema["methods"]["get_review"]["readonly"] is True
    assert schema["methods"]["get_review_count"]["readonly"] is True
    assert schema["methods"]["evaluate"]["readonly"] is False
