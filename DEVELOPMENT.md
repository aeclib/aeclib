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

- **Standardized Reporting:** Validation rules must return a `ComplianceResult` object (`PASS`, `FAIL`, or `NOT_APPLICABLE`).
- **Minimalist Logging:** Use `logger.info` for informational logic path hints to user. Use `logger.error` for system/data errors. Do *not* use `logger.warning` preceding returning compliance failures; the `ComplianceResult` message is the authoritative report.
- **Statelessness:** Rules must be implemented as pure, stateless functions. They take design facts as input and return a deterministic result.
- **Direct Fact Validation:** Always validate the design fact (e.g., occupant count) directly against a calculated legal limit, rather than converting the design into a secondary metric (e.g., density).
- **Mathematical Intuition:** Logic should be written to be as readable as possible, making intuitive sense to an architect.

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

## 3. Build and Test Sequence
`aeclib` uses **tox** to orchestrate testing, linting, and formatting in isolated environments.

### 3.1 The "Build" Command
To run the full suite (Tests + Linting + Formatting Check):

```bash
tox
```

### 3.2 Automated Formatting and Fixing
To automatically fix linting issues and reformat the code to meet the project's style standards (Line length 88, etc.):

```bash
tox -e fix
```

### 3.3 Running Specific Tasks
- **Tests only:** `pytest` or `tox -e py39`
- **Linting check only:** `tox -e lint`
- **Formatting check only:** `tox -e format`

### 3.4 Style Standards
- **Linter/Formatter:** `ruff`
- **Max Line Length:** 88 characters
- **Quotes:** Double quotes preferred
- **Import Sorting:** Automatic via `ruff` (isort rules)

## 4. Commit Standards
- **Format:** Use the [Conventional Commits](https://www.conventionalcommits.org/) specification.
- **Types:** `feat`, `fix`, `docs`, `test`, `refactor`.
- **Content:** Focus on the technical rationale (the "Why") behind a change.
