# Design record

Use the project's existing format. Otherwise include only the sections that help
a reader assess the decision:

- **Problem and outcome:** who is affected, why now, scope, and observable success.
- **Evidence and constraints:** current behavior, measured needs, facts, estimates,
  and assumptions. Link sources rather than duplicating background material.
- **Options:** current approach and credible alternatives, compared against the
  same decision criteria. Include real strengths and consequential weaknesses.
- **Recommendation:** boundaries, contracts, data or state flow, invariants, and
  relevant failure handling. Explain why the added complexity earns its place.
- **Tradeoffs and uncertainty:** strongest objection, accepted costs, experiments,
  and conditions that would change the decision.
- **Delivery:** milestones, prerequisite PRs, compatibility, operational transition,
  ownership, and cleanup.
- **Decisions still needed:** name the question and its decision owner if known.
  Distinguish recommendations from decisions actually agreed.

A short decision note may fit in a few paragraphs. Use a full RFC when uncertainty
or coordination warrants it. Do not fill sections to make the document appear
complete. Do not invent availability or performance numbers to satisfy a template.

Record lasting rationale where a future maintainer would otherwise be surprised,
especially when reversing the decision is costly. Use existing intent documents
or decision records; do not create a parallel documentation system by default.
