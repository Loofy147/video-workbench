# ADR-0001: Keep the product separate from the FastVideo framework

- **Status:** Accepted
- **Date:** 2026-10-15
- **Decision owner:** Project maintainer

## Context

The existing [FastVideo repository](https://github.com/Loofy147/FastVideo) is a framework/fork reference containing multiple apps and model/runtime-specific implementation choices. The product workflow and scope are still being defined. Extending that monorepo immediately would couple product discovery to the framework's structure before there is evidence that this is the right boundary.

## Decision

Maintain this repository, `Loofy147/video-workbench`, as the product's source of truth. Treat FastVideo as a reference and potential source of selectively reusable components.

The product repository owns product requirements, UX, domain contracts, orchestration, tests, integration policy, release process, and product-specific documentation. Any reused component must pass a documented audit for license/provenance, dependencies, fit, security, maintenance state, tests, and adaptation cost.

Do not wholesale-copy the framework and do not create a third application inside the FastVideo monorepo as a substitute for the standalone product.

## Consequences

### Positive

- Product scope and technical decisions can evolve without inheriting the full framework monorepo.
- Model/runtime implementations can be replaced behind product-owned contracts.
- Product-specific quality, provenance, test, and release gates remain inspectable.

### Trade-offs

- Initial work is required to define contracts and selectively adapt any reused code.
- Framework changes do not automatically arrive in the product; reuse must track a source revision and be re-evaluated.

## Follow-up

Complete the FastVideo Studio and Dreamverse reuse audit before deciding whether to adopt any of their components. Keep the provider/model bake-off at the final-mile gate unless a documented architectural blocker is found.
