# hyperion-proxy-rotator

Rotate a pool of HTTP proxies across requests, retiring ones that fail onto a
cooldown so you stop hitting dead or blocked exits.

```python
import requests
from proxy_rotator import ProxyRotator, RotatingProxyAdapter

pool = [
    "http://user:pass@proxy-a:8000",
    "http://user:pass@proxy-b:8000",
    "http://user:pass@proxy-c:8000",
]

rotator = ProxyRotator(pool, strategy="round_robin", cooldown=60)

session = requests.Session()
session.mount("https://", RotatingProxyAdapter(rotator))
session.mount("http://", RotatingProxyAdapter(rotator))

resp = session.get("https://example.com")  # picks a proxy, retries on failure
print(resp.status_code)
```

Each request picks the next proxy. A transport error or a retire-worthy status
(407, 429, 502, 503, 504 by default) marks that proxy bad and retries on the
next one; a proxy that keeps working stays in rotation. Bad proxies return after
`cooldown` seconds.

## Using the rotator on its own

The core has no HTTP dependency of its own, so you can drive any client:

```python
from proxy_rotator import ProxyRotator

rotator = ProxyRotator(pool, strategy="random", cooldown=60)

proxy = rotator.next()
try:
    do_request(proxy)
    rotator.mark_good(proxy)
except SomeError:
    rotator.mark_bad(proxy)
```

## Install

```
pip install hyperion-proxy-rotator
```

## Or vendor it with Copier

To copy the code straight into a project instead of depending on the published
package, use [Copier](https://copier.readthedocs.io/):

```
copier copy gh:hyperion-ai-agency/hyperion-proxy-rotator path/to/project
```

That drops `src/proxy_rotator/` and `tests/` into the project and records a
`.copier-answers.yml`. The vendored code still needs `requests`. Pull later
upstream fixes into the vendored copy from the project root:

```
copier update
```

Copier defaults to the latest release tag. To vendor a specific version, pin it:

```
copier copy --vcs-ref v0.2.0 gh:hyperion-ai-agency/hyperion-proxy-rotator path/to/project
```

## Development

```
uv sync
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
uv run ruff check .
uv run ruff format .
uv run pytest -q
```

Commits follow [Conventional Commits](https://www.conventionalcommits.org/) and
releases are cut by python-semantic-release on push to `main`. Publishing to
PyPI uses [trusted publishing](https://docs.pypi.org/trusted-publishers/) over
OIDC (no stored token); configure the trusted publisher on PyPI (GitHub owner
`hyperion-ai-agency`, repository `hyperion-proxy-rotator`, workflow
`release.yml`) before the first release.
