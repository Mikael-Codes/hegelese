"""Run an objectwise binary-cut quotient exercise against a pinned real checker.

Python 3.10+, standard library only. The external checker is not redistributed.
This exercise does not claim to check naturality or the reconstruction theorem.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

COMMIT = "3199a7fd4d83ab061c5d445d28be6c07edb0d61e"
CHECKER_SHA256 = "f64de70ed86c4988871ed3d66ee1241ff97a40e4c95816217526444ec49215c9"
RECONSTRUCTION_SHA256 = "e072aa39bca31a86548776fea1960c2567aa873a7d9bbd9c84ecb0844864a11b"
MONOMIALS = list(range(1, 8))  # Nonempty subsets of the three non-root labels.
LINEAR = [i for i, mask in enumerate(MONOMIALS) if mask.bit_count() == 1]
INPUTS = ["add_t" + str(mask) for mask in MONOMIALS]


def project(vector, kept):
    return sum(((vector >> coordinate) & 1) << j for j, coordinate in enumerate(kept))


def expand(vector, kept):
    return sum(((vector >> j) & 1) << coordinate for j, coordinate in enumerate(kept))


def make_process(name, kept, exact_state=False):
    states = list(range(1 << len(kept)))
    observations = {
        "linear_t" + str(MONOMIALS[c]): {
            str(s): (expand(s, kept) >> c) & 1 for s in states
        } for c in LINEAR
    }
    if exact_state:
        observations["exactState"] = {str(s): expand(s, kept) for s in states}
    return {
        "name": name, "version": "1", "states": list(map(str, states)),
        "inputs": INPUTS, "initial": "0",
        "transitions": {
            str(s): {input_name: str(s ^ project(1 << coordinate, kept))
                     for coordinate, input_name in enumerate(INPUTS)} for s in states
        },
        "observations": observations,
    }


def make_proposal(h, request, name, kept, retain_exact=False):
    target = make_process(name, kept, exact_state=retain_exact)
    dispositions = {
        "initial": {"action": "retain", "reason": "The quotient sends zero to zero."},
        "step": {"action": "retain", "reason": "Addition descends through the linear quotient."},
    }
    for observation in request["source"]["observations"]:
        retain = observation != "exactState" or retain_exact
        dispositions["observation:" + observation] = {
            "action": "retain" if retain else "withdraw",
            "reason": "Check this observation on every source vector." if retain else
                      "Full vector identity is not part of the positive-case request.",
        }
    return {
        "schema": "hegelese-proposal/0.1", "operation": "Upheaval",
        "request_sha256": h.digest(request),
        "occasion": {"kind": "Rearticulation", "explanation": "Compare natural augmentation-power quotients at the four-label object."},
        "target": target,
        "mapping": {s: str(project(int(s), kept)) for s in request["source"]["states"]},
        "dispositions": dispositions, "assumptions": [],
    }


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_reconstruction(path):
    """Direct comparison matrices at n=4, r=3; no theorem dimension formula."""
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != RECONSTRUCTION_SHA256:
        raise ValueError("Reconstruction checker differs from the inspected file.")
    spec = importlib.util.spec_from_file_location("binary_cut_derived", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    rows = []
    for name, d, expected in [("identity", None, (1, 1)), ("quotient_J3", 3, (0, 1)),
                              ("quotient_J2", 2, (0, 0))]:
        basis, differentials = m.build(4, 3, d)
        full = 15
        source_basis = m.cuts(full) if d is None else m.augmentation_basis(full, d)
        comparison = []
        for a in source_basis:
            column = 0
            for row, (chain, b) in enumerate(basis[0]):
                target = chain[0]
                image = ({m.restrict_cut(a, target)} if d is None else
                         m.restrict_augmentation(a, full, target, d))
                if b in image:
                    column |= 1 << row
            comparison.append(column)
        assert all(m.apply_columns(differentials[0], c) == 0 for c in comparison)
        assert all(m.compose_zero(differentials[i], differentials[i + 1])
                   for i in range(len(differentials) - 1))
        ranks = [m.gf2_rank(matrix) for matrix in differentials]
        limit_dimension = len(basis[0]) - ranks[0]
        image_dimension = m.gf2_rank(comparison)
        kernel_dimension = len(source_basis) - image_dimension
        cokernel_dimension = limit_dimension - image_dimension
        h1 = len(basis[1]) - ranks[0] - (ranks[1] if len(ranks) > 1 else 0)
        assert (kernel_dimension, cokernel_dimension) == expected
        assert h1 == 1
        rows.append({"case": name, "n": 4, "r": 3, "augmentation_cutoff_d": d,
                     "source_dimension": len(source_basis), "limit_dimension": limit_dimension,
                     "comparison_rank": image_dimension, "kernel_dimension": kernel_dimension,
                     "cokernel_dimension": cokernel_dimension, "H1_dimension": h1,
                     "cochain_dimensions": [len(b) for b in basis], "differential_ranks": ranks,
                     "ordinary_comparison_is_isomorphism": kernel_dimension == cokernel_dimension == 0})
    return {"method": "Exact GF2 comparison matrix into the kernel of the normalized Roos differential",
            "checker_sha256": digest, "cases": rows,
            "scope": "One four-label reconstruction diagram. This finite calculation is not a proof of the universal theorem."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checker", required=True, type=Path, help="Inspected hegelese.py at the pinned commit.")
    parser.add_argument("--reconstruction-checker", type=Path, help="Optional inspected preprint/checks/verify-derived.py.")
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent / "results")
    args = parser.parse_args()
    checker_bytes = args.checker.read_bytes()
    actual = hashlib.sha256(checker_bytes).hexdigest()
    if actual != CHECKER_SHA256:
        parser.error("Checker bytes differ from the inspected pinned file; expected SHA256 " + CHECKER_SHA256)
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("binary_cut_external_hegelese", args.checker)
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    assert h.VERSION == "0.3.0" and h.CHECKER == "hegelese-finite-checker/0.2"
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    source = make_process("J_four_labels", list(range(7)), exact_state=True)
    request = {"schema": "hegelese-request/0.1", "source": source,
               "required_observations": ["linear_t" + str(MONOMIALS[c]) for c in LINEAR]}
    exact_request = copy.deepcopy(request)
    exact_request["required_observations"].append("exactState")
    write_json(out / "request.json", request)
    write_json(out / "exact-state-required-request.json", exact_request)
    cases = [
        ("identity", list(range(7)), request, False, 128, 0, 0),
        ("quotient_J3", [i for i, m in enumerate(MONOMIALS) if m.bit_count() < 3], request, False, 64, 64, 0),
        ("quotient_J2", LINEAR, request, False, 8, 960, 0),
        ("negative_exactState", LINEAR, exact_request, True, 8, 960, 120),
    ]
    rows = []
    for name, kept, req, retain_exact, target_count, erased_pairs, failures in cases:
        proposal = make_proposal(h, req, name, kept, retain_exact)
        report = h.check(req, proposal, budget=100000)
        assert len(proposal["target"]["states"]) == target_count
        assert report["status"] == ("Refuted" if failures else "ExhaustivelyChecked")
        assert report["accepted"] == (failures == 0)
        assert report["evidence"]["failures"] == failures
        assert report["evidence"]["checks_completed"] == (1409 if retain_exact else 1281)
        assert report["structural_loss"]["erased_pairs"] == erased_pairs
        assert not report["evidence"]["budget_exhausted"]
        write_json(out / (name + ".proposal.json"), proposal)
        write_json(out / (name + ".report.json"), report)
        rows.append({"case": name, "source_states": 128, "target_states": target_count,
                     "status": report["status"], "accepted": report["accepted"],
                     "checks_completed": report["evidence"]["checks_completed"],
                     "failures": failures, "erased_pairs": erased_pairs,
                     "retained_coordinate_masks": [MONOMIALS[c] for c in kept]})
    summary = {
        "checker_repository": "https://github.com/Mikael-Codes/hegelese",
        "checker_commit": COMMIT, "checker_sha256": actual,
        "checker_version": h.VERSION, "python_version": sys.version.split()[0],
        "algebra": {"field": "F2", "labels": 4, "non_root_labels": [1, 2, 3],
                    "basis_subset_masks": MONOMIALS, "source_dimension": 7,
                    "state_encoding": "bit i is the coefficient of t_A for A with mask i+1"},
        "cases": rows,
        "checked_scope": "One finite object, all 128 vector states, all 7 addition inputs, declared retained observations.",
        "not_checked": ["Naturality over maps of finite label sets", "Reconstruction from objects of size at most r",
                        "Universal factorization or optimality", "Lineage acceptance"],
        "theorem_interpretation": {
            "source": "Binary-cut reconstruction preprint v2",
            "status": "External mathematical interpretation, not a Hegelese checker verdict",
            "claim": "For natural linear quotients of J with ordinary reconstruction cutoff r=3, J/J^2 is the universal most informative admissible quotient; identity J and J/J^3 do not meet that global cutoff.",
        },
    }
    if args.reconstruction_checker:
        reconstruction = check_reconstruction(args.reconstruction_checker)
        write_json(out / "reconstruction.json", reconstruction)
        summary["separate_reconstruction_check"] = reconstruction
    write_json(out / "summary.json", summary)
    print(json.dumps({"checker_commit": COMMIT, "cases": rows}, indent=2))


if __name__ == "__main__":
    main()
