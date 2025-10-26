# Tasks: Navigation Bar with Multi-Page Structure

**Input**: Design documents from `specs/003-nav-bar/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/  
**Branch**: `003-nav-bar`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
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

**Purpose**: Create template structure and navigation context

- [X] T001 Create `src/templates/base.html` with navigation bar structure per Jinja2 template inheritance pattern from research.md
- [X] T002 [P] Update `src/static/style.css` to add navigation bar CSS styles (nav bar container, links, active state highlighting)
- [X] T003 [P] Create helper function `create_navigation_context(current_page)` in `src/routes/web.py` to generate navigation items with active state

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user stories

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Add `get_all_sources()` function to `src/database/sources.py` using `db.query(db.Sources).pandas()` to retrieve all Sources records
- [X] T005 Implement error handling in `get_all_sources()` to catch exceptions and return None on database error
- [X] T006 Update `src/visualizations/scatter.py` to extract ra/dec from actual Sources data via Astrodbkit query, filter null values, and plot ra on x-axis, dec on y-axis per research.md
- [X] T007 Add `routes_browse()` and `routes_plot()` route handlers to `src/routes/web.py` (placeholder implementations initially)

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Navigate Between Pages (Priority: P1) 🎯 MVP

**Goal**: Users can navigate between Home, Browse Database, and Plots pages using the top navigation bar with active page highlighting

**Independent Test**: Visit http://localhost:8000, click each navigation link (Home, Browse Database, Plots), verify each page loads with correct content, navigation bar present on all pages, and active page is visually highlighted (different color/bold). Test should complete within 2 seconds per page navigation.

**Acceptance Criteria**:
1. Navigation bar appears at top of all pages with three links: Home, Browse Database, Plots
2. Clicking each navigation link loads the corresponding page and displays appropriate content
3. Active page is visually highlighted in navigation bar (e.g., different background color, bold text, or underline)
4. Navigation bar remains visible and accessible across all page transitions
5. No full browser refresh required (FastAPI routing)

### Implementation for User Story 1

- [X] T008 [US1] Refactor `src/templates/index.html` to extend `base.html`, move content to Jinja2 block, add introduction text about database per spec.md
- [X] T009 [P] [US1] Update homepage route in `src/routes/web.py` to pass `current_page="/"` and call `create_navigation_context("/")` to template context
- [X] T010 [US1] Update `src/main.py` to add `/browse` and `/plots` routes connected to route handlers in `src/routes/web.py`
- [ ] T011 [US1] Test navigation between all three pages, verify content displays correctly, active page highlighting works
- [ ] T012 [US1] Verify navigation bar remains visible on all pages without layout disruption
- [ ] T013 [US1] Test that clicking currently active navigation item refreshes page to show same content

**Checkpoint**: At this point, User Story 1 should be fully functional. Users can navigate between Home, Browse Database, and Plots pages with proper active state indication.

---

## Phase 4: User Story 2 - View Home Page Introduction (Priority: P2)

**Goal**: Users visit Home page and see brief introduction to the astronomical database with key information about available data

**Independent Test**: Navigate to Home page at http://localhost:8000, verify introductory text about the astronomical database is displayed clearly in the content area, providing context about the database and guiding users to other sections. Text should be 2-3 paragraphs as per spec.md assumptions.

**Acceptance Criteria**:
1. Home page displays brief introductory text about the astronomical sources database
2. Introduction text is 2-3 paragraphs maximum per spec.md assumptions
3. Text provides context about the database and guides users to other sections
4. Navigation bar with active "Home" state is visible
5. Content is readable and informative without requiring database connection

### Implementation for User Story 2

- [X] T014 [US2] Write introductory content for Home page in `src/templates/index.html` block (2-3 paragraphs about astronomical database)
- [ ] T015 [US2] Verify Home page loads and displays introduction text without database dependency
- [ ] T016 [US2] Test that Home page navigation link works from Browse Database and Plots pages

**Checkpoint**: At this point, User Story 2 should be complete. Home page displays clear introduction about the database.

---

## Phase 5: User Story 3 - Browse Full Database Table (Priority: P2)

**Goal**: Users can browse complete Sources table with client-side controls for sorting, pagination, and filtering to find specific records within 1 second of interaction

**Independent Test**: Navigate to /browse, verify all Sources are accessible through pagination, columns sort correctly on header click, filtering works via global search box, and all controls update within 1 second. State should reset when navigating away and returning.

**Acceptance Criteria**:
1. Browse Database page displays all Sources records with all columns (source, ra, dec, epoch, equinox, shortname, reference, other_references, comments)
2. Column headers are clickable to sort ascending/descending (toggle on repeated clicks)
3. Pagination controls allow navigation through pages with selectable page size (10, 25, 50, 100 rows per page)
4. Global search box filters table across all columns simultaneously
5. All interactions update results within 1 second as per spec.md
6. State resets when navigating away and returning to page (default: first page, 10 rows, no sort/filter)

### Implementation for User Story 3

- [X] T017 [US3] Create `src/templates/browse.html` extending `base.html` with Sources table structure and all column headers
- [X] T018 [US3] Implement `browse()` route handler in `src/routes/web.py` to call `get_all_sources()`, handle errors, pass data to `browse.html` template
- [X] T019 [P] [US3] Include DataTables CDN links (CSS and JS) in `browse.html` template head section per research.md decision to use DataTables library
- [X] T020 [US3] Initialize DataTables on Sources table in `browse.html` with configuration for sorting (single column, toggle asc/desc), pagination (page size: 10, 25, 50, 100), and global search/filtering
- [X] T021 [US3] Configure DataTables to meet spec requirements: single-column sorting (clicking different column clears previous sort), global search box, default 10 rows per page, state resets on page reload
- [X] T022 [P] [US3] Add CSS styling for table container and DataTables controls to `src/static/style.css`
- [ ] T023 [US3] Test table displays all Sources with pagination working correctly
- [ ] T024 [US3] Test column sorting with ascending/descending toggle, previous sort clears when clicking different column
- [ ] T025 [US3] Test filtering via global search box updates table within 1 second, searches all columns
- [ ] T026 [US3] Test pagination with different page sizes (10, 25, 50, 100 rows), verify state resets on navigation away and return

**Checkpoint**: At this point, User Story 3 should be complete. Users can browse, sort, filter, and paginate through all Sources data with fast client-side interactions.

---

## Phase 6: User Story 4 - View Astronomical Data Plots (Priority: P2)

**Goal**: Users can view interactive scatter plot of ra (right ascension) vs dec (declination) coordinates showing spatial distribution of astronomical sources

**Independent Test**: Navigate to /plots, verify interactive scatter plot displays with ra on x-axis and dec on y-axis using actual Sources data, hover tooltips show source info and coordinates, pan/zoom/reset tools work smoothly. All Sources with valid coordinates are plotted.

**Acceptance Criteria**:
1. Plots page displays interactive scatter plot with ra on horizontal axis and dec on vertical axis
2. Plot includes all Sources from database that have valid (non-null) ra and dec values
3. Hover tooltips display source identifier and coordinate values
4. Interactive features work: pan, zoom, reset, hover tooltips responsive within 100ms
5. Sources with null coordinates are excluded from plot

### Implementation for User Story 4

- [X] T027 [US4] Create `src/templates/plot.html` extending `base.html` with Bokeh plot container
- [X] T028 [US4] Update `plot()` route handler in `src/routes/web.py` to call `get_all_sources()`, filter sources with valid ra/dec, generate Bokeh plot via `create_scatter_plot()`, pass to template
- [X] T029 [US4] Ensure `create_scatter_plot()` in `src/visualizations/scatter.py` uses actual ra/dec data from Sources, filters nulls, sets proper axis labels
- [X] T030 [P] [US4] Add CSS styling for plot container to `src/static/style.css`
- [ ] T031 [US4] Test scatter plot displays all Sources with valid ra/dec coordinates
- [ ] T032 [US4] Test hover tooltips show source info and coordinates within 100ms
- [ ] T033 [US4] Test interactive features: pan, zoom, reset buttons work smoothly
- [ ] T034 [US4] Verify Sources with null ra or dec are excluded from plot
- [ ] T035 [US4] Test error handling when database unavailable - shows appropriate message

**Checkpoint**: At this point, User Story 4 should be complete. Users can view and interact with scatter plot visualization of Sources coordinates.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, validation, and quality assurance

- [X] T036 [P] Update `src/main.py` FastAPI app title and description to reflect multi-page navigation structure
- [ ] T037 Run quickstart.md validation - verify all 8 test scenarios pass
- [ ] T038 [P] Verify page load time < 2 seconds for all three pages (/, /browse, /plots)
- [ ] T039 [P] Verify table interactions (sorting, filtering, pagination) update within 1 second
- [ ] T040 [P] Verify scatter plot hover tooltips appear
- [ ] T041 [P] Test navigation bar visibility and functionality across all pages
- [ ] T042 Test workflow: Home → Browse → Plots → Home without errors or missing content
- [ ] T043 [P] Verify code follows Constitution principles (FastAPI-first, Astrodbkit abstraction, Bokeh visualizations, CSS separate, simplicity)
- [ ] T044 [P] Check all directory structure matches plan.md requirements
- [ ] T045 [P] Validate all endpoints in `contracts/web-api.yaml` are implemented correctly
- [ ] T046 [P] Verify database connection uses Astrodbkit exclusively (no direct SQL queries)
- [ ] T047 [P] Code cleanup - ensure route handlers are <50 lines per Constitution principle
- [ ] T048 [P] Test error handling: database connection fails on Browse and Plots, verify error messages display and navigation still works
- [ ] T049 [P] Test edge case: empty database shows appropriate messages on Browse and Plots pages
- [ ] T050 Final integration test - verify database queries, template rendering, navigation, table controls, and plot generation all work together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - FOUNDATION for all other stories
- **User Story 2 (Phase 4)**: Depends on User Story 1 completion (uses navigation structure)
- **User Story 3 (Phase 5)**: Depends on User Story 1 completion (uses navigation structure)
- **User Story 4 (Phase 6)**: Depends on User Story 1 completion (uses navigation structure)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) completes - FOUNDATION NAVIGATION
- **User Story 2 (P2)**: Depends on User Story 1 (navigation structure must exist)
- **User Story 3 (P2)**: Depends on User Story 1 (navigation structure must exist)
- **User Story 4 (P2)**: Depends on User Story 1 (navigation structure must exist)

### Within User Story 1

- Template structure (T008) must complete before route updates (T009)
- Routes (T010) can be added in parallel with template work

### Within User Story 3

- Template creation (T017) and route handler (T018) must complete before JavaScript implementation (T019-T021)
- CSS styling (T022) can be done in parallel with JavaScript
- Testing (T023-T026) can be done in parallel after implementation

### Within User Story 4

- Route handler (T028) must complete before template (T027) can be populated
- CSS styling (T030) can be done in parallel with route handler
- Testing (T031-T035) can be done in parallel after implementation

### Parallel Opportunities

- **Setup Phase**: Tasks T002 and T003 can run in parallel
- **Foundational Phase**: Tasks T004-T007 must complete mostly in order (database functions before route handlers use them)
- **User Story 3**: T019, T020, T021 can run in parallel after T017-T018 (different JavaScript features)
- **User Story 4**: T030 (CSS) can run in parallel with T027-T029 (template and plot)
- **Polish Phase**: T036, T038-T040, T043-T046, T048-T049 can run in parallel

---

## Parallel Example: User Story 3

```bash
# Example parallel work for US3:
Developer A: Create browse.html template and route handler (T017-T018)
Developer B: Implement client-side sorting JavaScript (T019)
Developer C: Implement pagination JavaScript (T020)
Developer D: Implement filtering JavaScript (T021)
Developer E: Add table controls CSS styling (T022)

