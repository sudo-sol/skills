"""Run against temporary copies; never modify the checkout or real agent installs."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.repo = self.base / 'repo'
        shutil.copytree(SOURCE, self.repo, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__'))
        self.skill = self.repo / 'skills/productivity/memory-bank/SKILL.md'
        self.yaml = self.skill.parent / 'agents/openai.yaml'

    def check(self, expected=0):
        result = subprocess.run(['bash', 'scripts/check-skills.sh'], cwd=self.repo, text=True, capture_output=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout

    def test_valid_package(self):
        self.check()

    def test_missing_closing_delimiter(self):
        self.skill.write_text(self.skill.read_text().replace('\n---\n', '\n', 1))
        self.assertIn('closing front-matter delimiter', self.check(1))

    def test_invalid_yaml(self):
        self.skill.write_text(self.skill.read_text().replace('license: MIT', 'license: [MIT'))
        self.check(1)

    def test_duplicate_key(self):
        self.skill.write_text(self.skill.read_text().replace('license: MIT', 'license: MIT\nlicense: MIT'))
        self.assertIn('duplicate YAML key', self.check(1))

    def test_quoted_boolean_rejected(self):
        self.yaml.write_text(self.yaml.read_text() + 'policy:\n  allow_implicit_invocation: "false"\n')
        self.assertIn('must be a boolean', self.check(1))

    def test_wrong_invocation_rejected(self):
        self.yaml.write_text(self.yaml.read_text() + 'policy:\n  allow_implicit_invocation: false\n')
        self.assertIn('out of sync', self.check(1))

    def test_missing_root_notices(self):
        for filename in ('LICENSE', 'THIRD_PARTY_NOTICES.md'):
            with self.subTest(filename=filename):
                notice = self.repo / filename
                content = notice.read_bytes()
                notice.unlink()
                self.assertIn(f'missing or empty root notice: {filename}', self.check(1))
                notice.write_bytes(content)

    def test_unregistered_skill(self):
        folder = self.skill.parent.parent / 'extra'
        shutil.copytree(self.skill.parent, folder)
        p = folder / 'SKILL.md'
        p.write_text(p.read_text().replace('name: memory-bank', 'name: extra'))
        self.assertIn('registrations differ', self.check(1))

    def test_optimized_python_still_validates(self):
        self.skill.write_text(self.skill.read_text().replace('\n---\n', '\n', 1))
        result = subprocess.run(['python3', '-O', 'scripts/check_skills.py'], cwd=self.repo, capture_output=True)
        self.assertEqual(result.returncode, 1)

    def test_linker_preserves_existing_installs_and_spaces(self):
        dest = self.base / 'agent skills'
        dest.mkdir()
        previous = dest / 'memory-bank'
        previous.symlink_to(self.base / 'missing-old-install')
        existing = dest / 'daily-check-in'
        existing.mkdir()
        (existing / 'keep').write_text('user content')
        for _ in range(2):
            subprocess.run(['bash', 'scripts/link-skills.sh', str(dest)], cwd=self.repo, capture_output=True, check=True)
        self.assertEqual(os.readlink(previous), str(self.base / 'missing-old-install'))
        self.assertEqual((existing / 'keep').read_text(), 'user content')
        self.assertEqual((dest / 'jira-ops').resolve(), self.repo / 'skills/work-tracking/jira-ops')
        self.assertEqual(len(list(dest.iterdir())), 11)

    def test_linker_rejects_internal_destination(self):
        result = subprocess.run(['bash', 'scripts/link-skills.sh', str(self.repo / 'new-folder')], cwd=self.repo, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.repo / 'new-folder').exists())


if __name__ == '__main__':
    unittest.main()
