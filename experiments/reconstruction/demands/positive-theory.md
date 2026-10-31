# Universal least-loss quotients for finite process views

1 November 2026. Research note. The statements below are proved directly; their categorical and database mechanisms are classical. Novelty of their formulation as a reconstruction-demand interface is not established.

## Result and scope

For a finite process observed through individually surjective views, allowing those views themselves to be quotiented does **not** generally create a universal least-loss reconstructed quotient. There is an exact criterion for two useful observation shapes:

> For independent views, or views over one protected common overlap, a universal least-loss reconstructed quotient exists if and only if every compatible tuple of view states is already realized by a source state.

When it exists, the quotient retains all the view states and identifies exactly source states with identical joint views. When coverage fails, the competing quotients that retain one view and collapse the others obstruct a universal choice. This is stronger than merely restating the intersection criterion: for this family it gives a finite test and explicit witnesses, without enumerating all congruences.

The result holds with arbitrary deterministic transitions and a distinguished initial state. It assumes no additional protected observation rules that would exclude the witness quotients; observations depending only on the protected overlap are permitted. It concerns ordinary finite processes, not homotopy reconstruction.

## 1. Processes, diagrams, and the order of loss

Fix a finite input alphabet \(I\). A finite process is a nonempty finite set \(P\), an initial state \(p_0\), and maps \(\delta_a:P\to P\) for \(a\in I\). A process homomorphism preserves the initial state and commutes with every \(\delta_a\). No reachability restriction is imposed: all declared states are in scope, as in the current Hegelese checker.

These processes form a category \(\mathsf{Proc}_I\). Its finite limits are computed on underlying sets, with coordinatewise transitions and the induced initial state. A bijective process homomorphism is an isomorphism. An objectwise surjective homomorphism is a quotient by its transition congruence.

For a finite diagram \(X:\mathcal C\to\mathsf{Proc}_I\), a quotient is an objectwise surjective natural map \(q:X\twoheadrightarrow Q\). Say that \(q\) loses no more information than \(q'\) when \(q'=f q\) for a natural map \(f\). Equivalently,

\[
\ker q_c\subseteq\ker q'_c\quad\text{for every object }c.
\]

A universal least-loss quotient in a specified class is a quotient \(u\) through which every quotient in that class factors. The factorization is unique because \(u\) is objectwise surjective. This order is opposite to seeking the smallest behavior-preserving automaton: here the quotient retains as many distinctions as the reconstruction demand permits.

Let \(i:\mathcal D\hookrightarrow\mathcal C\) be a full inclusion. Write

\[
T=\operatorname{Ran}_i i^*,\qquad \eta_X:X\to TX.
\]

A diagram is local, or reconstructed from \(\mathcal D\), when its unit is an isomorphism. All right Kan limits here are ordinary finite limits.

## 2. A general positive lemma from the adjunction

**Lemma 1.** If \(\eta_X\) is objectwise surjective, then it is the universal least-loss local quotient of \(X\).

**Proof.** Fullness of \(i\) implies that \(\operatorname{Ran}_i\) is fully faithful, so \(TX\) is local. For any map \(q:X\to Q\) with \(Q\) local, the restriction/right-Kan adjunction gives a unique factorization

\[
X\xrightarrow{\eta_X}TX\xrightarrow{\overline q}Q.
\]

If \(q\) is objectwise surjective, then \(\overline q\) is also objectwise surjective, since its image contains the image of \(q\). The hypothesis makes \(\eta_X\) itself an allowed quotient. Hence it is universal in the stated quotient class. \(\square\)

This is a standard reflection argument, not a new reflection theorem. Its hypothesis is substantive: a right-Kan unit can add missing compatible states and therefore fail to be a quotient. Factoring the unit through its image does not solve that problem in general, because the image need not be local.

Surjectivity of the unit is not necessary for arbitrary observation categories. For the single-arrow diagram \(\{0\}\hookrightarrow\{0,1\}\), with self-loop transitions, locality requires that the arrow become an isomorphism. The unique local quotient collapses the target to one point. Its right-Kan unit is not surjective at the source. The converse in the next theorem therefore depends on the view shape and the available witness quotients.

