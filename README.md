LogicLang

LogicLang is a Python-based propositional logic language that allows defining variables and functions, building logical expressions, and performing semantic evaluation. The language is designed for learning, experimenting, or automating reasoning in propositional logic.

Features

Define variables and functions of boolean expressions.

Use standard propositional operators:

Negation: ~

Conjunction: &

Disjunction: |

Implication: ->

Biconditional: <->

Perform semantic queries:

?sat expr — check if an expression is satisfiable

?valid expr — check if an expression is valid

?contr expr — check if an expression is contradictory

?model expr / ?countermodel expr — find a model or countermodel

?models expr / ?countermodels expr — iterate over all models or countermodels

?table expr — generate a truth table for an expression

Interactive REPL or run scripts from .logic files.

Comments supported using #.

Output statements using write or writeln.

Grammar Overview

Each line is self-contained, either a definition or a query.
