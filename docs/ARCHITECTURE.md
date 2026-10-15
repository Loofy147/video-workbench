# Architecture — Initial Boundaries

**Status:** Proposed logical boundaries; no application framework or deployment topology has been selected.

## Architectural intent

Keep product contracts **provider-independent**: concepts should remain independent from any one model, vendor, or inference framework. External systems should be integrated behind explicit adapters. Product-level contracts should remain testable without downloading weights or requiring a GPU.

This is an internal company-use workbench first. It should support related business and media artifacts while keeping the first implementation focused on the business-offering-to-video-campaign workflow.

## Proposed logical components

1. **Product interface** — company/project context, brief and concept editing, review/approval, job progress, artifact inspection, and export. The first interface technology is undecided.
2. **Application orchestration** — validates requests, checks required approvals, applies policy and defaults, creates jobs, dispatches work, handles cancellation/retry, and reports results.
3. **Domain contracts** — typed representations for projects, business briefs, concepts/scripts, review states, capabilities, jobs, attempts, artifacts, errors, and execution metadata. These contracts should not import a specific provider SDK.
4. **Provider/runtime adapters** — translate the approved product request to a selected runtime and normalize progress, outputs, and errors back to product contracts.
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

## Selection gates

Choose the stack only after the target workflow and non-functional requirements are known. Choose a persistence layer after defining durability and concurrency expectations. Choose providers/models after a representative workload and acceptance rubric exist, normally at the final-mile evaluation gate.

## Non-goals for this document

This is not yet a detailed deployment architecture, API specification, database schema, threat model, or production readiness claim. Those require a selected workflow and evidence from a running vertical slice.