# All can work simultaneously, integration testing when all complete
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Verify all three navigation pages work correctly with active page highlighting
6. Deploy/demo if ready

**Deliverable**: Functional multi-page navigation with Home, Browse Database, and Plots pages

### Incremental Delivery

1. Complete Setup + Foundational → Navigation and database infrastructure ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP: Navigation!)
3. Add User Story 2 → Home page introduction
4. Add User Story 3 → Browse Database with client-side controls
5. Add User Story 4 → Plots with scatter plot
6. Polish → Final validation

**Deliverable**: Complete navigation bar feature with all user stories implemented

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - **Developer A**: Complete User Story 1 navigation infrastructure (T008-T013)
3. Once User Story 1 is complete:
   - **Developer B**: Implement User Story 2 - Home page content (T014-T016)
   - **Developer C**: Implement User Story 3 - Browse Database (T017-T026) in parallel
   - **Developer D**: Implement User Story 4 - Plots (T027-T035) in parallel
4. Integration testing and polish together (T036-T050)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- User Story 1 is FOUNDATIONAL - must complete first before all other stories
- User Stories 2, 3, 4 are independent and can be worked in parallel after User Story 1
- Client-side table controls use DataTables library loaded via CDN per research.md decision
- Navigation bar uses Jinja2 template inheritance (base.html) per research.md
- All functions expected to be <50 lines per Constitution
- Commit after each logical group of tasks
- Stop at checkpoint to validate each story independently

