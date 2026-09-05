from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException

DEFAULT_RETIRE_STATUSES = frozenset({407, 429, 502, 503, 504})


class RotatingProxyAdapter(HTTPAdapter):
    def __init__(self, rotator, attempts=3, retire_statuses=DEFAULT_RETIRE_STATUSES, **kwargs):
        if attempts < 1:
            raise ValueError("attempts must be at least 1")

        self.rotator = rotator
        self.attempts = attempts
        self.retire_statuses = frozenset(retire_statuses)

        super().__init__(**kwargs)

    def send(self, request, **kwargs):
        last_error = None

        for attempt in range(self.attempts):
            proxy = self.rotator.next()
            kwargs["proxies"] = {"http": proxy, "https": proxy}

            try:
                response = super().send(request, **kwargs)
            except RequestException as exc:
                self.rotator.mark_bad(proxy)
                last_error = exc
                continue

            if response.status_code not in self.retire_statuses:
                self.rotator.mark_good(proxy)
                return response

            self.rotator.mark_bad(proxy)
            if attempt < self.attempts - 1:
                response.close()
                continue

            # Out of attempts. Hand back the last response rather than raising,
            # so the caller can still inspect it.
            return response

        raise last_error
