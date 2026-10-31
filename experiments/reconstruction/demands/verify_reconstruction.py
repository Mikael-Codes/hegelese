"""Exhaustive finite quotient tests for independent-view reconstruction.

Python 3.10+, standard library only. Writes results beside this file.
No theorem is used to generate feasible quotients. A second search explicitly
enumerates every source and endpoint equivalence for small repeated-fiber cases.
"""
from collections import Counter
import argparse
from functools import lru_cache
from itertools import combinations_with_replacement, product
import json
from pathlib import Path
import sys


def canonical(values):
    names = {}
    return tuple(names.setdefault(value, len(names)) for value in values)


@lru_cache(None)
def partitions(n):
    """Every equivalence relation once, as a restricted-growth string."""
    if n == 0:
        return ((),)
    def visit(prefix):
        if len(prefix) == n:
            yield prefix
        else:
            for label in range(max(prefix) + 2):
                yield from visit(prefix + (label,))
    return tuple(visit((0,)))


def refines(p, q):
    return all(p[i] != p[j] or q[i] == q[j]
               for i in range(len(p)) for j in range(i))


def triple_refines(p, q):
    return all(refines(a, b) for a, b in zip(p, q))


def minima(candidates):
    return [p for p in candidates if not any(q != p and triple_refines(q, p)
                                            for q in candidates)]


def intersection(candidates):
    return tuple(canonical(tuple(q[k][i] for q in candidates)
                           for i in range(len(candidates[0][k])))
                 for k in range(len(candidates[0])))


def projection_surjective(rows, sizes):
    return all({row[k] for row in rows} == set(range(size))
               for k, size in enumerate(sizes))


def connected_image(rows, sizes):
    """Connectedness of the bipartite image graph, for exactly two axes."""
    assert len(sizes) == 2
    neighbors = {("A", i): set() for i in range(sizes[0])}
    neighbors.update({("B", j): set() for j in range(sizes[1])})
    for i, j in rows:
        neighbors["A", i].add(("B", j))
        neighbors["B", j].add(("A", i))
    visited, todo = set(), [("A", 0)]
    while todo:
        node = todo.pop()
        if node not in visited:
            visited.add(node)
            todo.extend(neighbors[node] - visited)
    return len(visited) == sum(sizes)


def endpoint_search(rows, sizes):
    """Enumerate endpoint partitions; derive the only possible source kernel.

    Each quotient source must be exactly the product of quotient endpoints.
    Distinct source representatives with the same quotient tuple must merge.
    A quotient tuple absent from the original image cannot be manufactured.
    """
    feasible = []
    for endpoints in product(*(partitions(size) for size in sizes)):
        images = [tuple(p[row[k]] for k, p in enumerate(endpoints)) for row in rows]
        all_tuples = set(product(*(range(max(p) + 1) for p in endpoints)))
        if set(images) == all_tuples:
            feasible.append((canonical(images),) + endpoints)
    return feasible


def direct_search(rows, sizes):
    """Independent full search: quotient maps, naturality, product bijection.

    This does NOT force the source kernel from endpoint kernels. Every source
    equivalence is tried, and quotient functions are explicitly constructed.
    """
    feasible, examined = [], 0
    for congruences in product(*(partitions(n) for n in (len(rows),) + tuple(sizes))):
        examined += 1
        source_partition = congruences[0]
        source_blocks = set(source_partition)
        quotient_maps = []
        valid = True
        for axis, endpoint_partition in enumerate(congruences[1:]):
            function = {}
            for state, row in enumerate(rows):
                source_block = source_partition[state]
                target_block = endpoint_partition[row[axis]]
                if source_block in function and function[source_block] != target_block:
                    valid = False
                    break
                function[source_block] = target_block
            if not valid:
                break
            quotient_maps.append(function)
        if not valid:
            continue
        comparison = {block: tuple(f[block] for f in quotient_maps) for block in source_blocks}
        product_states = set(product(*(set(p) for p in congruences[1:])))
        if len(set(comparison.values())) == len(source_blocks) and set(comparison.values()) == product_states:
            feasible.append(congruences)
    return feasible, examined


def describe(rows, sizes, feasible):
    finest = minima(feasible)
    meet = intersection(feasible)
    universal = meet in feasible
    assert universal == (len(finest) == 1)
    if universal:
        assert all(triple_refines(finest[0], q) for q in feasible)
    return {"axis_sizes": sizes, "source_states": len(rows), "distinct_joint_images": len(set(rows)),
            "joint_surjective": len(set(rows)) == product_size(sizes),
            "endpoint_surjective": projection_surjective(rows, sizes),
            "feasible_quotients": len(feasible), "finest_quotients": len(finest),
            "universal_quotient_exists": universal, "intersection_feasible": universal,
            "minimal_kernels": finest, "intersection_kernel": meet}


