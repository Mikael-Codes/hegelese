# Running the Hegelese bridge

Python 3.10 or newer, standard library only. Tested with Python 3.14.7.

The script loads the actual `hegelese.py` from commit
`3199a7fd4d83ab061c5d445d28be6c07edb0d61e` after verifying its SHA256. The
checker is not redistributed in this bundle. Obtain the inspected file from
[the pinned source](https://github.com/Mikael-Codes/hegelese/blob/3199a7fd4d83ab061c5d445d28be6c07edb0d61e/hegelese.py).
Preserve its original UTF-8/LF bytes. Its SHA256 is
`f64de70ed86c4988871ed3d66ee1241ff97a40e4c95816217526444ec49215c9`.

```sh
python check_binary_cut_bridge.py --checker /path/to/hegelese.py
```

For the additional exact reconstruction comparison, provide the published
preprint bundle's `checks/verify-derived.py`. This dependency is separately
checked against SHA256
`e072aa39bca31a86548776fea1960c2567aa873a7d9bbd9c84ecb0844864a11b`.

```sh
python check_binary_cut_bridge.py --checker /path/to/hegelese.py --reconstruction-checker /path/to/preprint/checks/verify-derived.py
```

Output defaults to `results/` beside the script, independent of the current
working directory. Use `--output-dir /path/to/results` to override it.
The run writes two requests, four proposals, four full checker reports, and a
compact `summary.json`; the optional calculation also writes
`reconstruction.json`. The checker files are imported after digest validation;
their command-line entry points are not executed, and bytecode files are not
written.

The positive runs compare 128, 64, and 8 target states, each checking 1,281
equations. All pass. The required `exactState` negative control checks 1,409
equations and is refuted by 120 failures. The optional rank calculation gives
kernel/cokernel dimensions `(1,1)`, `(0,1)`, `(0,0)` for `J`, `J/J^3`, `J/J^2`
at four labels with reconstruction cutoff three.

All source states are vectors of a seven-dimensional augmentation ideal over
F2. They are not the four labels themselves. Integer state identifiers encode
the seven monomial coefficients, in subset-mask order 1 through 7. The inputs
add one monomial basis vector; observations read the three degree-one
coefficients. No representation of higher homotopy types is added to Hegelese.

The Hegelese reports certify the finite state maps. The separate rank
calculation checks one reconstruction diagram. Neither is a proof of the
universal result over all finite sets and all natural linear quotients.

## Quotient alternatives and forced losses

The second experiment has no external dependency:

```sh
python quotient_frontier.py
```

It writes `quotient-frontier-results.json` next to the script. It enumerates
all 25 partitions in the three demonstrations, checks all five feasible
quotients, verifies the forced-loss intersection, and supplies seven
separating witnesses for pairs whose merger is avoidable. The infeasible
case leaves forced losses undefined. This is a standalone reference
experiment, not an integration with Hegelese's existing protocol.
