"""Custom exception hierarchy for the config sub-package.

All config-related exceptions inherit from ``ConfigError``, enabling
callers to catch a single base class while still distinguishing
specific failure modes.
"""


class ConfigError(Exception):
    """Base exception for all configuration errors."""


class ConfigNotFoundError(ConfigError):
    """Raised when a required configuration file cannot be located."""


class ConfigValidationError(ConfigError):
    """Raised when a configuration value fails validation.

    Attributes:
        key: The configuration key that failed validation.
        value: The invalid value that was provided.
        allowed: Human-readable description of the allowed values.
    """

    def __init__(self, key: str, value: str, allowed: str) -> None:
        self.key = key
        self.value = value
        self.allowed = allowed
        super().__init__(
            f"Invalid value {value!r} for config key {key!r}. Allowed values: {allowed}"
        )
