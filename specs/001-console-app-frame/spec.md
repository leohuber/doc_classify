# Feature Specification: Console Application Frame

**Feature Branch**: `001-console-app-frame`  
**Created**: 2026-04-18  
**Status**: Draft  
**Input**: User description: "build a python application that can be installed as console script on a mac os x - for now only build the frame of the application"

## Clarifications

### Session 2026-04-18

- Q: What should the console command name be? → A: `doc-classify` (hyphenated, matches project name)
- Q: What is the minimum supported Python version? → A: Python 3.14
- Q: What is the initial version number? → A: `0.1.0` (SemVer initial development)
- Q: How should installation be automated? → A: Shell script (`install.sh`) that creates venv, installs package, and symlinks the console command — no manual environment setup required
- Q: How should releases be distributed? → A: A `release.sh` script that builds the Python package, bundles it with `install.sh` into a versioned zip file (`<project>-<version>.zip`), creates a git tag on main, and publishes a GitHub release with the zip attached
- Q: What is the installation model? → A: Users install exclusively from the released zip file (download → extract → run `install.sh`). Cloning the repo is not an installation path — it is only for development.
- Q: Is `--verbose` flag needed in the frame? → A: No. Verbose output is not needed — removed from scope.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Release and Install the Application (Priority: P1)

A maintainer creates a distributable release by running a release script from the main branch. The script reads the version from `pyproject.toml`, builds the Python package, bundles it together with the installation script into a versioned zip file, creates a git tag, and publishes a GitHub release with the zip file attached. An end user downloads the zip file from the GitHub release, extracts it, and runs the included installation script. The script automatically creates an isolated Python environment, installs the application, and makes the `doc-classify` command available on their system. No repository cloning, manual environment setup, or Python knowledge is required.

**Why this priority**: This is the foundational capability — without a working release and install pipeline, no features can reach end users. It validates the entire distribution chain from source to running application.

**Independent Test**: Can be fully tested by running `./release.sh` on main, downloading the resulting zip from GitHub, extracting it, running `./install.sh`, and invoking `doc-classify`. Delivers a complete distribution pipeline proof.

**Acceptance Scenarios**:

1. **Given** the maintainer is on the main branch with a clean working tree, **When** the maintainer runs `./release.sh`, **Then** the script reads the version from `pyproject.toml`, builds the Python package, creates a zip file named `doc-classify-<version>.zip` containing the package and `install.sh`, tags the repository with the version, and publishes a GitHub release with the zip file attached.
2. **Given** a user has downloaded and extracted the release zip file and Python 3.14+ is available, **When** the user runs `./install.sh`, **Then** the script creates an isolated Python environment, installs the application, and makes the `doc-classify` command available — all without manual intervention.
3. **Given** the installation script has completed, **When** the user runs `doc-classify` with no arguments, **Then** the application displays a help message describing available commands and usage.
4. **Given** the installation script has completed, **When** the user runs `doc-classify --version`, **Then** the application displays the current version number.
5. **Given** the system does not have Python 3.14+, **When** the user runs `./install.sh`, **Then** the script exits with a clear error message indicating the minimum Python version required.
6. **Given** the maintainer is on a branch other than main, **When** the maintainer runs `./release.sh`, **Then** the script exits with a clear error message indicating releases can only be created from the main branch.
7. **Given** a git tag for the current version already exists, **When** the maintainer runs `./release.sh`, **Then** the script exits with a clear error message indicating the version has already been released.

---

### User Story 2 - View Application Version (Priority: P2)

A user wants to verify which version of the application is installed. They run the console command with a version flag and see the current version.

**Why this priority**: Version reporting is essential for support, debugging, and ensuring the correct release is installed. It validates that version metadata flows from packaging to runtime.

**Independent Test**: Can be fully tested by running the console command with `--version` and verifying the output matches the version declared in `pyproject.toml`.

**Acceptance Scenarios**:

1. **Given** the application is installed, **When** the user runs the console command with `--version`, **Then** the displayed version matches the version declared in the project packaging metadata.

---

### Edge Cases

