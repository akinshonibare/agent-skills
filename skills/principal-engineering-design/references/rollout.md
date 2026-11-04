# Operational delivery and migrations

Make every transition intelligible, including partial completion and retries.
Use expand, migrate, and contract when old and new forms must coexist. Follow the
project's requirements for separate schema and consuming-code PRs.

For each consequential phase, specify:

- Entry conditions, dependencies, owner, and intended effect.
- How to observe correctness and the intended benefit, with a representative
  workload or cohort where applicable.
- What triggers an abort, who acts, and what state remains after aborting.
- Whether rollback restores behavior, data, both, or neither. A feature flag does
  not reverse writes, deleted data, or external side effects.
- How retries detect already-applied effects after a crash or partial failure.
- When temporary flags, compatibility paths, dual writes, and superseded resources
  can be removed, and who owns that removal.

Distinguish proposed verification from observations already collected. Include
benchmarks, live checks, or simulations in a PR only after performing them; never
turn a rollout plan into a claim of successful validation.

Avoid universal rollout percentages, thresholds, or fixed durations. Derive them
from the operating envelope and risk. Keep the plan proportional to the change.
