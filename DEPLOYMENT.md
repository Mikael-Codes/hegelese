# First production use: a finite-workflow CI gate

Hegelese 0.2.0 has one narrow deployment profile: a Linux CI job that checks a finite workflow change against a separately retained contract. It is not a public execution service, a general correctness verifier, or a replacement for application tests.

## The pilot

[`pilot/workflow.hgl`](pilot/workflow.hgl) proposes combining `editor_review` and `owner_review` into a public `review` state in a documentation-publishing model. The source has five states and five events; the target has four states. The approved contract requires preservation of `publicStatus` and `canPublish`. The internal review-route distinction is explicitly withdrawn.

The gate checks 36 obligations: one initial-state equation, 25 transitions, and ten observation equations. Allowing publication during review produces a counterexample. This is an included pilot model, not integration with an existing publishing application. For an actual application, validate or generate its model from application behavior and retain integration tests. The checker cannot establish that an inaccurately modeled application behaves like its model.

## Install and run

Use Python 3.10 or later. Build from a reviewed checkout:

```sh
python -m pip wheel --no-deps --wheel-dir dist .
python -m pip install --no-deps dist/hegelese-0.2.0-py3-none-any.whl
hegelese --version
hegelese-gate pilot/workflow.hgl --request pilot/request.json --report gate-report.json
```

There are no runtime dependencies. The build backend is pinned in `pyproject.toml`. CI builds and smoke-tests installed wheels on Python 3.10 and 3.12 from outside the source checkout. Wheels are workflow artifacts; no package has been published to PyPI. Retain the reviewed engine revision and package artifact for rollout and rollback.

The candidate must return the named Upheaval itself, for example `SimplifyReview;`. A precomputed evidence report, a success-looking record, or an ordinary value is rejected. The worker recomputes evidence against the caller's supplied request. The candidate's embedded request fingerprint must match it. Editing the candidate's requirements cannot silently weaken this contract.

| Outcome | Exit | CI action |
|---|---:|---|
| ExhaustivelyChecked | 0 | Pass this finite preservation check |
| Refuted | 1 | Fail; inspect the counterexample |
| Invalid | 2 | Fail; fix candidate, binding, or input |
| Unknown | 3 | Fail; incomplete checks are not acceptance |
| InternalError | 4 | Fail; investigate engine or runner |

Reports contain source location/spelling, content fingerprints, commitments, scope, limits, and counterexamples. `--report` writes atomically; inability to save the required report fails the command. JSON also appears on stdout. Reports are evidence records, not signatures or authorization tokens.

## GitHub deployment and trust boundary

The [gate workflow](.github/workflows/workflow-gate.yml) checks out the engine and approved contract from the PR base commit into `engine/`, and the candidate into `candidate/`. It executes reviewed engine code with candidate Hegelese as language input. It does not install or execute candidate Python. On pushes to `main`, it checks the committed candidate and contract together.

The stable status check is `workflow-gate`. Require it in branch protection or a ruleset to block merges. A workflow file alone does not enforce merge policy. Protect workflow, engine, and contract changes through repository review. Contributors who can change the check itself or bypass repository rules remain trusted. Contract changes need an explicit reviewed migration; do not edit requirements merely to make a failing candidate pass.

Actions are pinned to upstream commits, checkout credentials are not persisted, permissions are read-only, and the gate needs no secrets. Reports are retained for 14 days, including failed checks. Dependency upgrades should update pins through review. These choices follow GitHub's [secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use).

## Operational envelope

- One candidate per disposable worker; no daemon or HTTP endpoint.
- Parent-enforced five-second deadline by default, configurable up to 30 seconds. Timed-out workers are killed and reaped.
- Linux: 256 MiB address-space limit, CPU limit corresponding to the timeout, no core dumps, and 1 MiB output-file limit.
- Source at most 128 KiB; contract at most 256 KiB. Inputs must be regular files; final-component symlinks are rejected on supported POSIX platforms.
- Fuel and check budget default to 100000 each, maximum 1000000. Exhaustion never passes.
- Isolated Python imports, a temporary working directory, and no inherited CI secrets. The language exposes no file, network, import, or shell primitives.

These controls are not an operating-system sandbox against an interpreter exploit. Use disposable CI runners without secrets for external proposals. macOS supports local smoke tests and deadlines; the production memory/CPU profile is Linux. Windows is unvalidated. Public multi-tenant evaluation is outside this release's scope.

## Diagnose and roll back

1. Download `workflow-gate-evidence` from the failed job. Inspect status, source location, request fingerprint, and the first counterexample.
2. For `Refuted`, revise the candidate or explicitly review whether the requirement itself needs revision. Explanation cannot repair a failed equation.
3. For `Unknown`, inspect budget and complexity. Increase bounds only within the reviewed profile, or simplify the proposal.
4. For `InternalError`, rerun once to distinguish a transient runner failure, then inspect engine revision and logs. Never suppress the exit code.
5. Upgrade engine and contract through review, retaining positive and negative tests. Pin consumers to the reviewed artifact or revision.
6. Roll back by restoring the previous engine artifact and matching contract/candidate revisions. The gate changes no application state, so there is no data migration to undo.

Static typing, richer relations, incremental dependency invalidation, and self-hosting remain language milestones. This deployment establishes one useful finite check without claiming those features are finished.