---

## Summary

**Total Tasks**: 50
- **Setup**: 3 tasks (Phase 1)
- **Foundational**: 4 tasks (Phase 2)
- **User Story 1**: 6 tasks (Phase 3)
- **User Story 2**: 3 tasks (Phase 4)
- **User Story 3**: 10 tasks (Phase 5)
- **User Story 4**: 9 tasks (Phase 6)
- **Polish**: 15 tasks (Phase 7)

**Task Distribution by Story**:
- Phase 3 (US1): 6 tasks - FOUNDATION NAVIGATION
- Phase 4 (US2): 3 tasks - Home page introduction
- Phase 5 (US3): 10 tasks - Browse Database with controls
- Phase 6 (US4): 9 tasks - Plots scatter plot

**Parallel Opportunities Identified**: 
- Setup tasks (T002-T003) can run in parallel
- User Story 3 DataTables configuration (T019-T021) can be developed in parallel
- User Story 4 CSS styling (T030) can run in parallel with template work
- Multiple test scenarios (T023-T026, T031-T035) can run in parallel
- Many polish tasks (T036-T050) can run in parallel

**Independent Test Criteria**:
- **US1**: Navigate between pages, verify active highlighting, complete in <2s per page
- **US2**: View Home page introduction (2-3 paragraphs), loads without database dependency
- **US3**: Browse Sources table, sort/filter/paginate with client-side controls, updates within 1s
- **US4**: View scatter plot with ra/dec coordinates, interactive features work, hover tooltips <100ms

**Suggested MVP Scope**: User Story 1 only (Phase 3)
- Delivers functional multi-page navigation structure
- Validates Jinja2 template inheritance and FastAPI routing
- Foundation for adding Browse Database and Plots features incrementally
