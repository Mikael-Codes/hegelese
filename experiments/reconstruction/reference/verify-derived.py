"""Exact F_2 verification of derived cut reconstruction on finite subset posets.

Run: python outputs/verify-derived.py
No third-party dependencies. Writes outputs/derived-checks.json by default.
Normalized Roos cochains use the value at the last object of each chain.
"""
from itertools import product
from math import comb
from pathlib import Path
import json


def cuts(t):
    """Represent each nontrivial cut by its block avoiding min(t)."""
    root = t & -t
    return [a for a in range(1, t + 1) if a & ~t == 0 and a & root == 0]


def restrict_cut(a, t):
    a &= t
    if not a or a == t:
        return None
    return a ^ t if a & (t & -t) else a


def gf2_rank(columns):
    pivots = {}
    for v in columns:
        while v:
            p = v.bit_length() - 1
            if p in pivots:
                v ^= pivots[p]
            else:
                pivots[p] = v
                break
    return len(pivots)


def compose_zero(d1, d2):
    for col in d1:
        out = 0
        while col:
            bit = col & -col
            out ^= d2[bit.bit_length() - 1]
            col ^= bit
        if out:
            return False
    return True


def augmentation_basis(t, d):
    return [a for a in cuts(t) if a.bit_count() < d]


def restrict_augmentation(a, old_t, t, d):
    """Pull back a rooted augmentation monomial and truncate at I^d."""
    root = t & -t
    poly = {0}
    for i in range(old_t.bit_length()):
        if not (a >> i) & 1:
            continue
        if not (t >> i) & 1:
            return set()
        v = (1 << i) if (1 << i) != root else (t ^ root)
        factor = [u for u in range(1, v + 1) if u & ~v == 0 and u.bit_count() < d]
        product = set()
        for u in poly:
            for w in factor:
                if u & w or (u | w).bit_count() >= d:
                    continue
                z = u | w
                if z in product:
                    product.remove(z)
                else:
                    product.add(z)
        poly = product
    return poly


def pullback_basis(a, fmap, t, d=None):
    root = t & -t
    def preimage(mask):
        v = sum(1 << i for i, j in enumerate(fmap) if t & (1 << i) and mask & (1 << j))
        return v ^ t if v & root else v
    if d is None:
        v = preimage(a)
        return {v} if v else set()
    poly = {0}
    for i in range(a.bit_length()):
        if not (a >> i) & 1:
            continue
        v = preimage(1 << i)
        factor = [u for u in range(1, v + 1) if u & ~v == 0 and u.bit_count() < d]
        terms = set()
        for u in poly:
            for w in factor:
                if u & w or (u | w).bit_count() >= d:
                    continue
                z = u | w
                if z in terms:
                    terms.remove(z)
                else:
                    terms.add(z)
        poly = terms
    return poly


def build(n, r, d=None):
    objects = [t for t in range(1, 1 << n) if t.bit_count() <= r]
    cut_bases = {t: cuts(t) if d is None else augmentation_basis(t, d) for t in objects}
    # Chains ending in a singleton have coefficient space zero and can be omitted.
    nonzero = [t for t in objects if t.bit_count() >= 2]
    chain_levels = [[(t,) for t in nonzero]]
    while chain_levels[-1]:
        nxt = [c + (u,) for c in chain_levels[-1] for u in nonzero
               if u != c[-1] and u & ~c[-1] == 0]
        if not nxt:
            break
        chain_levels.append(nxt)
    basis = [[(c, a) for c in chains for a in cut_bases[c[-1]]]
             for chains in chain_levels]
    if not basis:
        basis = [[]]
    index = [{x: i for i, x in enumerate(b)} for b in basis]
    differentials = []
    for q in range(len(basis) - 1):
        cols = [0] * len(basis[q])
        for row, (chain, a) in enumerate(basis[q + 1]):
            # Omit any object except the last: coefficient object is unchanged.
            for j in range(q + 1):
                short = chain[:j] + chain[j + 1:]
                cols[index[q][short, a]] ^= 1 << row
            # Omitting the last requires the coefficient restriction map.
            short = chain[:-1]
            for b in cut_bases[short[-1]]:
                image = ({restrict_cut(b, chain[-1])} if d is None
                         else restrict_augmentation(b, short[-1], chain[-1], d))
                if a in image:
                    cols[index[q][short, b]] ^= 1 << row
        differentials.append(cols)
    return basis, differentials


