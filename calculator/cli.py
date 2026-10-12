from calculator.calculation import ArithmeticCalculation
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.operations import Operations


def main() -> None:
    history: list[str] = []
    # Strategy: this dictionary picks which math job to use.
    operations = {
        "add": Operations.add,
        "subtract": Operations.subtract,
        "multiply": Operations.multiply,
        "divide": Operations.divide,
    }

    while True:
        try:
            line = input("calc> ")
        except EOFError:
            print()
            break

        parts = line.split()
        if not parts:
            continue
        name = parts[0].lower()

        if name == "exit":
            break
        if name == "history":
            entries = HistoryCommand(history).execute()
            if entries:
                for entry in entries:
                    print(entry)
            else:
                print("History is empty")
            continue
        if name not in operations:
            print(f"Unknown command: {name}")
            continue
        if len(parts) != 3:
            print("Error: expected 2 numbers, e.g. add 5 3")
            continue
        try:
            a, b = float(parts[1]), float(parts[2])
        except ValueError:
            print("Error: operands must be valid numbers")
            continue

        # Path for "add 5 3": read input -> choose Operations.add from the dict
        # -> create an ArithmeticCalculation -> create and execute a
        # CalculateCommand -> print the answer.
        calculation = ArithmeticCalculation.create(a, b, operations[name])
        try:
            result = CalculateCommand(calculation, history).execute()
        except ValueError as error:
            print(f"Error: {error}")
            continue
        print(result)