from typing import (
    Literal,
)

# Types will be replaced by our own typing in the future.
EventType = Literal["INSERT", "MODIFY", "REMOVE"]
RecordType = Literal[
    "NEW_IMAGE", "OLD_IMAGE", "NEW_AND_OLD_IMAGES", "KEYS_ONLY"
]
VulnerabilityType = Literal["INPUTS", "LINES", "PORTS"]
VulnerabilityStatusType = Literal[
    "SAFE", "VULNERABLE", "SUBMITTED", "REJECTED"
]
TreatmentStatusType = Literal[
    "UNTREATED", "IN_PROGRESS", "ACCEPTED", "ACCEPTED_UNDEFINED"
]
SeverityLevelType = Literal["low", "medium", "high", "critical"]
