# Hegelese implementation roadmap

**Hic Rhodos, Hic Saltus.**

This roadmap records intended work except where completion is explicitly noted.

## Completed foundation: articulated finite changes

The Python checker in `hegelese.py` now accepts JSON proposals against independently supplied requests, requires commitment dispositions, checks finite preservation equations, and returns scoped evidence or counterexamples. It handles the seven Upheaval aliases at the interchange boundary. It is not a parser or interpreter for the proposed Hegelese grammar.

The [articulation research agenda](ARTICULATION.md) defines the AI-facing protocol and a future comparative evaluation.

## Completed vertical slice: bootstrap interpreter 0.1

`hgl.py` now parses and evaluates `.hgl` source. It supports strict functions and lexical closures, single-function recursion, immutable bindings, records, lists, tagged values, pattern matching, finite process declarations, request declarations, and all seven Upheaval aliases. `check` connects source-level candidates to the finite checker and returns evidence with original source locations. The [bootstrap guide](BOOTSTRAP.md) specifies this implemented subset.

The three runnable examples cover ordinary computation, accepted lossy abstraction, and a refuted transition map. Tests additionally cover changed observations, withdrawn requirements, exact alias behavior, unknown checking outcomes, and bounded evaluation. This is dynamically checked: static typing and mandatory handling of unresolved evidence remain open. Changes are rechecked on execution; persistent dependency tracking is not implemented.

## 1. Freeze a bootstrap subset

The 0.2.0 deployment milestone adds an installable, fail-closed CI gate, a documentation-publishing workflow pilot, worker limits, and evidence artifacts. See [deployment](DEPLOYMENT.md). This is a narrow operational use before the general language is mature.

The first grammar and evaluation rules are implemented and documented. Stabilize this subset with usage feedback before extending it. Preserve the distinction between this executable grammar and the broader schematic proposal.

The tree-walking Python interpreter and structured diagnostics are complete for the subset. Next add a deliberately small static type checker and specify typed error handling. Keep parsing, evaluation, type checking, and evidence checking separate. File access and output belong at explicit host-service boundaries. Evaluation fuel and a separate finite-check budget currently expose exhaustion as `Unknown`; these are not a general security sandbox.

## 2. Execute one complete Upheaval

Finite process declarations, named candidate transformations, and scoped obligations now execute. Bounded run traces and registered application syntax from the broader proposal remain future work. All seven declaration spellings produce equivalent checked semantics.

Acceptance cases:

1. An ordinary functional program evaluates without philosophical annotations.
2. Four-phase counting admits a parity abstraction while declaring the loss of exact phase.
3. Three-phase counting is rejected at the transition from 2 to 0.
4. An incorrect initial state fails independently.
5. Unresolved or budget-limited checks remain visible as unknown.
6. An altered observation or withdrawn law invalidates dependent evidence.
7. Diagnostics identify the actual source location under every alias spelling.

The reference experiment supplies independent expected results. It is separate from the interpreter. Items 1–5 and alias source locations execute now; changed observations are rechecked, but general dependent-code invalidation in item 6 requires a persistent dependency model.

## 3. Make reflective accounts useful

Represent declared process structure, finite execution records, and explanatory accounts separately. Accounts may connect actual events and declared roles without rewriting chronology. Turning an account into changed behavior requires an explicit checked construction.

Compare this feature set against a typed functional library. Retain language-level machinery only where integration earns its complexity.

## 4. Write a Hegelese interpreter in Hegelese

Use strings, collections, recursion, tagged alternatives, and pattern matching to implement a parser and evaluator in Hegelese. Run that interpreter under the Python bootstrap, then execute the same language-level conformance suite through both paths.

Port components incrementally. Shared tests establish tested agreement; a general semantic-preservation claim requires a stronger argument. Document any unsupported constructs rather than hiding differences.

## 5. Explore compilation and self-hosting

Choose a compilation target after the interpreter clarifies the semantics. Build a compiler in Hegelese and work toward compiling its own source. Keep the execution substrate, build chain, and trusted components explicit.

## Open research questions

- Which reflective operations require native syntax rather than libraries?
- How should evidence be transported between concept versions?
- What guarantees can a useful small checker provide without a general proof assistant?
- How much candidate development can be automated without disguising supplied choices as necessity?
- Does Hegelese offer enough advantage over a functional library to justify a separate language?
