# Hegelese under critical reflection

**Hic Rhodos, Hic Saltus.**

23 September 2026. This is a provisional critique of the initial language proposal, informed by a substantial but incomplete reading of Antonio Wolf’s public work. The [reading ledger](reading-coverage.md) distinguishes fully read texts from consulted passages and merely retrieved documents. This is not Wolf’s endorsement of Hegelese.

## 1. The initial abstraction was too weak

The initial proposal joined immutable data, structured limitations, migrations, and preservation tests. It called the result dialectical development. Much of that is useful software design, but the name outran the mechanism.

The strongest objection encountered in Wolf is that independently selected terms and predicates do not become a concept merely through their collection. The relationships have to do explanatory work. His short critique of conceptual nonsequiturs makes this objection especially direct. [Hegel’s Critique of Formalism: Conceptual Nonsequiturs](https://empyreantrail.wordpress.com/2023/11/09/hegels-critique-of-formalism-conceptual-nonsequiturs/)

**Revision:** a development must address an identified limitation, account for its dependencies, and relate operations and commitments. A log retaining the old value is insufficient. This strengthens the engineering model while leaving its philosophical adequacy disputable.

## 2. Activity before labels

Wolf presents concepts through the activity they articulate and enact. In his comparison of Fichte and Hegel, the emphasis falls on thinking and self-relation rather than a private dictionary of stipulated names. [Fichte and Hegel On The Definition of Concepts](https://epochemagazine.org/40/fichte-and-hegel-on-the-definition-of-concepts/)

**Revision:** a concept package must expose operations, observations, and their claimed relations. This keeps the language functional in a substantive way: transformations operate on structured computations, not only strings describing ideas.

**Limit:** a programming interface remains stipulated. Making it operational does not establish that its distinctions were philosophically necessary. Hegelese must make that limitation visible instead of treating executability as an adequate theory of meaning.

## 3. Contradiction cannot be reduced to disagreement

Wolf distinguishes externally composed opposition from a development revealed through the content under examination. His account also treats contradiction as a moment within a larger philosophical activity rather than its sole purpose. [Hegelian Dialectic vs Formal Dialectic](https://empyreantrail.wordpress.com/2024/01/09/contradictio-est-regula-veri-hegelian-dialectic-vs-formal-dialectic/)

**Revision:** the original four-way `Evidence` data type belongs in a library. Disagreeing sources are a practical epistemic problem; their co-presence does not supply an immanent contradiction. A limitation record must state which demand failed, where that demand came from, and what the failure establishes.

**Limit:** preserving conventional type soundness is a deliberate engineering decision. Representing contradiction as analyzed content does not resolve philosophical disputes about contradiction or turn Hegelese into a complete formalization of speculative logic.

## 4. Immanence requires scrutiny of premises

In Wolf’s distinction between external reflection and immanence, the decisive issue is whether the movement imports something not warranted at the point of inquiry. Reflection is not prohibited wholesale; its resources matter. [Dialectics of External Reflection & Immanence](https://empyreantrail.wordpress.com/2017/08/17/dialectics-of-reflection-immanence/)

**Revision:** every construction carries a dependency account. A new application requirement is labeled as such. The counting example therefore says explicitly that demanding inverses is an additional commitment, rather than pretending that natural-number addition contradicts itself.

**Limit:** dependency closure is weaker than philosophical immanence. A closed derivation from poorly chosen definitions can still be philosophically empty. The specification forbids a boolean “immanent” annotation from conferring authority.

## 5. Preservation is contextual, and developments differ

Wolf’s treatment of positive and negative dialectics distinguishes the preservation of limited determinations from the overcoming of forms whose truth does not coincide with their initial appearance. This challenges a single, universal “keep everything” model of preservation. [Negative and Positive Dialectics](https://empyreantrail.wordpress.com/2017/04/28/negative-and-positive-dialectics/)

**Revision:** each source commitment receives an explicit disposition: retain, restrict, reformulate, or withdraw. Some developments use embeddings. Others require a relation that preserves only specified observations or achievements. The language should permit both without silently treating them as equivalent.

**Limit:** a programming language cannot determine which social commitments deserve preservation from a generic transition combinator. Evaluative judgments and their grounds must remain explicit.

## 6. Negation is not one universal function

Wolf distinguishes abstract, determinate, and absolute negation, giving particular weight to relation and self-operation. His account resists identifying the entire movement with a boolean complement or the arithmetic cancellation of two minus signs. [Hegelian Negations: Abstract, Determinate, & Absolute](https://empyreantrail.wordpress.com/2019/03/21/hegelian-negations-abstract-determinate-absolute/)

**Revision:** retain ordinary boolean `not`, numeric negation, and typed failure as separate operations. Do not introduce a polymorphic `negate : A -> A` and call every instance dialectical. An Upheaval records the specific relation through which a previous commitment is transformed.

**Limit:** adding three differently named negation functions would recreate the problem in a new vocabulary. The relevant distinctions must appear in what programs can express and check.

## 7. Self-reference is not automatically self-development

Wolf’s account of the negation of negation stresses categorial self-operation; his essay on reflection contrasts a static image with the activity of reflexion. Neither reduces to an object possessing a pointer to itself. [Negation of Negation](https://empyreantrail.wordpress.com/2018/03/27/sublation-negation-of-negation/), [On Reflection and Reflex](https://empyreantrail.wordpress.com/2017/08/27/sublation-reflection-speculation/)

**Revision:** a self-describing syntax tree, recursive function, or self-hosted compiler cannot by itself satisfy an Upheaval obligation. Staged reflection may inspect and propose revisions to specifications, but the revisions require checking under an explicit semantics.

**Limit:** the fixed evaluator and checking rules remain an external framework in a philosophically important sense. We must not conceal that fact behind the phrase “the program develops itself.”

## 8. Circularity needs an account of the circuit

Wolf distinguishes empty repetition, assuming a conclusion, and a content-dependent return to a beginning through articulated development. [On Epistemic Circularity](https://empyreantrail.wordpress.com/2024/12/10/on-epistemic-circularity/)

**Revision:** encountering a previously seen state returns `CycleDetected`, not “Absolute achieved.” Any claim about a productive recurrent system needs its own evidence. No target specification may validate its construction merely by referring back to itself.

**Limit:** formal techniques for reasoning about recursive or ongoing computations may eventually be useful, but their applicability must be established separately. A philosophical analogy is not a soundness argument.

## 9. Logical and empirical claims have different warrants

Wolf cautions against applying dialectical terminology indiscriminately to contingent objects and events. His criticism of a coal-mine/power-plant “dialectic” is particularly relevant to our temptation to rename any software workflow. [The Limits of Dialectics](https://epochemagazine.org/10/the-limits-of-dialectics-logical-necessity-and-empirical-contingency/)

**Revision:** distinguish observations, assumptions, finite tests, exhaustive finite checks, and proofs relative to premises. A sensor conflict cannot generate a guaranteed theory revision. A universal conditional cannot determine an unobserved contingent fact.

**Limit:** the author’s broader metaphysical conclusions do not become compiler axioms. Our assurance levels report evidence within the language’s specified scope.

## 10. A completed run is not Absolute Knowing

Wolf’s writing connects philosophical comprehension to recollection of development, and distinguishes a future within known categories from a genuinely new categorical development. [Why Philosophy Cannot Guide the Future](https://empyreantrail.wordpress.com/2019/05/13/why-philosophy-cannot-guide-the-future/)

**Revision:** replace unqualified stability with a named stopping criterion. Explanations reconstruct actual dependency relations after execution without fabricating a necessary path or claiming that no future development is possible.

**Limit:** this is not a prohibition on predictive models, simulations, or hypothesis generation. Those remain useful computational practices with their own warrants.

## 11. Test cases and category criticism are different

Wolf’s recent critique of hypotheticals differentiates testing particulars within categories from examining those categories themselves. [Against Hypotheticals](https://empyreantrail.wordpress.com/2026/08/23/against-hypotheticals/)

**Revision:** distinguish a counterexample to an implementation’s declared law from an argument about whether the declaration itself is adequate. A thousand successful cases cannot establish that the chosen concept captures the intended problem.

**Critical disagreement:** Hegelese remains an engineering language. Hypothetical inputs, counterfactual models, and property-based testing are valid tools for it. We adopt the distinction without turning Wolf’s restriction on philosophical hypotheticals into a restriction on programming.

## 12. Terminology should reveal structure without determining truth

Wolf’s discussions of term names and speculative English encourage vocabulary that helps readers follow related activities. His technology essay also explicitly distinguishes etymological illumination from determination of a concept. [Terming Conventions](https://empyreantrail.wordpress.com/2020/07/19/whats-in-a-term-name-hegels-terming-conventions/), [Speculative English](https://empyreantrail.wordpress.com/2026/07/21/speculative-english-how-language-thinks/), [The Idea of Technology](https://empyreantrail.wordpress.com/2024/01/01/the-idea-of-technology/)

**Revision:** prefer Upheaval in explanatory prose and honor `Aufheben`, `Sublation`, and `Upheaval` as exact language aliases. This equivalence is a language-design decision explicitly requested by the user. It is not a claim that the words have identical histories or everyday connotations.

**Limit:** etymological associations are not inference rules. Even a beautifully named construct needs precise behavior and useful examples.

## 13. Constraints can enable agency

Wolf’s account of degrees of freedom distinguishes removing all limitation from acting through determinate enabling conditions. [The Conceptual Degrees of Freedom](https://empyreantrail.wordpress.com/2022/05/06/the-conceptual-degrees-of-freedom/)

**Revision:** visible types, explicit effects, and declared obligations can support a programmer’s ability to act and understand consequences. Reflection should offer accountable change rather than an unrestricted escape from the language’s checks.

**Limit:** the practical value of those constraints is an empirical design question. A type system is not thereby a realization of absolute freedom.

## 14. Open systems do not imply arbitrary successors

Wolf’s Open Hegelianism considers historically situated systems and relations among them while continuing to insist on standards of adequacy. It cannot simply be reduced to “all perspectives are equally valid.” [Open Hegelianism: Alternate Modernities](https://empyreantrail.wordpress.com/2022/05/28/open-hegelianism-alternate-modernities/)

**Revision:** multiple candidate developments may be represented, with their commitments and evidence available for comparison. If the language has no justified selection rule, it returns ambiguity instead of inventing a uniquely necessary successor.

**Limit:** the specification does not adopt the essay’s comparative civilizational judgments. They are unnecessary to the computational proposal and would require their own historical assessment.

## 15. The critique must apply to the language itself

Wolf’s account of formalism grants its practical usefulness while questioning whether formal consistency alone captures the content of reasoning. [A Hegelian View On Formalism](https://empyreantrail.wordpress.com/2023/11/22/on-formalism-laws-of-thought/)

Our unavoidable tension is now explicit: Hegelese proposes formal machinery partly inspired by a criticism of the sufficiency of formal machinery. The honest response is to delimit its claims and expose its choices to criticism, not to declare the tension solved by a new keyword.

The successor specification therefore keeps three questions distinct:

1. Does this program follow the rules of the language?
2. Does the proposed development satisfy its stated obligations?
3. Are those rules, representations, and obligations adequate to the problem?

The first two can increasingly be supported by machines. The third remains an open site of inquiry, including inquiry into Hegelese itself.

## Decision record

| Earlier draft | Revision |
|---|---|
| Motto about preserving and exposing | **Hic Rhodos, Hic Saltus.** |
| Replacement of German/academic terminology | One keyword with exact aliases; Upheaval is preferred prose |
| Conflict as central mechanism | Development of representations and operations, grounded in explicit demands |
| Standpoint as foundation | Standpoint as scoped interpretation; concept packages describe operational commitments |
| Preservation of data sufficient | Explicit preservation/restriction/reformulation/withdrawal of commitments |
| Runtime checks as main warrant | Evidence classified by scope and assumptions |
| Repeat until stable | Named stopping criteria; ambiguity, cycles, and exhaustion remain distinct |
| History as evidence of development | History plus dependency account; a trace alone proves little |
| Authorship migration as flagship | Useful application example; counting/differences is a stronger test case |
| New-language value assumed | Compare against a strong typed functional library implementation |

The full-corpus review remains open. The long commentaries and remaining ethics, aesthetics, history, religion, nature, and comparative-philosophy writings may reveal further objections; the coverage ledger records them as unread rather than silently treating them as irrelevant.
