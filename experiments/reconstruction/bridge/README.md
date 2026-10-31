# From checked change to necessary loss

Research connection and executable experiments for Hegelese, 31 October 2026.

The [version 2 binary-cut preprint](https://autio.github.io/ai-science/binary-cut-reconstruction/) is published. Its strongest connection to Hegelese is a precise change in the question: **from finding what a proposed transformation loses to determining what every transformation meeting a stated demand must lose.** The experiments here make that connection concrete. They are separate research tools, not changes to the Hegelese language or its acceptance rules.

The repository review uses Hegelese commit [`3199a7f`](https://github.com/Mikael-Codes/hegelese/tree/3199a7fd4d83ab061c5d445d28be6c07edb0d61e). Mathematical originality remains open: the preprint's possible contribution is its specific reconstruction calculation. Congruences, quotient factorization, automaton minimization, and the elementary results below are established mathematics, not additional novelty claims.

## 1. What the current implementation already provides

Hegelese checks a map between two finite deterministic processes. It verifies the initial state, every state/input transition, and retained observations. It also computes the map's fibers, exposing merged states even if the proposer did not name an observation distinguishing them. Its optional lineage protocol makes those findings constrain subsequent attempts against the same source and request. [Implementation](https://github.com/Mikael-Codes/hegelese/blob/3199a7fd4d83ab061c5d445d28be6c07edb0d61e/hegelese.py); [lineage protocol](https://github.com/Mikael-Codes/hegelese/blob/3199a7fd4d83ab061c5d445d28be6c07edb0d61e/LINEAGE.md).

This is already a substantive connection to the research: preservation is a relation that must be checked, and loss is mathematical content rather than explanatory prose. What the checker does not establish is that its particular losses were necessary, that no better admissible representation exists, or that the caller should authorize a loss. These questions require different evidence.

## 2. A real binary-cut example through the existing checker

Take four labels and work over the two-element field. The augmentation ideal J has seven independent coordinates, indexed by the nonempty subsets of three rooted generators. Treat its 128 vectors as process states. The seven inputs add the corresponding basis vector. Require preservation of the three degree-one coordinates; export exact state identity as an optional observation.

The adapter constructs three proposals and runs the unchanged, pinned Hegelese checker:

| Proposed target | Target states | Equations checked | State pairs merged | Hegelese result |
|---|---:|---:|---:|---|
| J, identity map | 128 | 1,281 | 0 | ExhaustivelyChecked |
| J/J³, discarding cubic information | 64 | 1,281 | 64 | ExhaustivelyChecked |
| J/J², retaining linear information | 8 | 1,281 | 960 | ExhaustivelyChecked |

All three preserve the required transitions and observations. A negative control that falsely claims J/J² also retains exact state identity is refuted, with 120 failed equations. These are actual checker results, not proposed outcomes. See [running instructions](RUNNING.md), [adapter](check_binary_cut_bridge.py), and the generated reports in `results/`.

Now impose the additional mathematical demand: reconstruct the entire natural diagram from probes with at most three labels, in ordinary sets (h=0). The preprint says that **J/J² is the largest qualifying natural linear quotient**. J/J³ still retains too much for that demand: at four labels its comparison has a one-dimensional cokernel. J itself has both a one-dimensional kernel and a one-dimensional cokernel there.

A separate exact calculation constructs the restriction matrices and compatibility equations at four labels. It confirms these failures directly:

| Diagram | Source dimension | Compatible-data dimension | Comparison rank | Kernel / cokernel dimensions |
|---|---:|---:|---:|---|
| J | 7 | 7 | 6 | 1 / 1 |
| J/J³ | 6 | 7 | 6 | 0 / 1 |
| J/J² | 3 | 3 | 3 | 0 / 0 |

All three have a one-dimensional first derived reconstruction group at this cutoff. Thus even the successful ordinary comparison does not establish the analogous h=1 claim. See [the exact reconstruction results](results/reconstruction.json). This finite calculation supports the example; the uniform result rests on the published proof.

This is the useful distinction. The ordinary checker approves all three preservation claims. The reconstruction theorem determines which quotient retains the most information while meeting a different, explicitly stated demand.

The 128 process states are vectors attached to four labels. The probe bound of three counts labels, not process states, execution steps, tests, or revisions. The uniform theorem concerns characteristic-two linear diagrams and naturality under **all** finite-set maps. One finite process run does not verify those hypotheses or prove the uniform theorem. The adapter's basis and transition alphabet are coordinate choices for this experiment.

In general, for h≥0 and r≥h+3, the theorem gives

\[
K(A,h)\text{ reconstructs from probes of size at most }r
\quad\Longleftrightarrow\quad
J^{r-h-1}\subseteq\ker(J\twoheadrightarrow A).
\]

Every qualifying quotient therefore factors uniquely through J/J^(r−h−1). This is the sense in which the loss is forced. The h parameter is homotopy degree; Hegelese currently has no such higher semantic layer.

There is also a useful observation-level obstruction. A required linear observation can survive a qualifying quotient only if it vanishes on J^(r−h−1). In the preprint's dual Boolean description this means degree at most r−h−2. If it fails this condition, the observation and the reconstruction demand are incompatible within the specified class. This is an immediate corollary, not a separate novelty claim.

## 3. A practical generalization—and a small obstruction

For a fixed deterministic process, a quotient is specified by an equivalence relation R on its states. It supports well-defined transitions exactly when

\[
s\,R\,t\Longrightarrow\delta(s,i)\,R\,\delta(t,i)
\]

for every input i. Retained observations must be constant on each equivalence class. These are ordinary transition congruences. Their established theoretical setting includes automata and coalgebra; see [Rutten, *Universal coalgebra: a theory of systems*](https://ir.cwi.nl/pub/48/).

Fix an extra demand and let C be the nonempty family of feasible congruences. The intersection R* of all members of C identifies precisely the pairs merged by **every** feasible quotient. A universal least-loss quotient exists if and only if R* itself meets the extra demand. Proof: intersections preserve both transition compatibility and observation constancy; if R* is feasible it refines every feasible quotient, and any feasible least relation must equal that intersection. This is elementary order theory.

The [partition experiment](quotient_frontier.py) checks every partition in three small examples:

| Process and demand | Result |
|---|---|
| Four-phase cycle, retain parity, at most two target states | The parity quotient is the unique least-loss solution. Merging 0 with 2 and 1 with 3 is forced. |
| Three self-looping states, constant observations, at most two target states | Three incomparable finest quotients exist, one for each choice of merged pair. Some loss is unavoidable, but no particular pair-loss is forced. |
| Three-phase cycle, retain parity, at most two target states | No quotient satisfies the demand. The apparent parity identification conflicts with the wraparound transition. |

The second example prevents a misleading language feature: a size limit does not in general determine one necessary successor. The checker should expose the alternatives. It must also treat an empty feasible family separately; a vacuous intersection is not a legitimate proof that every loss is necessary.

Ordinary behavioral minimization usually asks for the coarsest behavior-preserving quotient, maximizing compression. The question here asks for the finest quotient meeting an additional demand, minimizing loss. Reusing the word “minimal” without specifying this order would hide a substantive difference.

A tractable alternative demand is a supplied set of required identifications. Close those identifications under equivalence and transitions. This produces the least transition congruence containing them. If a required observation varies on one of its classes, there is an obstruction; otherwise its quotient is the canonical least-loss solution. That construction is also classical. Its value here would be an executable contract: return a canonical quotient or an explicit reason the requested identifications cannot preserve the observations.

## 4. The most immediate connection to revision history

The current lineage system revises against the original source. It can repair an earlier merger because that source remains available. A succession of installed representations presents a different problem.

If a change actually maps S to T by q, and all later processing is a function g of the current T state alone, then

\[
\ker(q)\subseteq\ker(g\circ q).
\]

A later deterministic operation cannot recover a distinction already erased. A record that a loss occurred does not restore the lost state value. Recovery requires retaining extra information, consulting the original state, or acquiring new information from outside.

For a finite map q, the smallest auxiliary state set R allowing an injective encoding s↦(q(s),r(s)) has cardinality max_t |q⁻¹(t)|. Each fiber needs distinct residual values, and the same residual labels can be reused across fibers. Thus the four-phase parity quotient needs one extra bit for exact recovery. The binary-cut 128-to-8 quotient needs four extra bits: each fiber has 16 elements. Exact recovery then retains all seven bits in total. This storage bound allows residual updates to depend jointly on the quotient state, residual, and input; requiring an independently evolving residual process is a stronger condition.

This elementary fact gives the planned cross-source lineage protocol a concrete design requirement: state what information survives each installed change and where any claimed repair obtains its information. It also explains why retaining a source program's text is different from retaining its former runtime state.

There is a precise option between retaining everything and accepting an unmet new requirement. Assume q is a transition-preserving process quotient. Let B identify source states with the same newly required observations after every input word, including the empty word. The quotient by ker(q)∩B is the coarsest refinement of q that preserves those behaviors. Its extra state must be retained or acquired; it cannot be reconstructed from q alone after the distinctions have been discarded. This gives a useful baseline for migration with only the additional information needed.

## 5. Why this matters for the Hegelian direction

The strongest connection is the determination of a successor by the content and limits of the earlier situation. A report that “this proposal failed” is weaker than an obstruction that explains why an entire class of proposals fails. A chosen compression is weaker than a universal statement showing exactly what must be relinquished under the stated demand.

This is a mathematical interpretation motivated by Hegel, particularly the insistence that development take its determinations from the subject matter and that a negative result retain determinate content. It is not an identification of an optimization algorithm with Hegel's method. The caller still supplies the process, observations, allowed changes, and demand. A mathematical proof of unavoidable loss does not authorize that loss. [*Science of Logic*, Absolute Idea, §§1789 and 1795–1804](https://www.marxists.org/reference/archive/hegel/works/hl/hlabsolu.htm).

The earlier [*Determinate Preservation* work](https://autio.github.io/ai-science/determinate-preservation/) supplies a complementary question: which observations suffice for the chosen meaning of preservation? Its distinction between changing the observations and changing the generated model matters for Hegelese's open problem of legitimate requirement revision. It does not provide a ready-made migration protocol. The [current revision guarantees](https://github.com/Mikael-Codes/hegelese/blob/3199a7fd4d83ab061c5d445d28be6c07edb0d61e/docs/revision-guarantees.md) correctly leave that problem open.

## 6. The next contribution worth pursuing

Start with a library extension to the present checker, using the exhaustive finite examples here as reference cases. Given a protected request and an explicit candidate class, it should report one of: a unique least-loss quotient with factorization evidence; multiple incomparable alternatives with witnesses; infeasibility with an obstruction; or an unfinished search. Ordinary preservation, necessity, and caller authorization should remain separate results.

The mathematical research question is sharper than “apply category theory to Hegelese”: **which practically useful reconstruction demands on process diagrams admit a universal least-loss quotient, and which fail because common refinements no longer meet the demand?** The binary-cut theorem supplies one solved family and an exact tradeoff. The three-state example supplies an immediate boundary. Any generalization would need its own proof and priority search. Existing work on optimal abstractions and completeness is an essential comparator, including [Giacobazzi, Ranzato and Scozzari, *Making Abstract Interpretations Complete*](https://www.sci.unich.it/~scozzari/paper/JACM00.pdf); the generic ambition to construct a best abstraction is already established.

For engineering evaluation, compare this extension with a conventional protected requirements ledger and congruence checker on the same tasks. The potential contribution is useful certificates of forced loss, ambiguity, and impossibility, together with accountable revision. No new language necessity, AI productivity improvement, or general semantic verification is established by the present experiments.
