# Agent skills

Engineering workflows maintained by Akin Shonibare: simple designs, efficient
systems, fast incremental delivery, and concise pull requests.

## Global engineering defaults

`global/engineering-defaults.md` applies simplicity, efficiency, speed, and concise
writing to every coding task. The skills add deeper workflows when relevant.
Install the defaults into Codex's global `AGENTS.md` with `--global` below.

The installer preserves existing global instructions and updates only its marked
engineering-defaults block. Re-run it after changing the versioned defaults.
It honors `CODEX_HOME`, or accepts `--codex-home /path/to/profile`.
Start a new Codex session to load changed global instructions.

## Owned skills

| Skill | When to use it |
| --- | --- |
| `principal-engineering-design` | Investigate a substantial engineering problem, compare approaches, recommend a design, and plan delivery. |
| `engineering-pr` | Prepare or revise a reviewable PR and its description, respecting the repository's template. |

Skills can activate when a task matches their descriptions, or be invoked explicitly
with `$principal-engineering-design` or `$engineering-pr` in Codex. Other agents
use their own invocation and discovery mechanisms.

## Local setup

```sh
git clone --recurse-submodules https://github.com/akinshonibare/agent-skills.git
cd agent-skills
python3 scripts/install.py --global --dry-run
python3 scripts/install.py --global
```

The installer links the two owned skills into `~/.agents/skills/`, Codex's supported
user-wide discovery location. It refuses to replace existing files or links to
other sources. Running it again preserves correct links. The skills become
available on the next turn; restart Codex if discovery does not refresh.

Use `--dest /path/to/another/agents/skill-directory` for another agent's documented
discovery location. This tool only installs files; it does not configure that agent.

## Independently maintained skills

`upstream/mattpocock-skills` is a Git submodule. Its source and license remain
upstream-owned, and the parent repository pins the exact revision. Fetching it
does not enable its skills or run its setup workflow.

```sh
git submodule update --init
python3 scripts/install.py --list
```

Install a selected upstream skill only when you want its workflow. For example:

```sh
python3 scripts/install.py --skill upstream/mattpocock-skills/skills/engineering/codebase-design
```

Read the skill and its dependencies first: some upstream skills call other skills,
update project documents or issue trackers, or prescribe their own PR format.
The installer does not resolve dependencies or adapt upstream instructions.
Avoid also installing the same collection through a plugin.

To review an upstream update before adopting it:

```sh
git -C upstream/mattpocock-skills fetch origin
git -C upstream/mattpocock-skills log --oneline HEAD..origin/main
git -C upstream/mattpocock-skills diff HEAD..origin/main -- skills
```

When ready, update the submodule checkout and commit its new pin:

```sh
git -C upstream/mattpocock-skills checkout --detach origin/main
git add upstream/mattpocock-skills
git commit -m "Update Matt Pocock skills"
```

Installed links follow that checkout, so an update also changes any selected
upstream skills. Add other collections with `git submodule add <url> upstream/<name>`
and install only the skill folders you select.

## Private local guidance

`local/` is gitignored. Keep Shopify-specific rules you author, private notes, and
private skills there; they stay on this machine and are excluded from publication.
For a private skill, create `local/skills/<name>/SKILL.md` and install it explicitly:

```sh
python3 scripts/install.py --skill local/skills/<name>
git check-ignore local/skills/<name>/SKILL.md
```

Private skills are not installed by default. Other checkouts need their own local
files. The general skills consult the target project's instructions and templates;
they do not embed internal company policies or replace project conventions.

## Checks

```sh
python3 scripts/check.py
```

This checks owned skill metadata, reference links, and installer behavior. Use
`evals/scenarios.md` for manual behavior evaluation. It does not claim that the
skills have been evaluated by running an agent.

## Design influences

These skills are original instructions shaped by personal preferences. Useful
public references include [Matt Pocock's skills](https://github.com/mattpocock/skills),
[lightweight RFC guidance](https://github.com/dil-landrasi/skills/tree/main/rfc),
Shopify's [PR discipline article](https://shopify.engineering/on-the-importance-of-pull-request-discipline)
and its historical [modular monolith account](https://shopify.engineering/deconstructing-monolith-designing-software-maximizes-developer-productivity).
These are context, not a substitute for current repository instructions.
