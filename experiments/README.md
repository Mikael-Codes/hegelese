# Executable workflow comparison

Run from the repository root:

```sh
python3 experiments/workflow_comparison.py
python3 -m unittest discover -s tests -q
```

This is a six-case, hand-authored mechanism comparison, **not an AI benchmark,
independent validation, or a claim of superiority**. Results are in
[workflow-results.json](workflow-results.json).

The example extends the existing synthetic editorial workflow with cancellation.
A small table interpreter executes exactly the finite tables passed to the
checkers. There is no separate hand-translated application model. This closes
that particular modeling gap for this toy runtime; it does not connect the
checker to arbitrary application code, real authentication, concurrent events,
persistence or external effects. Inputs are classified events, not authenticated
users. The demo must not be used as an authorization service.

## A baseline that remembers

The independent baseline explores every reachable pair of old/new states by
breadth-first search and checks the caller's observation requirements. It uses
neither the proposed state mapping nor Hegelese's equations. The host preserves
previously retained observation names outside candidate control. This is an
in-memory harness, not a durable production history store. Every counterexample
is replayed through the table runtime.

This is stronger than sampled regression testing for these finite deterministic
models. Both methods receive the same current and inherited behavioral
obligations. Hegelese additionally requires a source/target map and structural
loss accounting; that extra input and extra policy are not free evidence of
better verification. The baseline does not implement structural-loss consent.

| Case | Behavioral baseline | Hegelese lineage |
| --- | --- | --- |
| Unchanged workflow | Accept | Accept |
| Merge equivalent review routes, no authorization | Accept | Unknown: unaccounted loss |
| Same merge, caller authorizes lost route identity | Accept | Accept |
| Approve directly from draft | Reject | Refute |
| Approve after cancellation | Reject | Refute |
| Remove a previously retained route observation | Reject | Refute |

The cancellation counterexample is `cancel, approve`. In the final case the
ordinary current-proposal finite check passes; **both** methods with retained
requirements reject it. This is evidence that persistent requirements matter,
not evidence that Hegelese uniquely supplies that benefit.

## What this shows and what remains open

A useful lossy abstraction can be permitted. A structural loss is not inherently
a semantic error. The extra authorization step may be useful governance or
unnecessary friction, depending on the application; this comparison cannot decide.

Next, compare against an equally protected requirements and counterexample ledger
with caller-authorized changes. Measure completed valid changes, erroneous
acceptances, needless rejections, specification/approval effort, and cost. Use
externally reviewed tasks, including cases unfavorable to Hegelese. Run a cost
pilot before an LLM experiment. Do not generalize six selected mutations into a
regression-reduction percentage.

The current lineage is still fixed-source/request, bounded to fewer than 32 prior
attempts, and cannot discharge inherited assumptions or transport requirements
across arbitrary source changes. A legitimate requirement-revision protocol is
future work. The experiment uses only standard Python and existing Hegelese code;
no new language syntax or new proof capability was added.

## Synthetic evaluation-runner extension

[Minimum safety mechanism demonstration](EVALUATION-RUNNER.md) connects checked
policy installation to synthetic reference access and scoring effects. Both gates
stop three constructed unsafe policies; no Hegelese-specific advantage is shown.
