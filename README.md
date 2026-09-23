# Hegelese

**Hic Rhodos, Hic Saltus.**

Hegelese is an experimental functional language design inspired by Hegel and critically informed by Antonio Wolf's writings. It explores how programs can describe the development of their computational concepts: what changes, what is preserved, and what evidence supports those claims.

**Current status:** an executable Hegelese bootstrap interpreter, a finite-process articulated-change checker, and specification proposal v0.3. Real `.hgl` programs now run through a Python parser and bounded functional evaluator. The bootstrap is dynamically checked; static typing, a compiler, general proof checking, and self-hosting remain future work. The [bootstrap language guide](BOOTSTRAP.md) defines the implemented syntax; the broader v0.3 examples remain proposals.

## Upheaval

`Aufheben`, `Sublation`, and `Upheaval` are exact aliases for the same Upheaval declaration. The accepted lowercase spellings are `aufheben`, `sublation`, `upheaval`, and `upheave`. Documentation uses **Upheaval**; `upheave` is the preferred verb. All seven spellings execute identically while diagnostics preserve the original spelling.

An Upheaval specifies a development between representations, the occasion for it, and the disposition of earlier commitments. It may address a limitation or rearticulate a successful process. Preservation must name a relation; retaining an old value in a log does not establish semantic preservation.

## Start here

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

The inventory records 51 fully read WordPress articles and two fully read Epoché essays as of 23 September 2026. Further entries are explicitly marked partially read, context-reviewed, or retrieved but unread. Full online corpus reading remains incomplete. Author interpretations, engineering proposals, and executed checks are distinguished in the documents.

The repository contains our specifications, research notes, source links, and inventory metadata. Downloaded copies of third-party articles and personal backup metadata are not included. Source authors are not represented as endorsing this project.