## 3. Independent views: an exact classification

Take a star-shaped category with one global object \(g\), view objects \(1,\ldots,m\), and arrows \(g\to i\), where \(m\ge1\). Let \(\mathcal D\) consist of the view objects. A diagram is a family

\[
p_i:P\longrightarrow A_i.
\]

Its right Kan completion replaces the global process by \(\prod_i A_i\), and the unit at the global object is the joint view

\[
p=(p_1,\ldots,p_m):P\longrightarrow\prod_i A_i.
\]

Assume each \(p_i\) is surjective. Quotients may change both the global process and every view. Reconstruction requires the quotient's global process to be the product of its quotient views. There are no additional protected observations beyond constant ones.

**Theorem 2.** The following are equivalent:

1. \(X\) has a universal least-loss local quotient.
2. The joint map \(p\) is surjective.
3. The relation of realized view tuples is the full product: \(p(P)=\prod_i A_i\).

When these conditions hold, the universal quotient has unchanged view processes and global process \(\prod_i A_i\); its global kernel is \(\bigcap_i\ker p_i\).

**Proof of sufficiency.** All view components of the unit are identities, and the global component is surjective by condition 2. Lemma 1 applies. In concrete terms, for any local quotient with view maps \(q_i:A_i\twoheadrightarrow B_i\), its global map is, after the local identification, the composite

\[
P\xrightarrow p\prod_i A_i\xrightarrow{\prod_i q_i}\prod_i B_i.
\]

This is the unique required factorization.

**Proof of necessity.** For each \(j\), form an axis quotient \(Q^{(j)}\): retain view \(A_j\), replace every other view by the terminal one-state process, and take the global process to be \(A_j\). Its global quotient map is \(p_j\). This is objectwise surjective by hypothesis, and it is local. All its maps preserve initial states and transitions, for every input.

Suppose \(u:X\twoheadrightarrow U\) is universal. Since the \(j\)-th view component of \(Q^{(j)}\) is the identity on \(A_j\), factorization through \(u\) implies that \(u_j\) has a left inverse. It is also surjective, so \(u_j\) is an isomorphism. This holds for every \(j\).

Locality now identifies \(U_g\) with \(\prod_j A_j\), and naturality identifies \(u_g\) with the joint map \(p\). Since \(u_g\) is surjective, \(p\) must be surjective. \(\square\)

The necessity argument also proves uniqueness up to the unique isomorphism of specified quotients. It does not rely on choosing or comparing numeric loss scores.

## 4. Compatible views over a protected overlap

The preceding result has a direct fiber-product extension. Fix a finite process \(C\), and a commuting family

\[
P\xrightarrow{p_i}A_i\xrightarrow{a_i}C,
\qquad a_i p_i=c\text{ independent of }i.
\]

Assume all \(p_i\) and \(a_i\) are surjective. The observation category consists of the \(A_i\), \(C\), and arrows \(A_i\to C\); the global object maps to all of them. Keep \(C\) fixed, but permit objectwise surjective quotients of \(P\) and the \(A_i\) over \(C\). Locality demands

\[
Q_g\cong B_1\times_C\cdots\times_C B_m.
\]

**Theorem 3.** A universal least-loss local quotient over \(C\) exists if and only if

\[
p:P\longrightarrow A_1\times_C\cdots\times_C A_m
\]

is surjective. When it exists it leaves every \(A_i\) and \(C\) unchanged and identifies exactly states with equal joint views.

**Proof.** Surjectivity makes the unit an allowed quotient over \(C\), so Lemma 1 proves sufficiency. For necessity, the \(j\)-th axis quotient retains \(A_j\), replaces every other \(A_i\) by \(C\) using \(a_i\), and has global process \(A_j\). It is local because

\[
A_j\times_C C\times_C\cdots\times_C C\cong A_j.
\]

Its quotient components are surjective, and its global map is \(p_j\). Universality therefore forces every view map of the purported least-loss quotient to be an isomorphism, exactly as in Theorem 2. Its global surjectivity then forces the displayed joint map to be surjective. \(\square\)