def product_size(sizes):
    answer = 1
    for size in sizes:
        answer *= size
    return answer


def stable(partition, transition):
    return all(partition[i] != partition[j] or partition[transition[i]] == partition[transition[j]]
               for i in range(len(partition)) for j in range(i))


def dynamic_case(name, rows, sizes, transitions):
    """One common input, supplied explicitly at source and every endpoint."""
    source_step, *endpoint_steps = transitions
    assert len(source_step) == len(rows)
    for state, row in enumerate(rows):
        assert rows[source_step[state]] == tuple(step[row[k]] for k, step in enumerate(endpoint_steps))
    all_quotients, count = direct_search(rows, sizes)
    feasible = [q for q in all_quotients if all(stable(p, step) for p, step in zip(q, transitions))]
    assert feasible
    result = describe(rows, sizes, feasible)
    result.update(name=name, rows=rows, transitions=transitions,
                  all_equivalence_tuples_examined=count, process_quotient_kernels=feasible,
                  observations="None; all transition systems have one common input.")
    return result


def relation_cases():
    records = []
    for sizes in product(range(1, 4), repeat=2):
        cells = list(product(*(range(n) for n in sizes)))
        for bits in range(1, 1 << len(cells)):
            rows = tuple(cell for i, cell in enumerate(cells) if (bits >> i) & 1)
            if not projection_surjective(rows, sizes):
                continue
            feasible = endpoint_search(rows, sizes)
            record = describe(rows, sizes, feasible)
            # Compare the proposed theorem only after exact enumeration.
            assert record["universal_quotient_exists"] == record["joint_surjective"]
            if record["joint_surjective"]:
                expected = (canonical(rows),) + tuple(tuple(range(n)) for n in sizes)
                assert record["minimal_kernels"] == [expected]
            record.update(relation_mask=bits, rows=rows, image_graph_connected=connected_image(rows, sizes))
            records.append(record)
    return records


def three_view_cases():
    sizes = (2, 2, 2)
    cells = list(product(range(2), repeat=3))
    records = []
    for bits in range(1, 1 << len(cells)):
        rows = tuple(cell for i, cell in enumerate(cells) if (bits >> i) & 1)
        if not projection_surjective(rows, sizes):
            continue
        record = describe(rows, sizes, endpoint_search(rows, sizes))
        assert record["universal_quotient_exists"] == record["joint_surjective"]
        record.update(relation_mask=bits)
        records.append(record)
    return records


def repeated_fiber_cases():
    """All set maps up to relabeling source states, for 1<=|X|<=4 and axes<=3.

    Nondecreasing image multisets include every possible joint-map fiber
    multiplicity. All endpoint labels remain distinct and are not modded out.
    Identity transitions make source relabeling immaterial to these cases.
    """
    records, examined = [], 0
    for sizes in product(range(1, 4), repeat=2):
        cells = tuple(product(*(range(n) for n in sizes)))
        for source_size in range(1, 5):
            for rows in combinations_with_replacement(cells, source_size):
                if not projection_surjective(rows, sizes):
                    continue
                fast = endpoint_search(rows, sizes)
                direct, count = direct_search(rows, sizes)
                examined += count
                assert set(fast) == set(direct), (sizes, rows)
                record = describe(rows, sizes, direct)
                assert record["universal_quotient_exists"] == record["joint_surjective"]
                record.update(rows=rows, all_equivalence_tuples_examined=count)
                records.append(record)
    return records, examined


def arrow_cases():
    """Walking arrow X->A, demanding the induced quotient arrow be bijective.

    Identity transitions only; the onto-or-singleton-image criterion below is
    deliberately not asserted for arbitrary process transitions.
    """
    records, examined = [], 0
    for target_size in range(1, 5):
        for source_size in range(1, 5):
            for images in combinations_with_replacement(range(target_size), source_size):
                rows = tuple((image,) for image in images)
                fast = endpoint_search(rows, (target_size,))
                direct, count = direct_search(rows, (target_size,))
                examined += count
                assert set(fast) == set(direct)
                record = describe(rows, (target_size,), direct)
                assert record["universal_quotient_exists"] == (len(set(images)) in (1, target_size))
                record.update(images=images, all_equivalence_pairs_examined=count)
                records.append(record)
    return records, examined


