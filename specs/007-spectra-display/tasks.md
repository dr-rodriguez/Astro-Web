# Tasks: Spectra Display Page

**Input**: Design documents from `/specs/007-spectra-display/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/web-api.yaml ✅

**Tests**: No tests requested in spec - skipping test tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `src/` at repository root
- Paths shown below follow plan.md structure

---

## Phase 1: Setup (Configuration & Infrastructure)

**Purpose**: Add configuration support for spectra functionality

- [ ] T001 Add SPECTRA_URL_COLUMN configuration variable to src/config.py

---

## Phase 2: Foundational (Database Access)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 [P] Implement get_source_spectra function in src/database/sources.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View Spectra Visualization from Inventory (Priority: P1) 🎯 MVP

**Goal**: Display all spectra for a source in a single interactive Bokeh plot with a legend, accessible from the inventory page

**Independent Test**: Navigate from inventory page to spectra visualization page and verify all spectra are displayed in an interactive plot with a visible legend showing observation_date | regime | telescope/instrument

### Implementation for User Story 1

- [ ] T004 [P] [US1] Create generate_spectra_plot function in src/visualizations/spectra.py
- [ ] T006 [US1] Add Bokeh plot generation with legend formatting in src/visualizations/spectra.py
- [ ] T007 [P] [US1] Create spectra.html template in src/templates/spectra.html
- [ ] T008 [US1] Implement spectra_display route in src/routes/web.py
- [ ] T009 [US1] Add spectra route registration in src/main.py
- [ ] T010 [US1] Add conditional spectra link to inventory.html in src/templates/inventory.html

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - users can navigate from inventory to spectra page and see all spectra in an interactive plot

---

## Phase 4: User Story 2 - Access Spectra Metadata Table (Priority: P2)

**Goal**: Display a metadata table showing observation details (observation_date, regime, telescope, instrument) with clickable links to access spectrum URLs

**Independent Test**: Navigate to spectra page and verify that a metadata table is displayed with key spectrum information including clickable links to access spectrum URLs

### Implementation for User Story 2

- [ ] T011 [US2] Extract spectrum metadata from database results in src/database/sources.py
- [ ] T012 [US2] Format metadata for table display with clickable URLs in src/visualizations/spectra.py
- [ ] T013 [US2] Add metadata table section to spectra.html template in src/templates/spectra.html

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - users can view spectra visualization and see detailed metadata table with clickable links

---

## Phase 5: User Story 3 - Handle Non-Displayable Spectra Gracefully (Priority: P3)

**Goal**: Skip unreadable or invalid spectra silently while displaying valid ones, with no error messages to users

**Independent Test**: Access spectra for a source where some spectra are invalid and verify that valid spectra are displayed while invalid ones are silently skipped

### Implementation for User Story 3

- [ ] T014 [US3] Implement graceful error handling for spectrum loading failures in src/visualizations/spectra.py
- [ ] T015 [US3] Add skip logic for invalid spectrum URLs in src/visualizations/spectra.py
- [ ] T016 [US3] Handle corrupt or unreadable spectrum files gracefully in src/visualizations/spectra.py
- [ ] T017 [US3] Display "No spectra available" message when no valid spectra load in src/templates/spectra.html

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently - system handles real-world data issues gracefully

---

## Phase 6: User Story 4 - Navigate Back to Inventory Page (Priority: P3)

**Goal**: Provide clear navigation to return from spectra page back to source inventory

**Independent Test**: Navigate from inventory to spectra page and back to inventory, verifying seamless transitions within 2 seconds

### Implementation for User Story 4

- [ ] T018 [US4] Add "Back to Inventory" link to spectra.html template in src/templates/spectra.html
- [ ] T019 [US4] Ensure navigation context is properly maintained in src/routes/web.py

**Checkpoint**: All user stories should now be independently functional - users can navigate seamlessly between inventory and spectra views

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T020 [P] Add CSS styling for spectra page to src/static/style.css
- [ ] T021 [P] Add CSS styling for spectra link in inventory page to src/static/style.css
- [ ] T022 Code cleanup and refactoring for spectra.py and related files
- [ ] T023 Validate quickstart.md implementation steps match actual code
- [ ] T024 Add loading indicator support during spectrum data retrieval (if not already implemented)
- [ ] T025 [P] Update documentation in README.md if needed
- [ ] T026 Run quickstart.md validation and verify all acceptance scenarios work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Enhances US1 with metadata table
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Adds error handling to US1/US2
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Adds navigation to US1/US2/US3

### Within Each User Story

- Core implementation before integration
- Configuration before usage
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Tasks within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- Polish phase tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch these User Story 1 tasks in parallel:
Task: "Create generate_spectra_plot function in src/visualizations/spectra.py"
Task: "Create spectra.html template in src/templates/spectra.html"
Task: "Add spectra route registration in src/main.py"
Task: "Add conditional spectra link to inventory.html in src/templates/inventory.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (configuration)
2. Complete Phase 2: Foundational (database access)
3. Complete Phase 3: User Story 1 (spectra visualization)
4. **STOP and VALIDATE**: Test User Story 1 independently - users can navigate from inventory to spectra page and see interactive plot
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (add metadata table)
4. Add User Story 3 → Test independently → Deploy/Demo (add error handling)
5. Add User Story 4 → Test independently → Deploy/Demo (add navigation)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (spectra visualization)
   - Developer B: User Story 2 (metadata table)
   - Developer C: User Story 3 (error handling) + User Story 4 (navigation)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability (US1, US2, US3, US4)
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Focus on: Specific file paths, clear actions, independent testability
