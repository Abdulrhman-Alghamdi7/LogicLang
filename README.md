# LogicLang

LogicLang is a Python-based **propositional logic language** for defining variables and functions, building logical expressions with standard operators (~, &, |, ->, <->), and performing semantic evaluation. It supports satisfiability, validity, contradictions, generating models and countermodels, and producing truth tables. Expressions are parsed into syntax trees and evaluated using Python lambdas. The language includes a REPL for interactive use or can run scripts from `.logic` files.

> **Note:** This project is a personal experiment, so the code is not commented.

---

## Features

- Define **variables** and **functions** of boolean expressions.
- Use **standard propositional operators**:
  - Negation: `~`
  - Conjunction: `&`
  - Disjunction: `|`
  - Implication: `->`
  - Biconditional: `<->`
- Perform **semantic queries**:
  - `?sat expr` — check if an expression is satisfiable
  - `?valid expr` — check if an expression is valid
  - `?contr expr` — check if an expression is contradictory
  - `?model expr` / `?countermodel expr` — find a model or countermodel
  - `?models expr` / `?countermodels expr` — iterate over all models or countermodels
  - `?table expr` — generate a truth table for an expression
- Interactive **REPL** or run scripts from `.logic` files.
- **Comments** supported using `#`.
- **Output statements** using `write` or `writeln`.

---

## Grammar Overview
```
Each line is self-contained: either a definition or a query.

digit           ::= '0' | '1' | ... | '9'
letter          ::= 'A'..'Z' | 'a'..'z' | '_'

false           ::= 'False' | 'false'
true            ::= 'True'  | 'true'
bool            ::= true | false

identifier      ::= letter (letter | digit | '_')*

# Function definitions
function_def    ::= identifier '(' identifier (',' identifier)* ')'

# Function calls
function_call   ::= identifier '(' (identifier | expr) (',' (identifier | expr))* ')'

atom            ::= identifier | function_call | bool
binary_op       ::= '|' | '&' | '->' | '<->'

expr            ::= atom
                  | expr binary_op expr
                  | '~' expr
                  | '(' expr ')'

definition      ::= (identifier | function_def) ':=' expr
query_type      ::= 'valid' | 'model' | 'countermodel' | 'models' | 'countermodels' | 'contr' | 'sat' | 'table'
query           ::= '?' query_type expr

comment         ::= '#' txt
txt             ::= any sequence of characters excluding newlines
write           ::= ('write' | 'writeln') (expr | txt)
```

---

## Usage

### REPL

Run the interactive REPL:

Example session:
```bash
python logiclang.py

>>> x := True
>>> y := False
>>> f(a, b) := a & b
>>> ?sat f(x, y)
False
>>> ?valid x | ~x
True
>>> writeln "Evaluation complete"
Evaluation complete
```

### Execution
Run `.logic` files:
`python logiclang.py examples/test.logic`

---

## Semantic Evaluation

LogicLang evaluates expressions **semantically**, checking all possible boolean assignments (or sampling if there are more than 8 variables) to determine:

- **Satisfiability**
- **Validity**
- **Contradictions**
- **Models and countermodels**
- **Truth tables**

Expressions are parsed into **syntax trees** and converted into **Python lambdas** for evaluation.

> **Note:** This README was generated with the assistance of an AI.
