import sys
from pathlib import Path

import pytest


@pytest.fixture
def contract(direct_vm, direct_deploy):
    direct_vm.check_pickling = True
    instance = direct_deploy(
        str(Path(__file__).resolve().parents[1] / "contracts/multimodal_acceptance_matrix.py"),
        sdk_version="v0.2.16",
    )
    yield instance
    assert direct_vm._captured_validators == [], "Phase 1 must never execute consensus"


@pytest.fixture
def core(contract):
    # Use the actual module loaded by the official SDK harness, not a fake SDK.
    return sys.modules[type(contract).__module__]
