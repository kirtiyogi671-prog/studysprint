"""Input validation helpers. All raise ValidationError on bad input."""
from datetime import date, datetime

from . import config


class ValidationError(ValueError):
    """Raised when user supplied data is invalid."""


def validate_name(value: str, label: str = "Name") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} cannot be empty.")
    value = value.strip()
    if len(value) > config.MAX_NAME_LEN:
        raise ValidationError(f"{label} must be at most {config.MAX_NAME_LEN} characters.")
    return value


def validate_difficulty(value) -> int:
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValidationError("Difficulty must be an integer 1-5.")
    if not 1 <= value <= 5:
        raise ValidationError("Difficulty must be between 1 and 5.")
    return value


def validate_quality(value) -> int:
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValidationError("Recall quality must be an integer 0-5.")
    if not 0 <= value <= 5:
        raise ValidationError("Recall quality must be between 0 and 5.")
    return value


def validate_minutes(value) -> int:
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValidationError("Minutes must be a whole number.")
    if not 1 <= value <= config.MAX_SESSION_MINUTES:
        raise ValidationError(f"Minutes must be between 1 and {config.MAX_SESSION_MINUTES}.")
    return value


def validate_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        raise ValidationError("Date must be in YYYY-MM-DD format.")