All observations obtained from \(C\) remain protected in every witness quotient. Thus the theorem accommodates a genuine retained semantic interface rather than requiring every observation to be constant. Additional requirements that exclude the axis witnesses invalidate this particular necessity argument and must be analyzed separately.

The theorem describes conditional independence of the view coordinates over \(C\), in the purely relational sense of all compatible combinations being realized. It makes no probabilistic independence assertion.

**Corollary 4 (common refinements).** Under the hypotheses of either Theorem 2 or Theorem 3, the following are equivalent: joint coverage; existence of a universal least-loss local quotient; and closure of the feasible local quotient kernels under intersections of nonempty families.

**Proof.** Suppose coverage holds, and let \(q^\alpha\) be a nonempty family of local quotients. Write \(R_i^\alpha=\ker q_i^\alpha\) for its view kernels. Locality implies that its global kernel is

\[
K^\alpha=\bigcap_i(p_i\times p_i)^{-1}(R_i^\alpha).
\]

Set \(R_i=\bigcap_\alpha R_i^\alpha\). Interchanging intersections shows that \(\bigcap_\alpha K^\alpha=\bigcap_i(p_i\times p_i)^{-1}(R_i)\). The resulting common-refinement quotient therefore injects into the product, or fiber product over \(C\), of the view quotients \(A_i/R_i\). It also surjects onto that matching process: lift each quotient coordinate to \(A_i\), then use original joint coverage. In the common-overlap case the lifts stay over the prescribed element of \(C\), because every \(R_i\) lies in \(\ker a_i\). The joint map is consequently an isomorphism of processes, so the common refinement is local.

Conversely, intersect the kernels of all axis quotients used above. Every view kernel becomes the diagonal, while the global kernel is \(\bigcap_i\ker p_i\). If closure holds, this image-of-the-joint-view diagram must be local, which says precisely that the original joint view covers the full matching process. \(\square\)

Thus, in these particular shapes, the general common-refinement criterion reduces exactly to a lossless-join test. For arbitrary diagram shapes or protected requirements, this reduction is not established here.

## 5. Finite certificates and failure modes

The criterion can be checked without listing process congruences. Compute the set \(E=p(P)\) of distinct joint tuples. In the independent case, coverage holds exactly when

\[
|E|=\prod_i|A_i|.
\]

In the common-overlap case, partition tuples and view states by \(c\in C\). Coverage holds exactly when, for every \(c\),

\[
|E_c|=\prod_i|a_i^{-1}(c)|.
\]

Repeated global states with the same tuple count once. Equality of these counts is sufficient because \(E\) is already a subset of the relevant product or fiber product. A failure can be exhibited by one missing compatible tuple together with the axis quotients from the proof. The tuple witnesses the non-surjective unit; the axis quotients certify that every hypothetical universal quotient would have to retain all view coordinates.

For two binary views, the diagonal relation \(E=\{(0,0),(1,1)\}\) has surjective individual views but fails coverage. Retaining the first axis and collapsing the second is admissible, as is the reverse. Their common refinement retains the missing correlation and is not local. This remains a process counterexample with self-loops or with a simultaneous swap of both coordinates.

Even connectedness of the bipartite view relation is insufficient: \(\{(0,0),(0,1),(1,0)\}\) is connected but misses \((1,1)\). A reset-to-zero transition makes it a finite process with a nonidentity transition and the same obstruction.

Individual surjectivity cannot silently be dropped. Extra unused view states can require arbitrary attachments or further identifications. The general single-arrow counterexample with inclusion of two fixed states into three fixed states illustrates this. Conversely, dynamics can sometimes force a unique attachment: include fixed states \(a,b\) into \(\{a,b,c\}\) with \(\delta(c)=a\). The unique least-loss local quotient merges \(c\) with \(a\). Thus the set-theoretic classification of arbitrary arrows should not be asserted unchanged for all processes.

When coverage fails, feasible quotients still exist, but their axis witnesses have a nonlocal common refinement. Requiring a chosen state-count cap or a chosen extra loss authorization introduces further constraints and can remove those witnesses from the admissible class.

