# Hegelese

**Hic Rhodos, Hic Saltus.**

Hegelese is an experimental functional language for **changing a program's representation while making the consequences explicit and checkable**. Inspired by Hegel and critically informed by Antonio Wolf's writings, it asks: what changes, what survives, what is relinquished, and what evidence supports the claim?

An AI can propose a convincing rewrite. A programmer needs to know whether it still does what matters. A Hegel-inspired reader can ask a deeper question: can a form be transformed while its achievements acquire a place within the new organization? Hegelese brings these questions together in an executable experiment.

**Current status:** an executable Hegelese bootstrap interpreter, a finite-process articulated-change checker, and specification proposal v0.3. Real `.hgl` programs now run through a Python parser and bounded functional evaluator. The bootstrap is dynamically checked; static typing, a compiler, general proof checking, and self-hosting remain future work. The [bootstrap language guide](BOOTSTRAP.md) defines the implemented syntax; the broader v0.3 examples remain proposals.

![An abstract geometric structure unfolds and reorganizes, with a recurring red path suggesting what is retained through the change.](assets/hegelese-upheaval.png)

For a concise account of the research question, executed comparisons, and open objections, see the [technical review brief](REVIEW-BRIEF.md).

## Upheaval

An Upheaval specifies a development between representations, the occasion for it, and the disposition of earlier commitments. It may address a limitation or rearticulate a successful process. Preservation must name a relation; retaining an old value in a log does not establish semantic preservation.

## An example: four moments, one rhythm

Imagine a four-step dance that repeats. Someone keeping the rhythm needs only to know whether the next beat falls on the left or the right; a choreographer may need to know the exact step. Both descriptions concern the same activity, but they retain different distinctions.

Here is the computational version. A process cycles through four phases. We propose replacing it with two alternating states:

```text
Original phases:    0 → 1 → 2 → 3 → 0 → …
What we retain:     E → O → E → O → E → …
New representation: 0 → 1 → 0 → 1 → 0 → …
```

`E` and `O` mean even and odd. The map sends phases 0 and 2 to the same new state, and phases 1 and 3 to the other. **We preserve the rhythm and deliberately give up the exact phase.** That loss is acceptable only when the application does not require the distinction.

This is a complete, executable Hegelese program:

```hegelese
let parity = fn(s) => if int(s) % 2 == 0 then "even" else "odd";
process FourPhase = {
  version: "1",
  states: ["0", "1", "2", "3"],
  inputs: ["tick"],
  initial: "0",
  step: fn(s, input) => str((int(s) + 1) % 4),
  observe: {parity: parity, exactPhase: fn(s) => int(s)}
};
process ParityToggle = {
  version: "1",
  states: ["0", "1"],
  inputs: ["tick"],
  initial: "0",
  step: fn(s, input) => str(1 - int(s)),
  observe: {parity: parity}
};
request KeepParity from FourPhase require ["parity"];
upheave Alternation {
  from KeepParity;
  into ParityToggle;
  using fn(s) => str(int(s) % 2);
  occasion {kind: "Rearticulation", explanation: "Understand a successful cycle through alternation, retaining parity."};
  retain initial because "The mapped source start is the target start.";
  retain step because "Every tick should commute with the parity projection; check every state.";
  retain "observation:parity" because "Parity is required by the application.";
  withdraw "observation:exactPhase" because "The map merges distinct phases. Exact phase cannot be reconstructed.";
  assumptions [];
};
check(Alternation);
```

Read `request` as **what must remain true**. Read `using` as the relationship between the old and new descriptions. Each `retain` makes a preservation claim; `withdraw` names an achievement we are giving up. The `because` clauses explain the proposal to a reader. The checker establishes the supported equations separately: eloquent reasons do not make a false claim pass.

Run the [included program](examples/four-phase.hgl) from the repository root:

```sh
python3 hegelese.py run examples/four-phase.hgl
```

