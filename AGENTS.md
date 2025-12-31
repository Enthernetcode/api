# Repository Guidelines

## Project Structure & Module Organization
- Repository is currently minimal; add application code under `src/` grouped by feature (e.g., `restaurants/handlers.py`, `restaurants/service.py`, `clients/chowdeck.py`).
- Mirror code layout in `tests/` for unit/integration coverage; keep sample payloads under `tests/fixtures/`.
- Keep utility scripts (data refresh, local seeding) in `scripts/`, and document them in `readme`.
- Check configuration into `.env.example` only; never commit real credentials.

## Build, Test, and Development Commands
- Standardize on a `Makefile` (add if missing) to keep commands reproducible:
  - `make install` — install runtime dependencies into a local environment.
  - `make serve` — run the dev server (e.g., `uvicorn src.main:app --reload` or `npm run dev`, depending on runtime).
  - `make lint` — run formatter and linter; fix reported issues before commits.
  - `make test` — execute the full test suite with coverage reporting.
- Document any runtime-specific tooling in `readme` and keep Make targets in sync.

## Coding Style & Naming Conventions
- Prefer 4-space indentation for Python and 2-space for JSON/YAML; target a 100-character line width.
- Use `snake_case` for functions/variables, `PascalCase` for classes, and lowercase hyphenated REST paths.
- Keep modules focused by domain; avoid large god-files by splitting handlers, services, and clients.
- Run your formatter (Black/Prettier) and type checks (mypy/tsc) before pushing.

## Testing Guidelines
- Match test modules to source modules (`tests/test_restaurants.py`, `tests/clients/test_chowdeck.py`).
- Write happy-path and failure-path tests for network calls; mock Chowdeck responses to avoid live traffic.
- Aim for at least 80% coverage on new or modified code; add regression tests when fixing bugs.
- For integration tests, spin up any required local services via scripts or docker-compose and document the steps.

## Commit & Pull Request Guidelines
- No meaningful history exists yet; follow Conventional Commits (`feat:`, `fix:`, `chore:`, etc.) with present-tense summaries.
- Keep PRs narrowly scoped; include a short description, linked issues, and a test plan (commands run and results).
- Document API or schema changes in the PR body and update `readme`/`AGENTS.md` when workflows change.
- Add screenshots or sample JSON responses for API changes when it clarifies the behavior.

## Security & Configuration Tips
- Store secrets only in local `.env` files; commit placeholders via `.env.example`.
- Validate and sanitize any upstream or user-supplied data before persisting or serving it.
- Log errors with enough context to debug data-fetch issues without leaking tokens or PII.
