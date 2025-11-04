Title: Aim for zero linting & formatting issues across all projects (M40)
Created: 2025-08-26
Tags: linting, formatting, ruff, black, mypy, pre-commit, CI, repo-health

Goal

Achieve and maintain zero linting/formatting issues across every project linked into this workspace (the "M40" objective). This includes eliminating errors/warnings from linters, type checkers, and formatters that we run in CI and locally.

Scope

- All Python repositories under `linked_projects/` plus `metaproject-life` itself.
- Tools: ruff (linting + fixes), Black (formatting), mypy (type checks), isort (imports), and optional project-specific linters where needed.
- CI enforcement via a GitHub Actions workflow and `pre-commit` hooks locally.

Basic contract

- Input: repository source files.
- Outputs: configs (pyproject.toml / .ruff.toml / .pre-commit-config.yaml), automated fixes applied where safe, and CI workflow that fails on regressions.
- Error modes: third-party incompatible code, generated code, and binary extensions — these will be whitelisted or excluded.

High-level plan

1. Scan & baseline
   - Run ruff/black/isort/mypy in check mode across each repo to collect current counts per repo.
   - Produce a short report with filenames and top rule violations.
2. Policy & config
   - Standardize on `pyproject.toml` with Black + ruff integration and an isort profile.
   - Configure ruff rules and per-repo ignores for unavoidable legacy issues.
3. Auto-fix & staged changes
   - Run ruff --fix and Black on each repo, commit changes in small logical commits per repo.
   - For large legacy files, create a `lint: allow` marker (or `noqa`) only when necessary with an explanation comment.
4. Types
   - Enable mypy in incremental mode; add `mypy.ini` and annotate critical modules first.
5. Developer UX
   - Add `pre-commit` config with hooks for ruff, black, isort, and mypy (optional fast checks).
   - Add a lightweight `make lint-fix` script for local fast autofix runs.
6. CI enforcement
   - Add GitHub Actions workflow to run `ruff check`, `black --check`, `isort --check`, and `mypy --strict` (or configured) on PRs; fail on any issue.
7. Monitoring & maintenance
   - Add a weekly CI job that runs full checks and reports regressions to a Slack/issue if available.

Edge cases & notes

- Generated code, vendor files, or binary extension modules should be excluded via `exclude` in ruff/pyproject and documented.
- For very large legacy repos, consider a staged approach: First, bring repo to an agreed minimal standard, then progressively tighten rules.
- When automated fixes risk behaviour change, prefer manual review and small commits.

Quick follow-ups (pick one)

- I can run the baseline scan now and report counts per repo.
- I can create the `pyproject.toml`, `.pre-commit-config.yaml`, and a `ci/lint.yml` GitHub Actions workflow template and apply them to one repo as a demo (recommended: `metaproject-life` or `backend`).

Done: saved as `data/notes/aim_zero_lint.md`.
