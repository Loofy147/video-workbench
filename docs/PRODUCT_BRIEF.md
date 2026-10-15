# Product Brief

**Status:** Discovery draft — target use and first workflow proposed from the project owner's stated company use cases. Acceptance criteria and technical implementation still require validation.

## Product intent

Build a standalone, internal company production workbench that turns business goals and source materials into structured, reviewable deliverables. It should support business demonstrations, advertising videos, briefs, project scopes, and other useful company outputs over time. The product owns the workflow and records; models, providers, and generation frameworks remain replaceable capabilities behind explicit interfaces.

This is an internal company-use product first, not a public multi-tenant SaaS commitment. It is not yet a production-ready video pipeline.

## Target user

The primary user is the company owner/operator. The initial user group may include a small internal team responsible for planning work, explaining company offerings, and producing business and marketing materials. The product should optimize for one company’s workflows and reusable assets before investing in public onboarding, multi-tenant access, billing, or marketplace features.

## Primary job-to-be-done

When the company has a product/service offering, business objective, or initiative to communicate, the owner/operator needs to turn rough notes and existing materials into a coherent, brand-consistent, reviewable deliverable package — so that the company can explain, pitch, promote, and execute the work without rebuilding context across disconnected tools.

## First demonstrable end-to-end workflow: business offering to video campaign pack

**Input:** A company offering or service, target audience, objective, differentiators, approved claims, call to action, available brand/reference assets, and intended destination/channel.

1. **Capture the business intent.** Create a project and record the offering, audience, goal, constraints, supporting material, rights/provenance, and intended output.
2. **Draft the brief.** Produce a structured creative brief from the source information. Keep assumptions and missing facts visible; require user review of claims and sensitive details before moving forward.
3. **Develop the video concept.** Generate a proposed script, scene/shot outline, duration target, style notes, aspect ratio, captions, and call to action from the approved brief.
4. **Review and revise.** Let the user edit/approve the brief and concept before media generation or assembly. Preserve revisions and the relationship between outputs.
5. **Produce the video.** Route the approved request through a provider-neutral capability contract to a chosen video backend when one is selected. Early contract/workflow tests may use an explicitly labeled stub, but a stub must never be represented as actual model execution.
6. **Inspect and export.** Show the video result or an actionable failure, retain the input/settings/backend and job metadata, and export the approved video with its brief, script, storyboard/shot outline, caption/copy, and output details.

This campaign pack is the first vertical slice because it connects business context, a required planning artifact, a visual output, review, and export in one traceable workflow. The brief and concept must remain useful deliverables even when video generation fails or is not yet configured.

## Pilot offering for the first campaign pack