- What happens when the user runs the console command with an unrecognized argument? The application displays an informative error message and the help text.
- What happens when the application is run outside a virtual environment? The application functions normally — virtual environments are a development practice, not a runtime requirement.
- What happens when the user installs on a system without a supported Python version? The installation script exits with a clear error message indicating the minimum Python version required.
- What happens when the user runs `install.sh` a second time? The script handles re-installation gracefully (updates the existing environment rather than failing).
- What happens when `release.sh` is run from a non-main branch? The script exits with a clear error indicating releases must be created from main.
- What happens when `release.sh` is run and the version tag already exists? The script exits with a clear error indicating the version has already been released.
- What happens when `release.sh` is run with uncommitted changes? The script exits with a clear error requiring a clean working tree.
- What happens when the `gh` CLI is not installed or not authenticated? The release script exits with a clear error indicating `gh` is required and must be authenticated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST be installable via a single shell script (`install.sh`) bundled in the release zip file. The script automatically creates an isolated Python environment, installs the package, and makes the console command available — no repository cloning, manual environment setup, or Python knowledge required.
- **FR-002**: System MUST register a console script entry point named `doc-classify` so that the command is available on the PATH after installation.
- **FR-003**: System MUST display a help message with usage information when invoked with no arguments or with `--help`.
- **FR-004**: System MUST display the current version when invoked with `--version`.
- **FR-005**: System MUST display an informative error message and help text when invoked with unrecognized arguments.
- **FR-006**: System MUST declare Python 3.14 as the minimum supported Python version in its packaging metadata.
- **FR-007**: System MUST use a single version source of truth — the version displayed at runtime MUST match the version in the packaging metadata. The initial version MUST be `0.1.0`.
- **FR-008**: System MUST return appropriate exit codes: 0 for success, non-zero for errors.
- **FR-009**: System MUST include a project configuration file (`pyproject.toml`) with all required packaging metadata (name, version, description, author, license, dependencies, entry points).
- **FR-010**: The installation script MUST verify that the minimum Python version (3.14) is available before proceeding, and exit with a clear error if not.
- **FR-011**: System MUST also remain installable via standard `pip install` for development workflows (editable mode).
- **FR-012**: System MUST include a release script (`release.sh`) that builds a distributable Python package from the source.
- **FR-013**: The release script MUST create a zip file named `doc-classify-<version>.zip` containing the built Python package and the `install.sh` script.
- **FR-014**: The release script MUST read the version from `pyproject.toml` as the single source of truth for the release version.
- **FR-015**: The release script MUST create a git tag matching the version (e.g., `v0.1.0`) on the current repository state.
- **FR-016**: The release script MUST publish a GitHub release using the `gh` CLI, attaching the zip file as a release asset.
- **FR-017**: The release script MUST verify it is running on the main branch and the working tree is clean before proceeding, exiting with a clear error otherwise.
- **FR-018**: The release script MUST verify that the version tag does not already exist before proceeding, exiting with a clear error if the version has already been released.
- **FR-019**: The release script MUST verify that the `gh` CLI is installed and authenticated before proceeding, exiting with a clear error otherwise.

### Key Entities

- **Application Package**: The installable Python package containing the console script entry point, version metadata, and CLI framework.
- **Installation Script**: The `install.sh` shell script that automates environment creation, package installation, and command registration.
- **Release Script**: The `release.sh` shell script that builds, packages, tags, and publishes a GitHub release.
- **Release Zip**: The `doc-classify-<version>.zip` distributable archive containing the built Python package and `install.sh`.
- **Console Command**: The `doc-classify` command registered as an entry point, serving as the user's primary interface to the application.
- **CLI Arguments**: The set of flags and options accepted by the console command (initially `--help`, `--version`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can download the release zip, extract it, and install the application by running a single script — no repository cloning, manual environment setup, or pip commands required.
- **SC-002**: The console command responds to `--help` and `--version` flags correctly on every invocation.
- **SC-003**: Unrecognized arguments produce a user-friendly error message — no tracebacks or cryptic output are shown to the user.
- **SC-004**: The application's version output displays `0.1.0` and matches the version declared in the project packaging metadata with 100% consistency.
- **SC-005**: The application runs successfully on macOS with Python 3.14 or later.
- **SC-006**: A maintainer can create a complete GitHub release by running a single script from the main branch.
- **SC-007**: The release zip file contains everything needed for a user to install the application (Python package + install script) — no additional downloads required.
- **SC-008**: The release script prevents duplicate releases by checking for existing version tags before proceeding.

## Assumptions

- The target platform is macOS, but standard Python packaging practices will be used so the application is not inherently platform-specific.
- This specification covers only the application frame — no business logic, data processing, or external integrations are in scope.
- The console command is named `doc-classify`.
- Users have Python 3.14+ available on their system; the installation script bundled in the release zip handles everything else (venv creation, package installation, command symlinking).
- The project will follow the conventions established in the doc_classify constitution (Ruff linting, Google-style docstrings, type hints, etc.).
- An argument parsing library from the Python standard library or a well-known third-party library will be used — the specific choice is an implementation detail.
- Standard `pip install -e .` remains supported for developer workflows (requires cloning the repository).
- The `gh` CLI (GitHub CLI) is available on the maintainer's system for creating releases.
- Releases are always created from the main branch with a clean working tree.
