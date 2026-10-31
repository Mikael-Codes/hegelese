# Reference reconstruction verifier

`verify-derived.py` is an unchanged copy from version 2 of *Sharp reconstruction for truncated binary-cut diagrams*.

- [Published source](https://autio.github.io/ai-science/binary-cut-reconstruction/source/checks/verify-derived.py)
- [Immutable repository source](https://github.com/Autio/autio.github.io/blob/81196c9640ba8fa3f75b35a12d0756de4e411462/ai-science/binary-cut-reconstruction/source/checks/verify-derived.py)
- SHA-256: `e072aa39bca31a86548776fea1960c2567aa873a7d9bbd9c84ecb0844864a11b`

The bridge imports its exact finite-complex construction and independently constructs the comparison matrices. It does not call the reference verifier's predicted-dimension formula. Both programs use only Python's standard library.
