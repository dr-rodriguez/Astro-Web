# Tasks: Individual Source Inventory Page

**Input**: Design documents from `specs/004-source-inventory/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/  
**Branch**: `004-source-inventory`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `src/` at repository root per plan.md
- **Database module**: `src/database/` for Astrodbkit queries
- **Templates**: `src/templates/` for Jinja2 templates
- **Routes**: `src/routes/` for FastAPI route handlers
- **Static files**: `src/static/` for CSS and JavaScript
- Paths follow Constitution requirements

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Database query function for inventory retrieval

- [X] T001 Add `get_source_inventory(source_name)` function to `src/database/sources.py` that calls `db.inventory(source_name)` and returns dictionary of table names to lists of dictionaries
- [X] T002 [P] Implement error handling in `get_source_inventory()` to catch all exceptions and return None on database error
- [X] T003 [P] Filter out empty tables in `get_source_inventory()` function - only return tables that have data (length > 0)

**Checkpoint**: Setup complete - database query function ready

---

## Phase 2: User Story 1 - View Comprehensive Source Inventory (Priority: P1) 🎯 MVP

**Goal**: Users navigate to an individual source's inventory page and view all data associated with that source from multiple related tables in organized data tables

**Independent Test**: Navigate to `http://localhost:8000/source/{source_name}` (URL-encoded) and verify multiple data tables are displayed (Sources, Photometry, Spectra, Parallaxes, etc.) within 5 seconds. Each table represents a different key from the inventory result. Only tables with data are displayed. Empty or non-existent keys are not shown.

**Acceptance Criteria**:
1. Navigate to inventory page using URL-encoded source name within 2 seconds
2. Multiple data tables displayed for keys that have data (Sources + at least one other table)
3. Each table displays data from one key in the inventory result
4. Empty or non-existent tables are not displayed
5. Source identifier displayed prominently at top of page
6. Navigation bar visible and functional

### Implementation for User Story 1

- [X] T004 [US1] Add `inventory(request, source_name)` route handler to `src/routes/web.py` that calls `get_source_inventory(source_name)` and passes data to template
- [X] T005 [US1] Handle error case in `inventory()` route handler when `get_source_inventory()` returns None - set error context and display message
- [X] T006 [P] [US1] Create `src/templates/inventory.html` template extending `base.html` with structure for displaying multiple data tables
- [X] T006.5 [US1] Add loading state skeleton structure to `src/templates/inventory.html` that displays "Loading source inventory..." message (shown while data loads server-side) per FR-012
- [X] T007 [US1] Implement dynamic table generation in `src/templates/inventory.html` - iterate over inventory_data.items() keys (table names) and generate HTML table for each non-empty key
- [X] T007.5 [US1] Display source identifier prominently at top of `src/templates/inventory.html` using h1 or prominent heading element per FR-006
- [X] T008 [US1] Add conditional rendering in `src/templates/inventory.html` to only display tables that have data (check if value exists and length > 0)
- [X] T009 [P] [US1] Add inventory page CSS styles to `src/static/style.css` - inventory-container, inventory-table-section, data-table styling per quickstart.md
- [X] T010 [US1] Add `/source/{source_name}` route to `src/main.py` that connects to `web.inventory()` handler
- [X] T011 [US1] Register inventory route in `src/main.py` FastAPI app with proper path parameter handling
- [X] T012 [US1] Test inventory page displays Sources table plus at least one other table (Photometry, Spectra, Parallaxes, etc.)
- [X] T013 [US1] Verify only tables with data are displayed, empty tables are not shown
- [X] T014 [US1] Test inventory page loads within 5 seconds for sources with moderate data
- [X] T015 [US1] Verify loading indicator displays "Loading source inventory..." message per FR-012

**Checkpoint**: At this point, User Story 1 should be fully functional. Users can navigate to source inventory pages and view all data associated with that source in organized data tables.

---

## Phase 3: User Story 2 - Navigate to Source from Browse Page (Priority: P2)

**Goal**: Users can click on a source identifier in the browse page table to navigate to that source's inventory page, maintaining context and providing clear path back

**Independent Test**: Start from browse page at `/browse`, click on any source identifier in the Sources table, arrive at that source's inventory page with all data displayed. Navigation completes within 2 seconds. Navigation bar works correctly. Can return to browse page via navigation.

**Acceptance Criteria**:
1. Source identifiers in browse page are clickable links
2. Clicking source identifier navigates to inventory page for that source
3. Navigation completes within 2 seconds
4. Can return to browse page using navigation bar
5. Context is maintained (user can navigate back and forth)

