# Feature Specification: Configuration System

**Feature Branch**: `002-config-system`  
**Created**: 2026-04-19  
**Status**: Draft  
**Input**: User description: "build a configuration system with a config sub-package of doc-classify package. the config system should have two modes - development mode where the config is stored in the .tmp/config directory of the project and prod mode where the config is stored in the users home directory. Default is development. With a zsh script the mode can be changed just before a new release and another script reverses the mode to development. There are two types of configs - permanent configs in pyproject.toml (like version) and user adaptable configs in the .tmp/config directory or the users home directory."

## Clarifications

### Session 2026-04-19

- Q: Where is the mode indicator stored? → A: Source code constant in the config module (e.g., `MODE = "development"`). The zsh scripts use sed to toggle this value. The constant is baked into the released package.
- Q: What initial user-adaptable config keys for v1? → A: Minimal bootstrap set (log_level, output_format) — enough to validate the system end-to-end. Additional keys added by future features.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read Configuration Values at Runtime (Priority: P1)

As a user running doc-classify, the application reads configuration values seamlessly from the correct location based on the active mode, without any manual setup beyond initial installation.

**Why this priority**: This is the core value of the configuration system — the application must be able to load and provide configuration values for all other features to function.

**Independent Test**: Can be fully tested by importing the config sub-package and reading both permanent and user-adaptable config values. Delivers the ability for the application to behave differently based on configuration.

**Acceptance Scenarios**:

1. **Given** the application is in development mode, **When** a config value is requested, **Then** user-adaptable config is read from the project's `.tmp/config/` directory and permanent config is read from `pyproject.toml`.
2. **Given** the application is in production mode, **When** a config value is requested, **Then** user-adaptable config is read from the user's home directory and permanent config is read from `pyproject.toml`.
3. **Given** a user-adaptable config file does not exist yet, **When** the application starts, **Then** a default configuration file is created in the appropriate location with sensible defaults.
4. **Given** permanent config values exist in `pyproject.toml`, **When** a permanent config value (e.g., version) is requested, **Then** the value is read from `pyproject.toml` regardless of the active mode.

---

### User Story 2 - Modify User-Adaptable Configuration (Priority: P1)

As a user, I can view and change user-adaptable configuration values so that the application behavior adapts to my preferences and environment.

**Why this priority**: Users need the ability to customize the application's behavior. Without this, the configuration system provides no user-facing value.

**Independent Test**: Can be fully tested by modifying a user-adaptable config value and verifying the application reflects the change on the next run.

**Acceptance Scenarios**:

1. **Given** the application is running in development mode, **When** a user edits the config file in `.tmp/config/`, **Then** the application reflects the updated values on the next invocation.
2. **Given** the application is running in production mode, **When** a user edits the config file in the home directory, **Then** the application reflects the updated values on the next invocation.
3. **Given** a user sets an invalid value for a config key, **When** the application loads the config, **Then** a clear error message is displayed indicating the invalid value and the expected format.

---

### User Story 3 - Switch to Production Mode Before Release (Priority: P2)

As a developer preparing a release, I run a zsh script that switches the application's configuration mode from development to production, ensuring the released version reads config from the user's home directory.

**Why this priority**: Essential for the release workflow — ensures that distributed versions of the application use the correct production configuration paths.

**Independent Test**: Can be fully tested by running the release mode script and verifying that the mode indicator changes and the application subsequently reads config from the home directory location.

**Acceptance Scenarios**:

1. **Given** the application is in development mode, **When** the release mode script is executed, **Then** the configuration mode switches to production.
2. **Given** the mode has been switched to production, **When** the application starts, **Then** user-adaptable config is read from the user's home directory.
3. **Given** the mode is already production, **When** the release mode script is executed again, **Then** the script completes without error (idempotent behavior).

---

### User Story 4 - Revert to Development Mode After Release (Priority: P2)

As a developer who has completed a release, I run a zsh script that reverts the configuration mode back to development, restoring the local project config path for continued development work.

**Why this priority**: Developers must be able to return to their development workflow after a release without manual intervention.

**Independent Test**: Can be fully tested by running the revert script after a mode switch and verifying that the application reads config from `.tmp/config/` again.

**Acceptance Scenarios**:

1. **Given** the application is in production mode, **When** the revert script is executed, **Then** the configuration mode switches back to development.
2. **Given** the mode has been reverted to development, **When** the application starts, **Then** user-adaptable config is read from `.tmp/config/`.
3. **Given** the mode is already development, **When** the revert script is executed again, **Then** the script completes without error (idempotent behavior).

