# aeclib STYLE Standards

Engineering and stylistic principles for `aeclib` contributors.

## 1. Architecture
- **Structure:** Organize code by technical discipline (e.g., `interior`, `egress`).
- **Atomicity:** Map each distinct provision to a single authoritative function; reuse these functions across modules to avoid duplicating logic.
- **Traceability:** Use docstrings to map functions to their corresponding provisions (Title, Version, and Section).

## 2. Logic & Interface
- **Parameters:** Use required parameters for the provision's general rule and optional parameters for its exceptions.
- **Standardized Returns:** Use `ComplianceResult` as the return objects.
- **Reporting:** Failures and non-applicable cases must include a message starting with `[FAIL]` or `[NOT_APPLICABLE]`.

## 3. Testing
Tests verify the "Contract," not the "UI."
- **Status Assertions:** Verify `ComplianceStatus` (PASS/FAIL).
- **Robustness:** Do not test specific message string content to prevent brittle tests.