def check(n, r, d=None):
    basis, diffs = build(n, r, d)
    ranks = [gf2_rank(d) for d in diffs]
    cohom = [len(b) - (ranks[q] if q < len(ranks) else 0)
             - (ranks[q - 1] if q else 0) for q, b in enumerate(basis)]
    while len(cohom) < r:
        cohom.append(0)
    if r == 1:
        expected = [0] * r
    elif r >= n:
        dimension = (2 ** (n - 1) - 1 if d is None
                     else sum(comb(n - 1, j) for j in range(1, min(d, n))))
        expected = [dimension] + [0] * (r - 1)
    else:
        c = comb(n - 1, r)
        if d is None or d >= r:
            expected = [sum(comb(n - 1, j) for j in range(1, r + 1))]
        else:
            expected = [sum(comb(n - 1, j) for j in range(1, min(d, n)))]
        start = 1 if d is None else max(1, r - d)
        expected += [c if start <= q <= r - 2 else 0 for q in range(1, r)]
    d_squared_zero = all(compose_zero(diffs[q], diffs[q + 1])
                         for q in range(len(diffs) - 1))
    assert d_squared_zero, (n, r, "d^2 != 0")
    assert cohom == expected, (n, r, cohom, expected)
    return {"n": n, "r": r, "augmentation_cutoff_d": d, "cochain_dimensions": [len(b) for b in basis],
            "differential_ranks": ranks, "cohomology_dimensions": cohom,
            "predicted_dimensions": expected, "d_squared_zero": d_squared_zero,
            "pass": True}


def apply_columns(columns, v):
    out = 0
    while v:
        bit = v & -v
        out ^= columns[bit.bit_length() - 1]
        v ^= bit
    return out


def check_naturality():
    """Check cochain maps for every function between sets of sizes at most three."""
    cache = {(n, r, d): build(n, r, d)
             for n in range(1, 4) for r in range(1, 4) for d in (None, 2, 3)}
    checked = 0
    for n in range(1, 4):
        for m in range(1, 4):
            for fmap in product(range(m), repeat=n):
                def im(t):
                    return sum(1 << j for j in {fmap[i] for i in range(n) if t & (1 << i)})
                for r in range(1, 4):
                    for d in (None, 2, 3):
                        b_src, d_src = cache[m, r, d]
                        b_tgt, d_tgt = cache[n, r, d]
                        length = max(len(b_src), len(b_tgt))
                        src = b_src + [[]] * (length - len(b_src))
                        tgt = b_tgt + [[]] * (length - len(b_tgt))
                        maps = []
                        for q in range(length):
                            src_index = {x: i for i, x in enumerate(src[q])}
                            tgt_index = {x: i for i, x in enumerate(tgt[q])}
                            cols = [0] * len(src[q])
                            for chain in {c for c, _ in tgt[q]}:
                                image_chain = tuple(im(t) for t in chain)
                                if len(set(image_chain)) != len(chain):
                                    continue
                                cb = cuts(image_chain[-1]) if d is None else augmentation_basis(image_chain[-1], d)
                                for a in cb:
                                    col = src_index[image_chain, a]
                                    for v in pullback_basis(a, fmap, chain[-1], d):
                                        cols[col] ^= 1 << tgt_index[chain, v]
                            maps.append(cols)
                        for q in range(length - 1):
                            ds = d_src[q] if q < len(d_src) else [0] * len(src[q])
                            dt = d_tgt[q] if q < len(d_tgt) else [0] * len(tgt[q])
                            for j in range(len(src[q])):
                                assert apply_columns(dt, maps[q][j]) == apply_columns(maps[q + 1], ds[j]), (n, m, fmap, r, d, q)
                        checked += 1
    return {"all_set_maps_between_sizes": [1, 2, 3], "cutoffs": [1, 2, 3],
            "modules": ["V", "F_2", "F_3"], "cases": checked,
            "d_commutes_with_pullback": True}


def main():
    results = [check(n, r) for n in range(1, 6) for r in range(1, n + 1)]
    results += [check(n, r, d) for n in range(2, 6)
                for r in range(1, n + 1) for d in range(2, n + 1)]
    out = {"field": "F_2", "method": "normalized Roos cochain complex; exact bitset Gaussian elimination",
           "cases": results, "naturality": check_naturality(), "all_pass": all(x["pass"] for x in results)}
    target = Path(__file__).with_name("derived-checks.json")
    target.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(results), "naturality_cases": out["naturality"]["cases"],
                      "all_pass": out["all_pass"], "output": str(target)}))


if __name__ == "__main__":
    main()
