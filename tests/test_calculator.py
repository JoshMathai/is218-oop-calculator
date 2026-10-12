import runpy
import pytest
from calculator.calculation import Calculation, ArithmeticCalculation
from calculator.cli import main
from calculator.commands import CalculateCommand, HistoryCommand
from calculator.operations import Operations


def test_add():
    assert Operations.add(5, 3) == 8
    assert Operations.add(-2, 1.5) == -0.5

def test_subtract():
    assert Operations.subtract(5, 3) == 2
    assert Operations.subtract(0, 4) == -4

def test_multiply():
    assert Operations.multiply(5, 3) == 15
    assert Operations.multiply(2.5, 0) == 0

def test_divide():
    assert Operations.divide(6, 3) == 2
    assert Operations.divide(-1, 4) == -0.25

def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        Operations.divide(1, 0)

def test_factory_builds_concrete_calculation():
    calc = ArithmeticCalculation.create(2, 3, Operations.add)
    assert isinstance(calc, ArithmeticCalculation)
    assert (calc.a, calc.b, calc.operation) == (2, 3, Operations.add)

def test_abstract_class_cannot_be_created():
    with pytest.raises(TypeError):
        Calculation(1, 2, Operations.add)

def test_different_operations():
    assert ArithmeticCalculation.create(6, 3, Operations.divide).execute() == 2
    assert ArithmeticCalculation.create(6, 3, Operations.multiply).execute() == 18

def test_calculate_command_records_history():
    history = []
    calc = ArithmeticCalculation.create(5, 3, Operations.add)
    assert CalculateCommand(calc, history).execute() == 8
    assert history == ["add 5 3 = 8"]

def test_failed_calculation_not_recorded():
    history = []
    calc = ArithmeticCalculation.create(1, 0, Operations.divide)
    with pytest.raises(ValueError):
        CalculateCommand(calc, history).execute()
    assert history == []

def test_history_command_empty_and_copy():
    history = ["add 1 2 = 3"]
    result = HistoryCommand(history).execute()
    assert result == history
    result.append("junk")
    assert history == ["add 1 2 = 3"]
    assert HistoryCommand([]).execute() == []


def run_cli(monkeypatch, capsys, lines):
    it = iter(lines)
    def fake_input(prompt=""):
        try:
            return next(it)
        except StopIteration:
            raise EOFError
    monkeypatch.setattr("builtins.input", fake_input)
    main()
    return capsys.readouterr().out

def test_cli_operations_and_exit(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys,
                  ["add 5 3", "subtract 5 3", "multiply 5 3", "divide 6 3", "exit"])
    assert "8.0" in out and "2.0" in out and "15.0" in out

def test_cli_decimals_negatives(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys, ["add -1.5 0.5", "exit"])
    assert "-1.0" in out

def test_cli_errors_and_continue(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys,
                  ["", "foo", "add 1", "add 1 2 3", "add x 2",
                   "divide 1 0", "add 1 1", "exit"])
    assert "Unknown command: foo" in out
    assert out.count("expected 2 numbers") == 2
    assert "valid numbers" in out
    assert "Cannot divide by zero" in out
    assert "2.0" in out

def test_cli_history(monkeypatch, capsys):
    out = run_cli(monkeypatch, capsys,
                  ["history", "add 1 2", "divide 1 0", "history", "exit"])
    assert "History is empty" in out
    assert out.count("add 1.0 2.0 = 3.0") == 1

def test_cli_eof(monkeypatch, capsys):
    run_cli(monkeypatch, capsys, ["add 1 2"])

def test_main_module_runs(monkeypatch):
    # Runs "python -m calculator" inside a test. Input ends right away (EOF).
    def fake_input(prompt=""):
        raise EOFError
    monkeypatch.setattr("builtins.input", fake_input)
    runpy.run_module("calculator", run_name="__main__")