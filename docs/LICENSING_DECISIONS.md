# License Decisions and Scope

**Review date:** 2026-10-15. This is an engineering recommendation and scope record, not jurisdiction-specific legal advice.

## 1. Video Workbench software

**Decision: no license is selected by this change.** The base repository is public, but the owner has not made the corresponding public/private and reuse-policy decision. This PR deliberately removes the proposed root PolyForm Internal Use file rather than silently applying a license that does not grant general distribution rights.

The next decision must distinguish: (a) internal-only use, potentially with private repository access and a license that reflects that boundary; or (b) public collaboration/adoption, with a license that permits the intended uses and a verified contribution/provenance policy. Do not accept unrestricted outside contributions or claim that the project is broadly reusable while this decision remains open. A public repository's visibility is not equivalent to a general license grant.

The root [README](../README.md), [NOTICE](../NOTICE.md), and [licensing/provenance intake policy](LICENSING_AND_PROVENANCE.md) now consistently record the unresolved state. The former PolyForm proposal is not being merged. This is a product-owner decision, not a CI or engineering choice.

## 2. Contribution Network application

**Recommended open-source candidate: GNU AGPL v3.0-or-later**, because the product is network-oriented and the project intends to connect public contributions with funded/customer work. A draft licensing review is staged at [Contribution Bounties Centre PR #17](https://github.com/Loofy147/Contribution-bounties-centre-/pull/17); it is deliberately unmerged pending owner verification of source rights and AppDeploy exclusions. AGPL is designed to address the server-side source-sharing gap for modified network software. It still permits commercial use; it is not a noncommercial license. It also carries reciprocal source-availability obligations for covered modified versions used over a network.

A separate draft licensing PR is the correct place to stage this change. Do not merge it until the repository owner verifies rights to the existing code and generated-platform source, and documents the boundary around AppDeploy-provided SDK/client packages. The app currently imports those packages without declaring them in package.json and is not demonstrated to build independently. A repository LICENSE cannot license third-party SDKs the project does not own. For future contributions, keep a record that the contributor agrees to the project's license; decide whether a Developer Certificate of Origin or contributor agreement is needed before accepting outside contributions. AGPL is not being applied to Video Workbench.

Official text and purpose: https://www.gnu.org/licenses/agpl-3.0.html

## 3. Strategic Contribution Network repository

No license is added to the business-model/governance repository at this stage. Its business-model, economic, governance, and launch-thesis documents are not automatically open-source just because they are in a public GitHub repository. Default copyright remains; do not redistribute or adapt those docs beyond applicable platform terms without a deliberate rights grant. If the owner later wants openly reusable documentation, select a documentation-appropriate license explicitly and scope it to that material.

## 4. Trading research repository

No open-source license is proposed here. The repository is private and contains research code, imported reports, audit artifacts, and user-supplied market data. Keep its data provenance and research-use terms separate. Trading/legal decisions remain outside this license change.

## 5. Future contribution-cloud control plane

The currently empty future portfolio-control repository stays deferred and receives no license until its intended public/private boundary and first-party code/content scope are decided.

## 6. Separate rights that a software license does not solve

The code license does not grant rights to third-party logos, screenshots, product marks, user footage, music, voice, fonts, model weights, datasets, API services, or source data. Those have separate terms. Video Workbench campaign manifests must record asset origin, rights status, and supporting evidence; claim/evidence records must distinguish documentation, direct observation, inference, and unverified statements. A renderer's passing media probe is not a factual, copyright, privacy, or publication approval.

## Sources reviewed

- GitHub licensing guide: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository
- PolyForm Internal Use License 1.0.0: https://polyformproject.org/licenses/internal-use/1.0.0
- PolyForm license texts at the versioned steward repository: https://github.com/polyformproject/polyform-licenses/tree/1.0.0
- SPDX license-list request status for PolyForm Internal Use: https://github.com/spdx/license-list-XML/issues/2849
- GNU AGPL v3.0: https://www.gnu.org/licenses/agpl-3.0.html
- Creative Commons guidance not to use CC licenses for software: https://creativecommons.org/faq/index.html
