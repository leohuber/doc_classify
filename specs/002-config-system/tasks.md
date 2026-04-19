# Tasks: Configuration System

**Input**: Design documents from `/specs/002-config-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Included — constitution requires tests for new code, and spec defines acceptance scenarios for each story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create config sub-package directory structure and test directory

- [ ] T001 Create config sub-package directory at src/doc_classify/config/ and test directory at tests/test_config/ with __init__.py files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core modules that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T002 [P] Create custom exception hierarchy in src/doc_classify/config/_exceptions.py (ConfigError base, ConfigNotFoundError, ConfigValidationError — Google docstrings, specific exception classes per Constitution I & III)
- [ ] T003 [P] Create config defaults and schema in src/doc_classify/config/_defaults.py (DEFAULT_LOG_LEVEL="info", DEFAULT_OUTPUT_FORMAT="text", VALID_LOG_LEVELS frozenset, VALID_OUTPUT_FORMATS frozenset, DEFAULT_CONFIG_TEMPLATE string, CONFIG_FILE_NAME="config.toml", CONFIG_SCHEMA dict mapping keys to allowed values)
- [ ] T004 [P] Create mode constant and helper in src/doc_classify/config/_mode.py (MODE: Literal["development", "production"] = "development", get_mode() → str function, DEVELOPMENT/PRODUCTION named constants)
- [ ] T005 Create path resolution in src/doc_classify/config/_paths.py (get_config_dir() → Path, _find_project_root() → Path using __file__ ancestor + pyproject.toml check, DEV_CONFIG_SUBDIR=".tmp/config", PROD_CONFIG_DIR="~/.doc-classify" — depends on _mode.py)
- [ ] T006 Create validation logic in src/doc_classify/config/_validation.py (validate_config(data: dict) → dict function, raises ConfigValidationError with key name and expected format for invalid values, logs warning for unknown keys — depends on _defaults.py)

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 — Read Configuration Values at Runtime (Priority: P1) 🎯 MVP

**Goal**: Application reads config values seamlessly from the correct location based on active mode, with auto-creation of defaults on first run.

**Independent Test**: Import config sub-package → read permanent values (version, name) → read user values (log_level, output_format) → verify correct paths per mode → verify defaults created when absent.

### Implementation for User Story 1

- [ ] T007 [P] [US1] Create PermanentConfig in src/doc_classify/config/_permanent.py (frozen dataclass with version: str and name: str fields, load via importlib.metadata.version/metadata, read-only by design per FR-013)
- [ ] T008 [US1] Create UserConfig in src/doc_classify/config/_user.py (dataclass with log_level: str and output_format: str, load_user_config() reads TOML via tomllib from mode-dependent path, _create_default_config() writes DEFAULT_CONFIG_TEMPLATE to path with mkdir -p, _ensure_config_exists() auto-creates if missing — depends on _paths, _defaults, _validation, _exceptions)
- [ ] T009 [US1] Create public API in src/doc_classify/config/__init__.py (AppConfig dataclass combining permanent: PermanentConfig + user: UserConfig, get_config() → AppConfig, get_permanent() → PermanentConfig, get_user_config() → UserConfig convenience functions, module docstring, __all__ exports)

### Tests for User Story 1

- [ ] T010 [P] [US1] Write tests/test_config/test_mode.py (test MODE defaults to "development", test get_mode() returns valid literal, test DEVELOPMENT/PRODUCTION constants match expected values)
- [ ] T011 [P] [US1] Write tests/test_config/test_paths.py (test dev mode returns .tmp/config/ relative to project root, test prod mode returns ~/.doc-classify/, test _find_project_root() finds pyproject.toml ancestor, use tmp_path and monkeypatch fixtures)
- [ ] T012 [P] [US1] Write tests/test_config/test_permanent.py (test version matches importlib.metadata.version("doc-classify"), test name is "doc-classify", test PermanentConfig is frozen/immutable)
- [ ] T013 [US1] Write tests/test_config/test_user.py (test default config file created when absent with correct content, test load reads existing TOML correctly, test correct path used per mode using tmp_path, test log_level and output_format defaults)
- [ ] T014 [US1] Write tests/test_config/test_integration.py (test get_config() returns AppConfig with both permanent and user data, test fresh directory with no config produces working defaults, test dev mode reads from .tmp/config/, test prod mode reads from home dir)

**Checkpoint**: User Story 1 fully functional — config system reads values from correct locations, creates defaults automatically

---

## Phase 4: User Story 2 — Modify User-Adaptable Configuration (Priority: P1)

**Goal**: Users edit the TOML config file and the application reflects changes on next invocation, with clear error messages for invalid values.

**Independent Test**: Edit config.toml with valid values → app reflects changes. Edit with invalid values → clear error message with key name and expected format.

### Implementation for User Story 2

- [ ] T015 [US2] Enhance error messages in _user.py and _validation.py to include the specific invalid key, the invalid value provided, and the list of allowed values per FR-012 and SC-005 in src/doc_classify/config/_user.py and src/doc_classify/config/_validation.py

### Tests for User Story 2

- [ ] T016 [P] [US2] Write tests/test_config/test_validation.py (test valid log_level values all pass, test valid output_format values pass, test invalid log_level raises ConfigValidationError with key name in message, test invalid output_format raises ConfigValidationError, test unknown keys produce warning but don't fail, test error message contains expected format hint)
- [ ] T017 [US2] Add modification scenarios to tests/test_config/test_user.py (test editing config.toml and reloading reflects new values, test editing to invalid value raises error on next load, test partial edit preserving other keys)

**Checkpoint**: User Story 2 complete — config edits reflected, invalid values produce clear errors

---

## Phase 5: User Story 3 — Switch to Production Mode (Priority: P2)

**Goal**: Developer runs a zsh script to switch mode constant from "development" to "production" before release.

**Independent Test**: Run set-mode-prod.zsh → verify _mode.py constant changed to "production" → run again (idempotent, no error).

### Implementation for User Story 3

- [ ] T018 [US3] Create set-mode-prod.zsh in project root (#!/usr/bin/env zsh, set -euo pipefail, sed -i replacement of MODE = "development" to MODE = "production" in src/doc_classify/config/_mode.py, idempotent — check current value first, echo confirmation message, chmod +x)

### Tests for User Story 3

- [ ] T019 [US3] Write mode switching tests in tests/test_config/test_scripts.py (test set-mode-prod.zsh changes constant to "production" via subprocess, test idempotent — running when already production succeeds without error, use tmp_path with copy of _mode.py to avoid modifying source)

**Checkpoint**: Production mode switch works — ready for release workflow

---

## Phase 6: User Story 4 — Revert to Development Mode (Priority: P2)

**Goal**: Developer runs a zsh script to revert mode constant from "production" back to "development" after release.

**Independent Test**: Run set-mode-dev.zsh → verify _mode.py constant changed to "development" → run again (idempotent, no error).

### Implementation for User Story 4

- [ ] T020 [P] [US4] Create set-mode-dev.zsh in project root (#!/usr/bin/env zsh, set -euo pipefail, sed -i replacement of MODE = "production" to MODE = "development" in src/doc_classify/config/_mode.py, idempotent — check current value first, echo confirmation message, chmod +x)

### Tests for User Story 4

- [ ] T021 [US4] Write mode revert tests in tests/test_config/test_scripts.py (test set-mode-dev.zsh changes constant to "development" via subprocess, test idempotent — running when already development succeeds without error, test round-trip: prod→dev→prod all succeed)

**Checkpoint**: Development mode revert works — post-release workflow complete

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Validation, cleanup, and quality assurance across all stories

- [ ] T022 [P] Run uv run ruff check src/doc_classify/config/ tests/test_config/ and fix any violations
- [ ] T023 [P] Run uv run ruff format src/doc_classify/config/ tests/test_config/ and verify formatting
- [ ] T024 Run uv run pytest to verify full test suite passes (existing + new tests)
- [ ] T025 Validate quickstart.md examples work end-to-end (import config, read values, verify defaults created)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational — core config reading
- **US2 (Phase 4)**: Depends on US1 — validation builds on reading infrastructure
- **US3 (Phase 5)**: Depends on US1 — needs config system to verify mode switch works
- **US4 (Phase 6)**: Depends on US1 — needs config system to verify mode revert works
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P1)**: Depends on US1 — validation extends the reading infrastructure
- **User Story 3 (P2)**: Depends on US1 — can run in parallel with US2 and US4
- **User Story 4 (P2)**: Depends on US1 — can run in parallel with US2 and US3

### Within Each User Story

- Implementation before tests (tests reference the implemented modules)
- Models/dataclasses before service logic
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- Phase 2: T002, T003, T004 can all run in parallel (no cross-dependencies)
- Phase 3: T007 parallel with other US1 implementation. T010, T011, T012 parallel test writing
- Phase 4 + Phase 5 + Phase 6: US2, US3, US4 can all start once US1 is complete
- Phase 5 + Phase 6: US3 and US4 are fully independent — can run in parallel
- Phase 7: T022 and T023 in parallel

---

## Parallel Example: User Story 1

```bash
# After Foundational phase, launch parallel implementation:
Task T007: "Create PermanentConfig in src/doc_classify/config/_permanent.py"
# (parallel — different file, no deps on T008/T009)

# After T007+T008+T009, launch parallel tests:
Task T010: "Write tests/test_config/test_mode.py"
Task T011: "Write tests/test_config/test_paths.py"
Task T012: "Write tests/test_config/test_permanent.py"
```

## Parallel Example: US3 + US4

```bash
# After US1 complete, launch both script stories in parallel:
Task T018: "Create set-mode-prod.zsh" (US3)
Task T020: "Create set-mode-dev.zsh" (US4)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test US1 independently — config reads work, defaults created
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP!
3. Add User Story 2 → Test independently → Validation complete
4. Add User Stories 3+4 (parallel) → Test independently → Release workflow ready
5. Polish → All quality gates pass

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- `tomllib` is stdlib (Python 3.11+) — no dependency to add
- TOML writing uses string template (research.md R2) — no `tomli-w` needed
- Mode constant sed replacement targets `_mode.py` only (research.md R4)
