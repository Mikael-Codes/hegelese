# A genuine right-Kan reconstruction demand with no universal least-loss quotient

1 November 2026. This is an elementary counterexample and a complete classification of one small case. No novelty claim is made. It does not use a state-count bound as a substitute for reconstruction.

## 1. The indexing category and the reconstruction condition

Let \(C\) be the walking-arrow category

\[
c\xrightarrow{u}d,
\]

with identities and no other morphisms. Let \(D\subset C\) be the full subcategory on \(d\). Work with **covariant** diagrams; replacing both categories by their opposites gives the corresponding contravariant convention.

A diagram is a map \(f:X_c\to X_d\). Right Kan extension of a diagram \(Y\) on \(D\) is

\[
\operatorname{Ran}_{D\hookrightarrow C}Y
=(Y\xrightarrow{\mathrm{id}}Y).
\]

Indeed, the comma category \((c\downarrow D)\) consists of the single object \(u\), and \((d\downarrow D)\) consists of the identity. Thus the reconstruction unit is

\[
(f,\mathrm{id}):(X_c\xrightarrow{f}X_d)
\longrightarrow(X_d\xrightarrow{\mathrm{id}}X_d).
\]

A diagram is reconstructed from \(D\) exactly when its displayed arrow is an isomorphism. This is an actual right-Kan locality condition.

The same calculation holds for diagrams of finite deterministic processes. To realize the examples below, give every state a self-loop for one input `tick`, give every state the same retained output, and choose the state labeled \(0\) as initial. All displayed maps are then process homomorphisms preserving transitions, initial state, and observations. The category computation does not depend on replacing those equations with weaker tests.

## 2. The counterexample

Take

\[
X_c=\{0,1\},\qquad X_d=\{0,1,2\},
\qquad f(0)=0,\ f(1)=1.
\]

There are two objectwise-surjective quotient maps from this diagram onto the reconstructed diagram

\[
A_c=A_d=\{0,1\},\qquad A(u)=\mathrm{id}.
\]

Define \(q^0\) and \(q^1\) to be the identity at \(c\), and at \(d\) define

\[
q^0_d=(0\mapsto0,\ 1\mapsto1,\ 2\mapsto0),
\qquad
q^1_d=(0\mapsto0,\ 1\mapsto1,\ 2\mapsto1).
\]

Both naturality squares commute, both maps are objectwise surjective, and both targets reconstruct from \(D\). They also preserve the processes specified above. Their kernel relations are

\[
\begin{array}{c|cc}
&c&d\\\hline
\ker q^0&\text{equality}&\{0,2\}\mid\{1\}\\
\ker q^1&\text{equality}&\{0\}\mid\{1,2\}.
\end{array}
\]

Their objectwise intersection is equality at both objects. Its quotient is therefore the original diagram \(X\), which is **not** reconstructed, since \(f\) is not surjective.

Suppose a universal least-loss reconstructed quotient \(q_*:X\twoheadrightarrow A_*\) existed. Both \(q^0\) and \(q^1\) would factor through it. Hence

\[
\ker q_*\subseteq\ker q^0\cap\ker q^1=\text{equality}.
\]

Since \(q_*\) is objectwise surjective, it would be an isomorphism of diagrams, forcing \(X\) itself to reconstruct. This is a contradiction. Therefore there is **no universal least-loss reconstructed quotient**, even in this two-object finite diagram category.

There are exactly three feasible quotient kernels in this example: the two above and the indiscrete kernel at both objects. The two displayed kernels are the incomparable finest feasible kernels. They exhibit a disjunctive necessity: the extra state \(2\) must be identified with a represented state, but neither choice is forced individually.

## 3. Why closure under limits does not prevent the example

The product of the two reconstructed targets is reconstructed:

\[
(\{0,1\}^2\xrightarrow{\mathrm{id}}\{0,1\}^2).
\]

The paired map \((q^0,q^1)\) has image

\[
\{(0,0),(1,1)\}
\hookrightarrow
\{(0,0),(1,1),(0,1)\}.
\]

This image diagram is isomorphic to \(X\), so it is not reconstructed. Thus the missing closure property is closure under the relevant **images/subobjects**, not closure under products or limits. The intersection of quotient kernels is the kernel of the map into a product; its quotient is the image of that map, rather than the entire product.

Nor does the ordinary right-Kan reflector itself solve the quotient problem. Its unit here is the inclusion at \(c\) and the identity at \(d\), and is not objectwise surjective. The reflected object is universal among maps to reconstructed diagrams, but it is not a quotient of the specified source in the required sense.

