# Development Guidelines for aeclib

This document provides instructions for setting up your development environment and defines the architectural, style, and implementation standards for `aeclib`.

## 1. Getting Started

### 1.1 Local Installation
To set up a local development environment, clone the repository and create an editable install. This allows you to run and test the library directly from your local source code.

```bash
# From the project root
pip install -e .
```

### 1.2 Development Dependencies
[Optional placeholder for future linting/formatting tools like ruff, black, mypy]

## 2. Development Standards
All contributors (human and AI) must adhere to these rules to ensure the library remains a professional, authoritative compliance engine.

### 2.1 Intent: Compliance-Only Logic
The primary goal of `aeclib` is to validate designs, not to generate them.

- **Boolean Returns:** Validation rules must return a `bool` (`True` for Pass, `False` for Fail).
- **Side-Effect Reporting:** Compliance failures must be reported using the standard Python `logging` module (e.g., `logger.warning`).
- **Statelessness:** Rules must be implemented as pure, stateless functions. They take design facts as input and return a deterministic result.

### 2.2 API Style: The "Architect-Friendly" Interface
The library should integrate seamlessly into existing AEC workflows (Revit, Rhino, JSON exports).

- **Direct Parameters:** Acceptance of raw design facts (e.g., `gross_area`, `net_area`, `design_occupancy_count`) directly from JSON or BIM data.
- **No Schema Dictation:** Do not force users to wrap their data in custom library classes or schemas.
- **Embedded Legal Knowledge:** The library must handle the "internal logic" of the code, such as automatically selecting the correct area basis (Gross vs. Net) or load factor.
- **Authoritative Constants:** Hard-code standard thresholds (like the 7.0 density limit) within the library to ensure it remains the "source of truth."

### 2.3 Documentation & Traceability
Every rule must be traceable back to a specific technical or legal provision.

- **"Applicable to" List:** Docstrings must include a concise list of the specific standard editions and sections to which a rule applies (e.g., IBC 2018, 2021, 2024).
- **Minimalist Docstrings:** Focus on the "What" (the provision) and the "How" (args/returns), removing redundant technical or legal explanations.

### 2.4 Technical Standards
- **Python Version:** Target Python >= 3.9.
- **Type Hinting:** Mandatory for all public APIs.
- **Domain-First Namespacing:** Organize rules by technical domain (e.g., `aeclib.occupancy`) and expose them at the top level via `__init__.py`.
- **String-Friendly Enums:** Use `StrEnum`-style patterns internally for robust data management while allowing users to provide raw strings.

## 3. Testing
`aeclib` uses **pytest** as the primary testing framework.

### 3.1 Running Tests
If you have performed an editable install (`pip install -e .`), you can run the tests from the root of the project:

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/occupancy/test_occupancy.py
```

If you have not performed an editable install, you must manually set the `PYTHONPATH`:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
pytest
```

### 3.2 Adding New Tests
Every new validation rule or domain must include a corresponding test file in the `tests/` directory. Tests should verify both `True` (Pass) and `False` (Fail) scenarios and confirm that appropriate warnings are logged.

## 4. Commit Standards
- **Format:** Use the [Conventional Commits](https://www.conventionalcommits.org/) specification.
- **Types:** `feat`, `fix`, `docs`, `test`, `refactor`.
- **Content:** Focus on the technical rationale (the "Why") behind a change.
