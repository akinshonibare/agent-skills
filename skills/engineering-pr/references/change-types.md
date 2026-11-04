# PR emphasis by change type

Adapt the repository template rather than replacing it with a separate template
for every change type.

| Change | Reviewer needs |
| --- | --- |
| Bug fix | Trigger, incorrect behavior, corrected behavior; additional observed evidence if collected. |
| Feature | User need, resulting behavior, scope, and consequential design choice. |
| Refactor | Existing maintenance cost, structural change, and any behavior change that means it is more than a refactor. |
| Performance | Bottleneck, change, representative workload, before/after measurements if collected, and tradeoffs. |
| Migration or operational change | Compatibility, sequencing, impact, rollout checks, rollback limits, and cleanup; link the detailed plan. |
| Documentation or small maintenance | The concrete correction and why it matters, often in one or two sentences. |

No-template default:

```markdown
## Why
Concrete problem and its impact.

## What
Resulting behavior and any consequential implementation choice.
```

Add `Validation` only after collecting evidence beyond routine CI, for example:

> On staging, retried the same request three times and observed one notification.

> Against a representative snapshot, median query time fell from 420 ms to 65 ms
> over 100 runs; cache state was held constant.

These are illustrative wording, not observations to reuse. Include actual evidence
and its relevant limits. Add rollout or risk sections when the change warrants
them or the repository requires them.
