# Documentation workflow pilot

`workflow.hgl` proposes merging editor and owner review into a public review state.
`request.json` is the independently retained contract: public status and publication
permission must be preserved. Internal review routing is explicitly withdrawn.

Run from the repository root:

```sh
python hgl_gate.py pilot/workflow.hgl --request pilot/request.json --report gate-report.json
```

The accepted candidate passes 36 obligations. The regression suite checks that
early publication, weakened requirements, and fabricated reports cannot pass.
This is a finite model, not an integration with an external publishing application.
See [deployment instructions](../DEPLOYMENT.md) for the operational boundary.
