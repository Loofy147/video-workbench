# Video Workbench

A standalone, internal company production workbench for turning business goals and source materials into reviewable deliverables: business briefs, project scopes, product/service demonstrations, and advertising videos. The first proposed vertical slice is a business offering to video campaign pack. This repository owns the product experience, project/artifact records, orchestration, and delivery controls; it is separate from the FastVideo framework repository.

## Current state

**Stage:** Product discovery and foundation. The first target user, primary job-to-be-done, supported workflow, application stack, and deployment model are not yet locked. Treat proposed workflows and architecture boundaries as hypotheses until validated.

## Product records

- [Product brief](docs/PRODUCT_BRIEF.md) — hypothesis, scope boundaries, workflow candidate, and discovery exit gate.
- [Architecture boundaries](docs/ARCHITECTURE.md) — logical responsibilities and provisional job lifecycle.
- [Roadmap and exit gates](docs/ROADMAP.md) — staged implementation plan and evidence gates.
- [Licensing and provenance](docs/LICENSING_AND_PROVENANCE.md) — third-party/model intake and asset-handling policy.
- [ADR-0001: separate product repository](docs/decisions/ADR-0001-separate-product-repository.md) — product/framework boundary decision.
- [Contributing guide](CONTRIBUTING.md) — change, test, and provenance expectations.

## Principles

- Keep the product independent of any single model, vendor, or inference framework.
- Integrate external runtimes through explicit adapters and stable product contracts.
- Audit components for license, provenance, maintenance, security, and operational fit before reuse.
- Keep model/provider selection and benchmark bake-offs at the final-mile decision gate unless an earlier decision is proven to block architecture.
- Do not commit credentials, private assets, generated media, model weights, or unreviewed third-party code.

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
