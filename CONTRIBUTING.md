# Contributing to NexaLayer SDK

Thank you for considering contributing to the NexaLayer SDK.

## Development setup

- **Python**: From repo root, `cd python && pip install -e ".[dev]"` then run tests with `pytest`.
- **Node**: From repo root, `cd node && npm install && npm run build` then `npm test`.

## Pull requests

1. Fork the repository and create a branch from `main`.
2. Make changes with clear commits; follow existing code style.
3. Add or update tests where relevant.
4. Ensure `pytest` (Python) and `npm test` (Node) pass.
5. Open a PR with a short description and link any related issues.

## Code style

- Python: Black, isort; line length 88.
- TypeScript: Prettier; project tsconfig for strict mode.

## Questions

Open an issue for bugs or feature requests. For security issues, see [SECURITY.md](SECURITY.md).
