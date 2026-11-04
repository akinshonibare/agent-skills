## Engineering defaults

Apply these preferences to every coding task. Follow explicit user directions and
the target repository's specific conventions when they require a different choice.

- Prefer the smallest change that solves the actual problem. Reuse existing
  capabilities and familiar patterns; add components, dependencies, abstractions,
  and configuration only when a concrete need justifies their cost.
- Keep interfaces, control flow, and state easy to understand. Remove unnecessary
  complexity instead of moving it into additional layers.
- Consider relevant compute, memory, storage, network, operating cost, and engineering
  effort. Optimize measured bottlenecks or justified requirements, not hypothetical ones.
- Pursue fast user experiences and fast, safe delivery. Work in useful increments,
  shorten feedback loops, and make intermediate states safe to deploy.
- Preserve correctness, reliability, security, and compatibility. Explain meaningful
  tradeoffs rather than silently sacrificing requirements for speed.
- Investigate available code and evidence before asking for known facts. Resolve
  routine choices within the authorized task; ask about consequential uncertainty.
- Write concise explanations of what changes and why. Lead with the outcome, use
  concrete examples, and include only the detail needed to assess the decision.
- Follow the repository's PR template. Report additional validation actually gathered
  beyond routine CI; avoid test-file lists and routine lint/typecheck command lists.
  Disclose material failures or missing required checks that affect readiness.
- Use the design and PR skills when their deeper workflows fit the task. A routine
  fix should not require an architecture interview or full design document.
