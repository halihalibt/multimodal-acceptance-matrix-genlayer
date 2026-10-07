# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""Frozen V1 deterministic core. Evaluation execution is intentionally Phase 2."""

from genlayer import *
import hashlib
import json
from urllib.parse import urlsplit


def _error(category: str, code: str) -> None:
    raise gl.vm.UserError(f"{category}:{code}")


def _text(value: object, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _error("EXPECTED", code)
    return value


def _json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def validate_criteria(criteria: object) -> list[dict[str, str]]:
    """Validate sequential IDs; retain exact specification text and list order."""
    if not isinstance(criteria, list) or not 1 <= len(criteria) <= 6:
        _error("EXPECTED", "INVALID_CRITERIA_COUNT")
    canonical = []
    ids = set()
    for index, criterion in enumerate(criteria, start=1):
        if not isinstance(criterion, dict) or set(criterion) != {
            "id", "text", "importance", "assessment_mode"
        }:
            _error("EXPECTED", "INVALID_CRITERION")
        criterion_id = _text(criterion["id"], "INVALID_CRITERION_ID")
        if criterion_id in ids:
            _error("EXPECTED", "DUPLICATE_CRITERION")
        if criterion_id != f"C{index}":
            _error("EXPECTED", "INVALID_CRITERION_ID")
        text = _text(criterion["text"], "INVALID_CRITERION_TEXT")
        if criterion["importance"] not in ("MUST", "SHOULD"):
            _error("EXPECTED", "INVALID_IMPORTANCE")
        if criterion["assessment_mode"] not in ("BINARY", "GRADED"):
            _error("EXPECTED", "INVALID_ASSESSMENT_MODE")
        ids.add(criterion_id)
        canonical.append({
            "id": criterion_id, "text": text,
            "importance": criterion["importance"],
            "assessment_mode": criterion["assessment_mode"],
        })
    if not any(c["importance"] == "MUST" for c in canonical):
        _error("EXPECTED", "NO_MUST_CRITERION")
    return canonical


def canonical_specification(
    title: str, brief: str, artifact_url: str, criteria: object
) -> dict:
    title = _text(title, "INVALID_TITLE")
    brief = _text(brief, "INVALID_BRIEF")
    artifact_url = _text(artifact_url, "INVALID_ARTIFACT_URL")
    try:
        url = urlsplit(artifact_url)
        valid = (
            artifact_url.startswith("https://") and url.scheme == "https"
            and bool(url.hostname) and url.username is None and url.password is None
            and not any(ch.isspace() or ord(ch) < 32 for ch in artifact_url)
        )
        # Access also validates malformed ports; no request is made.
        url.port
    except ValueError:
        valid = False
    if not valid:
        _error("EXPECTED", "INVALID_ARTIFACT_URL")
    return {"title": title, "brief": brief, "artifact_url": artifact_url,
            "criteria": validate_criteria(criteria)}


def specification_hash(specification: dict) -> str:
    spec = canonical_specification(
        specification["title"], specification["brief"],
        specification["artifact_url"], specification["criteria"]
    )
    return hashlib.sha256(_json(spec).encode("utf-8")).hexdigest()


def validate_matrix(criteria: object, matrix: object) -> list[dict[str, str]]:
    """Reject malformed classifications; UNKNOWN is never an error fallback."""
    expected = validate_criteria(criteria)
    if not isinstance(matrix, list) or len(matrix) != len(expected):
        _error("MODEL_ERROR", "INVALID_MATRIX_LENGTH")
    result = []
    seen = set()
    for criterion, cell in zip(expected, matrix):
        if not isinstance(cell, dict) or set(cell) != {"criterion_id", "status"}:
            _error("MODEL_ERROR", "INVALID_MATRIX_CELL")
        criterion_id = cell["criterion_id"]
        if not isinstance(criterion_id, str):
            _error("MODEL_ERROR", "INVALID_CRITERION_ID")
        if criterion_id in seen:
            _error("MODEL_ERROR", "DUPLICATE_CRITERION")
        seen.add(criterion_id)
        if criterion_id != criterion["id"]:
            _error("MODEL_ERROR", "WRONG_CRITERION_ORDER")
        allowed = ("PASS", "FAIL", "UNKNOWN")
        if criterion["assessment_mode"] == "GRADED":
            allowed = (*allowed, "PARTIAL")
        if cell["status"] not in allowed:
            _error("MODEL_ERROR", "INVALID_STATUS")
        result.append({"criterion_id": criterion_id, "status": cell["status"]})
    return result


def derive_verdict(criteria: object, matrix: object) -> str:
    expected = validate_criteria(criteria)
    canonical = validate_matrix(expected, matrix)
    must = [cell["status"] for criterion, cell in zip(expected, canonical)
            if criterion["importance"] == "MUST"]
    if all(status == "UNKNOWN" for status in must):
        return "UNDETERMINED"
    if "FAIL" in must:
        return "REJECTED"
    if "PARTIAL" in must or "UNKNOWN" in must:
        return "NEEDS_REVISION"
    return "ACCEPTED"


def material_consequence(criterion: dict, left: str, right: str) -> str:
    """One-cell relation. Tolerance is symmetric but deliberately non-transitive."""
    if not isinstance(criterion, dict) or set(criterion) != {
        "id", "text", "importance", "assessment_mode"
    }:
        _error("EXPECTED", "INVALID_CRITERION")
    if criterion["importance"] not in ("MUST", "SHOULD"):
        _error("EXPECTED", "INVALID_IMPORTANCE")
    if criterion["assessment_mode"] not in ("BINARY", "GRADED"):
        _error("EXPECTED", "INVALID_ASSESSMENT_MODE")
    allowed = ("PASS", "FAIL", "UNKNOWN")
    if criterion["assessment_mode"] == "GRADED":
        allowed = (*allowed, "PARTIAL")
    if left not in allowed or right not in allowed:
        _error("MODEL_ERROR", "INVALID_STATUS")
    if left == right:
        return "AGREEMENT"
    if criterion["importance"] == "SHOULD" and criterion["assessment_mode"] == "GRADED":
        if (left, right) in (("PASS", "PARTIAL"), ("PARTIAL", "PASS"),
                             ("PARTIAL", "FAIL"), ("FAIL", "PARTIAL")):
            return "AGREEMENT"
    return "MATERIAL_CONFLICT"


def validate_evaluation(criteria: object, output: object) -> dict:
    if not isinstance(output, dict) or set(output) != {"artifact_hash", "criteria"}:
        _error("MODEL_ERROR", "INVALID_OUTPUT")
    artifact_hash = output["artifact_hash"]
    if (not isinstance(artifact_hash, str) or len(artifact_hash) != 64
            or any(c not in "0123456789abcdef" for c in artifact_hash)):
        _error("MODEL_ERROR", "INVALID_ARTIFACT_HASH")
    return {"artifact_hash": artifact_hash,
            "criteria": validate_matrix(criteria, output["criteria"])}


def evaluations_agree(criteria: object, left: object, right: object) -> bool:
    """Pure comparison of two complete outputs; does not execute a Validator."""
    expected = validate_criteria(criteria)
    leader = validate_evaluation(expected, left)
    validator = validate_evaluation(expected, right)
    if leader["artifact_hash"] != validator["artifact_hash"]:
        return False
    # Both authoritative verdicts are always independently derived in code.
    leader_verdict = derive_verdict(expected, leader["criteria"])
    validator_verdict = derive_verdict(expected, validator["criteria"])
    if leader_verdict != validator_verdict:
        return False
    return all(material_consequence(c, a["status"], b["status"]) == "AGREEMENT"
               for c, a, b in zip(expected, leader["criteria"], validator["criteria"]))


class MultimodalAcceptanceMatrix(gl.Contract):
    # JSON records avoid unsupported dict/list persistent storage annotations.
    # Decoding returns detached memory objects; one record write commits results.
    reviews: TreeMap[u256, str]
    review_count: u256

    def __init__(self):
        self.review_count = u256(0)

    @gl.public.write
    def create_review(self, title: str, brief: str, artifact_url: str,
                      criteria: list[dict[str, str]]) -> int:
        specification = canonical_specification(title, brief, artifact_url, criteria)
        review_id = int(self.review_count) + 1
        review = {"review_id": review_id, "creator": str(gl.message.sender_address),
                  **specification, "status": "PENDING",
                  "spec_hash": specification_hash(specification),
                  "artifact_hash": "", "matrix": [], "verdict": ""}
        encoded = _json(review)
        self.reviews[u256(review_id)] = encoded
        self.review_count = u256(review_id)
        return review_id

    def _load_review(self, review_id: int) -> dict:
        if (type(review_id) is not int or review_id < 1
                or review_id > int(self.review_count)):
            _error("EXPECTED", "UNKNOWN_REVIEW")
        return json.loads(self.reviews[u256(review_id)])

    def _require_pending_creator(self, review_id: int) -> dict:
        review = self._load_review(review_id)
        if review["creator"] != str(gl.message.sender_address):
            _error("EXPECTED", "NOT_CREATOR")
        if review["status"] != "PENDING":
            _error("EXPECTED", "ALREADY_EVALUATED")
        return review

    def _commit_evaluation(self, review_id: int, accepted_output: dict) -> None:
        """Internal deterministic persistence boundary for future accepted consensus.

        Not public and never called by evaluate in Phase 1. Tests call it directly
        to exercise the lifecycle without simulating or implementing consensus.
        """
        review = self._require_pending_creator(review_id)
        accepted = validate_evaluation(review["criteria"], accepted_output)
        verdict = derive_verdict(review["criteria"], accepted["criteria"])
        review.update(status="EVALUATED", artifact_hash=accepted["artifact_hash"],
                      matrix=accepted["criteria"], verdict=verdict)
        self.reviews[u256(review_id)] = _json(review)

    @gl.public.write
    def evaluate(self, review_id: int) -> None:
        self._require_pending_creator(review_id)
        _error("PHASE_NOT_IMPLEMENTED", "EVALUATION_REQUIRES_PHASE_2")

    @gl.public.view
    def get_review(self, review_id: int) -> dict:
        return self._load_review(review_id)

    @gl.public.view
    def get_review_count(self) -> int:
        return int(self.review_count)
