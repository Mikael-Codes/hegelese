# Exact finite reconstruction-demand checks

1 November 2026

`verify_reconstruction.py` is a standalone Python 3.10+ program using only the
standard library. It was run successfully with Python 3.14.7. From any working
directory, run:

```sh
python /path/to/verify_reconstruction.py
```

It writes `results.json` and five detailed case files beside the script. The
complete run takes about one second on the local machine; no network, GPU, or
external repository is used.

To write results into a separate directory, including a CI runner's temporary
directory, pass `--output-dir`:

```sh
python /path/to/verify_reconstruction.py --output-dir /path/to/temporary-results
```

The default output location is based on the script's path, not the working
directory. The override was also run from another working directory and its
six result files compared byte-for-byte with the default outputs.

The experiments treat a quotient as a tuple of equivalence relations on the
source and its views. Finer means less information lost: every equivalence
class refines the corresponding class in the other quotient. A universal
quotient must be finer than every feasible quotient, not merely have the
smallest numerical loss score or be one minimal element. The program lists
every minimal feasible tuple and separately tests whether the intersection of
all feasible tuples remains feasible.

## Exact coverage and outcomes

| Batch | Coverage | Cases | Cases with a universal quotient |
|---|---|---:|---:|
| Two independent views | Every nonempty relation in every grid of sizes 1–3 by 1–3, with both projections onto | 327 | 9 |
| Three independent views | Every subset of the 2×2×2 cube with all three projections onto | 193 | 1 |
| Repeated joint fibers | Every joint-map multiset with 1–4 source states and view sizes 1–3, both projections onto, up to permutation of source states | 194 | 25 |
| Walking arrow | Every map with source and target sizes 1–4, up to permutation of source states; identity transitions | 121 | 51 |
| Protected common overlap | Every full-projection subset of the eight-state fiber product of two four-state views over a two-state base | 49 | 1 |

In the first three batches, a universal quotient exists exactly when the
original joint map is onto the full Cartesian product. The nine universal
two-view relations are precisely the full rectangles, one for each grid
size. The universal three-view relation is the full cube. Repeated fibers do
not affect this criterion; when the joint map is onto, its kernel is the
source component of the universal quotient, while all views remain unchanged.

For the walking-arrow batch with identity transitions, a universal quotient
exists exactly when the arrow is onto or has a singleton image. This statement
is deliberately not applied to arbitrary process dynamics.

For the protected-overlap batch, both base maps are `[0,0,1,1]`. Endpoint
equivalences must refine these base maps, and reconstruction uses the fiber
product over the unchanged base. Exactly the full fiber-product relation has
a universal quotient. The other 48 cases have either two or four incomparable
minimal feasible quotients.

## How the searches check the mathematics

Partitions are generated as canonical restricted-growth strings; Bell counts
through five elements are checked. The larger relation batches enumerate all
endpoint partitions. For each choice, they compute every quotient tuple
actually hit by a source state and compare that set with the complete required
product. If coverage holds, the source equivalence is uniquely forced by the
requirement that its comparison map be bijective.

A separate search for the repeated-fiber and walking-arrow batches explicitly
tries every source and endpoint equivalence tuple. It constructs quotient
maps, rejects failures of naturality, and checks injectivity and surjectivity
of the induced comparison map. This second search does not prescribe the
source equivalence from the endpoint equivalences. Both searches give exactly
the same feasible sets in all these cases.

The protected-overlap batch likewise checks every source equivalence and every
endpoint equivalence refining the base. These three independent full-search
batches examine respectively 36,042, 11,414, and 257,728 congruence tuples, for
305,184 in total. This count excludes the additional explicit process examples.
The proposed existence criteria are asserted only after feasible sets have
been computed; the criteria are not used to generate feasible quotients.

## Minimal counterexamples and actual transitions

The walking-arrow example has two source states mapping to distinct states
of a three-state target. The unused third target state can be merged with
either represented state. These choices yield two incomparable finest
bijective quotient arrows. Their intersection is the original non-bijective
arrow. Total object cardinality is five.

For a span with surjective legs, take two source states and two two-state
views, with joint image `{(0,0),(1,1)}`. Collapsing either view makes the source
comparison bijective; the two choices are incomparable. Their intersection
leaves both views unchanged and fails to cover the product. This example has
total object cardinality six. It remains a counterexample when the shared
input flips both source states and both view states.

For a connected image graph, take the three-corner relation
`{(0,0),(0,1),(1,0)}`. Again there are two incomparable finest quotients. A
shared input resetting both views and all source states to zero is a
nonidentity transition compatible with this relation. Total cardinality is
seven. Connectedness is explicitly checked in the relation enumeration.

These minima are recorded with their precise search families in `results.json`.
The small bounds also cover every smaller nonempty example in the respective
families: a nonunique arrow needs at least two represented target states and
one unused target state; a nonunique surjective two-view example needs both
views nontrivial, and a two-state source can only give a disconnected full-
projection image on two two-state views.

Dynamics can resolve an ambiguity in the walking-arrow example. Let the two
represented target states be fixed and send the unused third state to the
first. Only attachment to that first state remains compatible with the
transition. Full congruence enumeration then gives a unique finest quotient.
This demonstrates why the identity-transition arrow classification must not
be generalized without qualification.

Two further process examples swap the two protected base cells. For diagonal
fibers, this ties the choices in the two cells together and reduces four
minimal set quotients to two minimal process quotients; a universal quotient
still does not exist. The complete fiber product still has its universal
quotient under the same base-swapping dynamics.

All these examples admit compatible initial states: choose the first source
state and its displayed images as the initial states. They are finite
deterministic processes with one common input. No nonconstant observations
are protected in the independent-view and arrow batches. The overlap batch
protects its stated base. Additional protected observations can change which
quotients are feasible.

## Scope

These are exact finite checks, not a proof of the general classification or
a claim of priority for the underlying categorical ideas. The broader proofs
must justify the all-size and arbitrary-dynamics assertions separately.
The experiments do establish concrete counterexamples to unrestricted
canonical least-loss reconstruction and distinguish ordinary minimal choices
from a universal quotient. They do not modify or extend the Hegelese language
or its deployed checker.
