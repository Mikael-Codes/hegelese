"""Hegelese bootstrap interpreter and articulated finite-change checker."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

ALIASES = {"Aufheben", "Sublation", "Upheaval", "aufheben", "sublation", "upheaval", "upheave"}
CHECKER = "hegelese-finite-checker/0.1"


class Invalid(ValueError):
    def __init__(self, path, message):
        self.path, self.message = path, message
        super().__init__(message)


def require(condition, path, message):
    if not condition:
        raise Invalid(path, message)


def fields(value, names, path):
    require(type(value) is dict, path, "Expected an object.")
    require(set(value) == set(names.split()), path,
            "Expected exactly these fields: " + names)


def words(value, path):
    require(type(value) is str and bool(value.strip()), path, "Expected nonempty text.")


def names(value, path, maximum):
    require(type(value) is list and 0 < len(value) <= maximum, path,
            f"Expected 1 through {maximum} distinct names.")
    for item in value:
        words(item, path)
    require(len(set(value)) == len(value), path, "Names must be distinct.")


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def process(value, path):
    fields(value, "name version states inputs initial transitions observations", path)
    words(value["name"], path + "/name")
    words(value["version"], path + "/version")
    names(value["states"], path + "/states", 1000)
    names(value["inputs"], path + "/inputs", 64)
    states, inputs = set(value["states"]), set(value["inputs"])
    require(type(value["initial"]) is str and value["initial"] in states,
            path + "/initial", "Initial state must be declared.")
    table = value["transitions"]
    require(type(table) is dict and set(table) == states, path + "/transitions",
            "Transitions must cover exactly the declared states.")
    for state, row in table.items():
        require(type(row) is dict and set(row) == inputs, path + "/transitions",
                "Each state must define every input exactly once.")
        for target in row.values():
            require(type(target) is str and target in states, path + "/transitions",
                    "Transition targets must be declared states.")
    observations = value["observations"]
    require(type(observations) is dict and len(observations) <= 32,
            path + "/observations", "Expected at most 32 observation tables.")
    for name, table in observations.items():
        words(name, path + "/observations")
        require(type(table) is dict and set(table) == states, path + "/observations",
                "Each observation must cover exactly the declared states.")
        require(all(type(x) in (str, int, bool, type(None)) for x in table.values()),
                path + "/observations", "Observation values must be strings, integers, booleans, or null.")


def validate(request, proposal, budget):
    require(type(budget) is int and 0 <= budget <= 1_000_000, "/budget",
            "Budget must be an integer from 0 through 1000000.")
    fields(request, "schema source required_observations", "/request")
    require(request["schema"] == "hegelese-request/0.1", "/request/schema", "Unsupported schema.")
    source = request["source"]
    process(source, "/request/source")
    required = request["required_observations"]
    require(type(required) is list, "/request/required_observations", "Expected a list.")
    for name in required:
        require(type(name) is str and name in source["observations"],
                "/request/required_observations", "Required observation must be exported by the source.")
    require(len(set(required)) == len(required), "/request/required_observations", "Duplicate requirement.")
    fields(proposal, "schema operation request_sha256 occasion target mapping dispositions assumptions", "/proposal")
    require(proposal["schema"] == "hegelese-proposal/0.1", "/proposal/schema", "Unsupported schema.")
    require(type(proposal["operation"]) is str and proposal["operation"] in ALIASES,
            "/proposal/operation", "Unknown Upheaval spelling.")
    require(proposal["request_sha256"] == digest(request), "/proposal/request_sha256",
            "Proposal does not refer to this exact request. Reconsider and recheck the change.")
    fields(proposal["occasion"], "kind explanation", "/proposal/occasion")
    require(proposal["occasion"]["kind"] in ("Rearticulation", "UnmetDemand"),
            "/proposal/occasion/kind", "Unsupported occasion kind.")
    words(proposal["occasion"]["explanation"], "/proposal/occasion/explanation")
    target = proposal["target"]
    process(target, "/proposal/target")
    require(set(source["inputs"]) == set(target["inputs"]), "/proposal/target/inputs",
            "This checker requires the same input alphabet.")
    mapping = proposal["mapping"]
    require(type(mapping) is dict and set(mapping) == set(source["states"]),
            "/proposal/mapping", "Mapping must cover exactly the source states.")
    require(all(type(v) is str and v in target["states"] for v in mapping.values()),
            "/proposal/mapping", "Mapping values must be target states.")
    commitments = {"initial", "step"} | {"observation:" + x for x in source["observations"]}
    dispositions = proposal["dispositions"]
    require(type(dispositions) is dict and set(dispositions) == commitments,
            "/proposal/dispositions", "Account for every exported source commitment exactly once.")
    mandatory = {"initial", "step"} | {"observation:" + x for x in required}
    for name, disposition in dispositions.items():
        fields(disposition, "action reason", "/proposal/dispositions/" + name)
        require(disposition["action"] in ("retain", "withdraw"), "/proposal/dispositions/" + name,
                "This checker supports retain and withdraw only.")
        words(disposition["reason"], "/proposal/dispositions/" + name + "/reason")
        require(name not in mandatory or disposition["action"] == "retain",
                "/proposal/dispositions/" + name, "A required commitment cannot be withdrawn.")
        if name.startswith("observation:") and disposition["action"] == "retain":
            require(name[12:] in target["observations"], "/proposal/target/observations",
                    "A retained observation must be exported by the target.")
    assumptions = proposal["assumptions"]
    require(type(assumptions) is list, "/proposal/assumptions", "Expected a list of unresolved assumptions.")
    for assumption in assumptions:
        words(assumption, "/proposal/assumptions")


def obligations(request, proposal):
    source, target, mapping = request["source"], proposal["target"], proposal["mapping"]
    yield {"law": "initial", "left": mapping[source["initial"]], "right": target["initial"]}
    for state in source["states"]:
        for item in source["inputs"]:
            yield {"law": "step", "state": state, "input": item,
                   "left": mapping[source["transitions"][state][item]],
                   "right": target["transitions"][mapping[state]][item]}
        for name, table in source["observations"].items():
            if proposal["dispositions"]["observation:" + name]["action"] == "retain":
                yield {"law": "observation", "observation": name, "state": state,
                       "left": table[state], "right": target["observations"][name][mapping[state]]}


def check(request, proposal, budget=100000):
    """Always recompute. Candidate prose and candidate-provided evidence confer no status."""
    try:
        validate(request, proposal, budget)
    except Invalid as error:
        return {"checker": CHECKER, "status": "Invalid", "accepted": False,
                "diagnostics": [{"path": error.path, "message": error.message}]}
    source, target = request["source"], proposal["target"]
    retained = [n for n in source["observations"]
                if proposal["dispositions"]["observation:" + n]["action"] == "retain"]
    total = 1 + len(source["states"]) * (len(source["inputs"]) + len(retained))
    checked, failed, counterexamples = 0, 0, []
    for obligation in obligations(request, proposal):
        if checked == budget:
            break
        checked += 1
        # Python equates True and 1; Hegelese observation tags remain distinct.
        if canonical(obligation["left"]) != canonical(obligation["right"]):
            failed += 1
            if len(counterexamples) < 10:
                counterexamples.append(obligation)
    exhausted = checked < total
    finite_status = "Refuted" if failed else "Unknown" if exhausted else "ExhaustivelyChecked"
    status = finite_status
    if proposal["assumptions"] and not failed:
        status = "Unknown"
    semantic_proposal = dict(proposal, operation="Upheaval")
    return {
        "checker": CHECKER, "status": status, "accepted": status == "ExhaustivelyChecked",
        "request_sha256": digest(request), "proposal_sha256": digest(semantic_proposal),
        "source_sha256": digest(source), "target_sha256": digest(target),
        "source_spelling": proposal["operation"],
        "articulation": {"status": "Complete", "meaning": "Required fields supplied; prose is not verified.",
                         "occasion": proposal["occasion"], "dispositions": proposal["dispositions"]},
        "evidence": {"status": finite_status, "domain": "All declared source states and inputs",
                     "source_states": source["states"], "inputs": source["inputs"],
                     "observations": retained, "checks_total": total, "checks_completed": checked,
                     "budget_exhausted": exhausted, "failures": failed,
                     "counterexamples": counterexamples, "counterexamples_omitted": max(0, failed - 10)},
        "unresolved_assumptions": proposal["assumptions"],
        "limits": ["Finite deterministic tables with total state maps and unchanged input alphabets only.",
                   "Reasons and occasion are supplied explanations, not checked philosophical derivations.",
                   "Target-only observations and claims about minimality, timing, resources, or external reality are not checked.",
                   "Hashes bind content but do not authenticate the request or certify the checker.",
                   "This checker accepts a scoped abstraction; it does not apply changes to a program."],
    }


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Invalid(str(path), "Duplicate JSON key: " + key)
            result[key] = value
        return result
    with Path(path).open("rb") as stream:
        data = stream.read(2_000_001)
    require(len(data) <= 2_000_000, str(path), "Input exceeds the 2 MB limit.")
    def constant(value):
        raise Invalid(str(path), "Nonstandard JSON constant: " + value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=constant)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    fingerprint = sub.add_parser("fingerprint", help="Hash a request without changing it.")
    fingerprint.add_argument("request")
    candidate = sub.add_parser("check", help="Check a JSON proposal against an independently supplied request.")
    candidate.add_argument("request")
    candidate.add_argument("proposal")
    candidate.add_argument("--budget", type=int, default=100000)
    execute = sub.add_parser("run", help="Execute a Hegelese bootstrap source file.")
    execute.add_argument("source")
    execute.add_argument("--fuel", type=int, default=100000)
    execute.add_argument("--budget", type=int, default=100000)
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            from hgl import run
            with Path(args.source).open("rb") as stream:
                data = stream.read(2_000_001)
            require(len(data) <= 2_000_000, args.source, "Source exceeds 2 MB.")
            report = run(data.decode("utf-8"), args.source, args.fuel, args.budget)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return {"Evaluated": 0, "ExhaustivelyChecked": 0, "Refuted": 1, "Invalid": 2, "Unknown": 3}[report["status"]]
        request = read_json(args.request)
        if args.command == "fingerprint":
            print(digest(request))
            return 0
        report = check(request, read_json(args.proposal), args.budget)
    except (OSError, ValueError, TypeError, RecursionError) as error:
        report = {"checker": CHECKER, "status": "Invalid", "accepted": False,
                  "diagnostics": [{"path": getattr(error, "path", "/input"), "message": str(error)}]}
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return {"ExhaustivelyChecked": 0, "Refuted": 1, "Invalid": 2, "Unknown": 3}[report["status"]]


if __name__ == "__main__":
    sys.exit(main())
