<!--
  Sync Impact Report
  ==================
  Version change: N/A → 1.0.0 (initial ratification)
  Modified principles: N/A (initial creation)
  Added sections:
    - Core Principles (5 principles: Code Quality, Modularity,
      Consistency, Readability, Python Standards Compliance)
    - Python Tooling & Standards
    - Development Workflow & Quality Gates
    - Governance
  Removed sections: N/A
  Templates requiring updates:
    - .specify/templates/plan-template.md ✅ compatible (generic
      Constitution Check gate)
    - .specify/templates/spec-template.md ✅ compatible (MUST/SHOULD
      language aligned)
    - .specify/templates/tasks-template.md ✅ compatible (phase
      structure supports linting/formatting tasks)
    - .specify/templates/checklist-template.md ✅ compatible (generic
      structure)
  Follow-up TODOs: None
-->

# doc_classify Constitution

## Core Principles

### I. Code Quality (NON-NEGOTIABLE)

All code in this project MUST meet a high quality bar before merge.
Non-negotiable rules:

- Every function and method MUST have a single, clear purpose.
- Dead code, commented-out code, and unreachable branches MUST be
  removed before merge.
- Cyclomatic complexity per function MUST NOT exceed 10. Functions
  exceeding this limit MUST be refactored into smaller units.
- All public APIs (functions, classes, modules) MUST have docstrings
  following Google-style docstring conventions.
- Magic numbers and string literals MUST be extracted into named
  constants with descriptive names.
- Exception handling MUST be specific — bare `except:` and
  `except Exception:` without re-raise or logging are prohibited.

**Rationale**: High code quality reduces defect density, lowers
maintenance cost, and ensures the codebase remains approachable
for all contributors over time.

### II. Modularity

The codebase MUST be organized into cohesive, loosely coupled
modules that can be understood, tested, and modified independently.

- Each module MUST have a single, well-defined responsibility
  (Single Responsibility Principle).
- Cross-module dependencies MUST flow in one direction; circular
  imports are prohibited.
- Shared utilities MUST live in a dedicated `utils` or `common`
  module — not duplicated across feature modules.
- Module boundaries MUST be enforced through clear public APIs;
  internal implementation details SHOULD be prefixed with `_`.
- New modules MUST be justified by a distinct functional domain —
  organizational-only modules are not permitted.

**Rationale**: Modular code enables parallel development, isolated
testing, and safe refactoring without cascading side effects.

### III. Consistency

All code MUST follow uniform patterns, conventions, and idioms so
that any part of the codebase reads as if written by one author.

- Naming conventions MUST follow PEP 8: `snake_case` for functions,
  methods, and variables; `PascalCase` for classes; `UPPER_SNAKE`
  for constants.
- Project structure and file organization MUST follow the layout
  established in the implementation plan — no ad-hoc directories.
- Error handling patterns MUST be uniform: use custom exception
  hierarchies rooted in a project-level base exception.
- Configuration MUST be loaded through a single mechanism (e.g.,
  environment variables via a settings module) — not scattered
  across files.
- Import ordering MUST follow: stdlib → third-party → local, each
  group separated by a blank line, enforced by Ruff's isort rules.

**Rationale**: Consistency eliminates cognitive overhead when
navigating the codebase and makes automated tooling more effective.

### IV. Readability

Code MUST be written for humans first and machines second. Every
contributor MUST be able to understand any module without needing
the original author's explanation.

- Variable and function names MUST be descriptive and
  self-documenting — avoid single-letter names except for trivial
  loop indices (`i`, `j`) or well-known conventions (`x`, `y`
  for coordinates).
- Functions MUST be short enough to fit on a single screen (~40
  lines maximum). If a function exceeds this, it MUST be split.
- Nested logic MUST NOT exceed 3 levels of indentation. Use early
  returns, guard clauses, or helper functions to flatten control
  flow.
- Type hints MUST be used on all function signatures (parameters
  and return types). Inline type comments are not acceptable —
  use PEP 484+ annotation syntax.
- Comments MUST explain *why*, not *what*. If code needs a comment
  to explain what it does, it SHOULD be refactored for clarity.

