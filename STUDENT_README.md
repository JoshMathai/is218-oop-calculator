# CLI Calculator

## Setup
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

## Run
python -m calculator

## Test
python -m pytest --cov=calculator --cov-report=term-missing --cov-fail-under=100

## Example
calc> add 5 3
8.0
calc> divide 6 0
Error: Cannot divide by zero
calc> history
add 5.0 3.0 = 8.0
calc> exit

## Successful GitHub Actions run
[(https://github.com/JoshMathai/is218-oop-calculator/actions/runs/38279003849)]

## Coverage exclusions
- `Calculation.execute()` has `# pragma: no cover` because it is only an abstract placeholder with no behavior.
- The `if __name__ == "__main__":` line in `__main__.py` has `# pragma: no cover` because it only calls `main()`, which is tested.

## Method types
- Static methods: the four methods in `Operations` need only a and b.
- Class method: `Calculation.create()` uses `cls` to build a new object.
- Instance method: `execute()` uses the object's own stored values (`self`).

## Patterns
- Factory: `ArithmeticCalculation.create()` builds calculations.
- Command: `CalculateCommand` and `HistoryCommand` each represent an action.
- Strategy: the operations dictionary in `cli.py` picks which operation function does the math.

## OOP ideas
- Encapsulation: a calculation keeps its numbers and operation together, and `HistoryCommand` returns a copy of the history list so it can't be changed from outside.
- Abstraction: `Calculation` promises that every calculation has `execute()`.
- Inheritance: `ArithmeticCalculation` inherits `create()` from `Calculation`.
- Polymorphism: a command can run any Calculation that has `execute()`, whatever it does inside.
- Composition: a command holds a calculation, and a calculation holds an operation.

## SOLID ideas
- Single responsibility: `Operations` does math, commands handle history, and `cli.py` handles input and output.
- Open/closed: to add a new operation, add one line to the dictionary in `cli.py`. Calculation and command code stay the same.
- Liskov substitution: any replacement calculation must still return a number or raise a proper error.
- Interface segregation: a calculation only needs `execute()`.
- Dependency inversion: a command depends on the `Calculation` idea, and a calculation is given an operation instead of hard-coding addition.

## Why execute() doesn't change
Subtract, multiply, and divide were added as new functions in `Operations`. `execute()` just calls `self.operation(self.a, self.b)`, so it works for any operation without edits.