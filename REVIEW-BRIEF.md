# Hegelese: a short invitation to critical review

**Question:** Can a system make its own revisions accountable by deriving what a
change loses and carrying the consequences of criticism into its next attempt?

The larger ambition is to support more capable AI-assisted conceptual and software
revision while keeping human correction effective. A system should be able to
change its representation, but also make the implications intelligible, distinguish
repair from relinquishment, and remain answerable to earlier objections. Hegel is
an intellectual source for this research question. The implementation is a narrow
engineering interpretation, not a computational realization of his philosophy.

## What runs today

Hegelese has a Python functional-language bootstrap and a finite change checker.
For a supplied source, target and state map, it checks preservation equations,
computes merged source-state groups, and can require explicit accounting for
current and historical findings. The caller retains the request and history.
Earlier retained observations cannot simply disappear from subsequent checks.

Three claims must remain distinct: a map erases a distinction; a required behavior
is preserved; a caller authorizes a loss. None implies the others. The precise
[guarantees and boundaries](docs/revision-guarantees.md) are written separately.
There is no SMT backend, infinite-state type system, or general proof-carrying-code
claim. History is currently limited to revisions against one fixed source/request.

## Evidence so far

The [workflow comparison](experiments/README.md) and
[synthetic evaluation runner](experiments/EVALUATION-RUNNER.md) are reproducible.
Both Hegelese and an independently implemented finite behavioral checker reject
our constructed behavioral violations. In the runner, ungated policies disclose a
synthetic reference, alter scoring, or turn a refusal into disclosure on retry;
both gates refuse installation. A harmless merger is accepted by Hegelese after
caller authorization. **No Hegelese-specific safety or efficiency advantage is
established.** These are hand-authored cases, not fresh-agent trials or independent
validation. The runner is a trusted-host API demonstration, not an OS sandbox.

## What may be distinctive—and may not be

The candidate contribution is an integrated account of structural loss, inherited
obligations and authority across revisions, potentially improving explanation and
review as well as correctness. Existing verification plus a protected requirements
ledger may provide the same benefit more simply. The [related-work comparison](docs/related-work-comparison.md)
is deliberately provisional. Practical value, originality and the need for a new
language are all open questions.

## Questions for a short review

1. Are the stated guarantees correct, and what is the smallest counterexample to
   an overstatement or implementation assumption?
2. What does this add to differential verification plus protected requirements,
   regression counterexamples and explicit authorization? Which prior work is closest?
3. When does a structural loss help a reviewer discover a consequential omission,
   and when does it merely report an irrelevant implementation distinction?
4. How should an authorized change to a mistaken earlier requirement preserve its
   history without making that requirement eternally binding?
5. What experiment could separate the value of loss reports, inherited obligations
   and authority handling? What outcome would justify abandoning the added mechanism?
6. Does the Hegelian interpretation suggest a productive missing mechanism, or
   obscure an already adequate technical account? Please identify the exact step.

A useful response is one counterexample, a better baseline, a reference, or a
suggested experiment. No endorsement is requested. Feedback will only be publicly
attributed with permission.
