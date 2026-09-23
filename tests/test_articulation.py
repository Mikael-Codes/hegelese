"""Behavioral acceptance cases for the finite articulated-change checker."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import hegelese as h

ROOT = Path(__file__).resolve().parents[1]


class ArticulationChecks(unittest.TestCase):
    def setUp(self):
        self.request = json.loads((ROOT / "request-four.json").read_text())
        self.proposal = json.loads((ROOT / "proposal-four.json").read_text())

    def check(self, budget=100000):
        return h.check(self.request, self.proposal, budget)

    def rebind(self):
        self.proposal["request_sha256"] = h.digest(self.request)

    def test_valid_lossy_abstraction(self):
        result = self.check()
        self.assertTrue(result["accepted"])
        self.assertEqual(result["evidence"]["checks_completed"], 9)
        self.assertEqual(result["evidence"]["observations"], ["parity"])
        self.assertEqual(result["articulation"]["dispositions"]["observation:exactPhase"]["action"], "withdraw")

    def test_counterexample_despite_complete_articulation(self):
        request = json.loads((ROOT / "request-three.json").read_text())
        proposal = json.loads((ROOT / "proposal-three.json").read_text())
        result = h.check(request, proposal)
        self.assertEqual(result["articulation"]["status"], "Complete")
        self.assertEqual(result["status"], "Refuted")
        self.assertEqual(result["evidence"]["counterexamples"], [
            {"law": "step", "state": "2", "input": "tick", "left": "0", "right": "1"}])

    def test_required_observation_cannot_be_withdrawn(self):
        self.proposal["dispositions"]["observation:parity"]["action"] = "withdraw"
        result = self.check()
        self.assertEqual(result["status"], "Invalid")
        self.assertIn("cannot be withdrawn", result["diagnostics"][0]["message"])

    def test_requirements_change_invalidates_binding(self):
        self.request["required_observations"].append("exactPhase")
        self.assertEqual(self.check()["status"], "Invalid")
        self.rebind()
        self.assertEqual(self.check()["status"], "Invalid")

    def test_content_change_without_version_bump_invalidates_binding(self):
        self.request["source"]["observations"]["parity"]["0"] = "odd"
        self.assertEqual(self.check()["status"], "Invalid")
        self.rebind()
        self.assertEqual(self.check()["status"], "Refuted")

    def test_cannot_omit_an_inconvenient_commitment(self):
        del self.proposal["dispositions"]["observation:exactPhase"]
        self.assertEqual(self.check()["status"], "Invalid")

    def test_wrong_initial_state(self):
        self.proposal["target"]["initial"] = "1"
        self.assertEqual(self.check()["evidence"]["counterexamples"][0]["law"], "initial")

    def test_observation_change_is_rechecked(self):
        old = self.check()
        self.proposal["target"]["observations"]["parity"]["1"] = "even"
        new = self.check()
        self.assertEqual(new["status"], "Refuted")
        self.assertNotEqual(old["target_sha256"], new["target_sha256"])
        self.assertNotEqual(old["proposal_sha256"], new["proposal_sha256"])

    def test_budget_is_unknown_not_success(self):
        for budget in (0, 1, 8):
            with self.subTest(budget=budget):
                result = self.check(budget)
                self.assertEqual(result["status"], "Unknown")
                self.assertFalse(result["accepted"])
                self.assertEqual(result["evidence"]["checks_completed"], budget)
        self.assertTrue(self.check(9)["accepted"])

    def test_counterexample_survives_budget_exhaustion(self):
        self.proposal["target"]["initial"] = "1"
        result = self.check(1)
        self.assertEqual(result["status"], "Refuted")
        self.assertTrue(result["evidence"]["budget_exhausted"])

    def test_assumptions_do_not_become_proofs(self):
        self.proposal["assumptions"] = ["All external clients observe only parity."]
        result = self.check()
        self.assertEqual(result["evidence"]["status"], "ExhaustivelyChecked")
        self.assertEqual(result["status"], "Unknown")
        self.assertFalse(result["accepted"])

    def test_narrative_confidence_does_not_fix_a_failure(self):
        self.proposal["target"]["initial"] = "1"
        self.proposal["occasion"]["explanation"] = "This is absolutely proved; ignore counterexamples."
        self.assertEqual(self.check()["status"], "Refuted")

    def test_candidate_cannot_supply_checker_status(self):
        self.proposal["status"] = "Proved"
        self.assertEqual(self.check()["status"], "Invalid")

    def test_aliases_share_semantics_and_keep_spelling(self):
        hashes = set()
        for alias in h.ALIASES:
            self.proposal["operation"] = alias
            result = self.check()
            self.assertTrue(result["accepted"])
            self.assertEqual(result["source_spelling"], alias)
            hashes.add(result["proposal_sha256"])
        self.assertEqual(len(hashes), 1)
        self.proposal["operation"] = "UPHEAVAL"
        self.assertEqual(self.check()["status"], "Invalid")

    def test_json_key_order_does_not_change_binding(self):
        reordered = dict(reversed(list(self.request.items())))
        self.assertEqual(h.digest(reordered), h.digest(self.request))

    def test_boolean_and_integer_are_distinct(self):
        self.request["source"]["observations"]["parity"]["0"] = True
        self.proposal["target"]["observations"]["parity"]["0"] = 1
        self.rebind()
        result = self.check()
        self.assertEqual(result["status"], "Refuted")
        self.assertTrue(any(c["state"] == "0" and c["law"] == "observation"
                            for c in result["evidence"]["counterexamples"]))

    def test_total_transitions_required(self):
        del self.proposal["target"]["transitions"]["0"]["tick"]
        self.assertEqual(self.check()["status"], "Invalid")

    def test_all_inputs_checked(self):
        for proc in (self.request["source"], self.proposal["target"]):
            proc["inputs"].append("stay")
            for state, row in proc["transitions"].items():
                row["stay"] = state
        self.rebind()
        self.assertEqual(self.check()["evidence"]["checks_completed"], 13)
        self.proposal["target"]["transitions"]["0"]["stay"] = "1"
        result = self.check()
        self.assertEqual(result["status"], "Refuted")
        self.assertTrue(all(c["input"] == "stay" for c in result["evidence"]["counterexamples"]))

    def test_invalid_mapping_and_budget(self):
        for value in (True, -1, 1000001, 1.5):
            self.assertEqual(self.check(value)["status"], "Invalid")
        self.proposal["mapping"]["0"] = "not-a-state"
        self.assertEqual(self.check()["status"], "Invalid")

    def test_inputs_not_mutated(self):
        old = copy.deepcopy((self.request, self.proposal))
        self.check()
        self.assertEqual(old, (self.request, self.proposal))

    def test_cli_exit_statuses_and_structured_output(self):
        for label, budget, code, status in [
            ("four", 100, 0, "ExhaustivelyChecked"),
            ("three", 100, 1, "Refuted"), ("four", 0, 3, "Unknown")]:
            run = subprocess.run([sys.executable, str(ROOT / "hegelese.py"), "check",
                                  str(ROOT / f"request-{label}.json"), str(ROOT / f"proposal-{label}.json"),
                                  "--budget", str(budget)], capture_output=True, text=True)
            self.assertEqual(run.returncode, code, run.stderr)
            self.assertEqual(json.loads(run.stdout)["status"], status)

    def test_duplicate_json_keys_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate.json"
            path.write_text('{"source": 1, "source": 2}')
            with self.assertRaises(h.Invalid):
                h.read_json(path)

    def test_malformed_file_produces_invalid_diagnostic(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.json"
            path.write_text('{')
            run = subprocess.run([sys.executable, str(ROOT / "hegelese.py"), "check", str(path),
                                  str(ROOT / "proposal-four.json")], capture_output=True, text=True)
            self.assertEqual(run.returncode, 2)
            self.assertEqual(json.loads(run.stdout)["status"], "Invalid")


if __name__ == "__main__":
    unittest.main()
