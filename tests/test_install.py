import contextlib
import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from install import GLOBAL_START, install, install_global


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


if __name__ == "__main__":
    unittest.main()
