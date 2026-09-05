import random
import threading
import time
from itertools import cycle

STRATEGIES = ("round_robin", "random")


class ProxyRotator:
    def __init__(self, proxies, strategy="round_robin", cooldown=60.0):
        pool = list(dict.fromkeys(proxies))
        if not pool:
            raise ValueError("proxies must be a non-empty iterable")
        if strategy not in STRATEGIES:
            raise ValueError(f"strategy must be one of {STRATEGIES}")

        self.strategy = strategy
        self.cooldown = cooldown

        self._pool = pool
        self._cycle = cycle(pool)
        self._blocked = {}
        self._lock = threading.Lock()

    def next(self):
        with self._lock:
            available = self._available()

            if not available:
                # Everything is cooling down; hand back the one that recovers
                # soonest rather than failing, and clear its penalty.
                soonest = min(self._blocked, key=self._blocked.get)
                del self._blocked[soonest]
                return soonest

            if self.strategy == "random":
                return random.choice(available)

            for _ in range(len(self._pool)):
                proxy = next(self._cycle)
                if proxy in available:
                    return proxy

            return available[0]

    def mark_bad(self, proxy):
        with self._lock:
            self._blocked[proxy] = time.monotonic() + self.cooldown

    def mark_good(self, proxy):
        with self._lock:
            self._blocked.pop(proxy, None)

    def _available(self):
        now = time.monotonic()

        recovered = [p for p, until in self._blocked.items() if until <= now]
        for proxy in recovered:
            del self._blocked[proxy]

        return [p for p in self._pool if p not in self._blocked]
