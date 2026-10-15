# Contributing

This repository is in early discovery. Small, reviewable contributions with clear provenance are preferred over broad scaffolding or framework imports.

## Before changing code or architecture

- Read [the product brief](docs/PRODUCT_BRIEF.md), [architecture boundaries](docs/ARCHITECTURE.md), and [licensing/provenance rules](docs/LICENSING_AND_PROVENANCE.md).
- Keep proposed workflows and components labelled as hypotheses until accepted.
- Explain the user problem, evidence, alternatives considered, and acceptance tests.
- Keep provider SDKs out of domain contracts and user-interface modules where practical.

## Provenance and safety

- Do not submit secrets, tokens, private assets, user footage, generated media, model weights, or large datasets.
- Cite external code and the exact source revision for any copy or adaptation.
- Check the license and notices of code, models, datasets, and assets independently.
- Do not assume the product license covers dependencies or remote services.
- Never claim tests, benchmarks, or deployment checks passed unless they were actually run; include environment and limitations.

## Changes and verification

- Keep pull requests focused and explain any contract or state-machine change.
- Add or update tests with behavior changes.
- Run the repository checks locally with `python -m unittest discover --start-directory tests --pattern "test_*.py" --verbose`.
- Record material architecture, licensing, and provider decisions as ADRs.
- Treat CI success as a necessary check, not as proof of end-to-end product readiness.

No project license has been selected. The repository is publicly visible but first-party code and content remain unlicensed unless a separate right applies. Do not assume public visibility grants redistribution rights, and do not treat this repository as open-source under an unselected license. Before external contributions or distribution, resolve intended public/private use, verify source ownership/provenance, choose an appropriate license, and define contributor terms. Do not assume any future software license will cover documentation, assets, media, model weights, or third-party runtimes.
