# Video Workbench

A standalone product workspace for a model-independent video creation workbench. This repository owns the product experience, domain contracts, orchestration, and delivery controls; it is separate from the FastVideo framework repository.

## Current state

**Stage:** Product discovery and foundation. The first target user, primary job-to-be-done, supported workflow, application stack, and deployment model are not yet locked. Treat proposed workflows and architecture boundaries as hypotheses until validated.

## Principles

- Keep the product independent of any single model, vendor, or inference framework.
- Integrate external runtimes through explicit adapters and stable product contracts.
- Audit components for license, provenance, maintenance, security, and operational fit before reuse.
- Keep model/provider selection and benchmark bake-offs at the final-mile decision gate unless an earlier decision is proven to block architecture.
- Do not commit credentials, private assets, generated media, model weights, or unreviewed third-party code.

## Product records

The product brief, architecture, decisions, licensing/provenance rules, and roadmap will be maintained under `docs/` as the foundation is added.

## Related framework

- [Loofy147/FastVideo](https://github.com/Loofy147/FastVideo) — reference framework and selective-reuse source; not the product repository.

## Status

This repository is being bootstrapped. No production-ready video pipeline or model integration is claimed at this stage.
