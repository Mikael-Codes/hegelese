"""Executable language conformance, including hostile evidence and resource cases."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

import hegelese
from hgl import run

ROOT = Path(__file__).resolve().parents[1]
FOUR = (ROOT / "examples/four-phase.hgl").read_text()


class InterpreterConformance(unittest.TestCase):
    def value(self, source):
        report = run(source)
        self.assertEqual(report["status"], "Evaluated", report)
        return report["value"]

    def test_functional_example(self):
        self.assertEqual(self.value((ROOT / "examples/functional.hgl").read_text()),
                         {"sumOfSquares": 30, "factorial": 720, "answer": 42})

    def test_precedence_and_integer_semantics(self):
        self.assertEqual(self.value("[2 + 3 * 4, (2 + 3) * 4, 10 - 3 - 2, -7 / 3, -7 % 3];"), [14, 20, 5, -3, 2])

    def test_lexical_scope_and_parameter_shadowing(self):
        self.assertEqual(self.value("let x = 10; let f = fn(y) => x + y; let g = fn(x) => f(x); g(2);"), 12)
        self.assertEqual(run("let f = fn(x) => later; let later = 1; f(0);")["status"], "Invalid")

    def test_immutability_duplicate_names(self):
        for source in ("let x = 1; let x = 2;", "let len = 3;", "let x = [1]; x[0] = 2;"):
            self.assertEqual(run(source)["status"], "Invalid")

    def test_strict_application_and_lazy_branches(self):
        self.assertEqual(self.value("[if true then 2 else 1 / 0, false && (1 / 0 == 0), true || (1 / 0 == 0)];"), [2, False, True])
        self.assertEqual(run("let ignore = fn(x) => 1; ignore(1 / 0);")["status"], "Invalid")

    def test_no_python_truthiness_or_boolean_arithmetic(self):
        for source in ("if 1 then 2 else 3;", "true + 1;", "!1;", "false || 3;", "[1][true];", "str(true);"):
            self.assertEqual(run(source)["status"], "Invalid", source)
        self.assertEqual(self.value("[true == 1, [true] == [1], {x: true} == {x: 1}];"), [False]*3)

    def test_records_strings_and_indexes(self):
        self.assertEqual(self.value('let a = {text: "hegel", values: [4, 5]}; [a.text[1], a.values[1], len(a), "a" + "b", [1] + [2]];'), ["e", 5, 2, "ab", [1, 2]])
        for source in ('{}.missing;', '[1][-1];', '"hi"[2];', '{x: 1, x: 2};'):
            self.assertEqual(run(source)["status"], "Invalid")

    def test_tagged_match(self):
        self.assertEqual(self.value('match variant("Some", 4) { Some(x) => x * 2; None(x) => 0; };'), 8)
        self.assertEqual(run('match variant("Missing", 4) { Some(x) => x; };')["status"], "Invalid")
        self.assertEqual(run('match 4 { Some(x) => x; };')["status"], "Invalid")

    def test_functions_have_exact_arity(self):
        for source in ('(fn(x) => x)();', '(fn(x) => x)(1, 2);', 'len();', '(fn(x, x) => x)(1, 2);', 'let rec x = 1;'):
            self.assertEqual(run(source)["status"], "Invalid")
        self.assertEqual(self.value('(fn() => 4)();'), 4)

    def test_recursion_and_output_are_bounded(self):
        self.assertEqual(run("let rec loop = fn(x) => loop(x); loop(0);", fuel=100)["status"], "Unknown")
        self.assertEqual(run("let rec tree = fn(n) => if n == 0 then 0 else (fn(x) => [x, x])(tree(n-1)); tree(40);", fuel=2000)["status"], "Unknown")
        self.assertEqual(run("1;", fuel=0)["status"], "Unknown")
        self.assertEqual(run("1;", fuel=-1)["status"], "Invalid")

    def test_four_phase_development(self):
        result = run(FOUR, "example.hgl")
        self.assertEqual(result["status"], "ExhaustivelyChecked")
        self.assertEqual(result["value"]["evidence"]["checks_completed"], 9)
        self.assertEqual(result["value"]["articulation"]["dispositions"]["observation:exactPhase"]["action"], "withdraw")
        self.assertEqual(result["value"]["source_location"], {"file": "example.hgl", "line": 21, "column": 1, "spelling": "upheave"})

    def test_three_phase_refutes_with_concrete_counterexample(self):
        source = FOUR.replace('["0", "1", "2", "3"]', '["0", "1", "2"]').replace('% 4)', '% 3)')
        report = run(source)
        self.assertEqual(report["status"], "Refuted")
        self.assertIn({"law": "step", "state": "2", "input": "tick", "left": "0", "right": "1"}, report["value"]["evidence"]["counterexamples"])

    def test_wrong_initial_state(self):
        source = FOUR.replace('initial: "0",\n  step: fn(s, input) => str(1', 'initial: "1",\n  step: fn(s, input) => str(1')
        report = run(source)
        self.assertEqual(report["status"], "Refuted")
        self.assertEqual(report["value"]["evidence"]["counterexamples"][0]["law"], "initial")

    def test_aliases_same_semantics_original_locations(self):
        hashes = set()
        for spelling in hegelese.ALIASES:
            report = run(FOUR.replace("upheave Alternation", spelling + " Alternation"))
            self.assertEqual(report["status"], "ExhaustivelyChecked")
            hashes.add(report["value"]["proposal_sha256"])
            self.assertEqual(report["value"]["source_location"]["spelling"], spelling)
        self.assertEqual(len(hashes), 1)
        self.assertEqual(run(FOUR.replace("upheave Alternation", "UPHEAVAL Alternation"))["status"], "Invalid")

    def test_required_commitment_cannot_be_withdrawn(self):
        report = run(FOUR.replace('require ["parity"]', 'require ["parity", "exactPhase"]'))
        self.assertEqual(report["status"], "Invalid")
        self.assertEqual(report["value"]["diagnostics"][0]["location"]["spelling"], "withdraw")

    def test_budget_and_assumptions_remain_unknown(self):
        self.assertEqual(run(FOUR, budget=2)["status"], "Unknown")
        self.assertEqual(run(FOUR.replace('assumptions []', 'assumptions ["External adequacy is unresolved"]'))["status"], "Unknown")

    def test_changed_observation_rechecks_and_rebinds(self):
        old = run(FOUR)["value"]
        changed = FOUR.replace('observe: {parity: parity}', 'observe: {parity: fn(s) => "even"}')
        new = run(changed)["value"]
        self.assertEqual(new["status"], "Refuted")
        self.assertNotEqual(old["target_sha256"], new["target_sha256"])
        self.assertEqual(old["request_sha256"], new["request_sha256"])

    def test_inspection_and_unchecked_development(self):
        prefix = FOUR.rsplit("check(Alternation);", 1)[0]
        self.assertEqual(self.value(prefix + 'inspect(FourPhase).transitions["3"].tick;'), "0")
        self.assertEqual(self.value(prefix + 'Alternation;')["kind"], "UncheckedDevelopment")
        self.assertEqual(self.value(prefix + 'check(Alternation).status;'), "ExhaustivelyChecked")

    def test_data_cannot_forge_evidence_type(self):
        report = run('{status: "ExhaustivelyChecked", accepted: true};')
        self.assertEqual(report["status"], "Evaluated")
        self.assertEqual(run('check({status: "ExhaustivelyChecked", accepted: true});')["status"], "Invalid")

    def test_invalid_source_reports_line_and_column(self):
        report = run("# hello\nlet x = 1;\nx + unknown;", "broken.hgl")
        self.assertEqual(report["status"], "Invalid")
        self.assertEqual(report["diagnostics"][0]["location"], {"file": "broken.hgl", "line": 3, "column": 5, "spelling": "unknown"})
        for source in ('let x = ;', 'let x = "unterminated;', 'let x = 1', 'fn(', 'match 1 {', 'upheave X {', '"\\q";', '@;'):
            self.assertEqual(run(source)["status"], "Invalid", source)

    def test_invalid_process_and_request(self):
        for source in (FOUR.replace('states: ["0", "1", "2", "3"]', 'states: []'), FOUR.replace('str((int(s) + 1) % 4)', '"outside"'), FOUR.replace('require ["parity"]', 'require ["missing"]')):
            self.assertEqual(run(source)["status"], "Invalid")

    def test_cli_and_checking_exit_codes(self):
        for filename, options, expected in (("functional.hgl", [], 0), ("four-phase.hgl", [], 0), ("four-phase.hgl", ["--budget", "2"], 3), ("three-phase.hgl", [], 1)):
            completed = subprocess.run([sys.executable, str(ROOT / "hegelese.py"), "run", str(ROOT / "examples" / filename), *options], capture_output=True, text=True)
            self.assertEqual(completed.returncode, expected, completed.stderr + completed.stdout)
            self.assertIn("status", json.loads(completed.stdout))


if __name__ == "__main__":
    unittest.main()