The report contains `ExhaustivelyChecked`: the checker verifies the initial state, every declared state/input transition, and every retained observation. In this example that is **nine checks**: one initial-state check, four transition checks, and four parity checks. For each transition it asks whether taking a step and then translating gives the same result as translating first and stepping in the new process. These local checks support preservation along any finite sequence of ticks in these declared processes; they do not certify the surrounding application.

### A persuasive proposal can still be wrong

Now try the [three-phase version](examples/three-phase.hgl):

```sh
python3 hegelese.py run examples/three-phase.hgl
```

Its first few beats look equally promising. But at the return from phase 2 to phase 0, the old process goes from even to even, while the proposed toggle goes from even to odd:

```text
Old process:        2 → 0     even → even
Proposed toggle:    0 → 1     even → odd
```

Hegelese returns `Refuted`, with the failing transition as a counterexample. No improvement to the explanation repairs that mismatch. Nor does an unfinished check count as success: running the four-phase example with `--budget 2` returns `Unknown`.

### Why this matters to three different readers

**For AI agents:** a proposed change comes with obligations and machine-readable feedback. The agent can inspect a counterexample, revise its proposal, and run the check again. In the [agent protocol](ARTICULATION.md), the caller supplies an independently retained request, so the candidate cannot quietly redefine what it was asked to preserve. That separation must also be enforced by the host's access controls; a fingerprint alone is not permission management.

**For programmers:** this makes a particular kind of refactoring claim explicit: a simpler representation preserves specified behavior under a stated map. Tests, types, and model checkers remain useful. Hegelese's experiment is to put the old model, new model, mapping, declared losses, and checked evidence together in one language. The example uses exhaustive finite checking rather than selected test inputs. It does not establish superiority over existing verification tools.

**For Hegel-inspired readers:** the interest lies in preservation through a changed organization. The old phases no longer stand as four independent distinctions in the new representation; their alternation survives, while exact position does not. This offers a small, inspectable analogy for Upheaval. It is a rearticulation of an already successful process, not a claim that the four-phase cycle contradicts itself or inevitably produces its successor. The application supplies the reason to prefer the simpler account. Whether this does justice to Hegel remains a philosophical question, informed by our [primary-text research](docs/science-of-logic-essence-concept.md).

The ambition is to make a change answerable: **show what it preserves, acknowledge what it loses, and let the evidence challenge its explanation.** The present achievement is deliberately narrow and runnable. The larger hypothesis—that this helps people and AI agents make better changes—still needs comparative evidence.

## When the proposer misses a loss

The checker now computes which source states a proposed map merges, **even when no observations were declared**. It can discover that phases 0 and 2 have become indistinguishable without being told to look for `exactPhase`. This establishes structural loss under the map; the application still determines whether that loss matters.

The opt-in **lineage protocol** makes those discoveries constrain later proposals. Each successor must repair inherited losses, carry them as unresolved, or cite the caller's explicit authorization to accept them. Repairs are checked over entire groups of merged states. Earlier retained observations remain obligations, and unfinished checks are run again. The caller retains the history independently of the proposing agent.

```sh
python3 examples/lineage_demo.py
```

This runnable demonstration first detects an undeclared loss, then refuses to accept a successor that forgets the finding, and finally accepts a checked repair. The repair keeps the distinctions; it does not pretend the original compression succeeded. For AI agents this provides feedback they did not nominate themselves; for programmers it makes earlier findings enforceable; for Hegel-inspired readers it makes criticism consequential to the next proposal. These are bounded engineering steps, not a claim to have mechanized Hegel's dialectic.

See [derived loss and accountable revision](LINEAGE.md) for the protocol, evidence, trust boundary, and limitations. The existing workflow gate still uses ordinary preservation checking; lineage enforcement requires the caller to use the new protocol.

## Start here

