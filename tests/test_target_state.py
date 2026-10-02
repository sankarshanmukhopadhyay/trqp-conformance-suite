import tempfile
import unittest
from pathlib import Path

from cts.run import target_state_from_file


class TargetStateTests(unittest.TestCase):
    def test_snapshot_digest_is_stable_and_content_bound(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "state.json"
            p.write_text('{"version":"a"}', encoding="utf-8")
            first = target_state_from_file(p)
            second = target_state_from_file(p)
            self.assertEqual(first["digest"], second["digest"])
            self.assertEqual(first["identity"], "sha256:" + first["digest"])
            p.write_text('{"version":"b"}', encoding="utf-8")
            changed = target_state_from_file(p)
            self.assertNotEqual(first["digest"], changed["digest"])

    def test_missing_snapshot_fails_closed(self):
        with self.assertRaises(SystemExit):
            target_state_from_file(Path("/definitely/not/present/state.json"))


if __name__ == "__main__":
    unittest.main()