## 4. Complete criterion for the walking-arrow case

Continue with nonempty finite sets, or with the self-loop constant-observation processes above. Write \(f:X\to Y\), and put \(I=f(X)\).

**Proposition.** Local quotient kernels correspond exactly to equivalence relations \(R\) on \(Y\) such that every \(R\)-class meets \(I\). The kernel at \(X\) is then \((f\times f)^{-1}R\).

**Proof.** A local target can be identified with an identity arrow \(A\to A\). A quotient onto it is a surjection \(q_Y:Y\twoheadrightarrow A\) such that \(q_X=q_Yf\) is also surjective. The latter condition says exactly that every fiber of \(q_Y\) meets \(I\). Conversely any such partition gives both surjections and the local quotient diagram. Its kernel at \(X\) is the asserted pullback. ∎

This yields the exact existence criterion:

**Theorem.** A universal least-loss local quotient exists if and only if either

\[
f\text{ is surjective},\qquad\text{or}\qquad |f(X)|=1.
\]

If \(f\) is surjective, equality on \(Y\) is feasible. The universal quotient is

\[
(X\xrightarrow{f}Y)\xrightarrow{(f,\mathrm{id})}
(Y\xrightarrow{\mathrm{id}}Y).
\]

If \(|I|=1\), every feasible class must contain that one image point, so there can only be one class. The universal quotient is the singleton identity diagram.

If \(I\ne Y\) and \(|I|\ge2\), keep all points of \(I\) in separate blocks and assign every point of \(Y\setminus I\) to an arbitrary image point. These assignments always give feasible partitions. For any two distinct points of \(Y\), some assignment separates them: retain separate image points; assign an extra point away from a specified image point; or assign two extra points to distinct image points. Therefore the intersection of all feasible relations on \(Y\) is equality. The intersection kernel at \(X\) is \(\ker f\), so its quotient is

\[
I\hookrightarrow Y,
\]

which is not local. The factorization argument from Section 2 excludes a universal least-loss quotient. ∎

This also proves minimality **within the walking-arrow category with nonempty state sets**: failure needs \(|X|\ge2\), \(|Y|\ge3\), so the two-state/three-state example has the smallest total number of states in that setting. No unrestricted minimality claim over all finite categories is needed.

## 5. Retained observations can be included exactly

For self-loop processes, let \(o_X:X\to O\) and \(o_Y:Y\to O\) be fixed observation tuples satisfying \(o_X=o_Yf\). A feasible quotient partition on \(Y\) must both meet \(I\) in every class and refine the observation fibers. For an observation value \(\alpha\), put

\[
Y_\alpha=o_Y^{-1}(\alpha),\qquad
I_\alpha=I\cap Y_\alpha.
\]

If some nonempty \(Y_\alpha\) has \(I_\alpha=\varnothing\), no observation-preserving local quotient exists. Otherwise choices separate by observation fiber, and a universal least-loss quotient exists exactly when, for every nonempty fiber,

\[
I_\alpha=Y_\alpha\quad\text{or}\quad |I_\alpha|=1.
\]

The universal relation is equality in a fully represented fiber and the indiscrete relation within a fiber with one represented state. A partially represented fiber with at least two represented states supplies the same ambiguity as before. This is a direct fiberwise application of Section 4, not a claim about arbitrary nontrivial dynamics.

For a counterexample retaining a nonconstant observation, add a state \(z\) to both objects in Section 2, send \(z\) to \(z\), and give it output \(1\) while the original states have output \(0\). Keep all transitions self-loops. The two ambiguous quotients still exist and preserve the now-nonconstant observation; the added state remains separate in both.

## 6. Consequences for the research question

Actual reconstruction locality can fail common-refinement closure already for a single arrow. Therefore the binary-cut universal quotient theorem cannot be generalized to all finite process diagrams merely by citing closure of right-Kan local objects under limits.

Two distinct positive mechanisms are visible even here: an objectwise-surjective reconstruction unit gives a universal quotient directly; or all feasible quotients may be forced to collapse to a smaller local object even when that unit is not surjective. The latter mechanism is exemplified by a one-point image and is not captured by demanding that the reflector unit be surjective.

The demand, source diagram, retained observations, and allowed maps remain fixed inputs. The counterexample identifies precisely where a unique necessary successor fails: the reconstruction condition requires a missing local state to be identified with some represented state but does not choose which one. This is conditional mathematical ambiguity, not a justification for authorizing either loss.
