# Tasks: Display Sources Data

**Input**: Design documents from `/specs/002-display-sources-data/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/  
**Branch**: `002-display-sources-data`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `src/` at repository root per plan.md
- **Database module**: `src/database/` for Astrodbkit queries
- **Tests**: `tests/` directory following existing pattern
- Paths follow Constitution requirements

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and database module structure

- [x] T001 Create `src/database/` directory for Astrodbkit database module
- [x] T002 [P] Create `src/database/__init__.py` for module initialization
- [x] T003 [P] Verify SIMPLE.sqlite exists in repository root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 [P] Create `src/database/sources.py` with Database connection function following Astrodbkit patterns from research.md
- [x] T005 Implement `get_sources_data(limit=10)` function in `src/database/sources.py` using `Database('sqlite:///SIMPLE.sqlite')`
- [x] T006 Implement error handling in `get_sources_data()` to catch all exceptions and return None on any database error
- [x] T007 Convert query results to list of dictionaries format (.to_dict('records')) in `src/database/sources.py` for Jinja2 template compatibility

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - View Sources Data on Front Page (Priority: P1) 🎯 MVP

**Goal**: Display the first 10 rows from the Sources table of SIMPLE.sqlite database on the homepage

**Independent Test**: Visit the homepage at http://localhost:8000 and verify that a table with 10 rows from the Sources table is displayed correctly with all columns (source, ra, dec, epoch, equinox, shortname, reference, other_references, comments) visible within 3 seconds

**Acceptance Criteria**:
1. Table displays exactly 10 rows from the Sources table with all available columns
2. Data displayed at full precision as stored in database (no rounding)
3. Page loads within 3 seconds
4. All columns visible: source, ra, dec, epoch, equinox, shortname, reference, other_references, comments

### Implementation for User Story 1

- [x] T008 [P] [US1] Import and call `get_sources_data()` in homepage route in `src/routes/web.py`
- [x] T009 [US1] Handle `get_sources_data()` returning None by setting error context in homepage route in `src/routes/web.py`
- [x] T010 [P] [US1] Replace Bokeh plot with Sources table structure in `src/templates/index.html` template
- [x] T011 [US1] Add conditional rendering in `src/templates/index.html` to show table or error message based on data availability
- [x] T012 [P] [US1] Add Sources table CSS styling (border, padding, alternating rows) to `src/static/style.css`
- [x] T013 [US1] Test homepage displays Sources table with 10 rows within 3 seconds
- [x] T014 [US1] Verify all columns visible (source, ra, dec, epoch, equinox, shortname, reference, other_references, comments)
- [x] T015 [US1] Verify data displayed at full precision matching database values
- [x] T016 [US1] Test error handling by temporarily moving SIMPLE.sqlite and verifying error message displays

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Homepage displays Sources table with 10 rows.

---

## Phase 4: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [x] T017 [P] Run quickstart.md validation - verify all setup instructions work
- [x] T018 Test server startup completes within 5 seconds
- [x] T019 Verify code follows Constitution principles (Astrodbkit abstraction, FastAPI-first, CSS separate)
- [x] T020 Check all directory structure matches plan.md requirements
- [x] T021 Validate all endpoints in `contracts/web-api.yaml` are implemented
- [x] T022 Verify database connection uses Astrodbkit exclusively (no direct SQL)
- [x] T023 [P] Documentation review - ensure `quickstart.md` is accurate and complete
- [x] T024 [P] Code cleanup - ensure functions are <50 lines per Constitution principle
- [x] T025 Final integration test - verify database query, template rendering, error handling all work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **Polish (Phase 4)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) completes

### Within User Story 1

- Routes and database integration before template modifications
- Template and CSS can be created in parallel
- Integration testing after all components complete

### Parallel Opportunities

- **Setup Phase**: Tasks T002 and T003 can run in parallel
- **Foundational Phase**: Tasks T004-T007 must complete in order (sequential dependencies)
- **User Story 1**:
  - T008 and T010 can run in parallel (route modification vs template)
  - T010 and T012 can run in parallel (template vs CSS styling)
  - T013-T016 can run in parallel after implementation (different test scenarios)
- **Polish Phase**: T017, T023, T024 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Example parallel work for US1:
Developer A: Add database query to homepage route in src/routes/web.py (T008-T009)
Developer B: Replace plot with table structure in src/templates/index.html (T010-T011)
Developer C: Add table CSS styling to src/static/style.css (T012)

# All can work simultaneously, integration testing when all complete
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Verify homepage loads at http://localhost:8000 with Sources table showing 10 rows
6. Deploy/demo if ready

**Deliverable**: Functional homepage displaying Sources data from database

### Incremental Delivery

1. Complete Setup + Foundational → Database query infrastructure ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP: Sources table!)
3. Polish → Final validation

**Deliverable**: Functional Sources data display with proper error handling

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - **Developer A**: Database integration in route (T008-T009)
   - **Developer B**: Template modifications (T010-T011)
   - **Developer C**: CSS styling (T012)
3. Integration testing (T013-T016)
4. Polish together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- User Story 1 is independently completable and testable
- Database connection uses Astrodbkit exclusively (no direct SQL)
- All functions expected to be <50 lines per Constitution
- Commit after each logical group of tasks
- Stop at checkpoint to validate story independently

---

## Summary

**Total Tasks**: 25
- **Setup**: 3 tasks (Phase 1)
- **Foundational**: 4 tasks (Phase 2)
- **User Story 1**: 9 tasks (Phase 3)
- **Polish**: 9 tasks (Phase 4)

**Task Distribution by Story**:
- Phase 3 (US1): 9 tasks

**Parallel Opportunities Identified**: 
- Setup tasks can run in parallel
- T008 and T010 in US1 can run in parallel
- T010 and T012 in US1 can run in parallel
- Multiple test scenarios can run in parallel

**Independent Test Criteria**:
- **US1**: Visit homepage → see Sources table with 10 rows and all columns within 3 seconds

**Suggested MVP Scope**: User Story 1 only (Phase 3)
- Delivers working Sources data display from database
- Validates Astrodbkit integration with FastAPI + Jinja2 stack
- Foundation for adding more tables and features incrementally
