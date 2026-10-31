"""Exhaustive finite quotient-frontier demonstrations (Python standard library).

Run: python quotient_frontier.py [--output PATH]

This demonstrates elementary process-congruence facts; it is not a novelty claim,
an integration with Hegelese, or an application of the binary-cut theorem.
All declared states are checked, including states unreachable from the initial
state. Quotient targets have exactly the partition blocks as their states.
"""

import argparse
import json
from itertools import combinations
from pathlib import Path


def partitions(n):
    """Enumerate each partition of range(n) once in canonical block order."""
    blocks = []

    def visit(state):
        if state == n:
            yield tuple(tuple(block) for block in blocks)
            return
        for block in blocks:
            block.append(state)
            yield from visit(state + 1)
            block.pop()
        blocks.append([state])
        yield from visit(state + 1)
        blocks.pop()

    yield from visit(0)


def block_index(partition):
    return {state: index for index, block in enumerate(partition) for state in block}


def refines(left, right):
    """True when left retains at least every distinction retained by right."""
    index = block_index(right)
    return all(len({index[state] for state in block}) == 1 for block in left)


def merged_pairs(partition):
    return {pair for block in partition for pair in combinations(block, 2)}


def transition_congruence(process, partition):
    index = block_index(partition)
    return all(
        len({index[successors[state]] for state in block}) == 1
        for successors in process["transitions"].values()
        for block in partition
    )


def observation_compatible(process, partition):
    return all(
        len({values[state] for state in block}) == 1
        for values in process["retained_observations"].values()
        for block in partition
    )


def intersection_partition(n, feasible):
    if not feasible:
        raise ValueError("An infeasible request has no forced-loss intersection here")
    indices = [block_index(partition) for partition in feasible]
    groups = {}
    for state in range(n):
        signature = tuple(index[state] for index in indices)
        groups.setdefault(signature, []).append(state)
    return tuple(tuple(block) for block in groups.values())


def quotient_process(process, partition):
    """Construct a target whose preservation equations can also be checked."""
    index = block_index(partition)
    return {
        "states": list(range(len(partition))),
        "source_blocks": partition,
        "initial": index[process["initial"]],
        "mapping": [index[state] for state in process["states"]],
        "transitions": {
            symbol: [index[successors[block[0]]] for block in partition]
            for symbol, successors in process["transitions"].items()
        },
        "observations": {
            name: [values[block[0]] for block in partition]
            for name, values in process["retained_observations"].items()
        },
    }


def verify_quotient(process, target):
    mapping = target["mapping"]
    assert mapping[process["initial"]] == target["initial"]
    for state in process["states"]:
        for symbol, successors in process["transitions"].items():
            assert mapping[successors[state]] == target["transitions"][symbol][mapping[state]]
        for name, values in process["retained_observations"].items():
            assert values[state] == target["observations"][name][mapping[state]]


def analyze(process):
    n = len(process["states"])
    assert process["states"] == list(range(n)) and n > 0
    assert process["initial"] in process["states"]
    for successors in process["transitions"].values():
        assert len(successors) == n and all(state in process["states"] for state in successors)
    for values in process["retained_observations"].values():
        assert len(values) == n

    candidates = list(partitions(n))
    assert len(candidates) == len(set(candidates))
    congruences = [p for p in candidates if transition_congruence(process, p)]
    observation_partitions = [p for p in candidates if observation_compatible(process, p)]
    behavioral = [p for p in congruences if observation_compatible(process, p)]
    feasible = [p for p in behavioral if len(p) <= process["target_state_bound"]]
    finest = [p for p in feasible if not any(q != p and refines(q, p) for q in feasible)]

    result = {
        "name": process["name"],
        "source": process,
        "counts": {
            "all_set_partitions": len(candidates),
            "transition_congruences": len(congruences),
            "observation_compatible_partitions": len(observation_partitions),
            "behavior_preserving_congruences": len(behavioral),
            "feasible_with_state_bound": len(feasible),
            "finest_feasible": len(finest),
        },
        "feasible_partitions": feasible,
        "finest_feasible_partitions": finest,
        "finest_quotient_processes": [quotient_process(process, p) for p in finest],
        "intersection_partition": None,
        "intersection_satisfies_state_bound": None,
        "forced_merged_pairs": None,
        "avoidable_pair_witnesses": None,
        "universal_least_loss_partition": None,
        "some_state_identity_loss_is_unavoidable": None,
    }
    for partition in feasible:
        verify_quotient(process, quotient_process(process, partition))
    if not feasible:
        result["status"] = "infeasible"
        result["explanation"] = (
            "No quotient satisfies the transitions, retained observations, and state bound. "
            "Forced losses are left undefined, rather than inferred vacuously."
        )
        return result

    meet = intersection_partition(n, feasible)
    forced = merged_pairs(meet)
    all_pairs = set(combinations(range(n), 2))
    witnesses = []
    for pair in sorted(all_pairs - forced):
        witness = next(p for p in feasible if pair not in merged_pairs(p))
        witnesses.append({"pair": pair, "separating_feasible_partition": witness})

    assert transition_congruence(process, meet)
    assert observation_compatible(process, meet)
    assert all(refines(meet, p) for p in feasible)
    assert forced == set.intersection(*(merged_pairs(p) for p in feasible))
    for witness in witnesses:
        assert witness["separating_feasible_partition"] in feasible
        assert witness["pair"] not in merged_pairs(witness["separating_feasible_partition"])
    meet_feasible = len(meet) <= process["target_state_bound"]
    assert meet_feasible == (meet in feasible)
    assert meet_feasible == (len(finest) == 1)
    if meet_feasible:
        assert finest == [meet]

    result.update({
        "status": "universal_least_loss_exists" if meet_feasible else "incomparable_finest_quotients",
        "intersection_partition": meet,
        "intersection_satisfies_state_bound": meet_feasible,
        "forced_merged_pairs": sorted(forced),
        "avoidable_pair_witnesses": witnesses,
        "universal_least_loss_partition": meet if meet_feasible else None,
        "some_state_identity_loss_is_unavoidable": all(bool(merged_pairs(p)) for p in feasible),
        "explanation": (
            "The intersection is feasible and retains every distinction any feasible quotient retains."
            if meet_feasible else
            "The intersection exceeds the state bound. Some loss can be unavoidable without any "
            "particular pair-loss being forced; there is no universal least-loss quotient."
        ),
    })
    return result


