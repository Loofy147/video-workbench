# Roadmap and Exit Gates

**Status:** Staged plan; the initial target user and first workflow are owner-informed working scope. The team still needs measurable acceptance criteria and execution evidence.

## Stage 0 — Product discovery and foundation

- [x] Record the target user as the company owner/operator, with a possible small internal team.
- [x] Define the primary job-to-be-done and a first workflow: business offering to video campaign pack.
- [ ] Validate the selected workflow, required outputs, review/approval rules, and exclusions against an actual company use case.
- [ ] Define measurable acceptance criteria and a representative test workload for the brief, concept, and real video output.
- [x] Audit FastVideo Studio and Dreamverse at an immutable source revision. Decision: copy neither app into the product foundation; use an FFmpeg-backed deterministic assembly path first and reconsider generation only if the workflow proves it needs generated shots.
- [ ] Decide initial product license and contribution policy; review whether public repository visibility is appropriate while that decision remains open.
- [ ] Maintain CI and inspectable decision records.

**Exit gate:** the product owner confirms the first workflow, accepts the first-render output contract, makes a repository visibility/distribution decision before external contributions, and reviews the source-level reuse audit. A written plan alone is not proof that video execution works.

## Stage 1 — Domain contracts and executable skeleton

- [ ] Define project, business brief, concept/script, review/approval, capability, render request, job, attempt, media/document artifact, result, and error contracts.
- [ ] Specify legal state transitions, cancellation, timeout, retry, partial-result behavior, artifact versioning, and provenance links.
- [ ] Implement contract validation and unit tests without a model runtime or GPU dependency.
- [ ] Add structured logs and correlation IDs with secret redaction.
- [ ] Represent a stub backend explicitly as test infrastructure.

**Exit gate:** deterministic tests cover successful, invalid, unapproved, cancelled, timeout, and failure flows; test outputs are distinguishable from real generated media.

## Stage 2 — Business offering to video campaign pack

- [ ] Capture an offering, audience, objective, differentiators, approved claims, call to action, and permitted source/brand assets.
- [ ] Draft an editable brief and script/scene outline; expose missing facts, assumptions, and claims needing confirmation.
- [ ] Require review/approval before producing the video.
- [ ] Submit the approved media-assembly request through the product-owned renderer contract; keep model-generation adapters optional.
- [ ] Retain the actual render lifecycle, renderer/version, settings, source manifest, output artifact/checksum, validation results, and actionable error information.
- [ ] Export the video, brief, script/scene outline, captions/copy, and relevant output metadata.

**Exit gate:** a reviewer can start from the ContribQuest offering, approve the planning artifacts, render and play a real MP4 from approved source assets, inspect provenance and output validation, and export all campaign artifacts. A stub, storyboard, or mock stream does not satisfy the real-video acceptance gate.

## Stage 3 — Final-mile provider/model evaluation

- [ ] Evaluate candidates against the same representative workload and acceptance rubric.
- [ ] Verify exact licenses/terms and operational constraints for each exact artifact or service.
- [ ] Measure quality, claims/brand fit, duration/aspect ratio, latency, throughput, memory/VRAM, cost, reliability, and output restrictions where relevant.
- [ ] Record environment, dependency versions, raw results, failed runs, and uncertainty.
- [ ] Choose only after evidence is reviewed; retain a fallback or document why none is viable.

**Exit gate:** a cited decision record separates measured results from vendor claims, estimates, and unknowns. No candidate is adopted just because its name or benchmark is prominent.

## Stage 4 — Broader company deliverables

- [ ] Prioritize the next output family based on demonstrated value: project scopes, executive/business briefs, presentations, or additional ad/demo formats.
- [ ] Reuse the project/artifact/review foundation instead of creating unrelated one-off generators.
- [ ] Add only workflows with concrete owners, measurable acceptance criteria, provenance, and error/recovery behavior.

**Exit gate:** the next output family has a defined user problem, a testable workflow, and evidence that it adds company value.

## Stage 5 — Beta hardening

- [ ] Complete threat model, data-retention rules, access controls, and secrets management.
- [ ] Validate packaging, observability, backup/recovery, workload limits, cost controls, and deployment rollback.
- [ ] Run end-to-end acceptance tests on representative hardware and inputs.
- [ ] Publish operating instructions and known limitations.

**Exit gate:** beta acceptance review with unresolved risks, owners, and rollback plan recorded.

## Cross-stage rule

Do not promote a stage based on documentation alone where executable evidence is required. Keep observed execution, simulation, hypothesis, estimate, and unverified claim distinguishable in test reports and decision records.
