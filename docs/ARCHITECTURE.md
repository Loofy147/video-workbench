# Architecture — Initial Boundaries

**Status:** Proposed logical boundaries; no application framework or deployment topology has been selected.

## Architectural intent

Keep product contracts **provider-independent**: concepts should remain independent from any one model, vendor, or inference framework. External systems should be integrated behind explicit adapters. Product-level contracts should remain testable without downloading weights or requiring a GPU.

This is an internal company-use workbench first. It should support related business and media artifacts while keeping the first implementation focused on the business-offering-to-video-campaign workflow.

## Proposed logical components

1. **Product interface** — company/project context, brief and concept editing, review/approval, job progress, artifact inspection, and export. The first interface technology is undecided.
2. **Application orchestration** — validates requests, checks required approvals, applies policy and defaults, creates jobs, dispatches work, handles cancellation/retry, and reports results.
3. **Domain contracts** — typed representations for projects, business briefs, concepts/scripts, review states, capabilities, jobs, attempts, artifacts, errors, and execution metadata. These contracts should not import a specific provider SDK.
4. **Execution adapters** — implement product-owned capabilities behind stable contracts. The first video adapter assembles approved media with an installed FFmpeg executable; any later model/runtime adapter normalizes progress, outputs, and errors without owning project or artifact records.
5. **Artifact and provenance layer** — tracks artifact identity/type (document or media), versions, source project, upstream inputs, reviewer/approval status, dimensions/duration when known, checksums when practical, storage reference, rights/provenance, and export metadata.
6. **Persistence and queue** — stores durable project/job/artifact state and supports background work where the chosen workload requires it. Database and queue technology remain open.
7. **Observability and evaluation** — captures correlation IDs, lifecycle events, timings, resource/cost estimates when available, and reproducible quality evaluation data.

These are logical responsibilities, not a mandate to deploy seven separate services. The initial implementation should prefer the smallest structure that preserves clear contracts and enables testing.

## Provisional job lifecycle

The starting state model is:

`draft → queued → running → succeeded | failed | cancelled`

The job lifecycle is separate from review state. A generated draft may be successful as a job but not approved for publication. Review status should therefore be recorded on the relevant artifact/version instead of overloading job status. The implementation may refine this state machine after retry, cancellation, partial output, and resume semantics are specified. A retry should be traceable as an attempt; it must not silently erase the failed attempt.

## Contract principles

- Include stable project, artifact, job, attempt, and correlation IDs where appropriate.
- Record the business inputs, approved claims, normalized request, relevant settings, provider/runtime identity, timestamps, and attempt information.
- Keep assumptions and claims requiring human confirmation visible; do not silently invent factual company claims.
- Separate user-facing errors from internal diagnostics; redact secrets from logs.
- Represent outputs as artifact references and metadata; do not embed video bytes in job JSON.
- Link generated video to the brief/concept versions and user approval from which it was produced.
- Make cancellation, timeout, retry, partial-failure, review, and export behavior explicit.
- Record the versions or revisions needed to understand how a result was produced, subject to provider availability.
- Do not claim reproducibility when a remote provider cannot guarantee it.

## Initial execution choice

The first demonstrable video path is deterministic media assembly with an installed FFmpeg executable, not generative inference. The product should compose owner-approved screen recordings, still images, title/motion cards, captions, and approved audio into a real MP4. Check for the executable and required codecs at runtime, validate the resulting file, and report failure explicitly. Do not bundle FFmpeg until the exact distribution/build and its license obligations have been reviewed. This choice keeps the first workflow usable on ordinary hardware and avoids making the product's business workflow depend on GPU access, model weights, or vendor accounts.

Model-based generation remains an optional capability for future shots. If adopted, it must sit behind a product-owned contract and be evaluated independently for cost, quality, runtime, terms, output provenance, security, cancellation, and error handling.

## Current executable slice

The CLI implementation lives in `src/video_workbench/render.py` and `tools/render_campaign.py`. It validates a versioned JSON campaign manifest, constrains input paths to the campaign directory, records SHA-256 checksums and supplied provenance, assembles card/image/video scenes and optional audio with FFmpeg, validates the output with FFprobe, and writes a sidecar manifest. A default review watermark is used. Unwatermarked rendering requires an approval record and supported claim-evidence states, but those records are manifest assertions rather than an authentication system or independent legal/factual review.

The renderer is tested independently of a model, API, GPU, database, or web frontend. It is an executable vertical-slice foundation, not yet a full application workflow.

## Selection gates

Choose the UI framework and persistence layer only when the first workflow and non-functional requirements justify them. Keep the initial implementation as small as possible. Consider a model/runtime only after a representative workload demonstrates that generated media adds value beyond recorded footage, graphics, and captions.

## Non-goals for this document

This is not yet a detailed deployment architecture, API specification, database schema, threat model, or production readiness claim. Those require evidence from a running vertical slice.
