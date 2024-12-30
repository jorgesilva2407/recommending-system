import random
from datetime import datetime
from functools import wraps
from fpgrowth_py import fpgrowth


class Model:
    def __init__(self, version: str = "v1"):
        self._rules: list[tuple[set[str], set[str]]] = []
        self._tracks: list[str] = []
        self._version = version
        self._fit_time = None

    def fit(
        self,
        playlists: list[set[str]],
        tracks: list[str],
        min_support: float = 0.1,
        min_confidence: float = 0.5,
    ):
        self._tracks = tracks

        try:
            _, rules = fpgrowth(
                playlists, minSupRatio=min_support, minConf=min_confidence
            )
            self._rules = [(rule[0], rule[1]) for rule in rules]
        except Exception as e:
            print("ERROR: Setting rules to empty list.", e)
            self._rules = []

        self._fit_time = datetime.now()

    def predict(self, x: set[str]) -> set[str]:
        result = set()
        for rule in self._rules:
            if rule[0].issubset(x):
                result.update(rule[1])

        if len(result) == 0:
            return random.sample(self._tracks, 10)

        return result

    @property
    def version(self):
        return self._version

    @property
    def fit_time(self):
        return self._fit_time
