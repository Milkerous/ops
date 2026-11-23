import hashlib
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from handoff_a_to_b import make_handoff
from scan_runtime_logs import main as scan_main


def artifact(path, root, job_id):
    data = path.read_bytes()
    return {
        "uri": f"artifact://{job_id}/{path.relative_to(root).as_posix()}",
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
    }


class E13ExtraTests(unittest.TestCase):
    def test_scanner_masks_hit_and_never_prints_full_value(self):
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "probe.log"
            key = "sk-" + "demo1234567890abcdefghijk"
            log.write_text(f'api_key = "{key}"\n')
            output = io.StringIO()
            with redirect_stdout(output):
                code = scan_main([str(log)])
            self.assertEqual(code, 1)
            printed = output.getvalue()
            self.assertNotIn(key, printed)
            self.assertIn("sk-d***", printed)

    def _run(self, root, job="job-x", trace="trace-x", status="SUCCEEDED", stage_job=None):
        inner = root / "incremental-report.json"
        inner.write_text('{"findings": []}\n')
        stage = {
            "schema_version": "e11e12-1",
            "kind": "incremental-check",
            "status": "SUCCEEDED",
            "commit": "a" * 40,
            "job_id": stage_job or job,
            "trace_id": trace,
            "data": {"commit": "a" * 40, "findings": []},
            "artifacts": [artifact(inner, root, job)],
        }
        stage_path = root / "incremental-check.json"
        stage_path.write_text(json.dumps(stage) + "\n")
        result = {
            "schema_version": "e11e12-1",
            "status": status,
            "target_commit": "a" * 40,
            "job_id": job,
            "trace_id": trace,
            "stages": [
                {"name": "incremental-check", "artifact": artifact(stage_path, root, job)}
            ],
        }
        result_path = root / "result.json"
        result_path.write_text(json.dumps(result) + "\n")
        return result_path

    def test_handoff_rejects_failed_a_task(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self._run(root, status="FAILED")
            with self.assertRaisesRegex(ValueError, "did not succeed"):
                make_handoff(result, "a" * 40)

    def test_handoff_rejects_stage_job_mismatch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self._run(root, stage_job="job-other")
            with self.assertRaisesRegex(ValueError, "identity or target mismatch"):
                make_handoff(result, "a" * 40)


if __name__ == "__main__":
    unittest.main()
