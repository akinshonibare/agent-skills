---
name: engineering-pr
description: "Prepare or revise pull requests: coherent scope, logical sequencing, concise descriptions of what changed and why, and meaningful evidence beyond routine CI. Use when drafting a PR, updating its description, splitting work into PRs, or assessing PR readiness. Follow the repository's existing template."
---

# Engineering PR

Make the change easy to assess for a reviewer who has not read the conversation.

## Discover the format and final change

Read applicable repository instructions and contribution guidance. Find the Git
root and inspect templates there as well as in the working directory: `.github/`,
`docs/`, root templates, and `PULL_REQUEST_TEMPLATE/` variants. Follow any explicitly
selected template and its required headings, ordering, and checkboxes. Do not infer
that a nested application has no template because none is present in its directory.

Read the actual diff against the appropriate base and relevant history. Distinguish
branch work from unrelated local changes. Describe the final implementation; do
not carry abandoned approaches or obsolete scope into the title and description.

## Structure the change

Keep one coherent, reviewable purpose per PR. Split separable prerequisites and
unrelated cleanup when useful or required by the repository. Explain dependencies
and keep intermediate states safe to deploy. Product increments can span multiple
PRs, especially schema changes and migrations.

Use logically ordered commits when they help review. Separate mechanical refactoring
from behavior changes where practical. Follow the repository's history convention;
do not require every PR to have one commit or use a particular stacking tool.
Recommend a sequence without rewriting history or pushing unless authorized.

## Write for the reviewer

Lead with the concrete problem and resulting behavior. Explain **why** the change
is needed and **what** changes. Add consequential implementation decisions and
accepted tradeoffs only when they help assess the diff. A concrete trigger and
before/after example can replace several paragraphs of abstract rationale.

Use a precise title and short connected prose. Small changes often need one or two
sentences. Link detailed design rationale instead of retelling the investigation.
Use diagrams, tables, screenshots, or snippets when they explain something prose
cannot explain as clearly, rather than making a visual mandatory for every PR.

With no repository template, default to `Why` and `What`. Add other sections only
when they contain relevant information. Read
[change-types.md](references/change-types.md) for change-specific emphasis.

## Evidence beyond CI

Routine test-file lists, lint commands, and typecheck commands do not earn a
Validation section. Run checks required by the task and repository, but avoid
repeating ordinary CI work in the description.

Include validation only for additional evidence actually gathered: manual UI
testing, live environment observations, representative benchmarks, targeted
experiments, simulations, or other verification beyond routine CI. State the
environment, scenario, and observed result; include limitations relevant to the
claim. Distinguish measured improvements from expected ones.

Preserve required repository sections such as Tophat. If no additional verification
was performed and the template requires an entry, say so briefly rather than
inventing evidence or padding it with a CI command list. Never mark an unperformed
check complete. Disclose material failures or missing required checks that affect
readiness; this reporting preference does not hide them.

For transitions or hard-to-reverse effects, describe the concrete impact, blast
radius, mitigation, and rollback limits when relevant or required by the template.
Do not add a generic danger checklist to a routine change.

Before handoff, ensure the title, description, links, required fields, and actual
diff agree. Preparing a PR does not authorize merging or deploying it. External
publication and Git operations follow the user's task and existing authorization.
