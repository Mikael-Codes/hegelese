# Hegelese implementation roadmap

**Hic Rhodos, Hic Saltus.**

This roadmap records intended work except where completion is explicitly noted.

## Completed foundation: articulated finite changes

The Python checker in `hegelese.py` now accepts JSON proposals against independently supplied requests, requires commitment dispositions, checks finite preservation equations, and returns scoped evidence or counterexamples. It handles the seven Upheaval aliases at the interchange boundary. It is not a parser or interpreter for the proposed Hegelese grammar.

The [articulation research agenda](ARTICULATION.md) defines the AI-facing protocol and a future comparative evaluation. The next milestone connects this executable evidence boundary to the functional language core. Machine-readable diagnostics, version-bound obligations, and candidate checking are requirements for that core.

## 1. Freeze a bootstrap subset

Write a precise grammar and evaluation rules for immutable bindings, lexical scope, strict evaluation, integers, booleans, strings, functions, conditionals, lists, tagged alternatives, and pattern matching. Define equality and arithmetic explicitly. Preserve source spans and original keyword spellings.

Build a tree-walking Python interpreter with structured diagnostics and a deliberately small type checker. Keep parsing, evaluation, type checking, and evidence checking separate. File access and output belong at explicit host-service boundaries. Pure evaluation still needs a policy for resource exhaustion.

## 2. Execute one complete Upheaval

Implement finite process declarations, bounded runs, registered transformations, and scoped obligations. All seven Upheaval spellings must produce equivalent semantics.

Acceptance cases:

1. An ordinary functional program evaluates without philosophical annotations.
2. Four-phase counting admits a parity abstraction while declaring the loss of exact phase.
3. Three-phase counting is rejected at the transition from 2 to 0.
4. An incorrect initial state fails independently.
5. Unresolved or budget-limited checks remain visible as unknown.
6. An altered observation or withdrawn law invalidates dependent evidence.
7. Diagnostics identify the actual source location under every alias spelling.

The reference experiment supplies independent expected results. It must not be presented as the interpreter itself.

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
