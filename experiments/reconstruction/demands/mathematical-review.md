# Independent review of the reconstruction-demand results

1 November 2026. Reviewed `positive-theory.md` alongside the walking-arrow counterexample in `counterexample-proof.md`. This is an internal mathematical audit, not a claim of novelty or external peer review.

## Verdict

No mathematical blocker found. The general sufficient condition, independent-view criterion, and protected-common-overlap criterion are valid with their stated hypotheses. The walking-arrow example is a genuine right-Kan reconstruction counterexample, not a state-count surrogate. The two notes correctly limit the more complete arbitrary-arrow classification to trivial dynamics.

## Checks of the positive theory

- The coefficient category is explicitly finite **pointed transition systems** with fixed input alphabet, not finite machines with an arbitrary fixed observation interface built into every morphism. This distinction matters. In the specified category, finite limits really are computed on state sets; initial states make equalizers and the relevant limits nonempty. Observations are treated separately under explicit restrictions.
- For a full inclusion, restriction followed by right Kan extension is an idempotent reflection onto reconstructed diagrams. If its unit is objectwise surjective, it is an admissible quotient and has the required factorization property. The arrows point in the correct direction, and any factor map to a surjective quotient is itself surjective.
- In the independent-view theorem, individual surjectivity of every view is exactly what makes each axis witness a quotient. Retaining one view and replacing the others by the terminal process commutes with every input transition and preserves the initial state. A universal quotient must therefore retain every view isomorphically, forcing joint coverage.
- In the common-overlap theorem, the quotient of each other view to the protected overlap is admissible because its structure map is assumed surjective. The global axis map is the surjective selected view. The common-overlap equations ensure naturality. The resulting fiber product is the retained view itself. Observations that factor through the protected overlap remain preserved; arbitrary additional observations are expressly outside this necessity argument.
- The counting criteria count **distinct tuples**, not source states with multiplicities. Since realized tuples already lie in the indicated product or fiber product, the displayed equalities are equivalent to coverage.
- The dynamic examples are valid: simultaneous swapping preserves the diagonal relation, and resetting all coordinates to zero preserves the three-corner relation. Surjectivity of individual views alone does not produce missing joint states.
- The uniqueness criterion for identity-dynamics arrows must not be generalized to arbitrary dynamics. The supplied example with an extra state transitioning to one represented fixed state correctly shows how dynamics can force a unique attachment.

The elementary counterexample uses five states in total, and the minimality claim is appropriately restricted to the walking-arrow category with nonempty values. No unsupported global minimality assertion is made.

## A further consequence available in the stated view shapes

The exact view theorems can additionally identify the requested common-refinement boundary. Under their existing hypotheses, the following are equivalent:

1. Joint coverage holds.
2. A universal least-loss reconstructed quotient exists.
3. The reconstructed quotient kernels are closed under intersections of nonempty families.

For the extra implication from coverage to closure, let \(R_i^\alpha\) be the view kernels of a family of local quotients. Locality and naturality determine each global kernel as equality of the quotient-view tuple. Consequently its intersection is equality modulo \(R_i=\bigcap_\alpha R_i^\alpha\) in every coordinate. Full original coverage surjects onto the product of the view quotients \(A_i/R_i\), or onto their fiber product over the unchanged protected overlap. Thus the intersection quotient is again local. There are only finitely many distinct kernels on these fixed finite sets, so no infinite-size issue is hidden here.

Conversely, intersecting all axis-witness kernels retains every original view and identifies global states only when their joint views agree. Its quotient has global state set equal to the realized tuple relation. If coverage fails, that intersection quotient is not local. Hence closure fails.

This consequence uses the special view shapes and admissible witness quotients. It is not a theorem about arbitrary diagram categories or arbitrary additional observation and authorization policies.

## Scope and attribution

The notes distinguish classical lossless-join, congruence, reflection, and quotient-factorization facts from the proposed interface that reports necessity, ambiguity, and infeasibility. Nothing in this mathematical review certifies a new theorem relative to the literature. The separate literature comparisons remain necessary.

The results support conditional necessity: fixed diagrams, admissible quotients, and retained interfaces determine what can or cannot be preserved. They do not authorize a loss, derive the user's requirements, or show that every reconstruction demand selects one successor.
