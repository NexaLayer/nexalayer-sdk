# Changelog

## [0.1.5] - 2026-10-17

### Added

- Add session usage access through `get_session_usage()` and `Session.usage()`.
- Document current dynamic and shared-static starting prices.
- Document `PRODUCT_NOT_FOUND` (404) and `PRICE_MISMATCH` (409) API errors.
- Add PyPI discovery metadata, classifiers, and project links.

### Changed

- Hide proxy credentials from session and rotation responses by default.
- Add `include_credentials=True` as an explicit opt-in when connection credentials are required.
- Align the Python SDK release line with the published `@nexalayer/mcp` package at 0.1.5.

## [0.1.1] - 2026-10-16

- Add `country`, `in_stock`, `limit`, and `cursor` product filters to both SDKs.
- Keep npm and PyPI package versions aligned.

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial SDK skeleton: Python and Node clients with session abstraction.
- Stubs for auth, account, billing, products, sessions, and stats endpoints.
- Example scripts: quickstart and rotate (Python and Node).
- Error types and lightweight request/response models.

### Changed

- Nothing yet.

### Fixed

- Nothing yet.

## [0.1.0] - YYYY-MM-DD

- Initial source release.
