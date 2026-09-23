"""Regression checks for the semantic experiment, not a Hegelese interpreter."""

import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "process_reference", ROOT / "docs" / "process-reflection-reference.py"
)
reference = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = reference
spec.loader.exec_module(reference)


class ReferenceContract(unittest.TestCase):
    def test_recorded_evidence_matches_execution(self):
        actual = json.loads(json.dumps(reference.experiment()))
        recorded = json.loads((ROOT / "docs" / "process-reflection-results.json").read_text())
        self.assertEqual(actual, recorded)

    def test_observation_change_invalidates_abstraction(self):
        source = reference.Process("FourPhase", (0, 1, 2, 3), 0,
                                   (1, 2, 3, 0), (0, 1, 0, 1))
        altered = reference.Process("ChangedObservation", (0, 1), 0,
                                    (1, 0), (0, 0))
        evidence = reference.check_abstraction(source, altered, (0, 1, 0, 1))
        self.assertEqual(evidence["status"], "Refuted")
        self.assertEqual([c["state"] for c in evidence["counterexamples"]], [1, 3])
        self.assertTrue(all(c["law"] == "observation" for c in evidence["counterexamples"]))


if __name__ == "__main__":
    unittest.main()
