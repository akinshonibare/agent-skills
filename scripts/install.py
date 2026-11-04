#!/usr/bin/env python3
"""Link selected skill sources without replacing existing installations."""

import argparse
import ast
import os
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
GLOBAL_START = "<!-- agent-skills:engineering-defaults:start -->"
GLOBAL_END = "<!-- agent-skills:engineering-defaults:end -->"


def skill_name(source):
    content = (source / "SKILL.md").read_text()
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", content, re.S)
    if not frontmatter:
        raise ValueError(f"Missing skill frontmatter: {source}")
    names = re.findall(r"^name:[ \t]*(.+)$", frontmatter.group(1), re.M)
    if len(names) != 1:
        raise ValueError(f"Expected one skill name: {source}")
    name = names[0].strip()
    if name.startswith(("'", '"')):
        name = ast.literal_eval(name)
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError(f"Invalid skill name in {source}")
    return name


def installation_plan(root, sources, destination):
    root = root.resolve()
    names = set()
    plan = []
    for requested in sources:
        source = (root / requested).resolve()
        try:
            source.relative_to(root)
        except ValueError:
            raise ValueError(f"Skill source must be inside this repository: {requested}")
        name = skill_name(source)
        if name in names:
            raise ValueError(f"Duplicate skill name selected: {name}")
        names.add(name)
        target = destination / name
        correct = target.is_symlink() and target.resolve() == source
        if (target.exists() or target.is_symlink()) and not correct:
            raise ValueError(f"Refusing to replace existing installation: {target}")
        plan.append((source, target, correct))
    return plan


def install(root, sources, destination, dry_run=False):
    plan = installation_plan(root, sources, destination)
    if not dry_run and any(not correct for _, _, correct in plan):
        destination.mkdir(parents=True, exist_ok=True)
    for source, target, correct in plan:
        if correct:
            print(f"Already linked: {target}")
        elif dry_run:
            print(f"Would link: {target} -> {source}")
        else:
            target.symlink_to(source, target_is_directory=True)
            print(f"Linked: {target} -> {source}")


def install_global(root, codex_home, dry_run=False):
    source = root / "global" / "engineering-defaults.md"
    defaults = source.read_text().strip()
    if not defaults:
        raise ValueError(f"Empty engineering defaults: {source}")
    override = codex_home / "AGENTS.override.md"
    if override.is_file() and override.read_text().strip():
        raise ValueError(f"Global override would shadow AGENTS.md: {override}")
    target = codex_home / "AGENTS.md"
    if target.is_symlink():
        raise ValueError(f"Refusing to modify a symlinked instruction file: {target}")
    original = target.read_text() if target.exists() else ""
    block = f"{GLOBAL_START}\n{defaults}\n{GLOBAL_END}"
    if GLOBAL_START in original or GLOBAL_END in original:
        if original.count(GLOBAL_START) != 1 or original.count(GLOBAL_END) != 1:
            raise ValueError(f"Malformed engineering-defaults block: {target}")
        start = original.index(GLOBAL_START)
        end = original.index(GLOBAL_END)
        if end < start:
            raise ValueError(f"Malformed engineering-defaults block: {target}")
        updated = original[:start] + block + original[end + len(GLOBAL_END):]
    else:
        separator = "" if not original or original.endswith("\n\n") else "\n" if original.endswith("\n") else "\n\n"
        updated = original + separator + block + "\n"
    if updated == original:
        print(f"Global defaults already installed: {target}")
    elif dry_run:
        print(f"Would update owned engineering-defaults block: {target}")
    else:
        codex_home.mkdir(parents=True, exist_ok=True)
        target.write_text(updated)
        print(f"Installed global defaults: {target}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=Path.home() / ".agents" / "skills")
    parser.add_argument("--skill", action="append", help="Selected skill folder, relative to this repository")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--list", action="store_true", help="List owned, local, and fetched upstream skills")
    parser.add_argument("--global", dest="global_defaults", action="store_true", help="Install engineering defaults into a marked block in Codex's global AGENTS.md")
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))))
    args = parser.parse_args()
    if args.list:
        for group in ("skills", "local/skills", "upstream"):
            for manifest in sorted((ROOT / group).rglob("SKILL.md")):
                print(f"{skill_name(manifest.parent)}\t{manifest.parent.relative_to(ROOT)}")
        return
    sources = args.skill or [p.relative_to(ROOT) for p in sorted((ROOT / "skills").iterdir()) if (p / "SKILL.md").is_file()]
    install(ROOT, sources, args.dest.expanduser().absolute(), args.dry_run)
    if args.global_defaults:
        install_global(ROOT, args.codex_home.expanduser().absolute(), args.dry_run)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, SyntaxError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
