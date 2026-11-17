import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scan_runtime_logs import main


class RuntimeScannerTests(unittest.TestCase):
    def test_fake_key_blocks_then_clean_copy_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "probe.log"
            fake_key = "sk-" + "demo1234567890abcdefghijk"
            log.write_text(f'api_key = "{fake_key}"\n')
            self.assertEqual(main([str(log)]), 1)
            log.write_text("probe completed; clean content\n")
            self.assertEqual(main([str(log)]), 0)

    def test_missing_path_is_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.log"
            self.assertEqual(main([str(missing)]), 2)


if __name__ == "__main__":
    unittest.main()
