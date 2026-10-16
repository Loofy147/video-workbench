# Contribution Network / ContribQuest — Pilot Campaign Brief

**Status:** Draft for owner review. Not approved for publication.  
**Document type:** Internal product-explainer campaign pack  
**Prepared for:** Video Workbench first end-to-end workflow  
**Proposed duration:** 45–60 seconds; validate against the actual edit  
**Proposed format:** 16:9 screen-led explainer with captions; create vertical cuts only after the primary edit is approved  
**Evidence date:** 2026-10-15  
**Source of truth for current app behavior:** [Contribution-bounties-centre- README](https://github.com/Loofy147/Contribution-bounties-centre-/blob/main/README.md)

## 1. Purpose and release boundary

Use the current ContribQuest prototype as a real, inspectable pilot for Video Workbench. The immediate goal is to explain its documented bounty-and-review workflow and give an internal reviewer a practical way to inspect that workflow. This is **not yet a paid acquisition campaign** and must not imply validated external demand, production readiness, or guaranteed financial outcomes.

The asset is a planning concept until the owner approves the facts, records actual product footage, approves the edit, and confirms the publishing destination and rights. No finished video is represented by this document.

## 2. Audience, objective, and message

**Primary audience:** The company owner/operator and early reviewers or potential collaborators who need to understand the current prototype.

**Audience problem:** Work requests can be ambiguous when scope, completion conditions, and review decisions are not explicit.

**Communication objective:** Make the prototype's documented review mechanism understandable in under one minute, then invite the viewer to inspect the current prototype and report gaps.

**Single takeaway:** ContribQuest structures a bounty around explicit acceptance criteria and preserves a traceable review/revision path.

**Desired action for this pilot:** Open the current prototype, exercise the relevant flow where access permits, and report what was observed, what failed, and what remains unverified. Do not ask for payment, contribution, or personal data as a campaign conversion unless the owner explicitly approves that request and its terms.

**Message hierarchy**
1. A bounty can define 1–10 distinct acceptance criteria.
2. A contribution retains a snapshot of the criteria used for review.
3. The owner records pass/fail per criterion and written rationale; acceptance is blocked unless all criteria pass.
4. Work can be accepted, rejected, or returned for changes, while revision/review history is preserved.
5. The current prototype has material limits that must not be hidden or contradicted.

## 3. Creative direction

**Tone:** Clear, practical, evidence-led; show the workflow, not abstract claims of innovation.

**Visual approach:** Screen-led walkthrough with restrained titles and captions. Capture actual current UI only after checking that every depicted state is real and accessible. Use close-ups of criterion lists, review decisions, and revision history only if those elements can be demonstrated in the live app. If exact states cannot be reached, use a neutral diagram labeled “workflow concept” instead of fabricating a product screen.

**Motion and pacing:** One idea per scene; simple cuts or restrained highlights. Avoid visual effects that obscure whether a state came from the real application or a designed illustration.

**Audio:** Voiceover optional. Captions must carry the full meaning without audio. Use licensed or original music only after rights and usage terms are checked.

**Branding:** Use only owner-approved logos, type, color, product name, and screenshots. Do not copy private or third-party marks into the edit without permission.

**Frame and safe areas:** Proposed master 1920×1080, 16:9. Keep captions and critical labels away from the edges. These are production proposals, not approved delivery specs.

## 4. Draft timed storyboard and script

All timings and narration below are proposed. Replace illustrative visuals with actual captured states after a live walkthrough. If a promised state cannot be demonstrated, rewrite the line or remove the shot rather than simulating success.

| Time | Scene purpose | Picture / on-screen direction | Draft narration / caption | Evidence and production notes |
|---|---|---|---|---|
| 0–6s | State the problem | Plain opening title; then cut to a real bounty/task view if suitable | “Useful work needs more than a task title. It needs clear expectations and an inspectable decision.” | General framing, not a measurable product claim. Do not imply that every ambiguity is solved by the prototype. |
| 6–14s | Explain scope | Show an actual bounty's acceptance-criteria section; highlight the list only if the UI supports it | “In ContribQuest, a bounty can define one to ten distinct acceptance criteria.” | Verify the current UI and value range against the source README. If the UI cannot show this, use a clearly labeled explanatory graphic. |
| 14–22s | Show traceability | Show a real contribution record and its criteria snapshot, if the current UI exposes it | “When work is submitted, the criteria snapshot stays with the contribution—so review uses the agreed target.” | The source README documents a snapshot. Validate the corresponding live behavior before using screen footage that claims to prove it. |
| 22–34s | Explain review gate | Show each actual pass/fail decision and the written-rationale area; use no fabricated status values | “The owner records pass or fail for each criterion, with a written reason. Acceptance is blocked until every criterion passes.” | Demonstrate the gate with a safe test record before release. Do not create fake production-looking evidence. |
| 34–43s | Explain the revision path | Show an actual return-for-changes/revision/history path, if available in the live app | “Work can be accepted, rejected, or returned for changes, with revision and review history preserved.” | The behavior is documented in the README; live end-to-end execution remains a separate verification requirement. |
| 43–52s | Make the prototype boundary visible | Product name plus a readable disclosure; do not use a fake metrics dashboard | “ContribQuest is a current prototype. Paid bounty listings are not processed payouts, and live end-to-end verification is still outstanding.” | Keep this disclosure legible on screen long enough to read. Do not soften it into ambiguous language. |
| 52–60s | Pilot call to action | Show the real prototype landing page, only if the current link is accessible and the owner approves external linking | “Explore the prototype, exercise the workflow, and report what succeeds—and what still needs work.” | Pilot CTA: inspect and report. This is not a validated commercial conversion funnel. |

### Short caption-only alternative

“Clear criteria. A traceable review. A visible revision path. ContribQuest is a current prototype for structuring bounty work and reviewing contributions against explicit acceptance criteria. Paid bounty listings are not processed payouts, and live end-to-end verification is still outstanding. Explore the prototype and report what succeeds—and what still needs work.”

Use this alternative only after the owner approves the wording and confirms that the linked experience supports the requested inspection.

## 5. Claims and evidence ledger

Treat the source repository as the authority for documented behavior, not proof that each behavior has passed live end-to-end testing.

| Proposed claim | Current evidence | Permitted wording | Restriction before publication |
|---|---|---|---|
| Bounties support 1–10 distinct criteria | [Source README — Product model](https://github.com/Loofy147/Contribution-bounties-centre-/blob/main/README.md) | “A bounty can define 1–10 distinct acceptance criteria.” | Confirm that the current UI does not contradict the documented model. |
| Submitted work preserves the criteria used for review | Source README documents a criteria snapshot on the contribution | “The contribution preserves a snapshot of the criteria used for review.” | Do not suggest the snapshot itself independently proves the work is correct. |
| Owner records pass/fail per criterion, with written rationale; acceptance requires all to pass | Source README documents the review gate | State the workflow exactly as documented. | Capture a real walkthrough or show an explanatory diagram clearly labeled as such. |
| Work can be accepted, rejected, or returned for changes; history is preserved | Source README documents decisions and revision/review history | Use the literal workflow language. | Verify current interface paths live; do not imply the browser scenarios have already passed. |
| Acceptance currently grants 50 platform XP and increments the accepted-work count | Source README documents this current rule | Omit from the main script. If ever mentioned, state that XP is not an independently validated skill measure. | Do not use XP or accepted-work totals as proof of skill, business value, reliability, or impact. |
| Paid bounty entries exist as listings | Source README documents listings and explicitly excludes payment infrastructure | “Paid bounty listings are not processed payouts.” | Never imply escrow, in-app payment processing, guaranteed payouts, or that contributors will receive money through the current prototype. |
| The app is fully verified or production-ready | Source README says five browser scenarios still need live execution with separate contributor and bounty-owner accounts; standalone build remains unproven outside AppDeploy | **Do not make this claim.** | No production-readiness badge, uptime claim, security guarantee, or “fully tested” wording. |
| The prototype proves external demand or commercial viability | The strategic [first-consumer charter](https://github.com/Loofy147/contribution-network/blob/main/docs/10-first-consumer-project-charter.md) distinguishes founder usefulness from external demand and product-market fit | **Do not make this claim.** | Internal dogfooding and a working prototype do not establish demand, repeatable economics, or product-market fit. |

## 6. Explicitly prohibited or unapproved messaging

Do not state or visually imply any of the following without new, direct evidence and owner approval:

- “Guaranteed payouts,” “escrow protected,” “pay contributors automatically,” or any equivalent financial promise.
- “Verified skills,” “certified contributor,” or treating XP as a validated measure of competence.
- “Production-ready,” “fully tested,” “secure by design” as an assurance, or “independently verified” for behavior that has not been independently checked.
- “Proven demand,” “market leader,” “trusted by teams,” customer counts, completion rates, success rates, or ROI figures without traceable evidence.
- That the application builds or runs independently of AppDeploy; the source README says the checked-in package manifest does not declare its AppDeploy SDK/client dependencies.
- That the future **contribution-cloud/Contributions-centre** repository is the current app runtime or an active dependency.
- Fake contributor names, testimonials, customer logos, bounty values, payment events, success dashboards, acceptance states, or usage metrics presented as real.
- Any real person's identity, contribution data, private project information, or screenshot used without appropriate permission.

## 7. Public landing page inspection (read-only, 2026-10-16)

**Method:** Fresh JavaScript-rendered page extraction plus a read-only browser walk of the public site. No sign-in, form submission, data creation, edit, contribution submission, review, GitHub connection, or persistent mutation was performed.

### What was visible

- The public landing page loaded at the [current prototype URL](https://contribquest-lygj1x.v2.appdeploy.ai/).
- The hero reads “Your contribution HQ” and “SMALL CONTRIBUTIONS. REAL PROOF.”
- Public counters show **9** open bounties. XP, accepted-work, and in-review values are blank/dash when signed out; the XP caption says “Sign in to track XP”.
- The “High-signal opportunities” area displays two cards marked **Example**, attributed to “Community showcase”: a UX review showing **$220 offered**, and a translation task showing **$140 offered**.
- A “Reputation path” section shows “0 accepted / 2 to go” and the page says “50 XP per accepted contribution”.
- Public navigation includes “Explore bounties”, “Sign in to contribute”, “Post a bounty”, search, category filtering, and bounty-type filtering.

### What the read-only browser walk confirmed

| Check | Observation | Evidence boundary |
|---|---|---|
| Open landing page | Loaded successfully | Confirms public page availability at inspection time only |
| Open “Explore bounties” | Navigated to a “The Bounty Board” view with search and filter controls | Individual bounty detail cards and live criteria were not fully inspected in this run |
| Open “My contributions” | View displayed a sign-in-gated/empty state | No private contribution record or persistence was tested |
| Open “Manage work” | View displayed a sign-in-gated/empty state | Owner review and permission checks remain untested |
| Open “Goals & levels” | View displayed a sign-in-gated/empty state | Account-specific XP/level logic remains untested |
| Open “Leaderboard” | View displayed a sign-in-gated/empty state | Real ranking data and authorization remain untested |
| Open “Account & integrations” | View displayed a sign-in-gated/empty state | Authentication, GitHub connection, and integration controls remain untested |

The browser walk did not sign in or submit data, and it did not open individual bounty detail screens. The app repository's QA manifest still requires real browser scenarios with separate owner and contributor identities for contribution creation, review, revision, and exactly-once XP. Those core lifecycle scenarios remain **not verified**.

### Important findings for the campaign

1. **Do not treat the example offer cards as real marketplace traction or processed money.** They carry an “Example” label and a “Community showcase” byline, but their origin and commercial status were not independently verified. The application README explicitly says paid entries are listings; it has no escrow, payment processing, or guaranteed payout.
2. **Public board is not proof of a completed contribution lifecycle.** Landing page and navigation are public; account-specific workspace routes are gated without authentication. Do not narrate the review, revision, or XP path as a live demonstrated behavior until it has been exercised and recorded with the required roles.
3. **Current Open Graph metadata is not suitable as approved marketing copy.** At this inspection, the rendered page's Open Graph/Twitter description read: “Add a private Project 0 contribution ledger to ContribQuest for recording founder/operator contributions and linking them to GitHub or other work evidence. Only low-risk, non-sensitive work can receive self-verification XP, recorded idempotently and separately from community accepted-work gating. Keep the existing bounty, review, revision, GitHub integration and identity controls intact.” This reads as an implementation task, not a public product description. The checked-in `index.html` does not contain this Open Graph description; its actual source appears to be supplied by the deployed platform or deployment metadata and must be traced before editing.
4. **Do not conflate documented behavior with observed execution.** The canonical README and acceptance-protocol document describe criteria snapshots, per-criterion review, written rationale, accepted/rejected/changes-requested outcomes, revision history, and XP rules. This inspection did not test these authenticated backend transitions, data isolation, retry behavior, or exactly-once rewards.
5. **No full video-workbench run was reproduced in this environment.** A fresh Git clone attempt was blocked because the execution environment could not resolve `github.com`. Prior evidence recorded for the merged workbench includes CI run #76 passing 37 tests and HTTP smoke checks for real MP4 rendering, artifact downloads, versioning, claim persistence, ZIP export, checksum matching, and cross-origin mutation rejection. A new clean-start run is still desirable when a network-enabled runtime is available; this failure is an environment blocker, not evidence of a product defect.

### Required next evidence

- [ ] Owner-approved decision on audience, CTA, publish destination, and visual identity.
- [ ] Live authenticated scenarios with separate contributor and bounty-owner identities; attach pass/fail notes for each of the five QA manifest scenarios.
- [ ] Inspect one public bounty's actual details/criteria and verify the visible copy against the current source.
- [ ] Trace and replace the deployed Open Graph/Twitter description with owner-approved messaging; re-fetch it after deployment.
- [ ] Verify whether the displayed example offers are seeded examples and preserve an explicit example/demo label if so.
- [ ] Repeat a clean-start local workbench run and retain the exact project version, rendered MP4, sidecar, and same-version draft ZIP as acceptance evidence.
- [ ] Only then consider changing the draft brief to describe those authenticated flows as demonstrated.

## 8. Footage and asset plan

1. Run a live walkthrough using separate contributor and bounty-owner accounts where available. Record the actual build/version, account roles, scenario, observed output, and failures. Do not infer missing results.
2. Capture only screens needed to prove the claims: bounty criteria, contribution criteria snapshot, criterion-by-criterion review, and revision/review history.
3. Use synthetic records only in a safe test environment. Put a visible “DEMO DATA” label on any designed or synthetic example that could be mistaken for a live record.
4. If a scene cannot be captured live, replace it with a neutral text/diagram card and label it “workflow concept”; do not use generated UI to impersonate the real application.
5. Maintain a simple asset ledger for source URL, capture date, owner/permission, license, edit usage, and required attribution. Keep credentials and personal data out of captures.
6. Keep raw footage and the final export in an approved company-controlled location. Do not commit large media or private captures to this Git repository.

## 9. Review and acceptance checklist

Before the first cut:
- [ ] Product owner confirms audience, objective, terminology, pilot CTA, duration, and destination.
- [ ] Every factual line is mapped to the claims ledger and source.
- [ ] Current UI has been inspected for every screen-led claim.
- [ ] Any simulated or synthetic material is labeled; no fabricated metrics or outcomes appear.
- [ ] Logo, brand assets, fonts, music, voice, and screenshots have known usage rights.
- [ ] Captions, contrast, text legibility, and mobile-safe framing are checked.

Before approval for publication:
- [ ] Separate owner and contributor test scenarios are run where possible; report each pass/fail and any blocker.
- [ ] The final edit is checked against the real captured evidence, with every unsupported line removed or qualified.
- [ ] Prototype status, absence of in-app payout processing, and outstanding end-to-end verification remain clear.
- [ ] Product owner approves final copy, visual edit, CTA, link, destination, and permitted audience.
- [ ] Export settings and final artifact metadata are recorded. If generation or rendering fails, record the failure; do not present a placeholder as a finished video.

## 10. Proposed output package for Video Workbench

- This reviewed campaign brief and claims/evidence ledger.
- Approved script and timed storyboard.
- Caption and voiceover copy.
- Source/asset permission ledger.
- Review record with owner decisions and revisions.
- Final video **only after actual production and review**, or an explicit failure record identifying what prevented it.
- Export metadata: dimensions, aspect ratio, frame rate, duration, codec/container, audio/caption assets, source artifact versions, production path, tool/backend versions where available, and approval status.

## 11. Source references and unresolved questions

**Primary application source:** [Contribution-bounties-centre- README](https://github.com/Loofy147/Contribution-bounties-centre-/blob/main/README.md)  
**Strategic first-consumer charter:** [contribution-network/docs/10-first-consumer-project-charter.md](https://github.com/Loofy147/contribution-network/blob/main/docs/10-first-consumer-project-charter.md)  
**Current prototype URL (verify before publishing):** https://contribquest-lygj1x.v2.appdeploy.ai/  
**Video Workbench product brief:** [docs/PRODUCT_BRIEF.md](../PRODUCT_BRIEF.md)

Open decisions for the owner: public versus internal audience; final call to action; approved visual identity and assets; permitted publishing channels; exact timing and aspect ratio; whether live footage can demonstrate every documented behavior; and whether the video should remain an internal product explainer until those checks pass.