Use **Contribution Network / its current ContribQuest prototype** as the first real offering to test this workbench workflow, subject to owner review of the final messaging. The application source of truth is [Loofy147/Contribution-bounties-centre-](https://github.com/Loofy147/Contribution-bounties-centre-). Its README identifies Contribution Network as the strategic project and ContribQuest as the current live prototype. The separate [contribution-cloud/Contributions-centre](https://github.com/contribution-cloud/Contributions-centre) is described there as a future portfolio/repository control plane, not the current application runtime.

### Proposed demonstration

Create a concise product explainer/demo that communicates the problem, the contribution/bounty workflow, and how work is reviewed. A proposed initial target is a 45–60 second video, but timing and format remain acceptance choices to validate.

### Draft campaign pack

A source-grounded, owner-review draft brief and timed storyboard is maintained at [docs/examples/contribution-network-campaign-brief.md](examples/contribution-network-campaign-brief.md). It separates documented claims from unverified live behavior, makes the absence of in-app payout processing explicit, and prohibits claims of production readiness or validated market demand. The script, CTA, format, and publication remain unapproved until the actual application is inspected and the owner reviews the pack.

Ground the script and visuals in inspected source material:
- A bounty can define 1–10 distinct acceptance criteria.
- A submitted contribution is reviewed against the preserved criteria snapshot.
- The owner records pass/fail for each criterion and provides written rationale; acceptance is blocked unless every criterion passes.
- Work can be accepted, rejected, or returned for changes, with revision/review history preserved.
- The prototype records 50 platform XP for acceptance and increments an accepted-work counter; XP is not independently validated as a measure of skill.
- Paid bounty entries are listings only in the current prototype; there is no escrow, payment processing, or guaranteed payout.

### Claims and demonstration safeguards

- Describe ContribQuest as a current prototype, not as proven production-ready infrastructure.
- Do not imply that paid bounties are paid out through the app.
- Do not present platform XP as a validated skill score.
- Do not claim complete live end-to-end verification; the source README says its browser scenarios still need live execution with separate contributor and bounty-owner identities.
- Do not imply the source snapshot builds or runs independently of AppDeploy; the README explicitly records unresolved AppDeploy SDK/client dependencies.
- Clearly label fictional demonstration records and simulated activity. Do not expose real contributor information or private company data without approval.

The output package should include the approved creative brief, claims/evidence ledger, script, scene/shot outline, caption/voiceover copy, final video or explicit failure record, and export metadata. If the real video backend is not yet available, complete and review the planning artifacts first and label any rendered mock/animatic accurately.

## Broader outcome families — not all MVP scope

The same project/artifact foundation may later support:
- Product, service, company, or process demonstration videos.
- Advertising videos and accompanying campaign copy/captions.
- Business briefs and executive summaries.
- Project scopes, objectives, requirements, milestones, risks, and acceptance criteria.
- Presentations and other useful company-facing or internal deliverables.

These are product directions, not a commitment to ship all output types in the first release. Once the campaign-pack workflow is validated, select the next output family based on company value and implementation evidence. A standalone project-scope workflow may follow; it should not delay the first video campaign path unless the user validates it as more valuable.

## Boundaries for the first version

### Include in discovery and the first vertical slice
- Company/project context and a structured source brief.
- Explicit editable stages with user approval before video production.
- Reusable domain contracts for projects, jobs, document artifacts, media assets, errors, and provenance.
- Job status, traceable inputs/settings, safe error reporting, and output export.
- Record source/reference asset permissions and provenance where applicable.
- Tests for successful, invalid, failed, and stubbed execution paths.
- Evidence that distinguishes proposed content, user-approved claims, real media generation, and synthetic/test results.

### Defer
- Public SaaS, multi-tenant accounts, billing, marketplace, and broad collaboration features.
- A full document-generation suite or a generalized “make anything” agent in the first iteration.
- Advanced timeline editing, complex compositing, or a full professional editing suite unless the selected workflow proves they are necessary.
- Commitment to a specific model, provider, paid API, GPU platform, or deployment topology before the final-mile evaluation.
- Model weights, benchmark claims, and provider bake-offs before a representative workload and acceptance rubric exist.
- Adoption of FastVideo Studio/Dreamverse code before the selective-reuse, source/license, dependency, build/test, and security audit is recorded.

## Architecture principles

- Keep product and domain contracts provider-independent.
- Use explicit adapters for video generation, document generation, and media-processing capabilities.
- Treat each deliverable as a versioned artifact linked to its source project, inputs, review state, and generation/job history.
- Record job lifecycle states, errors, timestamps, execution identity, and relevant settings without leaking secrets.
- Do not embed large media bytes in job records; store references and metadata.
- Keep the smallest architecture that supports the selected workflow; do not introduce a microservice or database for every logical component.

## Success criteria to validate

For the first demonstrable workflow, a reviewer should be able to start from a real company offering, inspect and approve the brief and script, see how the video was produced or why it failed, and export the resulting assets with their provenance. Define measurable quality, duration, aspect-ratio, brand/claims, runtime, and cost criteria before selecting the real backend. No real inference capability should be claimed without an actual output and execution trace.

## Discovery exit gate

Do not call the MVP scope complete until the repository records:
- Confirmed target user and primary job-to-be-done.
- A bounded campaign-pack workflow with explicit exclusions.
- Acceptance criteria for both document artifacts and the video artifact.
- A review/approval step and handling for missing facts or disallowed claims.
- A representative test workload and evaluation rubric.
- The FastVideo Studio/Dreamverse selective-reuse findings.
- A documented plan for evaluating real video backends at the final-mile gate.
