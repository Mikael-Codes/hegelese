# Design validation

23 September 2026. **These are independent Python reference checks, not execution by a Hegelese compiler.** No compiler, parser, proof checker, or complete type system has been implemented in this task.

## Keyword equivalence probe

A small token-normalization probe checked all seven specified spellings in declaration-shaped and application-shaped examples (14 cases). Each produced the same normalized token sequence for its context while retaining the original source spelling and span. A quoted string containing the names remained unchanged, and an unspecified mixed-case variant was not recognized as the keyword. This validates the proposed alias table on these examples, not a complete lexer or parser.

## Counting/differences reference calculation

Pairs use natural-number coordinates and normalize by subtracting the smaller coordinate from both. Raw coordinate values ranged from 0 through 8 inclusive; canonical values represented differences from −8 through 8. Embedding/addition checks used source values from 0 through 25 inclusive. Arithmetic used exact integers.

| Property checked | Cases |
|---|---:|
| normalization preserves difference | 81 |
| normalization is idempotent | 81 |
| equivalence matches canonical equality | 6,561 |
| addition is well-defined on tested representatives | 6,561 |
| addition is associative | 4,913 |
| addition is commutative | 289 |
| zero is identity | 17 |
| inverse gives zero | 17 |
| embedding preserves addition | 676 |
| embedding preserves zero | 1 |
| generation from embedded counts | 81 |

All 19,278 arithmetic cases passed. A deliberately incorrect embedding `bad(n) = (n + 1, 0)` failed both zero preservation and addition preservation, confirming that the checks detect this substantive error.

The tests do not prove the laws for every natural number. The specification gives elementary mathematical arguments for selected laws, separately from these checks. No general universal property, philosophical necessity, empirical correctness, or performance claim was tested.

## Document checks

The specification, critical reflection, and reading ledger explicitly distinguish proposals, mathematical arguments, executable reference checks, and completed reading. The reading inventory records unread material without presenting downloaded text as completed research.
