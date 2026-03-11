from dataclasses import dataclass
from enum import Enum


class ComplianceStatus(str, Enum):
    """Standardized statuses for building code compliance checks."""

    PASS = "PASS"
    FAIL = "FAIL"
    NOT_APPLICABLE = "NOT_APPLICABLE"


@dataclass(frozen=True)
class ComplianceResult:
    """
    Standardized return object for all compliance functions.

    Attributes:
        status: The compliance outcome (PASS, FAIL, or NOT_APPLICABLE).
        message: A human-readable explanation of the result (optional for PASS).
    """

    status: ComplianceStatus
    message: str = ""

    def __bool__(self) -> bool:
        """
        Allows the result to be used in boolean contexts.
        Returns True for PASS, False otherwise.
        """
        return self.status == ComplianceStatus.PASS

    def __repr__(self) -> str:
        return f"[{self.status}] {self.message}"
