"""Hegelese v0.3 design experiment; Python, not a Hegelese implementation.

Run: python3 process-reflection-reference.py
Finite deterministic systems only. These are scoped exhaustive checks,
not an implementation of philosophical immanence or a general proof checker.
"""

from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Process:
    name: str
    states: tuple[int, ...]
    initial: int
    # One input, tick. The tuples encode complete next-state/observation tables.
    next_state: tuple[int, ...]
    observation: tuple[int, ...]

    def validate(self):
        assert self.states == tuple(range(len(self.states)))
        assert self.initial in self.states
        assert len(self.next_state) == len(self.states)
        assert len(self.observation) == len(self.states)
        assert all(s in self.states for s in self.next_state)


def run(process, ticks):
    process.validate()
    assert isinstance(ticks, int) and ticks >= 0
    state = process.initial
    trace = []
    for step in range(ticks):
        target = process.next_state[state]
        trace.append({"step": step, "before": state, "input": "tick",
                      "after": target, "observation": process.observation[target]})
        state = target
    return {"initial_observation": process.observation[process.initial],
            "final_state": state, "events": trace}


def check_abstraction(source, target, mapping):
    source.validate()
    target.validate()
    assert len(mapping) == len(source.states)
    assert all(s in target.states for s in mapping)
    checks = [{"law": "initial", "holds": mapping[source.initial] == target.initial}]
    for state in source.states:
        checks.extend([
            {"law": "step", "state": state,
             "left": mapping[source.next_state[state]],
             "right": target.next_state[mapping[state]],
             "holds": mapping[source.next_state[state]] == target.next_state[mapping[state]]},
            {"law": "observation", "state": state,
             "left": source.observation[state], "right": target.observation[mapping[state]],
             "holds": source.observation[state] == target.observation[mapping[state]]},
        ])
    failed = [c for c in checks if not c["holds"]]
    return {"source": source.name, "target": target.name, "mapping": mapping,
            "domain": {"states": source.states, "inputs": ["tick"],
                       "observation": "parity", "initial_state_included": True},
            "status": "Refuted" if failed else "ExhaustivelyChecked",
            "checks": checks, "counterexamples": failed}


def experiment():
    four = Process("FourPhase@1", (0, 1, 2, 3), 0, (1, 2, 3, 0), (0, 1, 0, 1))
    three = Process("ThreePhase@1", (0, 1, 2), 0, (1, 2, 0), (0, 1, 0))
    two = Process("ParityToggle@1", (0, 1), 0, (1, 0), (0, 1))
    accepted = check_abstraction(four, two, (0, 1, 0, 1))
    rejected = check_abstraction(three, two, (0, 1, 0))
    bad_initial = Process("WrongInitial@1", two.states, 1, two.next_state, two.observation)
    initial_rejected = check_abstraction(four, bad_initial, (0, 1, 0, 1))
    assert accepted["status"] == "ExhaustivelyChecked"
    assert len(accepted["checks"]) == 9
    assert rejected["counterexamples"] == [
        {"law": "step", "state": 2, "left": 0, "right": 1, "holds": False}]
    assert initial_rejected["counterexamples"] == [{"law": "initial", "holds": False}]
    # Short traces agree even for a false general abstraction.
    assert [x["observation"] for x in run(three, 2)["events"]] == [
        x["observation"] for x in run(two, 2)["events"]]
    assert [x["observation"] for x in run(three, 3)["events"]] != [
        x["observation"] for x in run(two, 3)["events"]]
    # No lossless decoder: two source states have the same abstract image.
    assert accepted["mapping"][0] == accepted["mapping"][2]
    return {"kind": "Python reference experiment, not Hegelese execution",
            "accepted": accepted, "rejected": rejected,
            "wrong_initial_state": initial_rejected,
            "sample_run": run(four, 8),
            "limits": ["Only the declared finite tables and parity observation were checked.",
                       "A trace is not a proof of all future behavior.",
                       "A semantic cycle is allowed; bounded execution returns a finite prefix.",
                       "The abstraction is supplied by the programmer, not discovered by dialectics."]}


if __name__ == "__main__":
    print(json.dumps(experiment(), indent=2))
