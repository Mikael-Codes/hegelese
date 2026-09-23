# Hegelese — specification proposal v0.3

**Hic Rhodos, Hic Saltus.**

23 September 2026. Status: language-design proposal, not an implemented language or a completed formal semantics. This revision supersedes v0.2 after a second reading pass through 28 further essays. The earlier version remains available for comparison. Its philosophical research is provisional: see [reading coverage](reading-coverage.md) and [first reflection](critical-reflection.md) and [second-pass reflection](critical-reflection-v0.3.md).

## 1. Purpose

Hegelese is a proposed pure functional language for expressing computations together with the development of their representations, operations, and commitments.

Its central question is: **How can a computation make its own organization available for inspection, and how can we develop its concepts while accounting for what changes and what remains valid?**

A useful answer needs more than a before/after value. It needs an explicit occasion for development, a construction, a treatment of earlier commitments, and evidence. A failed demand is one occasion. A successful process whose organization is being rearticulated is another. Neither occasion supplies a successor automatically.

This is a computational interpretation inspired by Hegel and critically informed by Antonio Wolf. A successful Hegelese check establishes its stated computational claim under its stated assumptions. Philosophical adequacy remains open to criticism.

The motto has an engineering consequence: every demonstration must say what executed, what was checked, what remains assumed, and what has only been proposed. This document itself is a proposal; its numerical example has a separate reference calculation, not a Hegelese execution.

## 2. Vocabulary and exact keyword equivalence

The preferred name in prose is **Upheaval**. The three user-requested spellings are **the same keyword**, not three operations, overloads, translation modes, or verification levels:

```text
Aufheben ≡ Sublation ≡ Upheaval
```

The lexer recognizes the following exact spellings as the single token `UPHEAVAL`:

```text
Aufheben  Sublation  Upheaval
aufheben  sublation  upheaval  upheave
```

The lower-case forms preserve the earlier draft’s examples; `upheave` is the preferred verb spelling. This is an explicit reserved-word set, not general case-insensitivity. User-defined identifiers remain case-sensitive. `UPHEAVAL` in all capitals is the specification’s token name, not another accepted source spelling.

All accepted spellings are valid in every grammatical position allowed for that token. For example, the following declarations differ only in source spelling:

```hegelese
Upheaval SignedCounting { ... }
Sublation SignedCounting { ... }
Aufheben SignedCounting { ... }
```

Likewise, these expressions have the same meaning:

```hegelese
Upheaval SignedCounting limitation
Sublation SignedCounting limitation
Aufheben SignedCounting limitation
upheave SignedCounting limitation
```

These are alternative versions, not simultaneous duplicate declarations. The ellipses are editorial placeholders, not language syntax.

The semantic tree uses one construct and ignores the spelling for type checking and execution. Source metadata retains the original spelling and location for diagnostics, editing, and source maps. A source-preserving formatter must not change it without an explicit normalization option. Generated examples use `upheaval` for declarations and `upheave` for applications.

In documentation, historic source titles retain their authors’ original terminology. Hegelese explanations otherwise use Upheaval.

## 3. Functional foundation

The proposed core has immutable values, algebraic data types, records, pattern matching, first-class functions, parametric polymorphism, lexical scope, and strict evaluation. Laziness is explicit. Errors are typed results. Effects are explicit at the program boundary.

```hegelese
let square = fn x => x * x

let sumOfSquares =
  [1, 2, 3, 4]
  |> map square
  |> fold 0 (fn total x => total + x)
```

Ordinary arithmetic, collection processing, validation, and I/O do not need philosophical annotations. Upheaval is a specialized construct whose additional obligations must earn their cost.

Operational determinism comes from the language’s evaluation rules. It is an engineering choice, not a philosophical claim that every development has exactly one inevitable successor.

## 4. Levels that must remain distinguishable

