import sys
from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def pinned_cloudpickle(direct_vm):
    # genlayer-test's Direct Mode path loader omits the runner's cloudpickle
    # dependency. Load THAT exact artifact for closure serialization checks,
    # without installing/upgrading any package or changing the contract runner.
    from gltest.direct import sdk_loader
    version = "v0.2.16"
    archive = sdk_loader.download_artifacts(version)
    runner = sdk_loader.extract_runner(
        archive, "py-genlayer",
        "1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6", version)
    digest = sdk_loader.parse_runner_manifest(runner)["py-lib-cloudpickle"]
    dependency = sdk_loader.extract_runner(archive, "py-lib-cloudpickle", digest, version)
    sys.path.insert(0, str(dependency / "src"))


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
