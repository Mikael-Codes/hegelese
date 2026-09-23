# Changes

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
