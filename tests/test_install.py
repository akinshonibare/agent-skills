import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from install import GLOBAL_START, apply_global_plan, global_installation_plan, install, install_global, main


class InstallerTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve() / "repo"
        self.destination = Path(self.temporary.name).resolve() / "installed"
        self.root.mkdir()

    def source(self, path, name):
        directory = self.root / path
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(f'---\nname: {name}\ndescription: "Example"\n---\n')
        return directory

    def run_install(self, sources, dry_run=False):
        with contextlib.redirect_stdout(io.StringIO()):
            install(self.root, sources, self.destination, dry_run)

    def test_repeat_install_preserves_correct_link(self):
        source = self.source("skills/design", "design")
        self.run_install(["skills/design"])
        target = self.destination / "design"
        inode = target.lstat().st_ino
        self.run_install(["skills/design"])
        self.assertEqual(source, target.resolve())
        self.assertEqual(inode, target.lstat().st_ino)

    def test_conflict_prevents_partial_installation(self):
        self.source("skills/first", "first")
        self.source("skills/second", "second")
        self.destination.mkdir()
        target = self.destination / "second"
        target.write_text("Managed elsewhere")
        with self.assertRaisesRegex(ValueError, "Refusing to replace"):
            self.run_install(["skills/first", "skills/second"])
        self.assertEqual("Managed elsewhere", target.read_text())
        self.assertFalse((self.destination / "first").exists())

    def test_preserves_link_to_another_source(self):
        self.source("skills/design", "design")
        self.destination.mkdir()
        target = self.destination / "design"
        elsewhere = Path(self.temporary.name) / "managed-elsewhere"
        target.symlink_to(elsewhere)
        with self.assertRaisesRegex(ValueError, "Refusing to replace"):
            self.run_install(["skills/design"])
        self.assertEqual(elsewhere, target.readlink())

    def test_dry_run_creates_nothing(self):
        self.source("skills/design", "design")
        self.run_install(["skills/design"], dry_run=True)
        self.assertFalse(self.destination.exists())

    def test_duplicate_names_are_rejected_before_writing(self):
        self.source("skills/design", "design")
        self.source("upstream/source/design", "design")
        with self.assertRaisesRegex(ValueError, "Duplicate skill name"):
            self.run_install(["skills/design", "upstream/source/design"])
        self.assertFalse(self.destination.exists())

    def test_rejects_sources_outside_repository(self):
        with self.assertRaisesRegex(ValueError, "inside this repository"):
            self.run_install(["../outside"])
        self.assertFalse(self.destination.exists())

    def test_supports_selected_local_and_upstream_skills(self):
        private = self.source("local/skills/private-context", "private-context")
        upstream = self.source("upstream/collection/skills/external", "external")
        self.run_install(["local/skills/private-context", "upstream/collection/skills/external"])
        self.assertEqual(private, (self.destination / "private-context").resolve())
        self.assertEqual(upstream, (self.destination / "external").resolve())

    def run_cli(self, arguments, environment=None):
        with patch("install.ROOT", self.root), patch("install.Path.home", return_value=self.destination), patch("sys.argv", ["install.py", *arguments]), patch.dict("os.environ", environment or {}), contextlib.redirect_stdout(io.StringIO()):
            main()

    def test_claude_cli_honors_config_directory_and_installs_only_owned_skills(self):
        owned = self.source("skills/design", "design")
        self.source("local/skills/private-context", "private-context")
        self.source("upstream/collection/skills/external", "external")
        profile = Path(self.temporary.name) / "claude-profile"
        self.run_cli(["--agent", "claude"], {"CLAUDE_CONFIG_DIR": str(profile)})
        self.assertEqual(owned, (profile / "skills" / "design").resolve())
        self.assertEqual(["design"], sorted(p.name for p in (profile / "skills").iterdir()))
        self.assertFalse(self.destination.exists())

    def test_both_agents_preflight_before_any_installation(self):
        self.source("skills/design", "design")
        claude_home = Path(self.temporary.name) / "claude"
        (claude_home / "skills").mkdir(parents=True)
        conflict = claude_home / "skills" / "design"
        conflict.write_text("Managed elsewhere")
        with self.assertRaisesRegex(ValueError, "Refusing to replace"):
            self.run_cli(["--agent", "both", "--claude-home", str(claude_home)])
        self.assertFalse(self.destination.exists())
        self.assertEqual("Managed elsewhere", conflict.read_text())

    def test_global_failure_prevents_skill_installation(self):
        self.source("skills/design", "design")
        (self.root / "global").mkdir()
        (self.root / "global" / "engineering-defaults.md").write_text("Prefer simplicity.\n")
        claude_home = Path(self.temporary.name) / "claude"
        claude_home.mkdir()
        (claude_home / "CLAUDE.md").write_text(GLOBAL_START + "\nUnfinished block")
        with self.assertRaisesRegex(ValueError, "Malformed"):
            self.run_cli(["--agent", "claude", "--global", "--claude-home", str(claude_home)])
        self.assertFalse((claude_home / "skills").exists())


class GlobalDefaultsTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        base = Path(self.temporary.name).resolve()
        self.root = base / "repo"
        self.home = base / "codex"
        (self.root / "global").mkdir(parents=True)
        self.source = self.root / "global" / "engineering-defaults.md"
        self.source.write_text("## Engineering defaults\n\nPrefer simple changes.\n")

    def run_install(self, dry_run=False):
        with contextlib.redirect_stdout(io.StringIO()):
            install_global(self.root, self.home, dry_run)

    def test_preserves_existing_instructions_and_updates_only_owned_block(self):
        self.home.mkdir()
        target = self.home / "AGENTS.md"
        original = "# Existing personal instructions\n\nKeep these intact.\n"
        target.write_text(original)
        self.run_install()
        first = target.read_text()
        self.run_install()
        self.assertEqual(first, target.read_text())
        target.write_text(first + "\nOther instructions after the owned block.\n")
        self.source.write_text("## Engineering defaults\n\nNew preference.\n")
        self.run_install()
        updated = target.read_text()
        self.assertTrue(updated.startswith(original))
        self.assertTrue(updated.endswith("\nOther instructions after the owned block.\n"))
        self.assertEqual(1, updated.count(GLOBAL_START))
        self.assertNotIn("Prefer simple changes.", updated)

    def test_dry_run_creates_nothing(self):
        self.run_install(dry_run=True)
        self.assertFalse(self.home.exists())

    def test_malformed_markers_leave_existing_file_intact(self):
        self.home.mkdir()
        target = self.home / "AGENTS.md"
        original = "Existing guidance\n" + GLOBAL_START + "\nIncomplete block\n"
        target.write_text(original)
        with self.assertRaisesRegex(ValueError, "Malformed"):
            self.run_install()
        self.assertEqual(original, target.read_text())

    def test_active_override_is_not_modified_or_ignored(self):
        self.home.mkdir()
        override = self.home / "AGENTS.override.md"
        override.write_text("Existing override\n")
        with self.assertRaisesRegex(ValueError, "shadow"):
            self.run_install()
        self.assertEqual("Existing override\n", override.read_text())
        self.assertFalse((self.home / "AGENTS.md").exists())

    def test_claude_import_preserves_existing_instructions_and_tracks_source(self):
        self.home.mkdir()
        target = self.home / "CLAUDE.md"
        original = "# Existing Claude guidance\n\nKeep this intact.\n"
        target.write_text(original)
        with contextlib.redirect_stdout(io.StringIO()):
            apply_global_plan(global_installation_plan(self.root, self.home, "claude"))
        first = target.read_text()
        self.assertTrue(first.startswith(original))
        self.assertIn("@" + str(self.source), first)
        self.assertNotIn("Prefer simple changes.", first)
        target.write_text(first + "\nGuidance after the block.\n")
        self.source.write_text("A changed preference.\n")
        with contextlib.redirect_stdout(io.StringIO()):
            apply_global_plan(global_installation_plan(self.root, self.home, "claude"))
        self.assertEqual(first + "\nGuidance after the block.\n", target.read_text())
        self.assertEqual(1, target.read_text().count(GLOBAL_START))

    def test_claude_dry_run_creates_nothing(self):
        with contextlib.redirect_stdout(io.StringIO()):
            apply_global_plan(global_installation_plan(self.root, self.home, "claude"), dry_run=True)
        self.assertFalse(self.home.exists())

    def test_claude_import_escapes_spaces(self):
        spaced_root = self.root.parent / "repo with spaces"
        (spaced_root / "global").mkdir(parents=True)
        source = spaced_root / "global" / "engineering-defaults.md"
        source.write_text("Prefer simplicity.\n")
        _, _, updated = global_installation_plan(spaced_root, self.home, "claude")
        self.assertIn("@" + str(source).replace(" ", "\\ "), updated)

    def test_symlinked_instruction_files_are_preserved_for_both_agents(self):
        self.home.mkdir()
        external = self.root.parent / "managed-guidance.md"
        external.write_text("Managed elsewhere\n")
        for agent, filename in (("codex", "AGENTS.md"), ("claude", "CLAUDE.md")):
            with self.subTest(agent=agent):
                target = self.home / filename
                target.symlink_to(external)
                with self.assertRaisesRegex(ValueError, "symlinked"):
                    global_installation_plan(self.root, self.home, agent)
                self.assertEqual(external, target.readlink())
                self.assertEqual("Managed elsewhere\n", external.read_text())


if __name__ == "__main__":
    unittest.main()
