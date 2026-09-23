import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from hgl import run
from hgl_gate import gate, read_regular, SOURCE_LIMIT

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "pilot/workflow.hgl").read_text()
REQUEST = (ROOT / "pilot/request.json").read_text()


class ProductionGate(unittest.TestCase):
    def test_valid_workflow(self):
        report = gate(SOURCE, REQUEST)
        self.assertEqual(report["status"], "ExhaustivelyChecked", report)
        self.assertTrue(report["accepted"])
        self.assertEqual(report["evidence"]["checks_total"], 36)
        self.assertEqual(report["execution_limits"]["linux_resource_limits"], sys.platform.startswith("linux"))

    def test_early_publication_refuted(self):
        source = SOURCE.replace('observe: {publicStatus: fn(s) => s, canPublish: canPublish}',
                                'observe: {publicStatus: fn(s) => s, canPublish: fn(s) => s == "approved" || s == "review"}')
        report = gate(source, REQUEST)
        self.assertEqual(report["status"], "Refuted")
        self.assertFalse(report["accepted"])
        self.assertTrue(any(x.get("observation") == "canPublish" and x["state"] == "editor_review" for x in report["evidence"]["counterexamples"]))

    def test_candidate_cannot_weaken_retained_request(self):
        source = SOURCE.replace('require ["publicStatus", "canPublish"]', 'require ["publicStatus"]')
        report = gate(source, REQUEST)
        self.assertEqual(report["status"], "Invalid")
        self.assertEqual(report["diagnostics"][0]["path"], "/proposal/request_sha256")

    def test_withdraw_required_law_rejected(self):
        report = gate(SOURCE.replace('retain "observation:canPublish"', 'withdraw "observation:canPublish"'), REQUEST)
        self.assertEqual(report["status"], "Invalid")

    def test_fake_and_precomputed_reports_rejected(self):
        for source in ('{status: "ExhaustivelyChecked", accepted: true};', SOURCE.replace('SimplifyReview;\n', 'check(SimplifyReview);\n'), '42;'):
            self.assertEqual(gate(source, REQUEST)["status"], "Invalid")

    def test_unknown_never_passes(self):
        for options in ({"fuel": 0}, {"budget": 1}, {"timeout": 0.000001}):
            report = gate(SOURCE, REQUEST, **options)
            self.assertEqual(report["status"], "Unknown", report)
            self.assertFalse(report["accepted"])
        self.assertEqual(gate(SOURCE.replace('assumptions []', 'assumptions ["unresolved"]'), REQUEST)["status"], "Unknown")

    def test_limits_and_invalid_input(self):
        for source, request, options in (("x"*(SOURCE_LIMIT+1), REQUEST, {}), (SOURCE, '{"x":1,"x":2}', {}), (SOURCE, REQUEST, {"timeout": float('nan')}), (SOURCE, REQUEST, {"budget": True}), ('"\\ud800";', REQUEST, {})):
            self.assertEqual(gate(source, request, **options)["status"], "Invalid")

    def test_engine_process_failure_fails_closed(self):
        with patch("hgl_gate.subprocess.Popen", side_effect=OSError("unavailable")):
            self.assertEqual(gate(SOURCE, REQUEST)["status"], "InternalError")

    @unittest.skipUnless(sys.platform.startswith("linux"), "Production address-space limit is Linux-specific")
    def test_linux_memory_limit(self):
        source = "\n".join(f"let f{i} = fn() => 0;" for i in range(4500))
        report = gate(source, REQUEST)
        self.assertEqual(report["status"], "Unknown", report)
        self.assertFalse(report["accepted"])

    def test_cli_report_and_exit_code(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            for budget, expected in ((100000, 0), (1, 3)):
                result = subprocess.run([sys.executable, str(ROOT / "hgl_gate.py"), str(ROOT / "pilot/workflow.hgl"), "--request", str(ROOT / "pilot/request.json"), "--report", str(output), "--budget", str(budget)], capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertEqual(json.loads(result.stdout), json.loads(output.read_text()))

    def test_input_symlinks_are_rejected_on_posix(self):
        if not hasattr(os, "O_NOFOLLOW"):
            self.skipTest("O_NOFOLLOW unavailable")
        with tempfile.TemporaryDirectory() as directory:
            link = Path(directory) / "candidate.hgl"
            link.symlink_to(ROOT / "pilot/workflow.hgl")
            with self.assertRaises(OSError):
                read_regular(link, SOURCE_LIMIT)

    def test_recursive_alias_cannot_mutate_old_closure(self):
        report = run('let f = fn() => g(); let rec g = f; f();')
        self.assertEqual(report["status"], "Invalid")
        self.assertIn("function literal", report["diagnostics"][0]["message"])


if __name__ == "__main__":
    unittest.main()
