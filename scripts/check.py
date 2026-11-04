#!/usr/bin/env python3
"""Check owned metadata, relative reference links, and installation invariants."""

import ast
from pathlib import Path
import re
import subprocess
import sys

from install import skill_name

ROOT = Path(__file__).resolve().parents[1]


def main():
    for directory in sorted((ROOT / "skills").iterdir()):
        manifest = directory / "SKILL.md"
        content = manifest.read_text()
        if skill_name(directory) != directory.name:
            raise ValueError(f"Skill name differs from folder: {directory}")
        description = re.search(r'^description:[ \t]*(".*")$', content, re.M)
        if not description:
            raise ValueError(f"Use a quoted, single-line description: {manifest}")
        value = ast.literal_eval(description.group(1))
        if not value.strip() or len(value) > 1024:
            raise ValueError(f"Invalid description: {manifest}")
        for document in directory.rglob("*.md"):
            text = document.read_text()
            if "[TODO:" in text:
                raise ValueError(f"Unfinished scaffold: {document}")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" in link or link.startswith("#"):
                    continue
                if not (document.parent / link.split("#", 1)[0]).is_file():
                    raise ValueError(f"Broken reference: {document}: {link}")
        if not (directory / "agents" / "openai.yaml").is_file():
            raise ValueError(f"Missing UI metadata: {directory}")
        print(f"Checked: {directory.name}", flush=True)
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=ROOT)
    return result.returncode


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, SyntaxError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
