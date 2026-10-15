# Video Workbench

A standalone, internal company production workbench for turning business goals and source materials into reviewable deliverables: business briefs, project scopes, product/service demonstrations, and advertising videos. The first implemented workflow is a business offering to video campaign pack. This repository owns the product experience, project/artifact records, orchestration, and delivery controls; it is separate from the FastVideo framework repository.

## Current state

**Stage:** Product discovery plus a working CLI renderer and local-only browser workflow. The browser can save versioned campaign briefs and storyboards, render a watermarked MP4, and expose technical validation/provenance. A deployed multi-user application, asset-upload workflow, identity-bound approval, and live ContribQuest walkthrough are still not complete.

## Product records

- [Product brief](docs/PRODUCT_BRIEF.md) — hypothesis, scope boundaries, workflow candidate, and discovery exit gate.
- [Architecture boundaries](docs/ARCHITECTURE.md) — logical responsibilities, current local application, and the initial low-dependency render path.
- [Roadmap and exit gates](docs/ROADMAP.md) — staged implementation plan and evidence gates.
- [Local browser workbench](docs/LOCAL_WORKBENCH.md) — startup, end-to-end use, local data handling, security boundary, and current gaps.
- [Licensing and provenance](docs/LICENSING_AND_PROVENANCE.md) — third-party/model intake and asset-handling policy.
- [FastVideo selective-reuse audit](docs/REUSE_AUDIT.md) — evidence-backed decision not to copy FastVideo Studio or Dreamverse.
- [Deterministic renderer](docs/RENDERER.md) — campaign manifest, FFmpeg/FFprobe validation, source provenance, and release gates.
- [License decisions](docs/LICENSING_DECISIONS.md) — code license, content-rights boundaries, and separate project policies.
- [Notice and license scope](NOTICE.md) — what the root license does and does not cover.
- [ADR-0001: separate product repository](docs/decisions/ADR-0001-separate-product-repository.md) — product/framework boundary decision.
- [Contributing guide](CONTRIBUTING.md) — change, test, and provenance expectations.

## Principles

- Keep the product independent of any single model, vendor, or inference framework.
- Integrate external runtimes through explicit adapters and stable product contracts.
- Audit components for license, provenance, maintenance, security, and operational fit before reuse.
- Keep model/provider selection and benchmark bake-offs at the final-mile decision gate unless an earlier decision is proven to block architecture.
- Do not commit credentials, private assets, generated media, model weights, or unreviewed third-party code.

## Pilot use case

The first proposed campaign-pack example is **Contribution Network / ContribQuest**. Before making product claims, use the canonical [Contributions Centre repository](https://github.com/Loofy147/Contribution-bounties-centre-) and its documentation as source evidence. Current limitations and unverified behavior must remain visible in the campaign brief.

- [Pilot scope, claim limits, and proposed demo](docs/PRODUCT_BRIEF.md#pilot-offering-for-the-first-campaign-pack)
- [Draft ContribQuest campaign brief and storyboard](docs/examples/contribution-network-campaign-brief.md) — source-grounded, owner-review only; not an approved script or finished video.
- [Current ContribQuest source and status](https://github.com/Loofy147/Contribution-bounties-centre-)

This identifies a pilot offering for Video Workbench; it does not merge the codebases or make Contributions a dependency of Video Workbench.

## Run the local browser workbench

From the repository root:

    python tools/workbench_server.py

Open <http://127.0.0.1:8765/> on the same machine. The local server binds only to loopback; keep its terminal open and press Ctrl+C to stop it. See [Local Browser Workbench](docs/LOCAL_WORKBENCH.md) for operating instructions and limitations.

The UI captures an offering, audience, objective, differentiators, call to action, a manually maintained claims/evidence ledger, and a short card storyboard. Claim entries are labeled documented-source, direct-observation, inference, or unverified; the UI requires a reference/note for the first two but does not independently verify the reference or claim. It writes a versioned Markdown brief and campaign JSON, renders a watermarked 1280×720 MP4, and exposes individual downloads plus a versioned draft ZIP. The ZIP contains the brief and manifest and, after a successful render, the MP4 and provenance sidecar. It does not upload media assets or support user accounts, identity-bound approval, remote use, or publication. The fixed draft watermark cannot be removed from the UI.

Project records and generated artifacts are stored locally under .workbench/projects/. This folder is Git-ignored and should not be committed.

## Render a campaign from the CLI

The standalone renderer also supports sourced image/video scenes and optional audio when provenance is supplied. From the repository root:

    python tools/render_campaign.py examples/contribquest-campaign.json --output outputs/contribquest-concept.mp4

This example is a watermarked concept draft, not live product footage. The command produces the MP4 and a companion JSON manifest. See the [renderer instructions](docs/RENDERER.md).

## Related framework

- [Loofy147/FastVideo](https://github.com/Loofy147/FastVideo) — reference framework and selective-reuse source; not the product repository.

## Verification

Run the foundation, local-workbench contract, and renderer tests locally:

    python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose

GitHub Actions runs repository contract checks and FFmpeg/FFprobe renderer tests on pull requests and pushes to main. Passing tests verifies the exercised contracts and local media path; it does not prove deployment readiness, live ContribQuest behavior, claim truth, publication rights, or production readiness.

## Licensing status

**No project license is selected in this PR.** The repository remains unlicensed by default; public visibility does not grant a general right to reuse, modify, or redistribute the first-party code. Before inviting outside contributors or distributing the software, the owner must decide the intended public/private boundary and select a license that matches those rights. PolyForm Internal Use was evaluated but is deliberately not added while the repository is public and that decision remains open. Product documents, sample creative content, assets, and third-party dependencies require separate rights review. See [license decisions](docs/LICENSING_DECISIONS.md) and [NOTICE.md](NOTICE.md).
