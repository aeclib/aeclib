# aeclib
Open-source automated code compliance building codes and standards.

aeclib translates building code provisions into executable and testable logic.

## Installation

```bash
pip install aeclib
```

## Intent
The goal of aeclib is to provide a unified "Logic Layer" for the AEC industry to support automated compliance and computational design.

## Usage
`aeclib` is designed as a **Stateless Logic Layer**. It provides the atomic building blocks of architectural compliance without dictating a specific data schema.

### Atomic Logic
Each function in `aeclib` maps to a specific engineering or code requirement. You are responsible for mapping your own data (JSON, BIM, or Database) to the function's parameters.

### Compositional Compliance
The library is designed to be composed into your own application logic. Below is an example of how a user might bring their own JSON design data and map it to a custom Python class to run a specific chapter's compliance check:

```json
{
  "space_id": "RM-101",
  "function_type": "business",
  "gross_area": 1500.0,
  "net_area": 1200.0,
  "design_occupancy_count": 12
}
```

```python
from aeclib.occupancy import validate_occupant_load_without_fixed_seating, validate_increased_occupant_load

class OccupancyValidator:
    def check_space_occupancy(self, data: dict):
        # 1. Check required minimum occupant load (Section 1004.5)
        is_load_valid = validate_occupant_load_without_fixed_seating(
            function_type=data["function_type"],
            gross_area=data["gross_area"],
            net_area=data["net_area"],
            design_occupancy_count=data["design_occupancy_count"]
        )

        # 2. Check maximum density limit (Section 1004.5.1)
        is_density_valid = validate_increased_occupant_load(
            area=data["gross_area"],
            occupant_count=data["design_occupancy_count"]
        )

        return is_load_valid and is_density_valid
```

### Expected Output
When a design fact fails to comply, the library will return `FAIL` and log a detailed warning:

```text
WARNING:aeclib:[FAIL] Design occupancy (35) is less than required minimum of 40 for educational_classroom (net area: 800.0, factor: 20).
```

When a design is compliant, the function returns `PASS`.

## License

Licensed under the Apache License 2.0.