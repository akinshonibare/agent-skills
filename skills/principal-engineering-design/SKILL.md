---
name: principal-engineering-design
description: "Investigate engineering problems, compare architecture options, recommend a design, and plan incremental delivery. Use for system design, technical RFCs, architecture decisions, substantial migrations, and critiques of existing designs. Skip the full workflow for routine fixes."
---

# Principal engineering design

Produce a decision someone can defend and a delivery plan someone can execute.
Scale the depth to the uncertainty, impact, and cost of reversing the decision.
A contained change may need a short note; a substantial migration may need a
design record and rollout plan. Do not manufacture a full RFC for every task.

## Establish context

Read applicable repository instructions, contribution guidance, existing intent
or design documents, relevant code, and history before asking for known facts.
Follow the project's documentation locations and vocabulary. Read supplemental
private guidance only when it applies to this project; never copy it into a public
artifact. Distinguish current implementation from historical design intent.

Establish the problem, affected users, desired outcome, scope, and constraints.
Use measured workload, latency, data size, growth, cost, and durability needs where
available. Label estimates and assumptions; do not invent targets or agreement.
Define what observation would demonstrate success.

Investigate facts independently. Ask about consequential decisions that remain
unresolved, with concrete alternatives and a recommendation. Carry accepted
decisions forward; do not reopen them without new evidence. Resolve routine
implementation choices within the authorized scope without extra approval gates.

## Compare designs

Include the current approach, the smallest plausible improvement, and meaningful
alternatives. Consider whether configuration, deletion, a narrower requirement,
or an existing capability solves the problem without a new system. Represent
alternatives fairly rather than making the preferred option win by construction.

Use the criteria that can change the decision:

- **Simplicity:** how much callers and maintainers must understand; moving parts,
  coupling, states, deployment units, and operating burden. Prefer familiar project
  patterns. A new abstraction should remove repeated complexity or support a real
  variation, rather than add indirection for hypothetical flexibility.
- **Efficiency:** relevant compute, memory, storage, network, money, and engineering
  effort. Optimize measured bottlenecks or justified requirements.
- **Speed:** user-visible performance, feedback time, and time to deliver safely.
  Prefer an early useful increment over a large speculative redesign.
- **Quality:** correctness, reliability, security, compatibility, and operability
  where they affect the outcome. Do not trade away a hard requirement silently.

Make tradeoffs explicit. Ask whether removing a component eliminates complexity
or pushes it back onto callers. Favor clear contracts that contain complexity,
without requiring every small model method to become a new layer.

For consequential unknowns, propose the smallest experiment that could change the
decision. State its question, success observation, limits, and disposal plan.
Continue discovery while its result could change the recommendation; otherwise
state the remaining assumptions and move forward.

## Recommend and challenge

Describe the preferred approach through boundaries, interfaces, state transitions,
and invariants. Discuss retries, idempotency, concurrency, partial failures, resource
limits, and recovery where relevant. Use mechanisms instead of promises such as
"ensure reliability." Include a diagram only when it makes a relationship clearer.

State why the choice fits, its strongest counterargument, accepted tradeoffs, and
the evidence that would justify changing direction. Identify cross-team effects,
dependencies, decision owners, and unresolved decisions without inventing approvals
or contacting stakeholders unless authorized.

For a written proposal or design critique, use
[design-record.md](references/design-record.md). Preserve an existing template
instead of forcing that structure. In a critique, distinguish defects, tradeoffs,
and unanswered questions; propose a simpler defensible target.

## Plan delivery

Plan coherent, reviewable PRs and their dependencies during design. Each intermediate
state must respect compatibility and deployment constraints. A demonstrable product
increment may require several prerequisite PRs; follow the repository's migration
rules rather than insisting every PR span every layer.

For operational transitions, read [rollout.md](references/rollout.md). Define
milestones, ownership, observations, abort conditions, rollback limits, and removal
conditions for temporary mechanisms. Include ongoing cost and maintenance ownership.

Before preparing a PR, compare the implemented result with the recommendation.
Explain consequential deviations and update applicable documentation. Describe
the chosen change and review-relevant tradeoffs rather than repeating the entire
alternatives discussion. If PR preparation is requested and `engineering-pr` is
available, use it; it is not required to finish a design request.

Perform implementation, experiments, deployments, or publication only within the
user's authorized task. A design request alone does not authorize those actions.
