# Roadmap and Exit Gates

**Status:** The first local browser vertical slice is implemented on the open draft PR. It now captures a campaign plan, saves versioned briefs/manifests, invokes the real local renderer, and exposes technical validation/provenance. It is still a single-machine pilot, not a deployed multi-user application.

## Stage 0 — Product discovery and foundation

- [x] Record the target user as the company owner/operator, with a possible small internal team.
- [x] Define the primary job-to-be-done and first workflow: business offering to video campaign pack.
- [ ] Validate the workflow, required outputs, review/approval rules, and exclusions against an actual company use case.
- [ ] Define measurable acceptance criteria and representative workload for brief, concept, and real video output.
- [x] Audit FastVideo Studio and Dreamverse at an immutable source revision. Decision: copy neither app into the product foundation; use deterministic FFmpeg assembly first.
- [ ] Resolve license and distribution policy. The PolyForm Internal Use 1.0.0 proposal is not final while the GitHub repository is public. Decide whether to make the repository private before approving an internal-use license; otherwise select a grant consistent with intended distribution.
- [x] Maintain CI and inspectable decision records.

**Exit gate:** The product owner confirms the first workflow, accepts the first-render output contract, makes a repository visibility/distribution decision before external contributions, and reviews the reuse audit. A written plan alone is not proof that video execution works.

## Stage 1 — Domain contracts and executable skeleton

- [ ] Define and stabilize the project, brief, concept/script, review/approval, capability, render request, job, attempt, artifact, result, and error contracts.
- [ ] Specify legal state transitions, cancellation, timeout, retry, partial-result behavior, and artifact versioning/provenance links.
- [x] Implement versioned campaign manifests and deterministic local render tests without a model or GPU dependency.
- [x] Add a loopback-only browser pilot to capture a brief/storyboard, persist versioned plan artifacts, invoke the renderer, and inspect/download outputs.
- [ ] Add structured logs and correlation IDs with secret redaction.
- [ ] Implement cancellation/retry and attempt history before introducing long-running or shared workloads.
- [ ] Define a durable persistence and backup approach if real multi-user or recovery requirements justify it.

**Exit gate:** Deterministic tests cover successful, invalid, unapproved, cancelled, timeout, and failure flows; test output is distinguishable from genuine captured product footage.

## Implemented vertical slice — 2026-10-15

- [x] Render title cards, still-image scenes, video clips, and optional background audio through an installed FFmpeg executable.
- [x] Validate H.264 codec, dimensions, frame rate, expected duration, exact decoded frame count, and optional AAC audio with FFprobe.
- [x] Write a sidecar manifest with input-manifest hash, source hashes/provenance, tool versions, output hash/size, claim-evidence records, approval state, and release blockers.
- [x] Reject unsafe relative paths, unsupported media types, invalid limits, duplicate scene IDs, and default overwrite attempts.
- [x] Block unwatermarked CLI output unless the manifest contains a timezone-aware approval record and supported claim-evidence states.
- [x] Provide a loopback-only browser flow for business offering, audience, objective, differentiators, call to action, and card storyboard.
- [x] Persist each saved plan as a versioned Markdown brief and JSON campaign manifest without overwriting earlier versions.
- [x] Render a watermarked 1280×720 draft from the saved version and expose playback/download plus the provenance/technical validation report.
- [x] Keep local project records and generated artifacts under Git-ignored .workbench/projects/.

**Scope limit:** The browser UI has no login, role system, authenticated approval, asset uploads, remote access, durable job queue, database, encrypted-at-rest guarantee, deployment, or live ContribQuest walkthrough. All browser renders retain a fixed NOT FOR PUBLICATION watermark. Renderer approval/evidence fields remain assertions, not independently authenticated or verified evidence.

## Stage 2 — Business offering to video campaign pack

- [x] Capture offering, audience, objective, differentiators, call to action, and a short card storyboard.
- [x] Draft and save an editable Markdown brief and versioned JSON render manifest.
- [x] Submit the current saved campaign version through the product-owned deterministic renderer.
- [x] Retain the actual renderer result summary, checksum/media properties, validation status, and release blockers.
- [ ] Add source-aware structured claim/evidence entry and clearly expose missing facts, assumptions, and claims requiring confirmation.
- [ ] Add safe asset intake with file-size/type limits, media probing, provenance capture, rights policy, and approved local asset references.
- [ ] Implement reviewer identity and authority, authenticated review/approval history, and an immutable decision trail before any unwatermarked or publishable release path exists.
- [ ] Export a reviewed pack containing brief, script/scene outline, captions/copy, video, and relevant output metadata.
- [ ] Validate the workflow against the live ContribQuest product using distinct owner/reviewer roles and genuine source evidence; record the walkthrough before producing public product claims.

**Exit gate:** A reviewer can start from the actual ContribQuest offering, review the planning artifacts, render and play an MP4 from permitted inputs, inspect provenance and output validation, and export the complete pack. A mock or storyboard alone does not satisfy the real-video acceptance gate.

## Stage 3 — Final-mile provider/model evaluation

- [ ] Evaluate candidates against the same representative workload and acceptance rubric.
- [ ] Verify exact licenses/terms and operational constraints for each exact artifact or service.
- [ ] Measure quality, claims/brand fit, duration/aspect ratio, latency, throughput, memory/VRAM, cost, reliability, and output restrictions where relevant.
- [ ] Record environment, dependency versions, raw results, failed runs, and uncertainty.
- [ ] Choose only after evidence is reviewed; retain a fallback or document why none is viable.

**Exit gate:** A cited decision record separates measured results from vendor claims, estimates, and unknowns. No candidate is adopted just because its name or benchmark is prominent.

## Stage 4 — Broader company deliverables

- [ ] Prioritize the next output family based on demonstrated value: project scopes, executive/business briefs, presentations, or additional ad/demo formats.
- [ ] Reuse the project/artifact/review foundation instead of creating unrelated one-off generators.
- [ ] Add only workflows with concrete owners, measurable acceptance criteria, provenance, and error/recovery behavior.

**Exit gate:** The next output family has a defined user problem, a testable workflow, and evidence that it adds company value.

## Stage 5 — Beta hardening

- [ ] Complete threat model, data-retention rules, access controls, and secrets management.
- [ ] Validate packaging, observability, backup/recovery, workload limits, cost controls, and deployment rollback.
- [ ] Run end-to-end acceptance tests on representative hardware and inputs.
- [ ] Publish operating instructions and known limitations.

**Exit gate:** Beta acceptance review with unresolved risks, owners, and rollback plan recorded.

## Cross-stage rule

Do not promote a stage based on documentation alone where executable evidence is required. Keep observed execution, simulation, hypothesis, estimate, and unverified claim distinguishable in test reports and decision records.
