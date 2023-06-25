from typing import List


def _to_float_inf(lst: List[float]):
    def to_inf(x):
        if x == "inf":
            return float("inf")
        return x

    return list(map(to_inf, lst))
