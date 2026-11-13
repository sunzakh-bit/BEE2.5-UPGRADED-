# Contributing to BEE2.5

Thanks for your interest in improving BEE2.5.

## Development principles

- Keep changes focused and explain why they are needed.
- Prefer small, testable modules over large tightly coupled components.
- Preserve compatibility with existing BEE2.4 packages where practical.
- Do not include proprietary Portal 2 assets or other files you do not have permission to redistribute.

## Before submitting changes

1. Run the test suite with `python -m pytest`.
2. Check formatting and lint with `ruff check .`.
3. Update documentation when behavior or package formats change.
4. Include tests for bug fixes and new functionality.

## Pull requests

Describe the problem, the approach, compatibility impact, and how you tested the change.