# Selective-Reuse Audit: FastVideo Studio and Dreamverse

**Review date:** 2026-10-15  
**Status:** Source-level audit complete for product-foundation decisions; no application code has been copied and no runtime/install/build test was run as part of this review.  
**Reviewed source snapshot:** [Loofy147/FastVideo](https://github.com/Loofy147/FastVideo/tree/d5253fd71055927f12aa6c4aa679b93a00238851) at `d5253fd71055927f12aa6c4aa679b93a00238851` (2026-10-09 commit shown by GitHub). The repository is a fork of `hao-ai-lab/FastVideo` and its root license metadata reports Apache-2.0.

## Decision summary

**Do not adopt either application as the Video Workbench product base and do not copy code at this stage.** The current product need is to turn approved company source material into reviewable briefs, storyboards, screen-led demonstrations, and exported campaign videos. Both applications are model/GPU-runtime-oriented tools with different primary workflows.

For the first demonstrable vertical slice, use a **deterministic local media-assembly path**: approved screen recordings, still images, title/motion cards, captions, and optional approved audio assembled into a real MP4 through an explicitly invoked FFmpeg executable. Keep generative video as an optional capability behind a product-owned adapter. This yields a concrete export without making the first workflow depend on a particular model, model weights, external prompt APIs, or a supported GPU. Check the installed FFmpeg build and codec availability at runtime; do not bundle an FFmpeg binary until its exact build/license and redistribution obligations are reviewed.

Revisit Dreamverse only if the campaign workflow proves it needs generated or streamed shots that cannot be supplied more simply from approved footage and graphics. Keep FastVideo Studio as an engineering reference for local job management rather than a product dependency.

## Candidate A — FastVideo Studio

**Source:** [README](https://github.com/Loofy147/FastVideo/blob/d5253fd71055927f12aa6c4aa679b93a00238851/apps/fastvideo_studio/README.md), [package manifest](https://github.com/Loofy147/FastVideo/blob/d5253fd71055927f12aa6c4aa679b93a00238851/apps/fastvideo_studio/package.json), [API server](https://github.com/Loofy147/FastVideo/blob/d5253fd71055927f12aa6c4aa679b93a00238851/apps/fastvideo_studio/server.py), [job runner](https://github.com/Loofy147/FastVideo/blob/d5253fd71055927f12aa6c4aa679b93a00238851/apps/fastvideo_studio/job_runner.py).

### Observed fit

- Provides a web UI for inference, fine-tuning/distillation, datasets, and gallery output.
- Uses a Next.js frontend and FastAPI backend, with a local SQLite database and a background job runner.
- Documents unit tests and browser tests; the documented Playwright workflow uses a mock backend, so those tests should not be confused with proof of real-model execution.

### Gaps and risks for this product

- The primary domain is operating model jobs and GPU workloads, not business briefs, approved-claim management, rights/provenance, creative review, campaign artifacts, and export packages.
- Importing its job runner would bring framework and runtime assumptions before Video Workbench has established its own product contracts.
- In the inspected API module, CORS is configured with `allow_origins=["*"]`. That is not by itself proof of an exploitable issue, but it is an explicit reason not to expose the service directly to an untrusted network without a full authentication, authorization, and deployment review.
- Its model/job UI and mock-backed tests are useful reference patterns, not proof of a suitable security or execution boundary for Video Workbench.

**Disposition:** No code reuse. Revisit only for a specific, demonstrated need; any candidate must be reviewed at an immutable source revision and pass license, dependency, test, security, and adaptation-cost gates.

## Candidate B — Dreamverse

**Source:** [README](https://github.com/Loofy147/FastVideo/blob/d5253fd71055927f12aa6c4aa679b93a00238851/apps/dreamverse/README.md), [backend dependency definition](https://github.com/Loofy147/FastVideo/blob/d5253fd71055927f12aa6c4aa679b93a00238851/apps/dreamverse/pyproject.toml), [generation backend contract](https://github.com/Loofy147/FastVideo/blob/d5253fd71055927f12aa6c4aa679b93a00238851/apps/dreamverse/dreamverse/generation_contracts.py), [asset routes](https://github.com/Loofy147/FastVideo/blob/d5253fd71055927f12aa6c4aa679b93a00238851/apps/dreamverse/dreamverse/routes/assets.py).

### Observed fit

- It is the closer of the two applications to the eventual need for generated video: it supports real-time generation/editing, streams results, manages media assets, and defines a `GenerationBackend` protocol for model-specific generation implementations.
- Its web UI and Python backend demonstrate an existing streaming-media workflow. The repository also includes a mock server to exercise parts of the frontend and AV pipeline without a GPU.

### Gaps and risks for this product

- It is still a model/runtime application, not a campaign workflow system. The current Video Workbench needs product-owned brief/script/approval records, claims evidence, asset rights, output versioning, and export metadata.
- Installation pulls in the FastVideo runtime and model-specific dependencies. The documented real-generation path needs compatible compute and model artifacts; the README warns that cold-start compilation/warmup can take tens of minutes for some profiles. Prompt rewrite/enhancement may also use external API credentials.
- The mock streaming server is useful for interface testing, but mock media is not evidence of real model execution.
- The inspected materials do not establish that its session and asset endpoints provide the project-level authorization, retention, audit, and tenant boundaries this product requires. Conduct a deployment/route security review before any network-facing integration.

**Disposition:** No code reuse in the first slice. If real generative shots become a proven requirement, prototype Dreamverse as an isolated optional backend through a product-owned adapter. Do not make its UI, session protocol, model stack, or runtime the source of truth for Video Workbench.

## License and provenance assessment

- GitHub identifies the reviewed FastVideo fork as derived from `hao-ai-lab/FastVideo`; root license metadata and the checked-in root `LICENSE` identify Apache License 2.0 for the repository source.
- That finding is **not** a blanket license for every linked model checkpoint, dataset, API, package, brand asset, or generated input/output. Each external artifact and dependency keeps its own terms and obligations.
- If a future change copies or adapts source code, pin the exact source revision, record the files and changes, preserve applicable notices/license text, and check all relevant dependencies and upstream provenance before merging.
- No FastVideo source or model artifacts were copied by this audit.

## Immediate implementation policy

1. Build the product-owned campaign workflow and artifact/approval records independently of either application.
2. Implement a small renderer capability that assembles approved media into a real MP4 using a verified external FFmpeg installation; fail clearly when a required binary, codec, input, or output validation step is unavailable.
3. Preserve a source manifest: project/brief/script revisions, input asset identifiers and rights, render parameters, renderer/version, timestamps, validation results, output hash, and any warnings/errors.
4. Test deterministic rendering with licensed or self-created fixtures, including missing input, unsupported media, failed render, and invalid output. A stub, storyboard, or mock stream cannot satisfy the real-MP4 acceptance gate.
5. Keep generative backends optional. Reconsider Dreamverse only against a representative campaign task, known compute budget, actual-output test, cancellation/failure behavior, and a reviewed security boundary.

## Explicitly unresolved owner decision

The Video Workbench repository is currently public and has no selected project license. Because the declared initial use is internal company work, this audit does not choose an open-source license or change repository visibility on the owner's behalf. Before inviting external contributors or adding confidential company assets, the owner must choose the distribution model and confirm whether the repository should remain public. No license or redistribution right should be inferred from visibility alone.
