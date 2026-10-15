# Licensing, Provenance, and Third-Party Intake

## Current repository status

This repository does not yet declare an open-source license. Public repository visibility is not a substitute for an explicit project license, and it does not establish that third-party code, weights, datasets, or assets may be redistributed. Resolve the intended product and contribution model before choosing and adding a `LICENSE` file.

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

The repository license decision must be recorded in an ADR and reflected consistently in `LICENSE`, `README.md`, and contributor guidance before declaring the project ready for outside contributions.
