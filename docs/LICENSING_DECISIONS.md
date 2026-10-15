# License Decisions and Scope

**Review date:** 2026-10-15. This is an engineering recommendation and scope record, not jurisdiction-specific legal advice.

## 1. Video Workbench software

**Selected for this internal-first stage: PolyForm Internal Use License 1.0.0.** The exact license text is in the root LICENSE file and is copied unchanged from the license steward's versioned repository.

Why it fits the stated first use: this is an internal company production tool, not a public software distribution or SaaS product at this stage. The license permits internal business use and changes but does not grant a right to distribute the software. It is source-available, not OSI-approved open-source software. The SPDX license-list request for this license was not accepted; do not falsely label it Apache-2.0, MIT, or an OSI license. For inventory tooling, use a clearly scoped custom LicenseRef rather than asserting an SPDX-listed identifier.

This decision has a hard boundary: do not distribute the workbench, offer third-party-hosted instances, or invite unrestricted outside contributors under this license. Revisit the license before any product distribution, hosted service for third parties, external code contribution, or change in the business model. A future permissive choice could be Apache-2.0 when broad reuse/adoption is desired; a future reciprocal network-service choice could be AGPL-3.0-or-later if modified server-side versions should be offered to network users. Those are alternatives, not additional grants under the current LICENSE.

The public GitHub repository remains viewable/forkable under GitHub's Terms of Service, but that is not a general license to use, modify, or redistribute the project outside the rights expressly granted. See the official GitHub licensing guide: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository

## 2. Contribution Network application

**Recommended open-source candidate: GNU AGPL v3.0-or-later**, because the product is network-oriented and the project intends to connect public contributions with funded/customer work. AGPL is designed to address the server-side source-sharing gap for modified network software. It still permits commercial use; it is not a noncommercial license. It also carries reciprocal source-availability obligations for covered modified versions used over a network.

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
