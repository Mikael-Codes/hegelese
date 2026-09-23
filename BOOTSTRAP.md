# Executable Hegelese bootstrap 0.1

**Hic Rhodos, Hic Saltus.**

This is the implemented language subset. The broader [v0.3 proposal](docs/hegelese-spec-v0.3.md) remains a design document. Its schematic syntax is not interchangeable with this grammar. The bootstrap is a dynamically checked, strict functional interpreter in Python 3.10+, using only the standard library. There is no static type checker, general proof checker, compiler, or self-hosted implementation yet.

## Run a complete development

From the repository root:

```sh
python3 hegelese.py run examples/functional.hgl
python3 hegelese.py run examples/four-phase.hgl
python3 hegelese.py run examples/three-phase.hgl
python3 hegelese.py run examples/four-phase.hgl --budget 2
python3 -m unittest discover -s tests -v
```

The functional example returns sum of squares 30, factorial 720, and a matched result 42. The four-phase development is exhaustively checked over nine local equations. The three-phase development is refuted at state `2` on `tick`: projecting the source successor gives `0`, while stepping the projected state gives `1`. The budget-limited example returns `Unknown`.

Output is JSON. A final ordinary expression has status `Evaluated` and exit code 0; that says only that evaluation completed. A final checker-created evidence value gives status `ExhaustivelyChecked` (exit 0), `Refuted` (1), `Invalid` (2), or `Unknown` (3). Syntax and runtime errors return `Invalid` with file, line, column, and source spelling. Evaluation exhaustion returns `Unknown`. These are intentionally distinguishable from successful checking.

## Ordinary programming

```hegelese
let square = fn(x) => x * x;
let total = fold(fn(acc, x) => acc + x, 0, map(square, [1, 2, 3, 4]));
let rec factorial = fn(n) => if n == 0 then 1 else n * factorial(n - 1);
let makeAdder = fn(x) => fn(y) => x + y;
{total: total, factorial: factorial(6), answer: makeAdder(40)(2)};
```

Bindings are immutable and sequential. Duplicate top-level names, including built-in names, are rejected. Functions capture their definition environment; later declarations do not alter that environment. Parameters and match binders may shadow outer names. `let rec` supports a single recursive function. Mutual recursion, local `let`, modules, and imports are deferred. Function application has exact arity; there is no implicit currying, but a function may return another function.

Function and argument evaluation is strict, left to right. Conditionals evaluate only their selected branch. `&&` and `||` short-circuit and require Booleans. There is no truthiness conversion or Boolean arithmetic. Lists may be heterogeneous in this dynamically checked subset.

Integers support `+ - * / %` and comparisons. `/` is floor division, including for negative operands; `%` satisfies `a = (a / b) * b + a % b`. Division by zero is invalid. `+` also concatenates two strings or two lists. No implicit numeric or string coercion occurs. Equality is structural on data and distinguishes Booleans from integers, including within lists and records. Equality on functions, process handles, requests, developments, and evidence is unsupported.

Records have named or quoted keys: `{answer: 42, "exact-phase": 2}`. Access uses `.answer` or `["exact-phase"]`. List and string indexes are zero-based nonnegative integers. Strings are Unicode and use JSON escapes; strings are indexed by Unicode code point, not grapheme cluster. Comments begin with `#` and end at the newline.

Tagged data uses `variant("Some", value)`. Every variant has one payload, which may be `null`, a record, or a list. Pattern matching binds that payload:

```hegelese
match variant("Some", 42) {
  Some(value) => value;
  None(value) => 0;
};
```

Tag names are unreserved identifiers. Duplicate branches are rejected; a missing branch fails when encountered. Match exhaustiveness is not statically checked. Nested and list patterns are deferred.

Built-ins: `len(sequenceOrRecord)`, `int(decimalString)`, `str(integer)`, `map(function, list)`, `fold(function, initial, list)`, `variant(tag, payload)`, `inspect(handle)`, and `check(development)`.

## Process, request, development, evidence

A `process Name = record;` requires exactly `version`, `states`, `inputs`, `initial`, `step`, and `observe`. States and input symbols are strings. `step` takes a state and input; each observation takes a state. Declaration evaluates these functions over all declared states and inputs, then validates the resulting total tables. No sampled execution trace substitutes for those tables. The original function syntax is not currently available through reflection.

