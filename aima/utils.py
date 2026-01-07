"""aima/utils.py

Minimal utilities used by the cleaned AIMA-based search codebase.

HW4 focus: keep the core small, readable, and executable.
We intentionally include only what `aima/search.py` needs.
"""

from __future__ import annotations

import heapq
import math
from functools import lru_cache, wraps
from typing import Any, Callable, Iterable, Iterator, List, Optional, Tuple, TypeVar

T = TypeVar("T")


def is_in(elt: Any, seq: Iterable[Any]) -> bool:
    """Identity-based membership test (classic AIMA helper)."""
    return any(elt is x for x in seq)


def memoize(fn: Callable[..., T], slot: Optional[str] = None) -> Callable[..., T]:
    """Memoize a function.

    - If `slot` is provided, cache the result on the first argument object.
    - Otherwise cache by arguments using an unbounded LRU cache.
    """

    if slot:

        @wraps(fn)
        def memoized(obj, *args, **kwargs):
            if hasattr(obj, slot):
                return getattr(obj, slot)
            val = fn(obj, *args, **kwargs)
            setattr(obj, slot, val)
            return val

        return memoized

    cached = lru_cache(maxsize=None)(fn)

    @wraps(fn)
    def memoized(*args, **kwargs):
        return cached(*args, **kwargs)

    return memoized


class PriorityQueue:
    """Priority queue with the operations used by AIMA best-first search.

    Supports:
    - append(item)
    - pop()  -> best item (min or max)
    - `item in pq`
    - `pq[item]`    -> priority
    - `del pq[item]`
    """

    def __init__(self, order: str = "min", f: Callable[[Any], Any] = lambda x: x):
        if order not in ("min", "max"):
            raise ValueError("order must be 'min' or 'max'")
        self.order = order
        self.f = f
        # IMPORTANT: we include an ever-increasing counter to avoid Python trying
        # to compare `item` values when priorities tie (Nodes are not orderable).
        self._counter = 0
        self.heap: List[Tuple[Any, int, Any]] = []  # (priority, counter, item)

    def append(self, item: Any) -> None:
        pr = self.f(item)
        if self.order == "max":
            pr = -pr
        self._counter += 1
        heapq.heappush(self.heap, (pr, self._counter, item))

    def extend(self, items: Iterable[Any]) -> None:
        for it in items:
            self.append(it)

    def pop(self) -> Any:
        if not self.heap:
            raise KeyError("pop from empty PriorityQueue")
        return heapq.heappop(self.heap)[2]

    def __len__(self) -> int:
        return len(self.heap)

    def __iter__(self) -> Iterator[Any]:
        for _, _, item in self.heap:
            yield item

    def __contains__(self, item: Any) -> bool:
        return any(it == item for _, _, it in self.heap)

    def __getitem__(self, key: Any) -> Any:
        for pr, _, it in self.heap:
            if it == key:
                return -pr if self.order == "max" else pr
        raise KeyError(key)

    def __delitem__(self, key: Any) -> None:
        # Remove first matching item; O(n) but good enough for HW4.
        for i, (_, _, it) in enumerate(self.heap):
            if it == key:
                self.heap.pop(i)
                heapq.heapify(self.heap)
                return
        raise KeyError(key)


def distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Euclidean distance."""
    return math.hypot(a[0] - b[0], a[1] - b[1])
