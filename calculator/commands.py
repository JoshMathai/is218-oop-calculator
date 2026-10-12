class CalculateCommand:
    # Composition: a command holds a calculation and a shared history list.
    def __init__(self, calculation, history: list):
        self.calculation = calculation
        self.history = history

    def execute(self):
        # If this fails, the next lines never run, so failures aren't saved.
        result = self.calculation.execute()
        c = self.calculation
        self.history.append(f"{c.operation.__name__} {c.a} {c.b} = {result}")
        return result


class HistoryCommand:
    def __init__(self, history: list):
        self.history = history

    def execute(self) -> list:
        # Return a copy so nobody can mess up the real history.
        return list(self.history)