def overlap_cases():
    """Two four-state views over a protected two-state common base.

    Endpoint equivalences must refine the fixed base maps [0,0,1,1].
    Reconstruction is a fiber product, not the full Cartesian product.
    Both endpoint search and independent full congruence search are used.
    """
    sizes, base = (4, 4), (0, 0, 1, 1)
    endpoint_partitions = tuple(p for p in partitions(4) if refines(p, base))
    cells = tuple((a, b) for a in range(4) for b in range(4) if base[a] == base[b])
    records, examined_total = [], 0
    for bits in range(1, 1 << len(cells)):
        rows = tuple(cell for i, cell in enumerate(cells) if (bits >> i) & 1)
        if not projection_surjective(rows, sizes):
            continue
        fast, direct, examined = [], [], 0
        for pa, pb in product(endpoint_partitions, repeat=2):
            base_a = {pa[a]: base[a] for a in range(4)}
            base_b = {pb[b]: base[b] for b in range(4)}
            fiber_product = {(a, b) for a in set(pa) for b in set(pb) if base_a[a] == base_b[b]}
            images = [(pa[a], pb[b]) for a, b in rows]
            if set(images) == fiber_product:
                fast.append((canonical(images), pa, pb))
            for px in partitions(len(rows)):
                examined += 1
                maps, valid = [dict(), dict()], True
                for state, (a, b) in enumerate(rows):
                    block = px[state]
                    for axis, value in enumerate((pa[a], pb[b])):
                        if block in maps[axis] and maps[axis][block] != value:
                            valid = False
                        maps[axis][block] = value
                if not valid:
                    continue
                comparison = {block: (maps[0][block], maps[1][block]) for block in set(px)}
                if len(set(comparison.values())) == len(set(px)) and set(comparison.values()) == fiber_product:
                    direct.append((px, pa, pb))
        examined_total += examined
        assert set(fast) == set(direct)
        finest, meet = minima(direct), intersection(direct)
        universal = meet in direct
        full = len(rows) == len(cells)
        assert universal == full == (len(finest) == 1)
        records.append({"relation_mask": bits, "rows": rows, "axis_sizes": sizes,
                        "base_size": 2, "base_maps": [base, base],
                        "source_states": len(rows), "fiber_product_states": len(cells),
                        "onto_fiber_product": full, "endpoint_surjective": True,
                        "feasible_quotients": len(direct), "finest_quotients": len(finest),
                        "universal_quotient_exists": universal, "minimal_kernels": finest,
                        "intersection_kernel": meet, "all_equivalence_tuples_examined": examined})
    # A nontrivial input swaps the two base cells. Its quotient constraints tie
    # choices in the two cells together, but do not restore universal existence.
    dynamic = []
    for full in (False, True):
        rows = cells if full else tuple((i, i) for i in range(4))
        pa_step = pb_step = (2, 3, 0, 1)
        px_step = tuple(rows.index((pa_step[a], pb_step[b])) for a, b in rows)
        all_feasible = []
        for pa, pb in product(endpoint_partitions, repeat=2):
            images = [(pa[a], pb[b]) for a, b in rows]
            ba = {pa[a]: base[a] for a in range(4)}
            bb = {pb[b]: base[b] for b in range(4)}
            expected = {(a, b) for a in set(pa) for b in set(pb) if ba[a] == bb[b]}
            if set(images) == expected:
                candidate = (canonical(images), pa, pb)
                if all(stable(p, step) for p, step in zip(candidate, (px_step, pa_step, pb_step))):
                    all_feasible.append(candidate)
        assert all(base[pa_step[a]] == 1 - base[a] for a in range(4))
        finest, meet = minima(all_feasible), intersection(all_feasible)
        assert (meet in all_feasible) == full
        dynamic.append({"name": "full_fiber_product_base_swap" if full else "diagonal_fibers_base_swap",
                        "rows": rows, "base_maps": [base, base], "base_transition": [1, 0],
                        "transitions": [px_step, pa_step, pb_step],
                        "feasible_quotients": len(all_feasible), "finest_quotients": len(finest),
                        "universal_quotient_exists": meet in all_feasible, "minimal_kernels": finest})
    return records, examined_total, dynamic


