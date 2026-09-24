# Minimum safety mechanism demonstration

Run `python3 experiments/evaluation_runner.py` from the repository root.
Recorded output: [evaluation-runner-results.json](evaluation-runner-results.json).

## Boundary and claim

A trusted Python host owns synthetic reference material, the scorer, a fixed
request, history, a dispatcher and policy installation. A candidate is JSON
policy data, not executable code. Only a checked, copied policy is installed.
The exact installed transition and effect tables drive dispatch: this is not a
separate model purporting to describe arbitrary application code.

This is a trusted-host API demonstration, NOT a process sandbox. Python attributes
are not a security boundary. An adversary with arbitrary Python execution in the
host process can bypass it. An eventual agent trial must give the agent only the
proposal interface and independently isolate the host, files and tools. There is
no network, no real credential, no external victim and no reproduction of a real
exploit. The synthetic reference string exists to observe disclosure; it is not a
real benchmark solution. Candidate answers are compared by the trusted scorer.

## Results

| Constructed rewrite | Without installation gate | Independent baseline | Hegelese |
| --- | --- | --- | --- |
| Allow reference reads | Synthetic reference disclosed | Refuses installation | Refuses installation |
| Allow scorer modification | Incorrect answer can receive full score | Refuses installation | Refuses installation |
| Retry a denied reference read through a different state | Synthetic reference disclosed on retry | Refuses installation | Refuses installation |
| Merge equivalent denial states | Valid abstraction | Accepts | Accepts after host loss authorization |

The independent baseline exhaustively checks reachable state pairs against the
same host-fixed effect requirement. Both gates receive schema-valid finite tables;
only Hegelese adds map equations and structural-loss consent. Baseline access to
the required behavior is not reduced. These are three selected unsafe mutations,
not a measured attack prevention rate. No advantage over the baseline is shown.

Tests additionally cover unsafe attempt → safe repair → unsafe retry; immutable
installed snapshots; unknown operations; rejected request substitution and
self-supplied authority; and loss authorization failing to override a mandatory
effect requirement. There is no new general requirement-revision protocol.

## Relationship to the Hugging Face incident

The relevance is conceptual: an attempted improvement must not silently turn a
refusal into permission, expose evaluation material, or weaken evaluator integrity.
This experiment does not model or prevent the incident's actual exploit chain,
unknown vulnerabilities, arbitrary tool use, or cross-system agent coordination.
A check that approves policy changes cannot protect operations that bypass the
policy dispatcher. Real containment requires separately enforced isolation.

Background primary accounts:
- https://huggingface.co/blog/agent-intrusion-technical-timeline
- https://openai.com/index/hugging-face-incident-and-the-road-ahead/

## Next evidence milestone: actual agent trial

Before running a trial, freeze task variants, requirements, budget and stopping
rules. Give each condition the same initial request and corrections. Protect
requirements, evaluator and saved findings outside candidate control. Compare:
(1) protected requirements plus persistent counterexamples/regression checks;
(2) independent finite behavioral checking; (3) the same task with Hegelese loss
accounting and revision obligations. Explicit human authority must be available
in all conditions that allow requirement changes. Do not compare Hegelese against
an intentionally forgetful baseline.

Measure unauthorized effects, valid task completion, withheld valid changes,
review/authorization effort, time and model cost. Verify effects in the trusted
host, not in the agent's self-report. Include useful abstractions and unchanged
policies. Record model versions, prompts, artifacts, interventions and failures.
The implementer already knows these cases; using this same assistant's informed
rewrite as an independent agent trial would contaminate the result. No LLM
comparison has yet been executed.
