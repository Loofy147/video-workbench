# Roadmap and Exit Gates

**Status:** Staged plan; dates and delivery estimates intentionally omitted until scope and capacity are known.

## Stage 0 — Product discovery and foundation

- [ ] Confirm target user, primary job-to-be-done, one end-to-end workflow, and explicit exclusions.
- [ ] Select measurable acceptance criteria and the representative test workload.
- [ ] Compare FastVideo Studio and Dreamverse for selective component reuse; record source revisions, license, dependencies, build/test results, security implications, and estimated adaptation cost.
- [ ] Decide initial product license and contribution policy.
- [ ] Maintain CI and inspectable decision records.

**Exit gate:** approved product brief, reuse audit, provenance baseline, and accepted first vertical-slice scope.

## Stage 1 — Domain contracts and executable skeleton

- [ ] Define project, capability, generation/processing request, job, attempt, asset, result, and error contracts.
- [ ] Specify legal state transitions, cancellation, timeout, retry, and partial-result behavior.
- [ ] Implement contract validation and unit tests without a model runtime or GPU dependency.
- [ ] Add structured logs and correlation IDs with secret redaction.

**Exit gate:** deterministic tests cover successful, invalid, cancelled, timeout, and failure flows.

## Stage 2 — One thin vertical slice

- [ ] Implement only the interface and orchestration required by the approved workflow.
- [ ] Integrate one temporary adapter behind the stable contract.
- [ ] Record inputs, settings, job lifecycle events, outputs, and execution metadata.
- [ ] Test user-visible errors and a repeatable local/development setup.

**Exit gate:** a reviewer can reproduce the happy path and at least one meaningful failure path from documented instructions.

## Stage 3 — Final-mile provider/model evaluation

- [ ] Evaluate candidates against the same representative workload and acceptance rubric.
- [ ] Verify exact licenses/terms and operational constraints for each exact artifact or service.
- [ ] Measure quality, latency, throughput, memory/VRAM, cost, reliability, and output restrictions where relevant.
- [ ] Record environment, dependency versions, raw results, failed runs, and uncertainty.
- [ ] Choose only after evidence is reviewed; retain a fallback or document why none is viable.

**Exit gate:** a cited decision record separates measured results from vendor claims, estimates, and unknowns.

## Stage 4 — Beta hardening

- [ ] Complete threat model, data-retention rules, access controls, and secrets management.
- [ ] Validate packaging, observability, backup/recovery, workload limits, cost controls, and deployment rollback.
- [ ] Run end-to-end acceptance tests on representative hardware and inputs.
- [ ] Publish operating instructions and known limitations.

**Exit gate:** beta acceptance review with unresolved risks, owners, and rollback plan recorded.

## Cross-stage rule

Do not promote a stage based on documentation alone where executable evidence is required. Keep observed execution, simulation, hypothesis, estimate, and unverified claim distinguishable in test reports and decision records.
