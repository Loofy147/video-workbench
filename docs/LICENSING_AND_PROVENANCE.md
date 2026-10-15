# Licensing, Provenance, and Third-Party Intake

## Current repository status

**No project license is selected.** The current branch deliberately does not add a root `LICENSE` file because the repository is public and the owner has not decided whether the project is internal-only or intended for broad public collaboration/adoption. Until this decision is made, do not imply that first-party code may be reused or redistributed under a general project license, and do not invite unrestricted outside contributions.

PolyForm Internal Use was evaluated as one internal-use option, but it is not adopted by this change. If public distribution or outside adoption is intended, choose a compatible license instead. Any future license decision must separately assess existing code provenance and the rights for third-party SDKs, documentation, model weights, datasets, APIs, source media, logos, and sample creative content. Read [license decisions](LICENSING_DECISIONS.md) and [NOTICE.md](../NOTICE.md).

## Required intake record

Before adopting an external component, record:

- Component name, version or immutable revision, source URL, and date reviewed.
- Exact license and the component files/notice that establish it.
- Whether use, modification, distribution, hosted service, and commercial use are permitted under the exact terms.
- Required notices, attribution, source-offer, copyleft, patent, or other obligations.
- Separate terms for model weights, code, tokenizer/configuration files, datasets, sample media, and hosted APIs.
- Runtime dependencies, maintenance signal, known security risks, and replacement cost.
- Decision owner, decision date, and accepted constraints.

A repository-level license must not be assumed to cover dependencies or downloaded model artifacts.

## Model and service review

For each candidate model or hosted service, check the exact artifact/version and applicable terms rather than relying on a model-family name or announcement. Verify commercial use, redistribution, fine-tuning, output-use restrictions, acceptable-use policy, geographic or account limitations, rate limits, data handling, retention, and pricing where applicable.

Model selection and benchmarking remain deferred until the final-mile evaluation, except where a documented blocker requires earlier investigation.

## Asset handling

Do not commit user footage, private media, API tokens, credentials, model weights, generated videos, or large datasets. Keep asset references and synthetic test fixtures in the repository; store real media in approved storage with documented access and retention controls.

## Contribution gate

Until the repository license and contribution policy are decided, contributions should be reviewed by a maintainer before being treated as reusable or redistributable product material. Every copied or adapted file must have an attributable source and a compatibility review. Do not bulk-copy the FastVideo repository or an external app into this project.

## Decision record

The unresolved license choice and rights boundaries are recorded in [License Decisions](LICENSING_DECISIONS.md), referenced by the root [README](../README.md), and scoped in [NOTICE.md](../NOTICE.md). Before selecting a license or accepting outside contributors, verify rights and provenance for existing material and decide the contributor acceptance process.
