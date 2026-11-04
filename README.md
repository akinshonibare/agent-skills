# Agent skills

Engineering workflows maintained by Akin Shonibare: simple designs, efficient
systems, fast incremental delivery, and concise pull requests.

## Global engineering defaults

`global/engineering-defaults.md` applies simplicity, efficiency, speed, and concise
writing to every coding task. The skills add deeper workflows when relevant.
Install the defaults for Codex, Claude Code, or both with `--global` below.

The installer preserves existing global instructions and updates only its marked
engineering-defaults block. Codex receives a copy in its global `AGENTS.md`;
re-run the installer after changing the versioned defaults. Claude Code receives
an import in its global `CLAUDE.md`, so future sessions read the maintained source
directly. Keep this checkout at its installed path, or re-run the installer after
moving it.

The installer honors `CODEX_HOME` and `CLAUDE_CONFIG_DIR`, or accepts
`--codex-home /path/to/profile` and `--claude-home /path/to/profile`.
Start a new session to load changed global instructions.

## Owned skills

| Skill | When to use it |
| --- | --- |
| `principal-engineering-design` | Investigate a substantial engineering problem, compare approaches, recommend a design, and plan delivery. |
| `engineering-pr` | Prepare or revise a reviewable PR and its description, respecting the repository's template. |

Skills can activate when a task matches their descriptions, or be invoked explicitly
with `$principal-engineering-design` or `$engineering-pr` in Codex, and
`/principal-engineering-design` or `/engineering-pr` in Claude Code.

## Local setup

```sh
git clone --recurse-submodules https://github.com/akinshonibare/agent-skills.git
cd agent-skills
python3 scripts/install.py --global --dry-run
python3 scripts/install.py --global
```

These commands default to Codex. To install for Claude Code, use:

```sh
python3 scripts/install.py --agent claude --global --dry-run
python3 scripts/install.py --agent claude --global
```

Use `--agent both --global` to configure both agents together. Owned skills are
linked into `~/.agents/skills/` for Codex and `~/.claude/skills/` for Claude Code
(or the configured Claude profile). Both read the same skill source directories.
The installer refuses to replace existing files or links to other sources, checks
all selected destinations before writing, and preserves correct links on repeat
runs. Skills are available on the next turn; restart the agent if discovery does
not refresh.

With the devx launchers, start a fresh session using `devx claude` or `devx codex`.
The installer configures each agent's instruction and skill files; it does not
modify devx or its managed configuration.

In Claude Code, use `/skills` to check discovery and `/context all` to confirm the
global `CLAUDE.md` loaded. These local links configure Claude Code on this machine;
they do not upload skills to claude.ai, Cowork, or cloud sessions. See the official
[skill loading documentation](https://code.claude.com/docs/en/skills) and
[instruction imports](https://code.claude.com/docs/en/memory).

Use `--dest /path/to/another/agents/skill-directory` for another agent's documented
discovery location. Without `--global`, this tool only links skills. `--global`
configures the selected agent's instruction file, regardless of `--dest`.

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
files. Add `--agent claude` when explicitly installing a selected private or upstream
skill for Claude Code. The general skills consult the target project's instructions
and templates; they do not embed internal company policies or replace project conventions.

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
