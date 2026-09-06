# CHANGELOG


## v0.2.0 (2026-09-06)

### Chores

- Add Copier setup to vendor the module + tests into projects
  ([#2](https://github.com/Hyperion-AI-Agency/hyperion-proxy-rotator/pull/2),
  [`bfce14d`](https://github.com/Hyperion-AI-Agency/hyperion-proxy-rotator/commit/bfce14df76c69a6afecb27c8f36c2ee801c515e5))

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_01PBsRau1b69sNDJwtaCSVrt

### Features

- Vendor the library into projects via Copier
  ([#3](https://github.com/Hyperion-AI-Agency/hyperion-proxy-rotator/pull/3),
  [`c1f2845`](https://github.com/Hyperion-AI-Agency/hyperion-proxy-rotator/commit/c1f2845ca14bd3a501d6d255a9f0a95be3cffe3d))

Explicit answers file + version-pin docs, and ship copier.yml in a release tag so 'copier copy
  gh:...' resolves the vendor config by default.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_01PBsRau1b69sNDJwtaCSVrt


## v0.1.0 (2026-09-05)

### Features

- Proxy rotation core and requests adapter
  ([#1](https://github.com/Hyperion-AI-Agency/hyperion-proxy-rotator/pull/1),
  [`0de1249`](https://github.com/Hyperion-AI-Agency/hyperion-proxy-rotator/commit/0de1249de70fa16c26e96aa2b70356cdfd755602))

ProxyRotator rotates a pool (round_robin or random) and retires failing proxies onto a cooldown.
  RotatingProxyAdapter mounts on a requests Session and rotates per request, retrying on transport
  errors and retire-worthy statuses.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_01PBsRau1b69sNDJwtaCSVrt


## v0.0.0 (2026-09-05)