## 6. Relation to classical work and the binary-cut theorem

The matching condition is a classical lossless-join condition. Ronald Fagin, Alberto O. Mendelzon, and Jeffrey D. Ullman, *A Simplified Universal Relation Assumption and Its Properties*, ACM Transactions on Database Systems **7** (1982), 343–360, §2, pp.345–346, define reconstruction by the natural join of projections; Theorem 1 identifies such relations with those defined by the corresponding local predicates. [Primary paper](https://s3.us.cloud-object-storage.appdomain.cloud/res-files/500-tods82.pdf). The condition in Theorem 3 is the common-overlap instance of this construction, and Theorem 2 has empty overlap.

The quotient and factorization arguments are also classical. J.J.M.M. Rutten, *Universal coalgebra: a theory of systems*, Theoretical Computer Science **249** (2000), 3–80, Theorems 7.1–7.4 give image/quotient factorization and nested-quotient results for systems. [Primary paper](https://fldit-www.cs.tu-dortmund.de/~peter/Rutten/UniversalCoalgebra.pdf). Our direct process proofs require only the elementary unary-operation special case.

Accordingly, neither the reflection lemma, the lossless-join condition, nor process quotient factorization is claimed new. The present contribution of this investigation is a precise positive/negative theorem for the proposed **universal least-loss reconstruction interface**, with hypotheses that can be checked by Hegelese. Whether that formulation has already appeared requires a focused prior-work comparison before any novelty claim.

The binary-cut theorem has a different algebraic source of uniqueness: all natural linear kernels form the augmentation-power chain, and the sharp cutoff identifies its least permissible kernel. Arbitrary process congruences do not form such a chain. Here uniqueness instead follows from coverage plus the ordinary right-Kan reflection; failure is forced by incompatible axis choices. The binary-cut result does not transfer to arbitrary process diagrams merely by replacing linear kernels with equivalence relations.

A further distinction is that classical complete-shell constructions in abstract interpretation already study minimal refinements under exactness requirements; their existence also depends on closure hypotheses. For example, Giacobazzi–Ranzato–Scozzari, *Making Abstract Interpretations Complete*, JACM **47** (2000), Theorem 5.10 and Example 5.16, establish positive results and nonexistence phenomena in their specified lattice setting. [Primary paper](https://www.sci.unich.it/~scozzari/paper/JACM00.pdf). This prevents presenting a generic least-abstraction principle as the new research claim.

## 7. The next research question

The concrete next step is to move from a single common overlap to finite families of views with different overlaps and protected observations. For each declared observation shape and authorization policy, determine whether admissible quotients have a least kernel, and return either that quotient or a verifiable obstruction.

The useful boundary to investigate is preservation of reconstruction under common-refinement images, not the mere existence of ordinary right Kan extension. Acyclic observation diagrams may make compatibility testing efficient, but acyclicity alone does not supply a universal least-loss quotient: the independent-view star is already acyclic and fails whenever a compatible tuple is missing. Additional conditions must address realized tuples and which local quotients the request actually permits.

An implementation should distinguish four outcomes: the universal quotient exists; feasible quotients exist but no least one does; the protected requirements make every reconstructed quotient impossible; or the bounded check is unfinished. Returning one arbitrary quotient must not be reported as a necessity theorem.

Independent bounded checks in the accompanying `results.json` verify the independent-view criterion on all 327 full-projection relations in grids with both axes of sizes one through three, and all 193 full-projection relations in the binary three-dimensional cube. Separate full congruence enumeration checks 194 joint-map multisets with source size at most four and view sizes at most three, up to source-state permutation, examining 36,042 source-and-view congruence triples. The protected common-overlap criterion is checked on all 49 full-projection subrelations of the eight-state fiber product for two four-state views with base maps `[0,0,1,1]`, examining 257,728 congruence triples. Two explicit process examples swap the protected base cells; diagonal fibers still have two incomparable minimal quotients, whereas the full fiber product has its universal quotient. These checks corroborate the theorems but do not replace their proofs or establish priority. The full coverage, walking-arrow checks, and runnable commands are recorded in `COMPUTATIONAL-CHECKS.md`.
