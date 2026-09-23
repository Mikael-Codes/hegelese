# Hegelese v0.3: validation and limits

23 September 2026.

## What ran

The [Python reference experiment](process-reflection-reference.py) executed successfully and produced [the recorded results](process-reflection-results.json). It evaluates finite deterministic transition tables with one input, `tick`, and a declared parity observation. It is not a Hegelese parser, interpreter, compiler, general proof checker, or implementation of philosophical reflection.

| Candidate | Scope | Actual result |
|---|---|---|
| Four-phase counter → parity toggle | Initial-state equation, 4 transition equations, 4 observation equations: 9 checks | All pass; `ExhaustivelyChecked` for the declared finite domain |
| Three-phase counter → parity toggle | Initial-state equation, 3 transition equations, 3 observation equations: 7 checks | Refuted at state 2: mapped successor is 0, target successor is 1 |
| Four-phase counter → toggle starting at 1 | Initial-state equation, 4 transition equations, 4 observation equations: 9 checks | Refuted by initial-state mismatch |

Additional assertions confirm that the invalid three-phase abstraction agrees on its first two ticks and disagrees at the third; and that the valid four-phase map identifies states 0 and 2, so it cannot support lossless reconstruction of the exact phase. An eight-tick four-phase trace is recorded as an example of productive recurrence.

All experiment assertions passed. The two refuted candidates are expected results, demonstrating that the checks reject substantive errors. The scope includes all states declared in these small tables, rather than only the states encountered in the sample run.

## What the results mean

The valid result checks finite local equations. The specification separately explains the induction from those equations to preservation over all finite tick sequences. That induction was not submitted to a proof assistant. The implementation records `ExhaustivelyChecked`, not a fabricated general proof status.

No claim about timing, resource use, other observations, nondeterministic systems, arbitrary functions, infinite state spaces, or a uniquely necessary abstraction was tested. The abstraction and its observation criterion were supplied explicitly.

## Earlier checks

The unchanged counting/differences and keyword-normalization experiments are described in [the earlier validation report](validation.md). That report records 19,278 finite arithmetic checks and 14 alias-context cases. Those historical results are not execution of the expanded v0.3 proposal. No new parser-level alias claim has been added.

## Document and coverage consistency

The updated inventory records 51 full WordPress articles, two passage-reviewed WordPress articles, three index/context entries, and 132 retrieved-but-unread entries, totaling 188. The full WordPress text count is 144,788 words out of 479,198 retrieved words, about 30.2%. Two external Epoché essays are additionally fully read; a third remains passage-reviewed.

The second pass adds 28 articles and 93,116 words. All 41 selected reading chunks were reviewed; an output-truncated tail was retrieved separately. Downloaded documents, video metadata, and search snippets were not promoted to completed reading. Failed video/playlist fetches are recorded explicitly.

The v0.3 specification retains the exact motto and all seven accepted Upheaval spellings. Local links in the new specification, reflection, and validation report were checked for existing targets. The old specification is retained to make the revision reviewable.
