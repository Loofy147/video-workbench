# Video Workbench

A standalone, internal company production workbench for turning business goals and source materials into reviewable deliverables: business briefs, project scopes, product/service demonstrations, and advertising videos. The first proposed vertical slice is a business offering to video campaign pack. This repository owns the product experience, project/artifact records, orchestration, and delivery controls; it is separate from the FastVideo framework repository.

## Current state

**Stage:** Product discovery and foundation. The internal-company user, primary job-to-be-done, first campaign-pack workflow, and deterministic first-render direction are recorded as working scope. The product UI/runtime stack, deployment topology, license/distribution model, and actual render pipeline are not yet complete. Treat the workflow as proposed until a real end-to-end export is verified.

## Product records

- [Product brief](docs/PRODUCT_BRIEF.md) — hypothesis, scope boundaries, workflow candidate, and discovery exit gate.
- [Architecture boundaries](docs/ARCHITECTURE.md) — logical responsibilities, provisional job lifecycle, and the initial low-dependency render path.
- [Roadmap and exit gates](docs/ROADMAP.md) — staged implementation plan and evidence gates.
- [Licensing and provenance](docs/LICENSING_AND_PROVENANCE.md) — third-party/model intake and asset-handling policy.
- [FastVideo selective-reuse audit](docs/REUSE_AUDIT.md) — evidence-backed decision not to copy FastVideo Studio or Dreamverse; first render path uses local media assembly.
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

The first video execution path is planned as deterministic assembly of approved footage, graphics, captions, and optional audio through an installed FFmpeg executable. Generative video is optional and is not yet implemented.

## Related framework

- [Loofy147/FastVideo](https://github.com/Loofy147/FastVideo) — reference framework and selective-reuse source; not the product repository.

## Verification

Run the initial foundation checks locally:

```bash
python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose
```

GitHub Actions runs the same tests on pull requests and pushes to `main`. These are documentation/foundation checks only; they do not prove the product pipeline is implemented or production-ready.

## Licensing status

The project license has not yet been selected. See [licensing and provenance](docs/LICENSING_AND_PROVENANCE.md) before contributing reusable code or redistributing project materials.
