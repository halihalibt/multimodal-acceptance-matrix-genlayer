# Real network evidence — Phase 4 closure

## Provenance and verification boundary

The user manually deployed, created Review #1 and evaluated it using Studio
Normal (Full Consensus). The three transactions below predate Work closure.
Work independently performed read-only RPC checks on 2026-10-08 UTC using
**genlayer-js 1.1.8**, without a signer, wallet signature, faucet or write transaction.

Canonical contract: `0xFE36de515cD28269E1347faD4f583319e9111312`. Chain ID: **61999**.
RPC: `https://studio.genlayer.com/api`.
Source commit: `6fed5915a839b9b4336cd4723a69fd80df37fb25`.
Canonical/deployed source SHA256: `563ac0b7c429f571acb45ff427840555105401155aebe2d906e0a8960c56daf2`.

The source was checked locally in both repositories and against the actual
base64-decoded deployment transaction data.contract_code. All three are identical.

## Transaction evidence

| Action | Transaction | Initial validators | Rotations | Votes | Finality / execution |
| --- | --- | --- | --- | --- | --- |
| deployment | [0xd87d70045996cdf565eec20a4bd1be1920063fbf724b2fba1c6fe634138b4fec](https://explorer-studio.genlayer.com/tx/0xd87d70045996cdf565eec20a4bd1be1920063fbf724b2fba1c6fe634138b4fec) | 5 | 0 | 3 AGREE, 2 IDLE | FINALIZED / Leader SUCCESS |
| create | [0x961ad43e7ef9c30c34b68b057c0a6e11989e0198a1c1858ab8f007882ff409f5](https://explorer-studio.genlayer.com/tx/0x961ad43e7ef9c30c34b68b057c0a6e11989e0198a1c1858ab8f007882ff409f5) | 5 | 0 | 3 AGREE, 2 IDLE | FINALIZED / Leader SUCCESS |
| evaluate | [0xf33c581cf9f1701576d75bcea60724cb1517bc84dd33f1eb3ab03705d770cf69](https://explorer-studio.genlayer.com/tx/0xf33c581cf9f1701576d75bcea60724cb1517bc84dd33f1eb3ab03705d770cf69) | 5 | 0 | 3 AGREE, 2 DISAGREE | FINALIZED / Leader SUCCESS |

Original transaction fields: execution_mode NORMAL, leader_only false,
num_of_initial_validators 5, rotation_count 0, status 7 / statusName FINALIZED,
result 6 / result_name MAJORITY_AGREE. The observed evaluate vote map is:

| Address | Vote |
| --- | --- |
| `0x3E5ee2507cc167C9925Bf10c67D7986581112024` | AGREE |
| `0x5310dcF075E0BD47d29B8ec6581F736C767f54D2` | AGREE |
| `0x76c25AFC12c75485703cCFfd0083AA6201455B25` | DISAGREE |
| `0x772ffCd1dF6Cc566eC4b8d3f4F4f8eBbb6B36C84` | DISAGREE |
| `0xacc2459F341D7a887bcA8FAA62F1EC9378d4Bc67` | AGREE |

Thus **3 AGREE / 2 DISAGREE**, not five AGREE. These are vote-map entries, which
include the Leader address; do not relabel them as five independent Validator
reruns. The transaction's validators array contains four Validator receipts.

Work also opened the public Explorer evaluation detail page and its Consensus
tab: FINALIZED, Normal, 0 rotations, 5 initial validators, Accepted, GenVM SUCCESS,
and the same five vote-map entries were visibly present. Explorer's additional
consensus data agrees with the original RPC transaction. No missing fields were
invented, and no inference from the initial validator count was needed.

The create transaction contains a canceled Validator run under leader_receipt
with ERROR / CONSENSUS_VALIDATOR_QUORUM_REACHED. The actual Leader is SUCCESS.
This is not failed application execution. Receipt parsing selects mode=leader
(or the first receipt for the older mode-less shape), requires finality and
explicit execution success, rejects conflicting named execution or Leader errors,
and never treats a consensus vote as execution success.

## Immutable Review #1

- review_id: `1`
- creator: `0x22Acaa233b7b985b36ef168F2DE9295334065B15`
- title: `Campaign Banner Review`
- status: `EVALUATED`
- verdict: `ACCEPTED`
- artifact_url: `https://raw.githubusercontent.com/halihalibt/briefproof-genlayer/cda51899044472637e01cba5a70878b3006fef0b/public/campaign-banner.png`
- artifact_hash: `7ad41f531eaa6391a3ac53e6f77de328e9d9087bd321904756e4d89977d5d378`
- spec_hash: `5d704bb43b083972a40cb8b8ff8e55d49c0739afdd1eb421f894e260a418165d`

Exact actual brief (no substitution of older manual-package text):

> Create a premium promotional banner for the fictional FORMA product launch. Show FORMA and the exact launch phrase “Make room for better.” Use a dominant blue visual family. Do not include prices, investment claims, or financial returns. Aim for a clean, premium, minimal composition.

| Criterion | Exact immutable text | Importance | Mode | Persisted result |
| --- | --- | --- | --- | --- |
| C1 | Brand name is clearly visible | MUST | BINARY | PASS |
| C2 | Required launch phrase is present | MUST | BINARY | PASS |
| C3 | Blue is the dominant visual family | MUST | BINARY | PASS |
| C4 | No prohibited price or investment claim appears | MUST | BINARY | PASS |
| C5 | Composition follows a clean, premium, minimal direction | SHOULD | GRADED | PASS |

SHA256 of the committed campaign-banner.png equals the persisted artifact_hash.
Recomputing the specification hash with canonical sorted-key compact UTF-8 JSON
and ensure_ascii=False equals the actual persisted spec_hash. The older manual
brief and precomputed hash are not authoritative for this review.

## Persistence and frontend readback

- User read get_review(1), refreshed Studio, and read the persisted result again.
- Work SDK reads: get_review_count() returned 1; get_review(1) returned an object
  after jsonSafeReturn normalization, not an envelope or fabricated result.
- Review ID, EVALUATED, ACCEPTED, all five PASS cells, both exact hashes, exact
  brief and criterion order matched. No signing wallet was required.
- BriefProof's actual createGateway and mounted React App were exercised with
  native fetch and the real SDK/RPC. First mount and fresh gateway/remount both
  reconstructed Review #1 and five PASS cells. Four gen_call/read requests total
  (count, explicit review, first mount, reconstructed mount); zero writes.
- This live React verification ran under JSDOM. It proves real integration reads,
  normalization and React reconstruction; it is not a full browser/CORS/layout test.

## Remaining limitations

- Full local Chromium smoke could not run: no Chromium executable; its official
  download returned an invalid/truncated ZIP. Cloud Browser cannot reach workspace
  127.0.0.1:5173 (ERR_CONNECTION_REFUSED). Local Vite server and build work.
- Browser wallet signing through BriefProof has not been executed by Work. The
  user-confirmed signing workflow was Studio. No live frontend write is claimed.
- Hosted-origin CORS and production hosting are unverified; hosting is unauthorized.
- This successful image example does not prove every codec variant, adversarial
  visible prompt injection, live failure rollback, hidden redirect handling,
  mutable resource disagreement or all possible provider errors. Prior locally
  tested protocol invariants and limitations remain in force.
- HTTP 429 handling/cooldown is tested deterministically; the live verifier did
  not intentionally exhaust the public rate-limit bucket.

No new blockchain transactions sent. No deployment, upgrade, faucet, public
hosting, automatic PR merge or Portal submission. Stop at Phase 4 closure;
Phase 5 requires separate authorization.
