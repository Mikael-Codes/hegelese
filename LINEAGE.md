# Derived loss and accountable revision

Implemented in Hegelese 0.3.0. These are finite engineering mechanisms inspired by the criticism that an author should not be the sole judge of what a change loses. They are not claims to have implemented Hegel's determinate negation or negation of negation.

## Two executable milestones

Run from the repository root:

```sh
python3 examples/lineage_demo.py
```

Expected output:

```text
ordinary preservation check: ExhaustivelyChecked
computed losses, with NO named observations: [['0', '2'], ['1', '3']]
unaccounted losses: Unknown
repaired map, but forgotten accounting: Unknown
repaired successor: ExhaustivelyChecked
The repair preserves four states; it does not claim the original compression succeeded.
```

The example removes every named observation from the four-phase process. The ordinary transition equations still pass. Nevertheless, the checker derives two erased distinctions from the map itself. A successor with an injective map cannot quietly forget the findings: it must account for them, and the checker verifies its repair over each entire historical group. The example caller retains every attempt, including unsuccessful ones.

This is a conservative repair, not a discovery that compression is always wrong. Keeping a lossy abstraction is also possible when the caller explicitly authorizes the particular losses and the preservation equations still hold.

## What the structural analysis establishes

Every ordinary `check`, including checks reached through `.hgl`, now returns `structural_loss`. The checker groups source states by their mapped target state. A group of size n represents n(n−1)/2 erased state-identity distinctions. Groups are compact; the report does not enumerate a quadratic list of pairs. It includes a witness and examines every declared source observation for variation within the group, regardless of its retain/withdraw disposition.

For any source-state observation f, a target-state function g with f = g ∘ mapping exists on the mapped states exactly when f is constant within each group. The checker reports witnesses for declared observations that fail this condition. Constancy establishes that such a function exists; it does not establish that the target's actual implementation supplies that function. The ordinary observation equation checks that separately.

The groups themselves require **no declared observation vocabulary**. This is an exact description of state-identity loss under the proposed map. It is not automatic extraction of all meaningful behavioral invariants, proof that every lost distinction matters, or proof that no alternative encoding could preserve it. All declared states, including unreachable states, are in scope. There is no timing, external environment, or history-sensitive observation model.

Finding IDs bind the source and the sorted source group, not the target state's name. Renaming the target cannot make the same finding disappear. Changed groups create new findings while old groups remain in the lineage.

Ordinary checking continues to accept valid lossy abstractions and reports the discovered losses. **The stronger accounting requirement is opt-in through the lineage protocol.** The existing workflow gate does not enforce lineage history automatically.

## Successor protocol

Python API:

```python
from hgl_lineage import empty_history, successor, check_lineage

history = empty_history(request)  # retained by the caller, outside the proposer
candidate = successor(proposal, history, resolutions={})
report = check_lineage(request, candidate, history)
history = report["next_history"]  # retain Unknown and Refuted attempts too
```

Only structurally valid candidate inputs produce `next_history`; `Invalid` input is rejected without entering the semantic history. A host may separately log those rejected submissions.

The same interface is available as JSON:

```sh
python3 hegelese.py lineage request.json candidate.json history.json --budget 100000
```

The successor has exactly four fields:

| Field | Meaning |
| --- | --- |
| `schema` | `hegelese-successor/0.1` |
| `history_sha256` | Exact fingerprint of the caller's independently retained history |
| `proposal` | Ordinary `hegelese-proposal/0.1` Upheaval proposal |
| `resolutions` | Finding ID → `{action, reason}` |

The history has `schema: "hegelese-lineage/0.1"`, `request_sha256`, `attempts`, and `authorized_losses`. Each attempt retains `proposal`, `budget`, and `resolutions`, preserving previous declarations and their explanations. Authorizations map particular finding IDs to nonempty caller-supplied reasons.

The successor is an implemented interchange artifact, not new `.hgl` grammar. The CLI and Python API execute it today; a dedicated language declaration is future work.

## How history changes acceptance

The checker validates historical inputs again and derives their findings again. It does not import a report's claimed status. Every historical merger group, plus every current merger group, becomes an accounting obligation in the successor.

| Resolution | Required evidence or authority | Outcome |
| --- | --- | --- |
| `repair` | Current map separates **every pair** in the old group | Repaired, or Refuted with a collision witness |
| `carry` | Explicit acknowledgment that the issue remains unresolved | Unknown |
| `accept_loss` | The caller's `authorized_losses` contains this exact finding ID | AuthorizedLoss; otherwise Refuted |
| Missing resolution | No accounting supplied | Unknown |

A host authorization acknowledges the loss; it does not turn it into preservation or excuse a false equation. An old authorization does not automatically cover a new group.

All observations retained by **any** attempt become inherited observation obligations. A successor cannot evade those equations by changing `retain` to `withdraw`. Initial-state and transition equations remain mandatory. Full-domain rechecking covers earlier counterexamples and unfinished checks instead of trusting prior verdicts or patching only one displayed witness. The base and additional inherited equations share a single comparison budget. Exhaustion remains Unknown unless an established failure already makes the result Refuted.

Historical assumptions remain unresolved, even if omitted from a later proposal. This subset has no mechanism to discharge such assumptions with evidence; prose cannot do it. Loss authorizations cannot waive observation obligations or assumptions.

`next_history` includes the current attempt even when its status is Unknown or Refuted. It is returned as data; the checker neither writes it nor applies the proposed program change. The caller must persist it atomically and pass the latest history on the next invocation.

## Trust boundary and limits

The caller must protect the request, history, loss authorizations, and choice of checking mode. A candidate bound to a truncated or different history is rejected when checked against the actual retained history. If the host lets the proposer replace that history, start a new one unnoticed, or invoke only the ordinary checker, this protection is lost. Hashes bind content; they do not supply authentication or storage access controls.

This release handles revisions against **one immutable source and request**. It does not transport proofs across a succession of different source programs or authorize requirement changes. That needs an explicit migration protocol. At most 32 attempts can be recorded; after that, a new check fails closed until a future archival/migration mechanism exists. JSON files retain the CLI's 2 MB input limit.

Structural passes are separate from the equation budget and bounded by the existing limits of 1,000 states and 32 observations per process, plus the attempt limit. The lineage CLI has no production worker deadline or hostile-code sandbox. Do not interpret the comparison budget as a wall-clock or memory bound.

## Philosophical and empirical standing

The practical change is that criticism can supply content the proposer omitted, and that content constrains later attempts. Hegel's discussion of method and the result becoming a new beginning motivates this direction; the [primary-text notes](docs/science-of-logic-essence-concept.md) retain the distinction between textual interpretation and engineering inference.

A merger analysis plus inherited obligations is not a demonstrated philosophical identity with determinate negation. Nor is history length a measure of earned trust: findings can remain unresolved, and old evidence can cease to apply when its scope changes. No comparative AI benchmark has established a reduction in semantic regressions. These milestones make that hypothesis more testable.