DEMOS = [
    {
        "name": "FourPhase_parity_bound_2",
        "states": [0, 1, 2, 3],
        "initial": 0,
        "transitions": {"tick": [1, 2, 3, 0]},
        "retained_observations": {"parity": ["even", "odd", "even", "odd"]},
        "target_state_bound": 2,
    },
    {
        "name": "ThreeSelfLoops_constant_bound_2",
        "states": [0, 1, 2],
        "initial": 0,
        "transitions": {"tick": [0, 1, 2]},
        "retained_observations": {"constant": ["same", "same", "same"]},
        "target_state_bound": 2,
    },
    {
        "name": "ThreePhase_parity_bound_2",
        "states": [0, 1, 2],
        "initial": 0,
        "transitions": {"tick": [1, 2, 0]},
        "retained_observations": {"parity": ["even", "odd", "even"]},
        "target_state_bound": 2,
    },
]


def verify_expected(results):
    expected_counts = [
        (15, 3, 4, 2, 1, 1),
        (5, 5, 5, 5, 4, 3),
        (5, 2, 2, 1, 0, 0),
    ]
    for result, counts in zip(results, expected_counts):
        assert tuple(result["counts"].values()) == counts
    four, loops, three = results
    assert four["status"] == "universal_least_loss_exists"
    assert four["universal_least_loss_partition"] == ((0, 2), (1, 3))
    assert four["forced_merged_pairs"] == [(0, 2), (1, 3)]
    assert len(four["avoidable_pair_witnesses"]) == 4
    assert loops["status"] == "incomparable_finest_quotients"
    assert set(loops["finest_feasible_partitions"]) == {
        ((0, 1), (2,)), ((0, 2), (1,)), ((0,), (1, 2))
    }
    assert loops["intersection_partition"] == ((0,), (1,), (2,))
    assert loops["forced_merged_pairs"] == []
    assert loops["some_state_identity_loss_is_unavoidable"] is True
    assert len(loops["avoidable_pair_witnesses"]) == 3
    assert three["status"] == "infeasible"
    assert three["forced_merged_pairs"] is None
    assert three["intersection_partition"] is None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().with_name("quotient-frontier-results.json"))
    args = parser.parse_args()
    results = [analyze(process) for process in DEMOS]
    verify_expected(results)
    report = {
        "schema": "finite-process-quotient-frontier/1",
        "purpose": "Standalone demonstration of elementary known congruence facts; no novelty claim.",
        "scope": "All declared source states, total deterministic transitions, fixed retained observations.",
        "initial_state_rule": "Each quotient starts in the block containing the source initial state.",
        "order_convention": "Finer partition means less state-identity loss; this is not automaton minimization.",
        "authorization_rule": "Conditional necessity of a loss does not authorize accepting it.",
        "verification": {
            "expected_demo_counts_and_structures": "passed",
            "all_feasible_quotient_preservation_equations": "passed",
            "intersection_and_avoidable_pair_witness_checks": "passed",
            "partitions_enumerated": sum(r["counts"]["all_set_partitions"] for r in results),
            "feasible_quotients_checked": sum(r["counts"]["feasible_with_state_bound"] for r in results),
        },
        "demos": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for result in results:
        counts = result["counts"]
        print(f"{result['name']}: {result['status']}; "
              f"{counts['all_set_partitions']} partitions, "
              f"{counts['feasible_with_state_bound']} feasible, "
              f"{counts['finest_feasible']} finest")
    print(f"All assertions passed. Wrote {args.output.resolve()}")


if __name__ == "__main__":
    main()