### Implementation for User Story 2

- [X] T016 [P] [US2] Make source identifiers clickable in `src/templates/browse.html` by wrapping them in anchor tags with href="/source/{urlencoded_source_name}"
- [X] T017 [US2] Import and use `urllib.parse.quote()` or Jinja2 `urlencode` filter to URL-encode source names in browse page links in `src/templates/browse.html`
- [X] T018 [US2] Test clicking source identifier in browse page navigates to correct inventory page
- [X] T019 [US2] Test navigation completes within 2 seconds between browse and inventory pages
- [X] T020 [US2] Verify navigation bar allows returning to browse page from inventory page
- [X] T021 [US2] Test multiple navigations back and forth between browse and inventory pages work correctly

**Checkpoint**: At this point, User Story 2 should be complete. Users can navigate from browse page to source inventory pages seamlessly.

---

## Phase 4: User Story 3 - Handle Invalid or Missing Sources (Priority: P3)

**Goal**: When users attempt to access inventory page for non-existent sources or with invalid identifiers, system provides clear feedback and handles errors gracefully

**Independent Test**: Attempt to navigate to inventory page for non-existent source (e.g., `/source/non_existent_source`) and verify clear error message displayed within 2 seconds. Test with URL-encoded identifiers containing special characters to verify proper decoding. Test with invalid source identifiers to verify graceful error handling.

**Acceptance Criteria**:
1. Attempting to access non-existent source displays clear "Source not found" error message
2. Error message displayed within 2 seconds
3. URL-encoded source names with special characters are correctly decoded
4. Database connection errors display appropriate error message
5. Navigation still works from error page

### Implementation for User Story 3

- [X] T022 [US3] Improve error handling in `inventory()` route handler in `src/routes/web.py` to distinguish between "source not found" (empty inventory) vs database connection errors
- [X] T023 [US3] Add error message display section in `src/templates/inventory.html` with "Source not found" message and link back to browse page
- [X] T024 [US3] Test error message displays when navigating to non-existent source within 2 seconds
- [X] T025 [US3] Test URL-encoded identifiers with special characters (spaces, commas, Unicode) are correctly decoded for database queries
- [X] T026 [US3] Test database connection error handling - verify appropriate error message displayed when database unavailable
- [X] T027 [US3] Verify navigation bar remains functional from error page

**Checkpoint**: At this point, User Story 3 should be complete. System handles errors gracefully with clear feedback to users.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, validation, and quality assurance

- [X] T028 [P] Verify inventory page loads within 5 seconds for sources with moderate data per FR-010
- [X] T029 [P] Verify response time < 2 seconds for error cases (invalid source) per SC-005
- [X] T030 [P] Test navigation between pages completes within 2 seconds per FR-006
- [X] T031 [P] Verify all URL-encoded identifiers with special characters handled correctly per FR-005
- [X] T032 [P] Run quickstart.md validation - verify all test scenarios pass
- [X] T033 [P] Verify code follows Constitution principles (FastAPI-first, Astrodbkit abstraction, CSS separate, simplicity)
- [X] T034 [P] Check all directory structure matches plan.md requirements
- [X] T035 [P] Validate all endpoints in `contracts/web-api.yaml` are implemented correctly
- [X] T036 [P] Verify database connection uses Astrodbkit exclusively (no direct SQL queries)
- [X] T037 [P] Code cleanup - ensure route handlers are <50 lines per Constitution principle
- [X] T038 [P] Test with sources that have data in different table combinations (Sources only, Sources + Photometry, Sources + Spectra + Parallaxes, etc.)
- [X] T039 [P] Verify loading state behavior (if implemented) - display "Loading source inventory..." during retrieval
- [X] T040 [P] Test edge case: source exists but all related tables return empty (should display only Sources table)
- [X] T041 [P] Verify all data rows displayed with native browser scrolling (no artificial limits) per FR-013
- [X] T042 Final integration test - verify inventory retrieval, template rendering, navigation, and error handling all work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **User Story 1 (Phase 2)**: Depends on Setup completion
- **User Story 2 (Phase 3)**: Depends on User Story 1 completion (inventory functionality must exist)
- **User Story 3 (Phase 4)**: Depends on User Story 1 completion (error handling in existing route)
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Setup (Phase 1) completes - FOUNDATION
- **User Story 2 (P2)**: Depends on User Story 1 (inventory functionality and route must exist)
- **User Story 3 (P3)**: Depends on User Story 1 (enhances existing error handling)

