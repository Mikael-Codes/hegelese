# Reconstruction and necessary loss

1 November 2026 · Petri Mikael Autio · Research experiments for Hegelese

Hegelese checks preservation under a supplied change. These experiments ask a further question: **which losses are forced by a reconstruction demand, and when does that demand fail to select one least-loss successor?**

The [public companion page](https://autio.github.io/ai-science/hegelese-reconstruction/) explains the results. This directory is intended to live at `experiments/reconstruction/` in the Hegelese repository. It contains research proofs, finite reference implementations, and recorded checks. It adds no language syntax and does not change the existing checker's acceptance rules.

## Results

The [binary-cut connection](bridge/README.md) turns the [published reconstruction preprint](https://autio.github.io/ai-science/binary-cut-reconstruction/) into a concrete example through Hegelese's unchanged checker. Three maps preserve the same observations, while the separate mathematical reconstruction demand distinguishes them. The preprint's possible originality concerns its exact modular calculation; priority remains open.

The [follow-up theorem](demands/positive-theory.md) answers the next research question for finite processes with individually surjective independent views, and for views over one protected common overlap:

> Joint coverage, existence of a universal least-loss reconstructed quotient, and closure of feasible quotient kernels under common-refinement intersections are equivalent.

Here joint coverage means that every compatible tuple of local view states is realized by a global state. The universal quotient, when it exists, preserves all view states and merges exactly global states with identical joint views. When coverage fails, explicit competing quotients obstruct a universal choice. Additional protected observations that exclude those witnesses require a separate analysis.

The [walking-arrow analysis](demands/counterexample-proof.md) gives a genuine right-Kan reconstruction counterexample with two source states and three observed states. It also completely classifies this shape for identity transitions, including compatible retained observations.

These follow-up results use classical lossless joins, congruences, and reflection arguments. They are useful exact answers for the proposed interface, with direct proofs and explicit boundaries; they are **not claimed as newly discovered mathematics relative to the literature**. The [internal mathematical review](demands/mathematical-review.md) checks validity, not priority or external peer acceptance.

## Run from the Hegelese repository root

Requires Python 3.10 or newer, with no third-party packages.

```sh
python experiments/reconstruction/bridge/check_binary_cut_bridge.py --checker hegelese.py --reconstruction-checker experiments/reconstruction/reference/verify-derived.py
python experiments/reconstruction/bridge/quotient_frontier.py
python experiments/reconstruction/demands/verify_reconstruction.py
```

The bridge checks the exact SHA-256 of the inspected Hegelese checker at commit `3199a7fd4d83ab061c5d445d28be6c07edb0d61e`. A changed checker requires a fresh review and intentional pin update. A historical reproduction can use the pinned upstream file instead of the current checkout's file. See [bridge running instructions](bridge/RUNNING.md).

For an extracted standalone archive, replace `experiments/reconstruction/` with the extraction path and supply the inspected `hegelese.py` explicitly. Its [pinned upstream source](https://github.com/Mikael-Codes/hegelese/blob/3199a7fd4d83ab061c5d445d28be6c07edb0d61e/hegelese.py) is not duplicated here. The mathematical reconstruction verifier is included under [reference](reference/README.md).

All scripts can direct generated results to temporary locations: `--output-dir` for the bridge and demand verifier, and `--output` for the partition experiment. Their defaults write beside the scripts, independently of the working directory.

## Evidence

- The real checker accepts the three positive binary-cut maps after 1,281 equations each. A false exact-state preservation claim is refuted by 120 failures.
- Separate exact matrices at four labels give reconstruction kernel/cokernel dimensions `(1,1)`, `(0,1)`, and `(0,0)` for J, J/J³, and J/J².
- The first process experiment enumerates all 25 partitions across three examples with unique, ambiguous, and infeasible outcomes.
- The follow-up enumerates 327 two-view relations, 193 three-view relations, 194 repeated-fiber cases, 121 arrow maps up to source permutation, and 49 protected-overlap cases. Independent full searches examine 305,184 congruence tuples; six additional examples have explicitly specified process dynamics.

All recorded assertions pass. [Exact coverage and limitations](demands/COMPUTATIONAL-CHECKS.md), [summary results](demands/results.json), and the detailed JSON case files describe what was enumerated. The finite computations support the proofs; they do not replace the all-size arguments.

## What remains open

The proved criteria do not cover arbitrary overlap diagrams or arbitrary protected observations and loss-authorizations. The next problem is to determine when those constraints preserve closure under common refinements, and to return a checked quotient, explicit ambiguity, infeasibility, or an unfinished result accordingly. No comparative AI benefit or need for new language syntax has been established.

The Hegelian motivation is conditional determination: make the limitations of a representation consequential to its successor. The source, admissible changes, observations, and demand remain supplied choices. A proof that some loss is unavoidable does not authorize it.

AI assistants helped develop the arguments, code, literature comparison, and separate internal critiques under the author's direction. This is a public research record, with external review open.
