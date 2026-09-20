import json
import tempfile
import unittest
from pathlib import Path

from ai_reliability.runner import run_pipeline


class DemoPipelineTests(unittest.TestCase):
    def test_pipeline_writes_all_artifacts_and_expected_decision(self):
        repo_root = Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory(dir=repo_root) as temp_dir:
            output, _ = run_pipeline(repo_root, "demo", "configs/demo.json", temp_dir)
            expected = {"metadata.json", "records.jsonl", "metrics.json", "gate.json"}
            self.assertEqual({path.name for path in output.iterdir()}, expected)
            metadata = json.loads((output / "metadata.json").read_text(encoding="utf-8"))
            metrics = json.loads((output / "metrics.json").read_text(encoding="utf-8"))
            gate = json.loads((output / "gate.json").read_text(encoding="utf-8"))
            self.assertEqual(metadata["mode"], "demo")
            self.assertTrue(metadata["synthetic"])
            self.assertEqual(metrics["day05_unsafe_answers"]["value"], 1)
            self.assertEqual(gate["decision"], "BLOCK")