---

### Edge Cases

- What happens when the `.tmp/config/` directory does not exist in a fresh clone? The system creates it automatically with default config values.
- What happens when the user's home directory config location is not writable? A clear error message is displayed with guidance.
- What happens when `pyproject.toml` is missing or malformed? The system fails gracefully with a descriptive error pointing to the issue.
- What happens when config files contain unknown keys? Unknown keys are ignored with a warning, preserving forward compatibility.
- What happens when both development and production config files exist simultaneously? Only the config file for the active mode is used; the other is ignored.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `config` sub-package within the `doc_classify` package that serves as the single entry point for all configuration access.
- **FR-002**: System MUST support two configuration modes: "development" and "production".
- **FR-003**: System MUST default to "development" mode when no explicit mode has been set.
- **FR-004**: In development mode, user-adaptable configuration MUST be read from and written to the `.tmp/config/` directory relative to the project root.
- **FR-005**: In production mode, user-adaptable configuration MUST be read from and written to a dedicated directory in the user's home directory (`~/.doc-classify/`).
- **FR-006**: Permanent configuration values (e.g., application version) MUST always be read from `pyproject.toml`, regardless of the active mode.
- **FR-007**: System MUST store the active mode as a source code constant in the config module, defaulting to "development".
- **FR-008**: System MUST provide a zsh script that switches the mode constant from "development" to "production" for release preparation.
- **FR-009**: System MUST provide a zsh script that reverts the mode constant from "production" back to "development" after a release.
- **FR-010**: Both mode-switching scripts MUST be idempotent — running them when already in the target mode produces no error.
- **FR-011**: System MUST automatically create default configuration files when they do not exist at the expected location.
- **FR-012**: System MUST validate user-adaptable configuration values on load and provide clear error messages for invalid entries.
- **FR-013**: Permanent config values MUST NOT be modifiable through the config sub-package (read-only access).
- **FR-014**: The `.tmp/` directory MUST be excluded from version control (added to `.gitignore`).
- **FR-015**: The initial user-adaptable configuration MUST include at minimum: `log_level` (controls logging verbosity) and `output_format` (controls output presentation). Additional keys will be added by future features.

### Key Entities

- **ConfigMode**: A source code constant in the config module representing the active mode ("development" or "production"). Determines which file system path is used for user-adaptable configuration. Modified by zsh scripts at release time, baked into the distributed package.
- **PermanentConfig**: Read-only configuration values sourced from `pyproject.toml`. Includes application metadata such as version. Accessible regardless of mode.
- **UserConfig**: User-modifiable configuration values stored in a TOML file at the mode-dependent path. Initial keys: `log_level` (string, e.g., "info", "debug", "warning", "error") and `output_format` (string, e.g., "text", "json"). Supports reading, validation, and default creation. Extensible by future features.
- **ConfigManager**: Central coordinator that resolves the active mode, loads the appropriate config sources, and provides a unified access interface.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access any configuration value with a single function call or attribute access, without needing to know the storage location.
- **SC-002**: Switching between development and production mode completes in under 2 seconds via the provided scripts.
- **SC-003**: A fresh project clone with no existing config files produces a working default configuration on first run with zero manual setup.
- **SC-004**: 100% of permanent configuration values remain consistent regardless of mode switches.
- **SC-005**: Invalid configuration values produce user-friendly error messages that identify the specific key and expected format.
- **SC-006**: The configuration system adds no perceptible startup delay to the application (configuration loads in under 100 milliseconds for typical config sizes).

## Assumptions

- The project uses `pyproject.toml` as the authoritative source for permanent/build-time configuration (confirmed by existing project structure).
- The user's home directory is writable and accessible when running in production mode.
- The `.tmp/` directory is a project-local scratch space suitable for development-time artifacts and is not committed to version control.
- The production config directory in the user's home follows the convention `~/.doc-classify/` (XDG base directory conventions are not required for v1).
- The zsh scripts are run manually by the developer as part of the release and post-release workflow — they are not triggered automatically.
- The configuration file format for user-adaptable config is TOML, consistent with the project's existing use of `pyproject.toml`.
- Click CLI integration (e.g., a `config` subcommand) is out of scope for this feature; the config sub-package provides a programmatic API only.
