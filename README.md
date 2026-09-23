# Hegelese

**Hic Rhodos, Hic Saltus.**

Hegelese is an experimental functional language design inspired by Hegel and critically informed by Antonio Wolf's writings. It explores how programs can describe the development of their computational concepts: what changes, what is preserved, and what evidence supports those claims.

**Current status:** specification v0.3 and an executable Python semantic experiment. There is no Hegelese parser, interpreter, compiler, or general proof checker yet. Hegelese syntax in the specification is proposed syntax.

## Upheaval

`Aufheben`, `Sublation`, and `Upheaval` are exact aliases for one proposed language construct. The accepted lowercase spellings are `aufheben`, `sublation`, `upheaval`, and `upheave`. Documentation uses **Upheaval**; `upheave` is the preferred verb.

An Upheaval specifies a development between representations, the occasion for it, and the disposition of earlier commitments. It may address a limitation or rearticulate a successful process. Preservation must name a relation; retaining an old value in a log does not establish semantic preservation.

## Start here

- [Language specification v0.3](docs/hegelese-spec-v0.3.md)
- [Critical reflection from the second corpus reading](docs/critical-reflection-v0.3.md)
- [Reading inventory and coverage](docs/reading-coverage.md), also available as [JSON](docs/reading-coverage.json)
- [Implementation and self-hosting roadmap](ROADMAP.md)
- [Reference experiment validation](docs/validation-v0.3.md)

The earlier [v0.2 specification](docs/hegelese-spec-v0.2.md) and [first critical reflection](docs/critical-reflection.md) preserve the design's history.

## Run the experiment

Requires Python 3.10 or later; no third-party packages.

```sh
python3 docs/process-reflection-reference.py
python3 -m unittest discover -s tests -v
```

The experiment checks whether a finite cyclic counter can be represented by a parity toggle. The four-phase counter admits this abstraction; the three-phase counter fails at its wraparound transition. A wrong initial state is rejected separately. Passing checks cover the specified finite domain and observations.

This is a semantic design experiment, not execution of a Hegelese program. The output distinguishes exhaustive finite checks from refutations. A short trace does not establish all future behavior, and an abstraction supplied by a programmer is not automatically a philosophically necessary development.

## Toward an implementation in Hegelese

Python is the proposed bootstrap implementation language. An interpreter written in Hegelese is an explicit subsequent milestone. We intend to define language behavior independently of Python and keep host services behind a small boundary, so that both implementations can share conformance tests.

Self-interpretation and a self-hosting compiler are separate milestones. Neither is a claim of philosophical self-grounding.

## Research provenance

The inventory records 51 fully read WordPress articles and two fully read Epoché essays as of 23 September 2026. Further entries are explicitly marked partially read, context-reviewed, or retrieved but unread. Full online corpus reading remains incomplete. Author interpretations, engineering proposals, and executed checks are distinguished in the documents.

The repository contains our specifications, research notes, source links, and inventory metadata. Downloaded copies of third-party articles and personal backup metadata are not included. Source authors are not represented as endorsing this project.
