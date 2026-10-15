# Video Workbench

A standalone, internal company production workbench for turning business goals and source materials into reviewable deliverables: business briefs, project scopes, product/service demonstrations, and advertising videos. The first proposed vertical slice is a business offering to video campaign pack. This repository owns the product experience, project/artifact records, orchestration, and delivery controls; it is separate from the FastVideo framework repository.

## Current state

**Stage:** Product discovery plus a working CLI-renderer vertical slice. The internal-company workflow is scoped, the reuse audit is recorded, and the local renderer now creates and validates real H.264 MP4s with provenance sidecars. A deployed application/UI, live ContribQuest walkthrough, and product release process are still not complete.

## Product records

- [Product brief](docs/PRODUCT_BRIEF.md) — hypothesis, scope boundaries, workflow candidate, and discovery exit gate.
- [Architecture boundaries](docs/ARCHITECTURE.md) — logical responsibilities, provisional job lifecycle, and the initial low-dependency render path.
- [Roadmap and exit gates](docs/ROADMAP.md) — staged implementation plan and evidence gates.
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

The first video execution path is implemented as a local CLI renderer. It can assemble text cards, still images, video clips, and optional audio through an installed FFmpeg executable; it validates the MP4 with FFprobe and writes a checksum/provenance sidecar. Generative video and the web UI are not implemented. See the [renderer instructions](docs/RENDERER.md).

## Render a campaign

From the repository root, run:

```bash
python tools/render_campaign.py examples/contribquest-campaign.json --output outputs/contribquest-concept.mp4
```

This example is a watermarked concept draft, not live product footage. The command produces the MP4 and a companion JSON manifest. Use the test command below to run unit and local FFmpeg integration tests.

## Related framework

- [Loofy147/FastVideo](https://github.com/Loofy147/FastVideo) — reference framework and selective-reuse source; not the product repository.

## Verification

Run the initial foundation checks locally:

```bash
python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
```

GitHub Actions runs repository contract checks and FFmpeg/FFprobe renderer tests on pull requests and pushes to `main`. Passing tests verifies this CLI renderer in the tested environment; it does not prove a deployed web application, live ContribQuest behavior, claim truth, publication rights, or production readiness.

## Licensing status

The first-party software source is covered by the [PolyForm Internal Use License 1.0.0](LICENSE). This is source-available, not OSI-approved open-source software, and it does not grant a right to distribute the software. Product documents and sample creative content are separately scoped in [NOTICE.md](NOTICE.md). Review [license decisions](docs/LICENSING_DECISIONS.md) before external contributions or any change from internal use.