### Within User Story 1

- Database function (T001-T003) must complete before route handler (T004-T005)
- Template creation (T006-T008) can be done in parallel with CSS styling (T009)
- Route registration (T010-T011) must complete before testing (T012-T015)
- Testing tasks (T012-T015) can be done in parallel after implementation

### Within User Story 2

- Template modification (T016-T017) can be done in parallel
- Testing tasks (T018-T021) can be done in parallel after implementation

### Within User Story 3

- Error handling improvements (T022-T023) must complete before testing
- Testing tasks (T024-T027) can be done in parallel after implementation

### Parallel Opportunities

- **Setup Phase**: Tasks T002 and T003 can run in parallel
- **User Story 1**: 
  - T006 (template) and T009 (CSS) can run in parallel
  - T012-T015 can run in parallel after implementation (different test scenarios)
- **User Story 2**: 
  - T016 and T017 can run together (both modify browse.html)
  - T018-T021 can run in parallel after implementation
- **User Story 3**: 
  - T024-T027 can run in parallel after implementation
- **Polish Phase**: T028-T034, T036-T042 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Example parallel work for US1:
Developer A: Create get_source_inventory() function in src/database/sources.py (T001-T003)
Developer B: Implement route handler in src/routes/web.py (T004-T005)
Developer C: Create inventory.html template (T006-T008)
Developer D: Add CSS styling to src/static/style.css (T009)
Developer E: Register route in src/main.py (T010-T011)

# Integration testing when all complete (T012-T015)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: User Story 1
3. **STOP and VALIDATE**: Test User Story 1 independently
4. Verify inventory page displays multiple data tables for a source
5. Deploy/demo if ready

**Deliverable**: Functional source inventory page displaying all data associated with a source in organized tables

### Incremental Delivery

1. Complete Setup → Database query function ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP: Inventory display!)
3. Add User Story 2 → Navigate from browse page
4. Add User Story 3 → Error handling
5. Polish → Final validation

**Deliverable**: Complete source inventory feature with navigation and error handling

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup together
2. Once Setup is done:
   - **Developer A**: Database integration (T001-T003)
   - **Developer B**: Route handler (T004-T005)
   - **Developer C**: Template creation (T006-T008)
   - **Developer D**: CSS styling (T009)
3. Integration: Register route (T010-T011) and test (T012-T015)
4. Once User Story 1 is complete:
   - **Developer B**: User Story 2 - Browse page links (T016-T021)
   - **Developer C**: User Story 3 - Error handling (T022-T027)
5. Polish together (T028-T042)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- User Story 1 is FOUNDATIONAL - must complete first before all other stories
- User Stories 2 and 3 are independent enhancements and can be worked in parallel after User Story 1
- All functions expected to be <50 lines per Constitution
- URL encoding handled by FastAPI automatically; use quote() for encoding in templates
- Inventory method returns dict of table names to lists of dicts
- Template iterates over inventory dict keys, checks for non-empty data
- Commit after each logical group of tasks
- Stop at checkpoint to validate each story independently

---

## Summary

**Total Tasks**: 42
- **Setup**: 3 tasks (Phase 1)
- **User Story 1**: 12 tasks (Phase 2)
- **User Story 2**: 6 tasks (Phase 3)
- **User Story 3**: 6 tasks (Phase 4)
- **Polish**: 15 tasks (Phase 5)

**Task Distribution by Story**:
- Phase 2 (US1): 12 tasks - FOUNDATION INVENTORY DISPLAY
- Phase 3 (US2): 6 tasks - Navigation from browse page
- Phase 4 (US3): 6 tasks - Error handling

**Parallel Opportunities Identified**: 
- Setup tasks (T002-T003) can run in parallel
- Template creation (T006-T008) and CSS styling (T009) in US1 can run in parallel
- Multiple test scenarios (T012-T015, T018-T021, T024-T027) can run in parallel
- Many polish tasks (T028-T042) can run in parallel

**Independent Test Criteria**:
- **US1**: Navigate to inventory page → see multiple data tables for source within 5 seconds
- **US2**: Click source in browse page → navigate to inventory within 2 seconds
- **US3**: Access non-existent source → see error message within 2 seconds

**Suggested MVP Scope**: User Story 1 only (Phase 2)
- Delivers functional source inventory page with all data displayed
- Validates astrodbkit inventory method integration with FastAPI + Jinja2
- Foundation for adding navigation links and error handling incrementally

