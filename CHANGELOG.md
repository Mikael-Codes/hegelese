# Changes

## 0.3.0 — derived loss and accountable revision

- Compute erased state distinctions from map fibers, without requiring named observations.
- Report nonrecoverable declared observations with witnesses, preserving typed values.
- Add opt-in successor checking against independently retained revision history.
- Verify whole-group repairs, require caller authorization for accepted losses, and keep unresolved findings visible.
- Recheck inherited observations; preserve earlier assumptions and prevent truncated-history substitution against a retained parent.
- Add a runnable two-milestone demonstration and adversarial regression tests.
- Keep the existing finite-check and workflow-gate acceptance rules; lineage enforcement is opt-in.

This is fixed-source revision accounting, not cross-source proof transport or automatic discovery of all behavioral invariants.

## 0.2.0 — first CI deployment profile

- Installable wheel with `hegelese` and `hegelese-gate`; no runtime dependencies.
- Independently retained request checking for candidate Hegelese developments.
- Fail-closed exit codes, atomic reports, worker deadlines, and Linux resource limits.
- Documentation-publishing pilot with 36 finite obligations.
- GitHub gate with separate reviewed-engine and candidate checkouts, pinned actions, read-only permissions, and evidence artifacts.
- Installed-package smoke tests on Python 3.10 and 3.12.
- Fixed recursive aliases mutating previously created closure environments: `let rec` now requires a function literal.
- Reject lone-surrogate string escapes before UTF-8 hashing or output.

The language remains dynamically checked. This release does not claim a general proof system, a hostile-code security sandbox, or integration with an external production application.
