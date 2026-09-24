# Revision guarantees and their scope

This is an analytic description of the current implementation, not a mechanized
proof of the checker. See [hgl_lineage.py](../hgl_lineage.py) and its tests.

## Representation and preservation

Let S and T be finite state sets, I their shared input alphabet, and m:S→T a total
map. With initial states s0,t0 and transition functions δS,δT, retained equations are:

- m(s0)=t0.
- For every s∈S and i∈I, m(δS(s,i))=δT(m(s),i).
- For each retained observation fS,fT and every s∈S, fS(s)=fT(m(s)).

Initial and step commitments are mandatory. Required observations cannot be
withdrawn. Observation comparison distinguishes supported JSON value types.
With these equations, induction on input-sequence length establishes mapped-state
agreement and retained observation equality along all finite input traces.
This mathematical implication assumes the supplied transition tables faithfully
specify execution; it is not a proof of Python correctness or external reality.
The implementation checks all declared source states, including unreachable ones.
The independent comparison baseline checks reachable state pairs instead, so the
methods need not agree on unrelated or unreachable internal structure.

## Structural loss

A map fiber is {s∈S | m(s)=t}. A fiber with more than one member loses state-identity
distinctions. An observation f on S can be recovered by some g on the image of m
exactly when it is constant on every fiber. Necessity follows from equality of
mapped states; sufficiency follows by defining g(m(s))=f(s). This does not prove
the candidate implements g; the observation equations test that separately.
A merger need not lose required behavior or constitute a safety violation.

## Historical obligations

For a fixed caller-owned request and validated finite history H, the protocol
collects observations marked retained in any prior or current proposal. Acceptance
requires their equations to hold in the current target, including observations
that the current proposal marks withdrawn. A missing target observation fails.
Historical structural groups are rederived; their IDs bind the source and group,
not a target label. Current groups are added. Every group requires a resolution:

- Repair: the current map is injective on the entire historical group.
- Accept loss: the caller's retained history authorizes that finding.
- Carry: unresolved, so acceptance is withheld.

Authorization of structural loss does not waive mandatory or inherited observation
equations. Current code has no operation to revoke an inherited observation
obligation. Assumptions from historical proposals also accumulate and prevent
acceptance; prose does not discharge them. Resource exhaustion withholds acceptance.

These claims assume honest host retention of the full history and exclusive host
control of authorizations. Hashes detect mismatched inputs, not forgery by a host
or agent that controls the trusted store. The function returns next history; it
does not independently secure or persist it. Fewer than 32 prior attempts are
supported. Cross-source migration and general proof transport are unimplemented.

## Legitimate requirement change: open design problem

An earlier commitment may be mistaken. Current behavior is conservative refusal,
not a complete account of justified revision. A prospective protocol should bind
an explicit host-authorized amendment to the exact old request, replacement request,
retired obligations, reasons and fresh checks. It should preserve the historical
claim and mark its changed authority, rather than erase it or pretend it was proved.
The amendment must not be an agent-controlled way to reset constraints. We have
not implemented or established the sufficiency of this design. It is a review
question, not a feature announcement.

## Safety connection

A trusted dispatcher can install only accepted snapshots and execute exactly the
checked tables. The synthetic runner demonstrates this link for selected effects.
Its host, checker, event classification, scorer and process boundary are trusted.
It cannot establish that requirements are morally or operationally appropriate,
that arbitrary code has no other effects, or that a sandbox cannot be escaped.
An actual benefit over conventional protected verification remains unmeasured.
