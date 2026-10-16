# Open-Source Foundation Audit — Everything, Puter, OpenCut, and ArtCraft

**Review date:** 2026-10-16  
**Purpose:** Decide what can be reused in Video Workbench under the owner's requirement for fully free/open-source components, without custom “fair-source”, noncommercial, source-available, or unclear asset terms.  
**Target workflow:** Business offering → source-backed brief/storyboard → reviewed local media → deterministic video draft → provenance and hand-off pack.  
**Repository baseline reviewed:** `Loofy147/video-workbench` main at `310614a12cec20664cff2df514f9c9e919511896`.  
**Status:** Source-level triage recorded. No upstream code copied, no dependencies installed, and no runtime/build test of the candidate repositories was performed.

## 1. Reuse policy

A repository-level MIT badge is not sufficient evidence to approve an entire application. Before copying or distributing a component, review its exact revision, root and nested licenses, dependency lockfile, bundled fonts/icons/images/audio/models, hosted-service dependencies, and build configuration.

### Pass criteria

- The code is under a recognized open-source license that permits the intended use and distribution. Permissive licenses (MIT, BSD, Apache-2.0) and copyleft licenses (GPL/AGPL/MPL) may qualify; copyleft obligations must be assessed rather than treated as “not open source”.
- Every dependency and bundled asset has a known, compatible license and required notices.
- No required proprietary hosted API, proprietary model, paid account, or vendor service is needed for the core workflow. Optional provider adapters can remain optional and clearly isolated.
- The candidate can be tested at an immutable commit, with a recorded dependency/license inventory and a practical replacement path.
- Unknown, custom restrictive, noncommercial, source-available, unlicensed, or rights-excluded material is not included in the approved build.

For non-code assets, accept only explicit rights suitable for the planned use (for example, CC0/CC-BY with required attribution or appropriately licensed fonts). Do not assume a software license grants rights to brand marks, screenshots, source media, music, model weights, or generated assets.

**Separate decision:** This policy governs third-party reuse. It does not select a license for Video Workbench's own code. The repository's product-license decision remains open in `LICENSING_DECISIONS.md`.

## 2. Findings and disposition

