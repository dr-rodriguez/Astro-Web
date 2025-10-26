# Tasks: Hello World Website

**Input**: Design documents from `/specs/001-hello-world-website/`  
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/  
**Branch**: `001-hello-world-website`

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `src/` at repository root per plan.md
- Paths follow Constitution requirements

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create `src/` directory structure (routes/, templates/, static/, visualizations/)
- [X] T002 [P] Create `src/main.py` with basic FastAPI app structure
- [X] T003 Configure uvicorn in pyproject.toml for development server on port 8000

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Add Jinja2Templates configuration to existing `src/main.py`
- [X] T005 Configure static file serving in `src/main.py`
- [X] T006 Create `src/routes/web.py` with route module structure
- [X] T007 Integrate web routes into main app in `src/main.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - View Hello World Page (Priority: P1) 🎯 MVP

**Goal**: Display a simple "Hello World" page that validates the entire web stack is working correctly

**Independent Test**: Start the server, visit http://localhost:8000 in a browser, and verify the page displays "Hello World" content with correct styling within 2 seconds

**Acceptance Criteria**:
1. Page loads with "Hello World" content within 2 seconds
2. Styling (colors, layout, fonts) appears as intended
3. Header displays "Astro Web" title
4. Footer displays "© 2025" copyright
5. Page renders correctly in modern browsers (Chrome, Firefox, Safari, Edge)

### Implementation for User Story 1

- [X] T008 [P] [US1] Create homepage route in `src/routes/web.py` for root path `/`
- [X] T009 [P] [US1] Create `src/templates/index.html` template with header, content, and footer structure
- [X] T010 [US1] Link CSS file in `src/templates/index.html`
- [X] T011 [P] [US1] Create `src/static/style.css` with clean minimal theme (light background, dark text, astronomy-inspired palette)
- [X] T012 [US1] Implement 404 handler route in `src/routes/web.py` for `/{path:path}`
- [X] T013 [US1] Create `src/templates/404.html` template for not found page
- [X] T014 [US1] Test homepage loads at http://localhost:8000 within 2 seconds
- [X] T015 [US1] Verify styling renders correctly (header "Astro Web", footer "© 2025")
- [X] T016 [US1] Test 404 page for non-existent URLs

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Homepage displays "Hello World" with correct styling.

---

## Phase 4: User Story 2 - View Simple Data Visualization (Priority: P2)

**Goal**: Display an interactive scatter plot embedded in the page demonstrating Bokeh integration

**Independent Test**: Open the homepage, view the scatter plot, and interact with it (hover over data points) to see tooltips appear within 100ms

**Acceptance Criteria**:
1. Scatter plot is displayed and is interactive
2. Tooltips appear on mouse hover within 100ms
3. Plot shows approximately 20 data points (temperature vs magnitude)
4. Visualization is aesthetically integrated with the page design

### Implementation for User Story 2

- [X] T017 [P] [US2] Create `src/visualizations/scatter.py` with scatter plot generation function
- [X] T018 [US2] Implement `get_sample_data()` function generating ~20 random (temperature, magnitude) pairs in `src/visualizations/scatter.py`
- [X] T019 [US2] Create Bokeh figure with proper sizing and styling in `src/visualizations/scatter.py`
- [X] T020 [US2] Add hover tooltips to scatter plot in `src/visualizations/scatter.py`
- [X] T021 [US2] Export plot as embeddable components (script, div) from Bokeh in `src/visualizations/scatter.py`
- [X] T022 [US2] Import and call scatter plot generation in homepage route in `src/routes/web.py`
- [X] T023 [US2] Pass plot components to `index.html` template in `src/routes/web.py`
- [X] T024 [US2] Embed Bokeh plot in `src/templates/index.html` template
- [X] T025 [US2] Test visualization displays on homepage
- [X] T026 [US2] Verify hover tooltips appear within 100ms
- [X] T027 [US2] Confirm data points are visible and interactive

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Homepage displays "Hello World" with interactive scatter plot visualization.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [X] T028 [P] Run quickstart.md validation - verify all setup instructions work
- [X] T029 Test server startup completes within 5 seconds
- [X] T030 Verify code follows Constitution principles (FastAPI-first, Bokeh visualizations, CSS separate)
- [X] T031 Check all directory structure matches plan.md requirements
- [X] T032 Validate all endpoints in `contracts/web-api.yaml` are implemented
- [X] T033 Test in all specified browsers (Chrome, Firefox, Safari, Edge)
- [X] T034 Verify no database dependencies (hard-coded data only)
- [X] T035 [P] Documentation review - ensure `quickstart.md` is accurate and complete
- [X] T036 [P] Code cleanup - ensure functions are <50 lines per Constitution principle
- [X] T037 Final integration test - all functionality works together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion AND User Story 1 for integration
- **Polish (Phase 5)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) completes
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) completes
  - Visualization can be developed in parallel with US1, but needs homepage route ready for integration
  - US2 is independently testable but integrates with US1's homepage

### Within Each User Story

- Phase 3 (US1):
  - Routes and templates before static CSS
  - Both can be created in parallel
  - Integration testing after all components complete
  
- Phase 4 (US2):
  - Visualization function before route integration
  - Data generation before plot creation
  - Template integration after route modification

### Parallel Opportunities

- **Setup Phase**: Tasks T001-T003 can run in parallel by different developers
- **Foundational Phase**: Tasks T004-T007 can run in parallel
- **User Story 1**:
  - T008 and T011 can run in parallel (route vs CSS)
  - T009 and T011 can run in parallel (template vs CSS)
- **User Story 2**:
  - T017-T021 can be developed together (visualization module)
  - T028, T035, T036 can run in parallel (Polish phase)

---

## Parallel Example: User Story 1

```bash
# Example parallel work for US1:
Developer A: Create homepage route in src/routes/web.py (T008)
Developer B: Create index.html template in src/templates/ (T009)
Developer C: Create style.css in src/static/ (T011)