| Level | Computational role | Example |
|---|---|---|
| Value | A particular input, state, or result | A natural number, a publication record |
| Concept specification | A declared carrier, operations, equations, observations, and dependencies | Natural-number addition with zero |
| Process description | A declared organization of computation, distinct from one run | A transition system with an observation function |
| Run | A finite execution record with inputs and provenance | Eight ticks of a repeating process |
| Development | A construction connecting specifications and accounting for a stated occasion | Extending addition, or rearticulating a process |

The word `concept` here names a finite programming artifact. It is not an assertion that a module is Hegel’s Concept or that an algebraic signature exhausts its philosophical meaning.

A `standpoint` remains available as an explicit interpretation of a concept or domain. It no longer serves as the philosophical foundation of everything. Its perspective, assumptions, scope, and observations must be visible; it does not become true merely because the programmer selected it.

## 5. Concepts include operations

A concept specification declares:

- A carrier type or family of types.
- Its construction and elimination operations.
- The equations or contracts it claims.
- Its imported dependencies and explicit assumptions.
- The observations through which its behavior can be compared.

For example, a declaration for counting exposes zero and addition. A record called `Counting` containing a string saying “all numbers are counts” would not fulfill that interface.

Wolf’s account of concepts as activities motivates this operational emphasis. It does not mechanically derive our module design. [Concepts As Logics](https://empyreantrail.wordpress.com/2017/09/29/concepts-as-logics-ways-of-thinking-being-doing/)

Version 0.3 must not equate static type checking with proof of the declared equations. A concept implementation can be well typed while a law is false, untested, or assumed.

## 6. Occasions, demands, and limitations

An occasion is one of `UnmetDemand`, `DerivedIncompatibility`, or `Rearticulation`. These are proposed tagged data constructors, not additional reserved keywords. Rearticulation names the existing process and the question a new account is meant to answer; it does not fabricate a failure to justify reflection. Multiple occasions may be recorded separately.

An ordinary model need not be inconsistent to be limited. Natural numbers with addition are perfectly coherent; a demand for an additive inverse for every number exceeds that structure.

A limitation therefore identifies:

```text
source specification and version
demand being assessed
origin of that demand
input or symbolic domain considered
derivation or counterexample
dependencies and evidence status
```

The demand’s origin matters. It may be an exported commitment of the source concept, a consequence established within a stated theory, or a new requirement introduced by an application. The last is legitimate engineering, but cannot silently be represented as an internally generated necessity.

Runtime failures, rejected observations, unmet application demands, and derived incompatibilities remain distinct result variants. A timeout does not become a contradiction. A counterexample does not by itself construct a successor.

The compiler must never obtain arbitrary proof privileges from a data value containing conflicting claims. Incompatible claims are objects for analysis, not trusted premises that authorize any conclusion.

## 7. What an Upheaval must supply

An Upheaval package connects a specified source to a specified target. It supplies:

| Component | Required account |
|---|---|
| Source and target | The precise specifications, including their versions |
| Occasion | A stated limitation, derived incompatibility, or successful activity being rearticulated |
| Construction | How target values and operations are obtained |
| Interpretation | How source values, requests, or observations are represented in the target |
| Commitment disposition | For each exported source commitment: retained, restricted, reformulated, or withdrawn, with a reason |
| Target obligations | The new requirements the construction claims to satisfy |
| Dependency account | What was used from the source and what was additionally supplied |
| Evidence | The exact status and scope of each check or proof |

Accounting for a commitment is mandatory; endorsing every old commitment is not. Some developments extend a sound partial account. Others reject an inadequate form while preserving only a specified achievement or relation. Treating every transition as an injective embedding would exclude the latter.

The initial authorship example remains a useful data migration. It is not the paradigmatic example of self-upheaval. A list of authors plus an equality test does not establish why a new conceptual organization is necessary.

## 8. Preservation means a stated relation

Preservation may concern values, observations, operations, or laws. Each must be specified separately.

For an embedding `e` between additive structures, a meaningful obligation is:

```text
e(a +old b) = e(a) +new e(b)
```

Retaining the source in an audit log establishes historical availability, not this equation. Similarly, preserving an operation’s name does not preserve its meaning.

A valid transformation may retain a source distinction within a broader organization. There need not be a total inverse that reconstructs every old value from every new value. When a restricted reconstruction exists, its domain must be stated.

When a law is withdrawn or restricted, downstream programs that relied on it must be rechecked. No implicit global change to a type’s meaning is allowed.

## 9. Dependency discipline and the limits of “immanence”

An explanation must expose its dependency graph. Every inference, construction, and discharged obligation points to its premises or inputs. Hidden use of an oracle, later theorem, new empirical fact, or target property is not permitted in a claim to derivation from the source alone.

The implementation substrate, observer facilities, and inferential premises are separately recorded. A host evaluator can use memory and pattern matching to execute a described process without those operations becoming premises of every claim about it. A derivation that invokes a target theorem does acquire that theorem as a dependency. Mere syntactic occurrence of a host operation is not a philosophical objection; undeclared inferential dependence is a verification problem.

This supports a modest computational check: the derivation uses only its declared dependencies. It does **not** certify philosophical immanence. An arbitrary assumption can be explicitly declared and still be philosophically objectionable.

No `immanent: true` switch may promote a construction to a higher assurance level. Likewise, a target cannot prove the validity of its own construction simply by asserting it. Self-reference alone supplies no proof.

This distinction responds to Wolf’s contrast between external reflection and internally developed consequence. [Dialectics of External Reflection & Immanence](https://empyreantrail.wordpress.com/2017/08/17/dialectics-of-reflection-immanence/)

## 10. Evidence is scoped

Evidence belongs to an obligation, a specification version, and a domain. Proposed classifications are:

| Status | What it establishes |
|---|---|
| Assumed | A premise has been declared; it has not been discharged |
| Observed | An external observation was recorded with provenance |
| Tested | A predicate passed on a specified finite sample |
| Exhaustively checked | Every case in a specified finite domain was checked |
| Proved relative to premises | A designated checker accepted a derivation under listed premises |
| Refuted | A valid counterexample or refutation was obtained |
| Unknown | No conclusion; includes unsupported obligations and budget exhaustion |

These labels are not a single ladder. A proof under unrealistic assumptions does not validate an empirical observation. A finite test cannot silently become a universal theorem. A proof also needs a consistent interpretation of its premises; acceptance by a checker is not a general consistency oracle.

Version 0.3 proposes runtime checks and explicit assumptions. A trusted general proof checker is future work, so examples must not fabricate `Proved` results.

The old `Result<Development, PreservationFailure>` is too narrow. A development attempt must also report an unsupported limitation, unmet target obligation, missing dependency, ambiguity, and unknown verification. An exploratory result may contain unresolved obligations; calling code must explicitly handle that status.

All runtime checks execute in a bounded evaluator or a restricted total fragment. A timeout yields `Unknown`, never `Passed` or `Refuted`. Pure does not imply terminating.

## 11. A worked development: counting and differences

This mathematical example is proposed because it exposes both the attraction and the limitation of our design.

Begin with nonnegative integers, zero, and addition. Add an explicit application demand: every element should have an additive inverse. The element 1 shows the demand fails in the current carrier, because no nonnegative `b` satisfies `1 + b = 0`.

**The new demand is additional. It is not logically forced by the existence of natural numbers.**

Construct differences from pairs of natural numbers. Interpret `(a, b)` as the difference between its coordinates. Two pairs represent the same difference when:

```text
(a, b) ~ (c, d)  iff  a + d = c + b
```

For a practical implementation, normalize a pair by removing `min(a,b)` from both coordinates. This yields a canonical pair with at least one zero coordinate.

```text
embed(n)       = normalize(n, 0)
zero           = normalize(0, 0)
add((a,b),(c,d)) = normalize(a+c, b+d)
negate((a,b))  = normalize(b, a)
```

Now `embed(1) + negate(embed(1))` is the new zero. Addition and zero from counting are preserved through `embed`. Nonnegativity remains true of embedded counting values, but is no longer a constraint on every value in the extended carrier.

Every normalized pair is expressible as `embed(a) + negate(embed(b))`; the new values are generated through the declared extension. This gives us a stronger example than adding unrelated record fields.

The following is **schematic proposed syntax**. Helper definitions are mathematical bindings described above; this is not a runnable Hegelese program:

```hegelese
upheaval SignedCounting {
  from Counting
  into Differences

  addresses AdditiveInverseDemand
  using DifferencePairConstruction

  retain zero     via embed
  retain addition via embed
  restrict nonnegative to embedded Counting

  establish additiveInverses
  establish generatedByCountingAndNegation
}

let development =
  upheave SignedCounting inverseLimitation
```

The same block can begin with `Aufheben`, `Sublation`, or `Upheaval`. The same application can use any of those spellings too.

There is an elementary justification for preservation: the sums of `(a,0)` and `(b,0)` normalize to `(a+b,0)`. For an inverse, adding `(a,b)` to `(b,a)` produces equal coordinates, which normalize to `(0,0)`. Normalization preserves the represented difference because it subtracts the same amount from both coordinates.

These are mathematical arguments, not machine-checked theorems in the proposed language. A separate Python reference calculation checks finite instances; see [validation](validation.md).

A stronger characterization could establish the universal property of this additive group completion. That remains an explicit mathematical obligation, not a result inferred from the passing examples. Neither that property nor the present construction would certify Hegelian necessity.

## 12. Development is staged, not untyped self-rewriting

The source and target types of a named Upheaval are known when a program is checked. Applying it returns a new value in the target representation. Existing values and functions retain their original types and meanings.

Research tools may generate a new candidate specification, but it must go through a new checking stage. A runtime program does not acquire permission to redefine its type system, erase failed checks, or reinterpret old proofs.

This staging allows functional immutability and conceptual development to coexist. The program can represent and inspect an evolving sequence of specifications without making any individual value mutable.

## 13. Becoming and recurrence

The earlier “repeat until stable” formulation was too strong and philosophically misleading. We distinguish a running process, its finite observations, and a development of the process’s representation.

A bounded development driver can return:

```text
Settled(criterion, evidence, state, trace)
NoApplicableRule(state, outstandingObligations, trace)
Ambiguous(candidates, state, trace)
CycleDetected(cycle, state, trace)
BudgetExceeded(state, trace)
```

`Settled` requires a named criterion. Absence of a known next rule means only `NoApplicableRule`. A repeated state is a detected cycle, not a proof of a self-grounding whole. A mathematically productive recurrent process may continue indefinitely; useful execution need not culminate in a final state.

Cycle detection is an outcome of the bounded development-search driver. A cyclic process being modeled can instead be intentional and productive. Detecting repeated states in that process does not itself constitute a failed computation or an advance in understanding.

Recollection is specified more carefully in section 18. Logical dependency order and execution order are separate relations. Later interpretation may explain earlier moments differently; it cannot revise recorded events or invent a necessity for an externally supplied choice.

## 14. Effects and empirical scope

The pure core may compute with recorded observations, but observations enter through explicit effects. A supplied random seed, external service response, clock value, or file content is part of a run’s reproducibility conditions.

The compiler cannot deduce contingent data from conceptual laws. For example, a law describing valid sensor readings does not determine the next physical reading. A theory of a protocol does not prove that an unobserved remote endpoint complied.

This boundary is reinforced by Wolf’s distinction between logical development and empirical contingency. [The Limits of Dialectics](https://epochemagazine.org/10/the-limits-of-dialectics-logical-necessity-and-empirical-contingency/)

Conflict-aware evidence remains an ordinary library facility. Two reports disagreeing about a reading do not automatically entail a new theory or an Upheaval.

## 15. Explanations must be generated from evidence

The proposed `explain` view shows:

```text
Source: Counting
Demand: Additive inverse for every element
Demand origin: Application requirement
Limitation: 1 has no additive inverse in the source carrier

Candidate construction: Normalized difference pairs
Retained: zero and addition, through the stated embedding
Restricted: nonnegativity, to embedded source values
New obligation: additive inverses

Evidence: [actual recorded status for each obligation]
Additional premises: [actual dependency list]
Unresolved: [actual remaining obligations]
```

Free-form commentary is allowed but visibly separate from executable checks and checked derivations. An LLM may propose a construction or explain a trace. It cannot confer an evidence status by sounding convincing.

## 16. Language versus library

Every proposed feature can be challenged by a strong library implementation. Hegelese should become a separate language only if integrating these facilities offers a substantial benefit:

- Dependency and commitment accounting attached to typed declarations.
- Source-aware explanations of why a development was attempted.
- Enforcement that unresolved obligations cannot silently be treated as satisfied.
- Rechecking of dependent code when a specification changes.
- A consistent source experience across the exact keyword aliases.

The first comparison should implement the same examples in an ordinary typed functional host and compare the resulting guarantees, readability, and effort. Philosophy alone does not establish the value of a new language.

## 17. Implementation boundary

An initial implementation should cover the ordinary functional core, exact keyword aliases, explicit concept packages, registered Upheaval constructions, bounded runtime checks, and evidence traces. A small finite-process library is the next prototype; native reflective syntax must wait for that experiment to justify it. Advanced effect inference, theorem-prover integration, automatic candidate generation, quotient syntax, and general reflective metaprogramming are deferred.

Before claiming a working language, demonstrate:

1. Alias-equivalent programs yield equivalent semantic trees and results, while preserving source spelling in diagnostics.
2. The counting/differences construction succeeds on stated finite checks and a deliberately broken embedding fails.
3. An unrelated migration cannot satisfy a named demand merely by preserving an unrelated field.
4. An unsatisfied or timed-out obligation remains visible to the caller.
5. A withdrawn commitment invalidates dependent uses instead of silently changing their meaning.
6. A cycle is reported as a cycle; empirical disagreement stays evidence disagreement.

The research question remains open: **How much content-sensitive development can a finite formal language support without disguising programmer-supplied choices as self-development?**

That question belongs inside Hegelese’s specification.

## 18. Reflection as a concrete research feature

The proposed interface has two distinct entry points, initially library functions rather than new keywords:

```text
run       : Process<S,I,O> × S × List<I> × Budget -> RunResult<S,O>
recollect : Run<S,I,O> × Interpretation -> Account
```

`Process` is explicitly declared code/data: a state carrier, an input carrier, a next-state operation, an observation operation, and dependencies. The first executable experiment uses finite tables. Future higher-order process descriptions will need a typed representation of syntax. Ordinary opaque functions do not become inspectable merely by being passed to `recollect`.

A run records its process version, initial state, input sequence, events, and completion status. The proposed implementation must distinguish completed, failed, and budget-limited prefixes. The small reference experiment includes only total finite transition tables and an explicit tick count.

An account contains references to existing events, declared interpretive roles, dependency edges, and propositions with evidence. Assertions about an entire process require the process description and separate obligations; they cannot be obtained from a finite run alone. Unsupported edges remain explanatory annotations. Explanatory compression may omit details from a view but retains a link to the original record.

An account never changes a program's behavior merely by explaining it. Turning an account into a new process requires an explicit Upheaval construction and another checking stage. This is how successful activity can become the object of development without treating every development as bug repair.

This is our engineering proposal prompted by Wolf's accounts of reflective activity. It is not an algorithm extracted from his philosophy, nor a claim that introspection implements Absolute Knowing.

## 19. Worked rearticulation: a process that succeeds

Take a four-phase counter. Its states are `0,1,2,3`, it begins at `0`, and each `tick` advances by one modulo four. Its observation is parity: even or odd. It works as specified.

We ask whether this process can be understood as an alternating two-phase process, retaining parity as the chosen observation. Supply the map `h(s) = s mod 2`, a two-state toggle, and an initial state of zero. The obligations are:

```text
h(initial_source) = initial_target
h(step_source(s, tick)) = step_target(h(s), tick)
observe_source(s) = observe_target(h(s))
```

These equations hold over every declared source state and input. The account gains a simpler organization of the behavior. It loses the distinction between phase 0 and phase 2, and between phase 1 and phase 3. That distinction is explicitly withdrawn as an observable of the new interface. The old four-phase description remains valid within its own version. No decoder from parity alone reconstructs the original phase.

Schematic proposed syntax, **not executable Hegelese**:

```hegelese
upheaval Alternation {
  from FourPhase
  into ParityToggle
  rearticulates FourPhaseActivity
  using parityProjection

  retain initialState via parityProjection
  retain tick via parityProjection
  retain parity via parityProjection
  withdraw exactPhase because NotRecoverableFromParity
}
```

The new `rearticulates` field is a proposed contextual field name, not a settled reserved keyword. All seven Upheaval spellings apply unchanged. The example accounts for all exported commitments of this deliberately small source interface; a richer source would require more dispositions.

Now attempt the same account for a three-phase counter. After states `0 -> 1 -> 2`, the next tick goes to `0`. Its parity is even again, whereas a two-state toggle predicts odd. The step equation fails at source state 2. Two observed ticks agree; the third exposes the error. A short successful trace therefore cannot establish the general abstraction.

The [reference experiment](process-reflection-reference.py) checks initial state, all transitions, and all observations in these finite tables, and catches an additional wrong-initial-state mutation. Its [recorded output](process-reflection-results.json) contains the actual scopes and counterexamples. This is Python executing a candidate semantic design, not a Hegelese compiler.

Mathematically, the initial-state and commuting-step equations imply by induction that all finite tick sequences preserve the mapped state; the observation equation then preserves their observations. The reference check exhausts finite local premises; that induction is stated here as a mathematical argument, not as a machine-checked proof. No conclusion is drawn about timing, resource consumption, other observations, other inputs, or philosophical necessity.

## 20. Revision of concepts and relations within a whole

Names identify versioned definitions; their wording cannot substitute for those definitions. A development may change a concept's carrier, operations, observation criteria, or law set. Existing evidence remains attached to the old version. Reuse in a new version requires an explicit transport argument or rechecking.

The source/target connection need not be an inclusion or an isomorphism. The finite-process example uses a many-to-one abstraction with an explicit observational limit. Other constructions may require simulations or partial interpretations. Each relation states exactly what it preserves.

The same value may occupy different roles in a declared whole. An explanatory `Moment` reference therefore contains a whole identifier, role identifier, and supporting relation. It does not supply a universal `opposite` operation, turn any pair into a contradiction, or confuse a logical role with an instant of clock time. This begins as account metadata, not a special type theory.

## 21. Research controls that the philosophy itself invites

The language's own concepts remain open to criticism. We do not reserve `Absolute` as a successful verification status. Nor does a program's ability to explain its own syntax discharge the assumptions of its evaluator or proof checker.

Source texts are versioned research inputs. Earlier uncertainty and later confidence in an author's work must not be silently merged into one timeless doctrine. Disagreement with an author is permitted at the level of mathematics, empirical claims, interpretation, or engineering value.

In particular, naming conventions may learn from Wolf's concern for intelligibility without importing rankings of natural languages, peoples, artistic tastes, or kinds of persons. The user-mandated aliases coexist precisely because access and stable meaning matter more than terminological uniformity.

The next implementation milestone is a runnable vertical slice: parse the aliases; evaluate an ordinary functional program; register a finite-process Upheaval; produce scoped evidence; reject a bad transition map; and invalidate an account when an exported observation changes. Only then compare its benefits against a typed functional library.
