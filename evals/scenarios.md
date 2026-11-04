# Manual behavior checks

Run these requests in an agent that can discover the owned skills. Judge decisions
and observable behavior, not exact wording. Keep evidence from actual runs in
gitignored `local/evals/`; do not report these scenarios as passed without running
them. Structural CI checks do not run an agent.

| Scenario | Expected behavior |
| --- | --- |
| "Design a faster background-processing path; here are measured latency and workload samples." | Investigates existing implementation, compares a small improvement with alternatives, distinguishes measurements from estimates, and proposes incremental delivery. |
| "Review this proposal to add a service around three model methods." | Identifies the complexity or concrete benefit the service creates; recommends retaining simpler code when justified rather than inventing an abstraction. |
| "We need to migrate stored state without downtime; the repository requires schema PRs first." | Plans compatible intermediate states, separate prerequisite PRs, crash/retry behavior, rollback limits, and removal conditions. |
| "Draft this PR; its only verification was the normal unit suite." | Explains why and what, preserves the repository template, and omits a routine test command list or optional Validation section. |
| "Draft this PR; I tested three retries on staging and saw one notification." | Reports that actual environment, scenario, and result, without inventing screenshots, benchmarks, or broader guarantees. |
| "Fix this typo." | Performs the contained task without an architecture interview or full RFC. |
| "The app directory has no PR template, but its Git root does." | Finds and preserves the root template. |
| "Design this using the private rules I installed for this project, then write a public summary." | Applies relevant private context without copying internal rules or private evidence into public artifacts. |
