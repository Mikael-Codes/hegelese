# Provisional related-work comparison

Prepared 24 September 2026. This is a focused comparison, not an exhaustive
literature review or novelty finding. Source scope is indicated below.

| Existing approach | Established overlap | Question remaining for Hegelese |
| --- | --- | --- |
| Differential verification | Relational properties between program versions | Does explicit loss/authority history improve the revision process? |
| Property-based testing with replay | Generated counterexamples, shrinking, retained failures | Does loss accounting reveal useful concerns outside the nominated observations? |
| Symbolic authorization analysis | Equivalence and permission changes across policies | Is there useful generality or review value beyond policy comparison? |
| Verifier-guided agent synthesis | Candidate generation, checked requirements, repair feedback | Does the revision protocol add value beyond a protected target and feedback? |

[SymDiff](https://www.microsoft.com/en-us/research/project/symdiff-differential-program-verifier/)
checks differential and relational properties over program versions. Its project
page was reviewed; the implementation and literature were not exhaustively audited.
Hegelese cannot claim that comparing old and new programs is new.

[Hypothesis](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)
retains and replays failures. Its documentation was reviewed. Remembering
counterexamples is not a novel distinction, and a fair baseline must remember.

[Cedar Analysis](https://aws.amazon.com/blogs/opensource/introducing-cedar-analysis-open-source-tools-for-verifying-authorization-policies/)
uses symbolic policy analysis to compare equivalence and permissiveness. The
official technical overview was reviewed. Authorization analysis is not merely a
repository write-permission check. We have not run Cedar against our examples.

[AutoCedar](https://arxiv.org/abs/2607.03656) describes reviewed intent, a fixed
checkable target, candidate policy synthesis and verifier feedback. Only its
abstract was reviewed in this comparison; its reported results have not been
independently reproduced. It is a particularly close conceptual comparator and
requires full-paper and artifact review before asserting a difference.

## Larger conceptual question

The ambitious question is whether a system can make the consequences and limits
of its own revisions available as content that constrains further development.
The current finite protocol is only one operational foothold. It does not show
that the system develops concepts autonomously or that Hegel's logic has been
formalized. More capable revision could require changing the observation vocabulary,
requirements and representation together, with explicit accounts of who authorizes
those changes and what evidence transfers. Those are research questions.

A successful result could be an ergonomic protocol on top of existing verifiers,
not a new logic or language. A null result could show that a conventional protected
ledger supplies the same benefit. Both outcomes should be allowed by the study.
