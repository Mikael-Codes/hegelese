# Articulated development for AI-assisted programming

**Hic Rhodos, Hic Saltus.**

Status: research direction plus an executable finite-process checker, version 0.1. The JSON proposal format is a bootstrap interchange format. It is not the Hegelese surface grammar or a complete interpreter.

Implementation update: the [bootstrap interpreter](BOOTSTRAP.md) now connects source-level process, request, and Upheaval declarations to this checker. The JSON interface remains available for externally retained requests. Static typing, general proof transport, and measured AI advantages remain future work.

## Thesis

AI can help produce candidate representations, explanations, distinctions, and obligations. Our hypothesis is that this makes a richer articulation of program changes practical. Hegelese should make those articulations computationally consequential: inspectable, challengeable, and bound to the definitions they concern.

The goal is not maximum explanation. It is sufficient articulation to discover an otherwise hidden assumption, loss, or failure, and to make a successful development usable by another person or tool.

This hypothesis remains unmeasured. The current executable work tests a checking protocol, not whether an AI performs better with it.

## Three independent questions

1. **Is the change articulated?** Are the source, target, construction, commitments, reasons, and assumptions actually supplied?
2. **Are its computational claims supported?** Do the declared preservation obligations pass their designated checks?
3. **Is this a good change for the task?** Are the chosen observations adequate, are the losses acceptable, and is the new representation useful?

A candidate can answer the first question well and fail the second. It can pass finite checks and still be a poor response to the third. Hegelese must keep those outcomes distinct. Neither an eloquent rationale nor a complete form supplies a proof.

The checker currently answers a restricted part of question two and checks the presence of the fields needed for question one. A separately supplied request fixes the required observations. It does not decide the adequacy of that request or the truth of explanatory prose.

## Roles and trust boundary

| Role | Supplies | Cannot establish merely by supplying it |
|---|---|---|
| Request author | Source definition and required observations | That these observations capture every real application need |
| Candidate author, human or AI | Target, map, commitment dispositions, occasion, reasons, assumptions | The evidence status of the proposal |
| Finite checker | Local equation checks, counterexamples, scope, content fingerprints | Philosophical necessity, empirical adequacy, or general program correctness |
| Reviewer or calling tool | Decision about the checked candidate in its application context | Universal validity beyond the recorded scope |

The request must be retained independently by the caller. An agent allowed to replace both request and proposal can weaken the problem and compute a new hash. Content fingerprints detect changed content against a fixed request; they do not create an access-control boundary. This checker never applies a proposal or changes files on acceptance.

## Executable protocol

Run from the repository root with Python 3.10 or later:

```sh
python3 hegelese.py check request-four.json proposal-four.json
python3 hegelese.py check request-three.json proposal-three.json
python3 hegelese.py check request-four.json proposal-four.json --budget 2
python3 hegelese.py fingerprint request-four.json
python3 -m unittest discover -s tests -v
```

The first command succeeds. The second returns a counterexample. The third returns an unknown result after two checks. Exit codes are 0 for `ExhaustivelyChecked`, 1 for `Refuted`, 2 for `Invalid`, and 3 for `Unknown`. Output from `check` is JSON suitable for an agent loop or a human-facing rendering.

### Request

The exact request fields are `schema`, `source`, and `required_observations`. The schema is `hegelese-request/0.1`.

A source process specifies `name`, `version`, `states`, `inputs`, `initial`, `transitions`, and `observations`. States and inputs are distinct nonempty strings. Transition tables cover every state/input pair; observation tables cover every state. Observation values are strings, integers, booleans, or null, with distinct type tags. In particular, `true` is not the integer `1`.

The prototype bounds a process to 1,000 states, 64 input symbols, and 32 observations. CLI input files are limited to 2 MB each. These are engineering bounds, not philosophical restrictions. The check budget limits equation comparisons, not total wall-clock time or memory. General sandboxing is not provided.

### Proposal

The exact fields are:

| Field | Meaning |
|---|---|
| `schema` | `hegelese-proposal/0.1` |
| `operation` | One of the seven exact Upheaval aliases |
| `request_sha256` | Fingerprint of the complete independently supplied request |
| `occasion` | `kind` and `explanation`; kind is `Rearticulation` or `UnmetDemand` |
| `target` | A complete finite process description |
| `mapping` | A total map from source states to target states |
| `dispositions` | One account for every exported source commitment |
| `assumptions` | A list of unresolved assumptions the proposal relies on |

