class NotFoundError(Exception):
    """Raised when an entity is not found in repository."""


class ValidationError(Exception):
    """Raised when input validation fails."""
