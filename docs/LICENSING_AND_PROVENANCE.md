# Licensing, Provenance, and Third-Party Intake

## Current repository status

This PR branch proposes PolyForm Internal Use License 1.0.0 for first-party software; current `main` remains unlicensed until an authorized merge. The proposal permits internal business use and changes but does not grant a general right to distribute the software, and it is not OSI-approved open-source software. The root text is copied unchanged from the license steward's versioned repository. Read [license decisions](LICENSING_DECISIONS.md) and [NOTICE.md](../NOTICE.md) for scope.

**Visibility decision required:** this GitHub repository is currently public. Do not merge the PolyForm proposal until the owner decides whether to make the repository private; if public distribution/collaboration is intended, choose a different license grant consistent with that intent. The proposal does not automatically cover third-party SDKs, code, model weights, datasets, APIs, source media, logos, or sample creative content.

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

The internal-use license and its limitations are recorded in [License Decisions](LICENSING_DECISIONS.md), referenced by the root [README](../README.md), and scoped in [NOTICE.md](../NOTICE.md). Do not invite unrestricted external contributions under the current license. Before changing licensing or accepting outside contributors, verify rights and provenance for all existing material and decide the contributor acceptance process.
