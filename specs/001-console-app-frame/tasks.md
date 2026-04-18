# Tasks: Console Application Frame

**Input**: Design documents from `/specs/001-console-app-frame/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/cli-contract.md ✅, quickstart.md ✅

**Tests**: Included — plan.md defines `tests/test_cli.py` as part of the project structure.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (per plan.md)

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project scaffolding, configure packaging, and install dependencies

- [X] T001 Create project directory structure: `src/doc_classify/` and `tests/` per implementation plan
- [X] T002 Create pyproject.toml with: build-system (hatchling), project metadata (name=`doc-classify`, version=`0.1.0`, requires-python=`>=3.14`), dependency `click>=8.1`, dev dependency-groups (ruff, pytest), entry point `doc-classify = "doc_classify.cli:main"`, and tool config for ruff (`select=["ALL"]`, `line-length=88`) in pyproject.toml
- [X] T003 Run `uv sync` to generate uv.lock and install all dependencies into the project virtual environment

---

## Phase 2: Foundational (Core CLI)

**Purpose**: Implement the Click CLI entry point that BOTH user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 [P] Create empty package init file in src/doc_classify/__init__.py
- [X] T005 [P] Implement Click CLI entry point in src/doc_classify/cli.py: `@click.group(invoke_without_command=True)` with `@click.version_option(version=version("doc-classify"), prog_name="doc-classify")` using `importlib.metadata.version`, `@click.pass_context` to show help when no subcommand given, Google-style docstring, type hints on all signatures
- [X] T006 Create tests/__init__.py and tests/test_cli.py with Click `CliRunner` integration tests covering: `--help` (exit 0, contains "Usage"), `--version` (exit 0, contains "0.1.0"), no args (exit 0, shows help), unknown option `--foo` (exit 2), unknown command `badcommand` (exit 2)

**Checkpoint**: `uv run doc-classify --help` and `uv run doc-classify --version` work correctly. `uv run pytest` passes. `uv run ruff check src/ tests/` clean.

---

## Phase 3: User Story 1 — Release and Install the Application (Priority: P1) 🎯 MVP

**Goal**: A maintainer can create a GitHub release with `./release.sh`, and an end user can install the application from the release zip by running `./install.sh` — no Python knowledge or repo cloning required.

**Independent Test**: Run `./release.sh` on main → download zip from GitHub → extract → run `./install.sh` → invoke `doc-classify --help` and `doc-classify --version`.

### Implementation for User Story 1

- [X] T007 [P] [US1] Create install.sh at repository root: check Python >=3.14 via version parsing (exit 1 with clear error if not met), create venv at `~/.local/share/doc-classify/` (or upgrade existing), pip install the wheel from the same directory, create symlink at `~/.local/bin/doc-classify`, handle re-installation gracefully, support `--help` flag, print PATH hint if `~/.local/bin` is not on PATH
- [X] T008 [P] [US1] Create release.sh at repository root: pre-flight checks in order (1. on main branch, 2. clean working tree, 3. `gh` CLI installed, 4. `gh` authenticated, 5. version tag `v<version>` does not exist) — each with clear error message and exit 1; read version from pyproject.toml via Python one-liner; run `uv build` to produce wheel in `dist/`; create `doc-classify-<version>.zip` containing wheel and install.sh; create git tag `v<version>`; publish GitHub release via `gh release create` with zip attached; clean up dist/ and zip staging area
- [X] T009 [US1] Make install.sh and release.sh executable (`chmod +x`), validate shell syntax with `bash -n install.sh` and `bash -n release.sh`, and verify scripts contain proper shebang (`#!/usr/bin/env bash`) and `set -euo pipefail`

**Checkpoint**: Both scripts pass syntax validation. `install.sh --help` prints usage. `release.sh` pre-flight checks fail gracefully when not on main or when tag exists.

---

## Phase 4: User Story 2 — View Application Version (Priority: P2)

**Goal**: A user can verify which version of the application is installed by running `doc-classify --version`, and the displayed version always matches the version declared in `pyproject.toml`.

**Independent Test**: Run `doc-classify --version` and verify output is exactly `doc-classify, version 0.1.0` matching `pyproject.toml`.

### Implementation for User Story 2

- [X] T010 [US2] Verify the version pipeline end-to-end: confirm `uv run doc-classify --version` output format matches cli-contract.md (`doc-classify, version 0.1.0`), confirm version is sourced from `importlib.metadata.version("doc-classify")` (not hardcoded), and ensure the dedicated version test in tests/test_cli.py validates output against the metadata

**Checkpoint**: `uv run doc-classify --version` outputs `doc-classify, version 0.1.0`. Version test in test_cli.py passes and validates against package metadata.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, final validation, and cleanup

- [X] T011 [P] Update README.md with project description, development setup instructions (uv sync, uv run commands), project structure overview, and link to quickstart.md patterns
- [X] T012 Run full validation suite: `uv run pytest` (all tests pass), `uv run ruff check src/ tests/` (no lint violations), `uv run ruff format --check src/ tests/` (formatting clean), and verify all CLI contract behaviors from contracts/cli-contract.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) — needs working CLI
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) — needs working --version
  - US1 and US2 can proceed in parallel (different files, no cross-dependencies)
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on US2
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) — No dependencies on US1

### Within Each Phase

- Setup: Sequential (T001 → T002 → T003)
- Foundational: T004 ∥ T005, then T006 (tests reference cli.py)
- User Story 1: T007 ∥ T008, then T009 (validation needs both scripts)
- User Story 2: Single task (T010)
- Polish: T011 parallel, T012 last (validates everything)

### Parallel Opportunities

- **Phase 2**: T004 (\_\_init\_\_.py) and T005 (cli.py) — different files, no dependencies
- **Phase 3**: T007 (install.sh) and T008 (release.sh) — different scripts, no dependencies
- **Phase 3 ∥ Phase 4**: US1 and US2 can run concurrently after Foundational completes
- **Phase 5**: T011 (README) can run in parallel with any remaining work

---

## Parallel Example: User Story 1

```bash
# Launch both scripts in parallel (different files, no dependencies):
Task T007: "Create install.sh at repository root"
Task T008: "Create release.sh at repository root"

# Then validate both together:
Task T009: "Validate install.sh and release.sh"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundational (T004–T006)
3. Complete Phase 3: User Story 1 (T007–T009)
4. **STOP and VALIDATE**: Test the release and install pipeline independently
5. Deploy/demo if ready — the entire distribution chain works

### Incremental Delivery

1. Setup + Foundational → CLI frame works (`doc-classify --help`, `--version`)
2. Add User Story 1 → Release and install pipeline works (MVP!)
3. Add User Story 2 → Version metadata verification complete
4. Polish → README, full validation, cleanup

### Single Developer Strategy

1. Complete Setup + Foundational sequentially
2. User Story 1 (P1): install.sh and release.sh in parallel, then validate
3. User Story 2 (P2): Quick verification task
4. Polish: README + full validation

---

## Notes

- [P] tasks = different files, no dependencies — safe for parallel execution
- [US*] label maps task to specific user story for traceability
- All code must follow constitution: Google-style docstrings, type hints, Ruff `select=["ALL"]`, line-length 88
- Shell scripts must use `#!/usr/bin/env bash` and `set -euo pipefail`
- Commit after each task or logical group
- Stop at any checkpoint to validate independently
