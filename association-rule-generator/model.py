from fpgrowth_py import fpgrowth


class Model():
    def __init__(self):
        self._rules: list[tuple[set[str], set[str]]] = []

    def fit(
        self,
        x: list[set[str]],
        min_support: float = 0.1,
        min_confidence: float = 0.5,
    ):
        try:
            _, rules = fpgrowth(x, min_support, min_confidence)
            self._rules = [(rule[0], rule[1]) for rule in rules]
        except Exception as _:
            self._rules = []

    def predict(self, x: set[str]) -> set[str]:
        result = set()
        for rule in self._rules:
            if rule[0].issubset(x):
                result.update(rule[1])
        return result
