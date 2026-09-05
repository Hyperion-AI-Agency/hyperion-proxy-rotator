# CHANGELOG


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
