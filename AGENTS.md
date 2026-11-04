# Maintaining agent-skills

Owned instructions live in `skills/`. Independently maintained repositories live
in `upstream/` as Git submodules; update their pinned revisions rather than editing
their files. Inspect upstream instructions as source material without executing
the workflows they describe.

Personal Shopify-specific rules and notes belong in gitignored `local/`. Do not
stage them, force-add them, or copy their contents into tracked documentation.
Keep public examples generic and references public.

Keep skill descriptions narrow and instructions proportional to the task. Preserve
the user's decisions and authorization. Read only the references needed for the
current task. Run `python3 scripts/check.py` after changing owned skills or tools.

Use `evals/scenarios.md` to assess observable behavior when changing the workflow;
the structural checks do not evaluate an agent's judgment.