def write(output_dir, name, value):
    target = output_dir / name
    target.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent,
                        help="Directory for results; defaults to the script directory.")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    # Bell counts make the partition generator independently auditable.
    assert [len(partitions(n)) for n in range(6)] == [1, 1, 2, 5, 15, 52]
    relations = relation_cases()
    cube = three_view_cases()
    repeated, repeated_examined = repeated_fiber_cases()
    arrows, arrow_examined = arrow_cases()
    overlaps, overlap_examined, overlap_dynamic = overlap_cases()
    examples = [
        dynamic_case("diagonal_span_bit_flip", ((0, 0), (1, 1)), (2, 2),
                     ((1, 0), (1, 0), (1, 0))),
        dynamic_case("connected_three_corner_reset", ((0, 0), (0, 1), (1, 0)), (2, 2),
                     ((0, 0, 0), (0, 0), (0, 0))),
        dynamic_case("arrow_identity_transition_counterexample", ((0,), (1,)), (3,),
                     ((0, 1), (0, 1, 2))),
        dynamic_case("arrow_dynamics_force_unique_attachment", ((0,), (1,)), (3,),
                     ((0, 1), (0, 1, 0))),
    ]
    assert [e["universal_quotient_exists"] for e in examples] == [False, False, False, True]
    assert [e["finest_quotients"] for e in examples] == [2, 2, 2, 1]
    assert examples[3]["minimal_kernels"] == [((0, 1), (0, 1, 0))]
    def summary(records):
        return {"cases": len(records),
                "universal_exists": sum(r["universal_quotient_exists"] for r in records),
                "finest_quotient_count_histogram": dict(sorted(Counter(r["finest_quotients"] for r in records).items()))}
    totals = {
        "python_version": sys.version.split()[0], "method": "Exact equivalence-relation enumeration; no external dependencies",
        "two_view_relations": dict(summary(relations), axis_sizes="1..3 each", individually_surjective=True),
        "three_view_relations": dict(summary(cube), axis_sizes=[2, 2, 2], individually_surjective=True),
        "repeated_fiber_full_search": dict(summary(repeated), source_sizes="1..4", axis_sizes="1..3 each",
                                           congruence_tuples_examined=repeated_examined,
                                           coverage="Every joint-map multiset, up to permutation of source states, with surjective endpoint maps"),
        "arrow_full_search": dict(summary(arrows), source_sizes="1..4", target_sizes="1..4",
                                  congruence_pairs_examined=arrow_examined,
                                  coverage="Every map up to permutation of source states; identity transitions"),
        "protected_overlap_full_search": dict(summary(overlaps), axis_sizes=[4, 4], base_size=2,
                                               base_maps=[[0, 0, 1, 1], [0, 0, 1, 1]],
                                               congruence_tuples_examined=overlap_examined,
                                               coverage="Every full-projection subset of the eight-state fiber product; every endpoint partition refining the protected base"),
        "protected_overlap_dynamic_examples": overlap_dynamic,
        "nontrivial_process_examples": examples,
        "minimal_counterexamples_in_enumerated_families": {
            "arrow_total_states": min(r["source_states"] + sum(r["axis_sizes"]) for r in arrows if not r["universal_quotient_exists"]),
            "surjective_span_total_states": min(r["source_states"] + sum(r["axis_sizes"]) for r in repeated if not r["universal_quotient_exists"]),
            "connected_surjective_span_total_states": min(r["source_states"] + sum(r["axis_sizes"]) for r in relations
                                                           if r["image_graph_connected"] and not r["universal_quotient_exists"]),
        },
        "all_assertions_pass": True,
        "limits": ["Finite exhaustive evidence supports but does not replace the general proofs.",
                   "Only constant observations or those factoring through the specified protected overlap are covered; extra restrictions are not covered.",
                   "The walking-arrow criterion is asserted only with identity transitions."]}
    write(args.output_dir, "two-view-relations.json", relations)
    write(args.output_dir, "three-view-relations.json", cube)
    write(args.output_dir, "repeated-fiber-cases.json", repeated)
    write(args.output_dir, "arrow-cases.json", arrows)
    write(args.output_dir, "protected-overlap-cases.json", overlaps)
    write(args.output_dir, "results.json", totals)
    print(json.dumps({"all_assertions_pass": True,
                      "two_view_relations": len(relations), "three_view_relations": len(cube),
                      "repeated_fiber_cases": len(repeated), "arrow_cases": len(arrows),
                      "protected_overlap_cases": len(overlaps),
                      "full_search_congruence_tuples": repeated_examined + arrow_examined + overlap_examined,
                      "explicit_process_examples": len(examples) + len(overlap_dynamic)}, indent=2))


if __name__ == "__main__":
    main()
