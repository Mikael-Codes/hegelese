# Reciprocity without losing causality: a research connection

Related preprint, version 1, 7 November 2026, by Petri Mikael Autio:

- [Explanatory page and interactive example](https://autio.github.io/ai-science/reciprocal-causal-abstraction/)
- [Preprint PDF](https://autio.github.io/ai-science/reciprocal-causal-abstraction/reciprocity-preprint.pdf)
- [Proofs, checkers, results and prior-work audit](https://autio.github.io/ai-science/reciprocal-causal-abstraction/research-source.zip)

**Status:** a mathematical research connection and proposed checking obligation. Hegelese's current language, finite-process checker and lineage protocol are unchanged. The paper has complete proofs, exact finite checks and internal AI reviews; historical priority and external mathematical review remain open.

## Why it belongs near Hegelese

Hegelese makes changes of representation answerable to stated preservation claims. Its current finite-process checks include commutation of a transition with the map between representations. The preprint studies a further question for a different semantics: if components are connected by simultaneous causal equations, when does local mechanism commutation preserve their joint solutions under intervention?

That distinction matters. A coarse description may correctly represent every update step while turning hidden motion into an apparent equilibrium. The paper's two-component example has fine values 0, 1 and 2. One component copies the other; the second keeps 0 and exchanges 1 with 2. Their only equilibrium is (0, 0). Merging 1 and 2 into ON creates an additional coarse equilibrium, (ON, ON), which has no fine equilibrium behind it.

This does not expose an error in the existing process checker: it demonstrates that causal equilibrium preservation is an additional obligation with its own semantics and assumptions.

## The result that a future certificate could use

Fix finite nonempty component state sets, a surjection for each component, and a loopless graph of allowed mechanism dependencies. Require exact componentwise commutation. Assume separately that the fine system has exactly one solution after every point intervention, including no intervention. A point intervention fixes selected components and replaces their equations.

Classify each component map as injective (all distinctions retained), constant (all distinctions erased), or partial (neither injective nor constant). The theorem proves:

> Every compatible simple fine system preserves its unique solutions under all matched point interventions if and only if the graph induced by partial components has no directed cycle.

The universal quantifier is essential. A partial cycle means that the graph and interface alone do not guarantee preservation for every compatible system. An installed system with such a cycle may still be correct. The theorem does not establish fine simplicity or dynamic convergence.

## Proposed checking obligations

A future Hegelese research extension could:

1. Declare the component state sets, actual mechanisms, interface maps and allowed dependency graph.
2. Check surjectivity, the graph's dependency bounds and all local commuting equations.
3. Require independent evidence of unique fine solutions under every point intervention.
4. Apply the partial-cycle criterion to certify exact transport of those solutions.
5. Distinguish a failed structural guarantee from an actual counterexample in the installed system, and keep unfinished checks unresolved.

The graph check does not make the full process inexpensive: establishing fine simplicity can require substantial work. No scalable implementation or measured programming benefit is claimed by this paper.

## Why retaining an output can require retaining its inputs

For upgrades that either retain an entire coordinate or leave its old map unchanged, the paper proves an exact descent criterion. If a fully retained output distinguishes two input values that the interface still merges, that input must also be retained. Valid upgrade sets are closed under these hidden-input predecessors.

Combining this closure with elimination of all remaining partial cycles gives a certificate whose minimum cost can be formulated exactly. In the two-component example, retaining one component breaks the partial cycle but fails descent; both must be retained. The optimization covers these whole-coordinate certificates, not every valid abstraction or every intermediate state partition.

A checker could explain such a failure with the two fine input states witnessing it. This fits Hegelese's interest in making discovered losses and failed preservation claims consequential for later proposals. The theorem does not itself decide whether an application is authorized to discard an observation.

## Hegelian inspiration and limits

The question arose from the [Hegel Reader](https://autio.github.io/hegel-reader/#day-93) and was checked against Hegel's [Encyclopaedia, §§154–159, especially §156 and its Addition](https://www.marxists.org/reference/archive/hegel/works/sl/slactual.htm). The relevant demand is to understand the mediation of reciprocally related sides within their whole. The paper turns one aspect of that demand into an explicit preservation problem.

The finite state spaces, product maps, intervention operation and uniqueness assumption are the researchers' choices. The result does not derive a new representation immanently, identify erasure with sublation, or define Hegel's Concept or freedom. It supplies a precise theorem that can inform one proposed engineering obligation.

The general paper and its source archive live with the research publication. This repository note provides the language-specific connection. Future executable feedback experiments can be added separately once their semantics, evidence format and limitations are specified.
