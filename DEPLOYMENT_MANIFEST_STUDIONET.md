# Stable Studionet deployment manifest — Phase 4 closure

- Network: **Stable Studionet** only; chain ID **61999**.
- RPC: `https://studio.genlayer.com/api`.
- Explorer: `https://explorer-studio.genlayer.com`.
- Canonical deployed contract: `0xFE36de515cD28269E1347faD4f583319e9111312`.
- Creator: `0x22Acaa233b7b985b36ef168F2DE9295334065B15`.
- Source repository: `halihalibt/multimodal-acceptance-matrix-genlayer`.
- Exact canonical source commit: `6fed5915a839b9b4336cd4723a69fd80df37fb25`.
- Source path: `contracts/multimodal_acceptance_matrix.py`.
- Source SHA256: `563ac0b7c429f571acb45ff427840555105401155aebe2d906e0a8960c56daf2`.
- Constructor arguments: none (`{}` in deployment calldata).

## Real transactions

| Action | Transaction | Finality | Leader execution | Consensus |
| --- | --- | --- | --- | --- |
| deployment | `0xd87d70045996cdf565eec20a4bd1be1920063fbf724b2fba1c6fe634138b4fec` | FINALIZED | SUCCESS | MAJORITY_AGREE |
| create | `0x961ad43e7ef9c30c34b68b057c0a6e11989e0198a1c1858ab8f007882ff409f5` | FINALIZED | SUCCESS | MAJORITY_AGREE |
| evaluate | `0xf33c581cf9f1701576d75bcea60724cb1517bc84dd33f1eb3ab03705d770cf69` | FINALIZED | SUCCESS | MAJORITY_AGREE |

All three were manually signed by the user through Studio before this closure.
Work fetched the original transactions through genlayer-js 1.1.8 getTransaction;
status is numeric 7 with statusName FINALIZED, result is 6 / MAJORITY_AGREE, and
leader_receipt contains the actual Leader SUCCESS execution. Work did not send them.

Deployment data.contract_code was base64-decoded and SHA256-checked against the
canonical source above. The decoded deployed bytes and both repository source files
are byte-for-byte identical. No contract compatibility patch was needed.

## Runtime provenance

Verified local packages: genlayer-js 1.1.8; genlayer-test 0.29.2;
genlayer-py 0.16.3; pytest 9.1.1. Canonical source pins
py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6;
the approved local Direct Mode uses GenVM v0.2.16. That header is also present in
the decoded deployed source. The RPC receipts do not independently advertise a
server-wide GenVM version; do not equate local pins with server-version telemetry.

## Persisted example

Review #1: Campaign Banner Review; EVALUATED; ACCEPTED; C1–C5 all PASS.
See REAL_NETWORK_EVIDENCE.md for exact immutable input, hashes, votes, readback,
verification scope and limitations. Hosting and Portal submission are not performed.