- [Run the derived-loss and lineage milestones](LINEAGE.md) — structural findings and accountable revisions
- [Deploy the finite-workflow CI gate](DEPLOYMENT.md) — the first narrow production use case
- [Executable bootstrap language guide](BOOTSTRAP.md)
- [Complete four-phase development](examples/four-phase.hgl) and [refuted three-phase development](examples/three-phase.hgl)
- [Language specification v0.3](docs/hegelese-spec-v0.3.md)
- [Critical reflection from the second corpus reading](docs/critical-reflection-v0.3.md)
- [Reading inventory and coverage](docs/reading-coverage.md), also available as [JSON](docs/reading-coverage.json)
- [Implementation and self-hosting roadmap](ROADMAP.md)
- [Articulated development for AI-assisted programming](ARTICULATION.md)
- [Reference experiment validation](docs/validation-v0.3.md)

The earlier [v0.2 specification](docs/hegelese-spec-v0.2.md) and [first critical reflection](docs/critical-reflection.md) preserve the design's history.

## Run Hegelese

Requires Python 3.10 or later; no third-party packages.

Version 0.2.0 also builds as an installable wheel with `hegelese` and `hegelese-gate` commands. The gate runs a candidate in a worker with a deadline and accepts only checked preservation against the caller's retained request. See [deployment and operational limits](DEPLOYMENT.md) and [release changes](CHANGELOG.md).

```sh
python3 hegelese.py run examples/functional.hgl
python3 hegelese.py run examples/four-phase.hgl
python3 hegelese.py run examples/three-phase.hgl
python3 hegelese.py run examples/four-phase.hgl --budget 2
python3 -m unittest discover -s tests -v
```

The ordinary functional example returns 30, 720, and 42. The four-phase counter admits a parity abstraction while declaring the loss of exact phase. The three-phase counter fails at its wraparound transition. Insufficient checking budget returns `Unknown`. Output includes actual evidence, content fingerprints, and source locations. Exit codes are 0 for evaluation or exhaustive checking, 1 for refutation, 2 for invalid input, and 3 for an unknown result.

The earlier independent Python experiment remains available as `python3 docs/process-reflection-reference.py`. Passing finite checks establish only their stated preservation obligations. They do not certify philosophical necessity, empirical adequacy, or general program correctness.

## Toward an implementation in Hegelese

The first agent-facing checking interface is executable now:

```sh
python3 hegelese.py check request-four.json proposal-four.json
python3 hegelese.py check request-three.json proposal-three.json
```

The first candidate passes its finite obligations; the second exits with a refutation and a concrete transition counterexample. The checker binds proposals to an independently supplied request, requires an account of every source commitment, and separates explanation from evidence. Budget exhaustion and unresolved assumptions cannot become accepted results. See [the protocol and evaluation agenda](ARTICULATION.md) for its scope and limitations. No AI productivity gain has yet been measured.

Python implements the current bootstrap. An interpreter written in Hegelese is an explicit subsequent milestone. The bootstrap guide records evaluation rules and limits, and the conformance suite now exercises actual source programs. The core exposes no file, network, or evaluator-replacement operations.

Self-interpretation and a self-hosting compiler are separate milestones. Neither is a claim of philosophical self-grounding.

## Research provenance

The [Antonio Wolf inventory](docs/reading-coverage.md) records 51 fully read WordPress articles and two fully read Epoché essays as of 23 September 2026. Further entries are explicitly marked partially read, context-reviewed, or retrieved but unread. Full online corpus reading remains incomplete.

Primary-text research also includes Hegel's *Science of Logic*, using the Marxists Internet Archive English transcription: a substantial passage-based reading of [Being (Book One)](docs/science-of-logic-book-one.md), selective readings across [Essence and the Concept](docs/science-of-logic-essence-concept.md), and a complete first reading of the final section, **The Idea (§§1631–1817)**. The [whole-work coverage ledger](docs/science-of-logic-whole-work-coverage.json) records 19 fully read HTML pages in the continuation, alongside the earlier passage coverage, out of 57 retrieved pages. **The whole work has not yet been read**, and German editions and alternative English translations have not been collated.

Primary-text claims, author interpretations, engineering proposals, and executed checks are distinguished in the documents.

The repository contains our specifications, research notes, source links, and inventory metadata. Downloaded copies of third-party articles and personal backup metadata are not included. Source authors are not represented as endorsing this project.

---

Created by **Petri Mikael Autio**.