**Rationale**: Readable code is debuggable code. Readability
directly correlates with onboarding speed and defect detection rate.

### V. Python Standards Compliance — Ruff (NON-NEGOTIABLE)

All Python code MUST pass Ruff with **all available rule sets
enabled** and zero violations. This is a hard gate — code with
Ruff violations MUST NOT be merged.

- Ruff MUST be configured in `pyproject.toml` (or `ruff.toml`)
  with `select = ["ALL"]` to enable every rule category.
- Per-file rule ignores (`# noqa`) MUST include an explicit rule
  code (e.g., `# noqa: E501`) and a justification comment.
  Blanket `# noqa` without a code is prohibited.
- The Ruff formatter (`ruff format`) MUST be used as the sole
  formatter. No other formatters (Black, autopep8, yapf) are
  permitted to avoid conflicts.
- Line length MUST be set to 88 characters (Ruff/Black default).
- Any rule that is intentionally disabled project-wide MUST be
  documented in `pyproject.toml` with a comment explaining why.
- Ruff MUST be integrated into CI — pull requests that fail Ruff
  checks MUST be blocked from merge.

**Rationale**: Enforcing all Ruff standards provides comprehensive
coverage of PEP 8, pyflakes, pycodestyle, isort, pydocstyle,
pylint, and dozens of additional rule sets in a single fast tool,
eliminating style debates and catching real bugs early.

## Python Tooling & Standards

This section codifies the mandatory toolchain for all Python
development in this project.

- **Linting & Formatting**: Ruff (`ruff check` + `ruff format`)
  is the single source of truth for linting and formatting.
- **Type Checking**: All code SHOULD be checked with a static type
  checker (mypy or pyright). Type errors SHOULD be resolved before
  merge.
- **Dependency Management**: Dependencies MUST be declared in
  `pyproject.toml`. Pinned versions MUST be used for reproducible
  builds.
- **Python Version**: The minimum supported Python version MUST be
  declared in `pyproject.toml` and enforced in CI.
- **Virtual Environments**: All development MUST occur within an
  isolated virtual environment. System-level package installation
  is prohibited.
- **Pre-commit Hooks**: Ruff SHOULD be configured as a pre-commit
  hook to catch violations before they reach CI.

## Development Workflow & Quality Gates

All changes MUST pass through the following quality gates before
merge:

1. **Local Validation**: Developer MUST run `ruff check .` and
   `ruff format --check .` locally before pushing. Both MUST pass
   with zero violations.
2. **Code Review**: Every change MUST be reviewed by at least one
   other contributor. Reviewers MUST verify adherence to all five
   core principles.
3. **CI Pipeline**: Automated CI MUST run linting (Ruff), type
   checking (if configured), and all tests. Any failure blocks
   merge.
4. **Test Coverage**: New code SHOULD include tests. Untested code
   MUST be justified with a comment or linked issue explaining why
   tests are deferred.
5. **Documentation**: Public API changes MUST be accompanied by
   updated docstrings. README or user-facing docs MUST be updated
   when behavior changes.

## Governance

This constitution is the supreme authority for all development
practices in the doc_classify project. In case of conflict between
this constitution and any other document, this constitution
prevails.

- **Amendments**: Any change to this constitution MUST be proposed
  as a pull request with a clear rationale. Amendment PRs MUST be
  reviewed and approved before merge.
- **Versioning**: This constitution follows semantic versioning:
  - MAJOR: Removal or redefinition of a core principle.
  - MINOR: Addition of a new principle or material expansion of
    existing guidance.
  - PATCH: Clarifications, typo fixes, non-semantic refinements.
- **Compliance Review**: All pull requests and code reviews MUST
  verify compliance with the core principles. Violations MUST be
  resolved before merge — no exceptions.
- **Complexity Justification**: Any deviation from these principles
  MUST be documented in the implementation plan with a written
  justification and a simpler alternative that was considered and
  rejected.

**Version**: 1.0.0 | **Ratified**: 2026-04-18 | **Last Amended**: 2026-04-18