| Candidate | Evidence at review | License / dependency position | Decision |
|---|---|---|---|
| **HeyPuter/everything** | [README at reviewed source](https://github.com/HeyPuter/everything/blob/06802a1e3749202e4db94d39c9ef5ab1a97d0ef1/README.md) lists application families and a 51-app catalogue; each app has its own folder and setup. | Root [LICENSE](https://github.com/HeyPuter/everything/blob/06802a1e3749202e4db94d39c9ef5ab1a97d0ef1/LICENSE) is MIT. That does not automatically clear each app's dependencies, bundled assets, or hosted-service requirements. | **Catalogue / selective candidates only.** No bulk adoption. Audit each chosen app separately. |
| **Everything — Documents** | [README](https://github.com/HeyPuter/everything/blob/06802a1e3749202e4db94d39c9ef5ab1a97d0ef1/src/documents/README.md) documents a standalone `/playground.html` path for local editing and DOCX open/download, separate from the cloud-backed app. | Its `AGENTS.md` explicitly forbids adding AGPL code/dependencies. A build-time license checker reviews locked dependency licenses and selected vendored assets. The standalone playground is not proof that every cloud-backed feature works offline. | **Conditional for a manual local-tool trial.** Run its license check/build and test required import/export behavior before adoption. |
| **Everything — Photo Studio** | [README](https://github.com/HeyPuter/everything/blob/06802a1e3749202e4db94d39c9ef5ab1a97d0ef1/src/photo-studio/README.md) describes a browser raster editor with layers, masks, selections, painting, PSD interchange, WebGPU plus WebGL2 fallback, and optional Puter storage/AI. | Root repository MIT; the local editor is described as having no application server. The full locked dependency/license and bundled-asset inventory was not independently executed. Optional AI services are not approved as a core dependency. | **Best creative-tool candidate for a local evaluation**, but not yet cleared for redistribution or embedded reuse. Keep it external to Video Workbench initially. |
| **Everything — Video Studio** | [README](https://github.com/HeyPuter/everything/blob/06802a1e3749202e4db94d39c9ef5ab1a97d0ef1/src/video-studio/README.md) describes a multi-track browser editor with timeline, captions, effects and export. | Uses Puter cloud for project/media storage. Its manifest includes a license allowlist, but that alone is not a full provenance, security, functionality, or self-hosting assessment. | **Do not make it a core dependency now.** A separate local build/runtime test and storage-adapter review are required. |
| **Everything — Spreadsheet** | [README](https://github.com/HeyPuter/everything/blob/06802a1e3749202e4db94d39c9ef5ab1a97d0ef1/src/spreadsheet/README.md) says editing can begin locally and draft state stays in the browser until cloud actions are requested. | Saving/opening/cloud file listing use Puter. The local-draft feature does not substitute for durable self-hosted storage. | **Optional later tool**, not part of the first workflow. |
| **Everything — Project Management** | [Package manifest](https://github.com/HeyPuter/everything/blob/06802a1e3749202e4db94d39c9ef5ab1a97d0ef1/src/projects/package.json) declares MIT. | This manifest does not prove the full dependency/asset/license inventory or eliminate the need to test Puter/service assumptions. | **Conditional.** Prefer Video Workbench's existing project records until the selected app passes a full audit. |
| **HeyPuter/puter** | [README](https://github.com/HeyPuter/puter/blob/2b254b88924dc9a6f58f05423358cc0f593da46d/README.md) describes a self-hostable platform for cloud storage, database, workers, AI and apps. The [self-host guide](https://github.com/HeyPuter/puter/blob/2b254b88924dc9a6f58f05423358cc0f593da46d/doc/self-hosting.md) describes a Docker Compose stack. | AGPL-3.0: genuinely open-source copyleft, not a proprietary restriction. Its deployment brings an operational stack and source-sharing obligations for covered modified versions. Current guide expects a domain/wildcard DNS for the full setup. | **Permissible in principle, not selected for the first local pilot.** Revisit only if we prove a need for shared identity/cloud storage/worker services and have reviewed AGPL compliance and operations. |
| **OpenCut (current rewrite)** | [README at reviewed source](https://github.com/OpenCut-app/OpenCut/blob/e668010778568641babef2cc40be4703ae6916d6/README.md) says it is being rewritten. Editor API, plugin system, headless mode, MCP and scripting are listed as coming features. | MIT at repository level. Feature roadmap is not evidence those APIs or automation routes are currently usable. | **Manual evaluation only.** Do not integrate against promised future APIs. Re-test when the required features exist and a pinned build works. |
| **OpenCut classic** | [README](https://github.com/OpenCut-app/opencut-classic/blob/cf5e79e919144200294fb9fed22a222592a0aeea/README.md) explicitly says archived and no longer maintained; export functionality was described as under refactor. | MIT. The self-host guide requires a database/Redis stack for full operation. | **Do not use as a foundation.** A frozen, unmaintained release with export refactoring is the wrong core dependency for a new workflow. |
| **ArtCraft desktop/client** | [README at reviewed source](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/README.md) describes an interactive image/video IDE. | Client code is MIT or Apache-2.0 at the user's option, but [NOTICE](https://github.com/storytold/artcraft/blob/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373/NOTICE) explicitly lists some bundled third-party content not covered by those licenses. Model/provider integrations may use external accounts or APIs. | **No wholesale reuse.** Potential future source reference only after excluded assets are removed/cleared, dependency SBOM is reviewed, and core local capability is demonstrated. |
| **ArtCraft Services backend** | [Development setup](https://github.com/storytold/artcraft-services/blob/873c5f7318adbf248626ed1809864242e9aa96f2/_docs/dev_setup.md) documents API, workers, MySQL, Redis, Elasticsearch and object-storage needs. | Its [LICENSE.md](https://github.com/storytold/artcraft-services/blob/873c5f7318adbf248626ed1809864242e9aa96f2/LICENSE.md) labels itself a work in progress and contains custom fair-source restrictions against commercial resale and building competing products. | **Reject for reuse under this project policy.** Do not copy the backend or treat it as an open-source commercial foundation. |

## 3. Chosen pilot architecture

**Keep Video Workbench as the source of truth for projects, versioned briefs, storyboards, review state, provenance, and the deterministic renderer.**

Do not merge the tools into one codebase yet. Use file-format boundaries first:

1. Create a brief and storyboard in Video Workbench.
2. Use a separately installed, locally running creative tool only when it is useful. Treat its output as an external file, not trusted provenance.
3. Bring selected media into Video Workbench through a controlled local intake path.
4. Record each asset's source, source hash, origin, rights status and evidence. Probe it with bounded execution and validate its content, not just filename/MIME.
5. Assemble a watermarked draft using the existing deterministic FFmpeg renderer.
6. Deliver a version-scoped pack containing the brief, manifest, render, technical report and provenance sidecar. Publication remains blocked until separate factual, rights and owner-review checks pass.

### First candidate tools

- **Photo Studio:** first candidate for optional local image adjustments, after its exact app/dependency license checks pass.
- **OpenCut:** optional editor to evaluate separately, not a runtime integration today because its current API/headless/MCP capabilities are not established as implemented.
- **Documents playground:** optional for DOCX interoperability tests; the workbench's Markdown brief remains canonical.
- **Puter self-hosted:** defer until shared identity/storage/worker requirements are demonstrated.
- **Everything Video Studio and Project Management:** defer pending full service/lockfile/runtime audit.

## 4. Immediate implementation order

1. **Record this reuse decision.** No third-party code is copied or added to the dependency tree in this change.
2. **Keep the first workflow small.** Do not install an app suite or deploy Puter merely to create the first campaign pack.
3. **Proceed through the existing Video Workbench route gates.** Validate the owner-approved workflow and acceptance contract, then implement bounded local media intake with license/rights provenance as specified in [DELIVERY_PLAN.md](DELIVERY_PLAN.md).
4. **Add external tools only when they improve a measured task.** Test the exact commit locally, record dependency/asset licenses, build/test results and service boundaries, and preserve a replacement path.
5. **Keep all final output watermarked/draft-only** until review authority, source evidence, asset rights and release gates are implemented and tested.

## 5. What this audit does not claim

- No candidate above has been built or run in this environment as part of this audit.
- “MIT” at repository root does not constitute a complete dependency/asset license clearance.
- “Self-hostable” does not mean operationally trivial, free of infrastructure cost, or automatically secure.
- AI APIs, weights, datasets, logos, music, example footage and output rights are separate from source-code licenses.
- The selected tools are candidates, not integrated product dependencies; this document is not legal advice.

## 6. Review references

- [Everything](https://github.com/HeyPuter/everything/tree/06802a1e3749202e4db94d39c9ef5ab1a97d0ef1)
- [Puter](https://github.com/HeyPuter/puter/tree/2b254b88924dc9a6f58f05423358cc0f593da46d)
- [OpenCut current rewrite](https://github.com/OpenCut-app/OpenCut/tree/e668010778568641babef2cc40be4703ae6916d6)
- [OpenCut classic archive](https://github.com/OpenCut-app/opencut-classic/tree/cf5e79e919144200294fb9fed22a222592a0aeea)
- [ArtCraft client](https://github.com/storytold/artcraft/tree/d4e4ac69bbd93d237eaf5d0260bc6a5ff3a5e373)
- [ArtCraft Services](https://github.com/storytold/artcraft-services/tree/873c5f7318adbf248626ed1809864242e9aa96f2)