```hegelese
request KeepParity from FourPhase require ["parity"];
upheave Alternation {
  from KeepParity;
  into ParityToggle;
  using fn(s) => str(int(s) % 2);
  occasion {kind: "Rearticulation", explanation: "Describe the cycle through alternation."};
  retain initial because "Preserve the mapped start.";
  retain step because "Check that projection commutes with each tick.";
  retain "observation:parity" because "The application requires parity.";
  withdraw "observation:exactPhase" because "Parity identifies distinct phases.";
  assumptions [];
};
check(Alternation);
```

The complete runnable definitions are in [four-phase.hgl](examples/four-phase.hgl). This syntax is the implemented bootstrap formulation of the earlier schematic examples. In particular, `from` references a request, which fixes both the source process and its required observations. All seven spellings `Aufheben`, `Sublation`, `Upheaval`, `aufheben`, `sublation`, `upheaval`, and `upheave` introduce the identical declaration construct. `UPHEAVAL` is not an alias. The bootstrap does not yet support the proposal's separate named-Upheaval application syntax.

A declaration constructs an **unchecked candidate**. `check` invokes the existing finite checker, recomputing obligations against the captured request. Only the checker creates an evidence value. An ordinary record containing `status: "ExhaustivelyChecked"` remains ordinary data and cannot be passed off as evidence to `check`. Evidence fields can be inspected, for example `check(Alternation).status`. A program can discard evidence or branch on it; mandatory handling of every unresolved result is not yet enforced. A nested report inside an ordinary final record does not change the outer `Evaluated` status.

`inspect(FourPhase)` exposes its validated tables; `inspect(KeepParity)` exposes the request; `inspect(Alternation)` exposes the proposed mapping and commitment account. These are read-only language values. Inspection cannot replace the evaluator or create an evidence value. An unchecked candidate may be incomplete or invalid until checked; its display is explicitly marked `UncheckedDevelopment`.

Definitions retain their original meaning. Content fingerprints bind evidence to exact captured source, target, request, and proposal content. Re-running after an observation change recomputes the check; old reports are not accepted as input evidence. There is no persistent dependency database or incremental invalidation engine yet.

The source file's author controls its request. For adversarial candidate generation, retain the request outside that author's write authority and use the existing `check request.json proposal.json` interface. A source-level declaration is not an access-control boundary. Fingerprints neither authenticate authors nor certify the host interpreter.

## Compact grammar

```text
program     := statement* EOF
statement   := "let" "rec"? name "=" expression ";"
             | "process" name "=" expression ";"
             | "request" name "from" expression "require" expression ";"
             | UPHEAVAL name "{" development-field* "}" ";"
             | expression ";"
development-field := ("from" | "into" | "using" | "occasion" | "assumptions") expression ";"
             | ("retain" | "withdraw") key "because" expression ";"
expression  := literal | name | "(" expression ")"
             | "fn" "(" names? ")" "=>" expression
             | "if" expression "then" expression "else" expression
             | "match" expression "{" (name "(" name ")" "=>" expression ";")* "}"
             | "[" expressions? "]" | "{" record-fields? "}"
             | expression "(" expressions? ")"
             | expression "." name | expression "[" expression "]"
             | ("-" | "!") expression | expression binary-op expression
```

Comma-separated sequences have no trailing comma. Record fields use `key: expression`. Names use ASCII letters/underscore followed by letters, digits, or underscore; reserved words cannot be names or unquoted record keys. Literals are decimal integers, quoted strings, `true`, `false`, and `null`. Unary minus supplies negative integers.

Precedence, low to high: `||`; `&&`; `== !=`; `< > <= >=`; `+ -`; `* / %`; unary `- !`; calls, fields, and indexing. Binary operators associate left. Function bodies and conditional branches extend rightward; parenthesize a function or conditional to apply an operation to the whole expression.

## Bounds and remaining work

Default evaluation fuel is 100000, configurable from 0 through 1000000. Evaluation, function calls, structural equality, and result rendering consume fuel. Finite checking has its own `--budget` with the same default and range. Fuel does not meter every host instruction; this interpreter is not a security sandbox or a wall-clock limiter. Python nesting limits can end an otherwise valid computation with `Unknown`.

Source is limited to 2 MB, integer literals to 1000 decimal digits, arithmetic results to 4096 bits, and concatenation results to 10000 elements. Finite-process limits remain 1000 states, 64 inputs, and 32 observations. General unbounded execution, tail-call optimization, static inference, typed errors, host I/O, staged syntax reflection, dependency tracking, general proof transport, and self-hosting remain future work.

The research distinction remains deliberate: equivalence, lossy abstraction, refinement, restricted applicability, and requirement revision need different preservation relations. This implementation only checks the existing finite total-map relation. It makes no claim of philosophical necessity or measured AI productivity gains.