# All can work simultaneously, integrate when all complete
```

---

## Parallel Example: User Story 2

```bash
# Example parallel work for US2:
Developer A: Create scatter.py module (T017-T021)
Developer B: Test US1 homepage functionality (T014-T016)

# Then integrate visualization into homepage
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Verify homepage loads at http://localhost:8000 with correct styling
6. Deploy/demo if ready

**Deliverable**: Functional "Hello World" website with proper styling, no visualization

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP: basic page!)
3. Add User Story 2 → Test independently → Deploy/Demo (complete with visualization)
4. Polish → Final validation

**Deliverable**: Functional "Hello World" website with interactive scatter plot

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - **Developer A**: User Story 1 (homepage infrastructure)
   - **Developer B**: User Story 2 (visualization module - standalone development)
3. Integration: Developer B's visualization integrates into Developer A's homepage
4. Polish together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No database - all data is hard-coded
- Manual testing only (no automated tests per requirements)
- All functions expected to be <50 lines per Constitution
- Commit after each logical group of tasks
- Stop at any checkpoint to validate story independently

---

## Summary

**Total Tasks**: 37
- **Setup**: 3 tasks (Phase 1)
- **Foundational**: 4 tasks (Phase 2)
- **User Story 1**: 9 tasks (Phase 3)
- **User Story 2**: 11 tasks (Phase 4)
- **Polish**: 10 tasks (Phase 5)

**Task Distribution by Story**:
- Phase 3 (US1): 9 tasks
- Phase 4 (US2): 11 tasks

**Parallel Opportunities Identified**: 
- Setup tasks can all run in parallel
- Foundational tasks can all run in parallel
- T008, T009, T011 in US1 can run in parallel
- T017-T021 in US2 can run in parallel

**Independent Test Criteria**:
- **US1**: Visit homepage → see "Hello World" content with styling within 2 seconds
- **US2**: View scatter plot → interact with hover tooltips within 100ms

**Suggested MVP Scope**: User Story 1 only (Phase 3)
- Delivers working "Hello World" website without visualization
- Validates entire FastAPI + Jinja2 stack
- Foundation for adding visualization incrementally

