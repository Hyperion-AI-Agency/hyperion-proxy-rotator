# hyperion-python-template

A template for a single, independently versioned Python package published to
PyPI with no stored token. Click **Use this template** to make a new repo, then
work through the rename checklist below.

Batteries included:

- **uv** for the environment, build, and publish
- **hatchling** build backend, mandatory `src/` layout
- **Ruff** for linting and formatting
- **pre-commit** running Ruff (lint and format), the test suite, and file hygiene on every commit
- **commitizen** enforcing [Conventional Commits](https://www.conventionalcommits.org/) on the `commit-msg` hook
- **python-semantic-release** for automatic version bump, `CHANGELOG.md`, tag, and GitHub release
- **PyPI trusted publishing** over OIDC, so no `PYPI_TOKEN` is ever stored

## Rename checklist

Replace the placeholder in these spots, then delete this section:

1. `pyproject.toml` — `name` (`my-package`), `description`, `authors`, and the `[project.urls] Repository`.
2. `pyproject.toml` — `[tool.hatch.build.targets.wheel] packages` (`src/my_package`).
3. Rename the directory `src/my_package/` to `src/<your_import_name>/` and fix the imports in `__init__.py`, `core.py`, and `tests/`.
4. `LICENSE` — copyright holder. To use a different license, pick one at [choosealicense.com](https://choosealicense.com/) and update the `license` field in `pyproject.toml` to match.
5. This `README.md` — rewrite it to lead with a working usage example.

## Develop

```
uv sync
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
uv run ruff check .
uv run ruff format .
uv run pytest -q
```

## Releasing

Set up [PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/) once:
add a trusted publisher on PyPI pointing at this repository and the workflow
`release.yml`. No token goes in the repo.

After that, every push to `main` is analyzed by python-semantic-release. Commit
types decide the bump: `fix:` patches, `feat:` adds a minor, a `!` or a
`BREAKING CHANGE:` footer majors. It writes the version and `CHANGELOG.md`, tags
`vX.Y.Z`, cuts a GitHub release, and publishes to PyPI. Commits with no
releasable type publish nothing.
