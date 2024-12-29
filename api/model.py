import random
from fpgrowth_py import fpgrowth


class Model:
    def __init__(self):
        self._rules: list[tuple[set[str], set[str]]] = []
        self._tracks: list[str] = []

    def fit(
        self,
        playlists: list[set[str]],
        tracks: list[str],
        min_support: float = 0.1,
        min_confidence: float = 0.5,
    ):
        self._tracks = tracks
        try:
            _, rules = fpgrowth(playlists, min_support, min_confidence)
            self._rules = [(rule[0], rule[1]) for rule in rules]
        except Exception as _:
            self._rules = []

    def predict(self, x: set[str]) -> set[str]:
        result = set()
        for rule in self._rules:
            if rule[0].issubset(x):
                result.update(rule[1])

        if len(result) == 0:
            return random.sample(self._tracks, 10)

        return result