Every source exports `initial`, `step`, and `observation:NAME` for each observation. Each disposition contains `action` and `reason`. This subset supports `retain` and `withdraw`; the fuller specification's restriction and reformulation relations remain future work. Initial state, transitions, and required observations cannot be withdrawn. A withdrawal of an optional observation must be explicit.

The occasion is an articulation, not an independently checked derivation. This prototype does not prove that an unmet demand arose internally or that a rearticulation was necessary. Nonempty assumptions remain unresolved and prevent an accepted overall result, even when the finite equations pass. They cannot be used to override a counterexample.

Unknown fields, including an agent-supplied evidence status, are rejected. Duplicate JSON keys are rejected rather than silently taking the last meaning. Input and output schemas are deliberately different.

### Evidence

The checker tests these local obligations over **all declared source states**, including unreachable states, and all declared inputs:

```text
h(source.initial) = target.initial
h(source.step(s, i)) = target.step(h(s), i)
source.observe(name, s) = target.observe(name, h(s))
```

The observation equation applies to every retained observation, not just the minimum required set. The source and target must have the same input alphabet. No target-only observation or additional target law is certified.

The report includes the checker version, exact request/source/target/proposal fingerprints, original operation spelling, disposition account, total and completed checks, unresolved assumptions, and counterexamples. It returns at most ten counterexamples and separately reports the total failure count. A known counterexample remains a refutation even if the checking budget is later exhausted.

Canonical JSON uses sorted object keys without insignificant whitespace. Array order remains significant for fingerprints. The operation spelling is normalized only in the semantic proposal fingerprint; the original spelling stays in the report. Every invocation recomputes the evidence. The checker does not import or trust old evidence records. Hashes are not signatures, and a copied JSON report is not self-authenticating.

## An agent interaction

1. The caller fixes the request and makes it available to the candidate author.
2. The author supplies a proposal with a total account of source commitments.
3. The caller invokes the checker against its retained request.
4. The author receives the structured report and may revise the proposal.
5. If the requirement itself needs revision, that is a separate decision that creates a new request. The old failure remains a failure against the old request.

An agent may generate both an implementation and its accompanying tests. That makes the independently retained requirement and independently executed checker especially important. More generated text is not a substitute for an independent criterion.

For the included three-phase example, the explanation is complete but the transition map fails at state `2` on `tick`. Rewording the explanation does not change the result. Removing the required parity observation is rejected as invalid. A short agreeing trace cannot replace the transition check.

## Why this is a language experiment

The current implementation could live in a library. That is intentional: it gives us a concrete standard that future language syntax must improve upon. Hegelese should eventually connect commitments to declarations, locate failures at source spans, track affected uses, and express the process and its development without a separate hand-maintained JSON account.

The functional core remains necessary. This protocol is the first implementation of the evidence boundary that the core will call, not a replacement for parsing, closures, types, or effects. Self-hosting remains an explicit goal: the schema validator and finite checker are candidates for later implementation in Hegelese.

## Evaluation agenda

We should evaluate whether articulation improves outcomes, not reward an agent for longer answers or greater confidence. A useful initial comparison would give the same model and resource budget a set of finite process tasks through three interfaces: an ordinary implementation request with tests; an articulated request and narrative review; and an articulated request with executable checks.

Use the same behavioral requirements and independent held-out checks in every condition. Include valid lossy abstractions, impossible requested maps, changed observation requirements, multiple inputs, unreachable states, and deliberately misleading short traces. Record:

- Correct accepted transformations and invalid transformations mistakenly accepted.
- Honest refusals or unknown results when the requested preservation cannot be established.
- Undeclared losses and attempts to weaken the requirement.
- Number of revisions and total checking, token, and human-review effort.
- Whether a second agent or person can reconstruct the accepted scope from the artifact.
- Reviewer ability to distinguish finite evidence, assumptions, and narrative claims.

The current regression suite exercises the protocol's failure modes. No comparative AI experiment has been run, and it would be premature to claim productivity or reliability gains. If articulation adds cost without improving these outcomes, we should simplify the design.

## Next steps in order

1. Use the checker on a fixed set of candidate changes and inspect whether its reports are sufficient for correction.
2. Implement the small functional interpreter and connect its process declarations to this checking boundary.
3. Replace duplicated JSON definitions with references to versioned language declarations and source locations.
4. Add explicitly specified restriction and reformulation relations, rather than treating every development as a total state map.
5. Run the comparative AI evaluation before claiming an AI-specific advantage.
6. Reimplement the evaluator and checker in Hegelese as the language becomes expressive enough.

The governing principle is **articulate enough to make the change answerable to criticism**.
