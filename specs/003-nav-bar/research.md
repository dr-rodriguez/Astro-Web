# Phase 0: Research & Technical Decisions

**Feature**: Navigation Bar with Multi-Page Structure  
**Date**: 2025-01-27  
**Purpose**: Resolve technical unknowns and establish implementation patterns

## Research Questions

### Q1: How should the navigation bar be integrated across all pages?

**Decision**: Extract navigation bar to a shared template partial or use Jinja2 template inheritance with a base template.

**Rationale**: FastAPI + Jinja2 supports template inheritance. Create `base.html` with navigation bar, and each page (`index.html`, `browse.html`, `plot.html`) extends base and fills content block.

**Alternatives Considered**: 
- Inline navigation in each template: Too much duplication
- JavaScript-based SPA approach: Too complex, violates FastAPI-first principle
- Server-side partial rendering: Not supported by Jinja2 without extra libraries

### Q2: How should client-side table controls (sorting, filtering, pagination) be implemented?

**Decision**: Use DataTables JavaScript library (via CDN). All Sources data loaded once on page load and passed to DataTables initialization. DataTables handles sorting, pagination, and global search functionality.

**Rationale**: DataTables provides production-quality table controls (sorting, pagination, filtering) with minimal implementation code, meeting <1s performance goals. Library loads via CDN (no build step required). Simpler than implementing vanilla JS equivalents.

**Alternatives Considered**:
- Vanilla JavaScript implementation: Would require significant code for sorting/filtering/pagination logic, violating simplicity principle
- Server-side pagination/filtering: Breaks client-side performance requirements and doesn't meet spec.md assumptions (L155-156)
- Web framework (React/Vue): Far too complex for prototype

### Q3: How should Bokeh scatter plot display actual ra/dec data from Sources?

**Decision**: Update `src/visualizations/scatter.py` to query Sources via Astrodbkit, extract ra/dec columns, filter null values, pass to Bokeh figure with ra on x-axis, dec on y-axis.

**Rationale**: Uses existing visualization module pattern. Maintains Astrodbkit abstraction (Principle II). Reuses Bokeh integration (Principle III).

**Alternatives Considered**:
- Generate static image: Loses interactivity
- Use different library: Violates Bokeh-first principle
- Hard-coded coordinates: Doesn't use actual data

### Q4: How should navigation bar indicate active page?

**Decision**: Pass `current_page` context variable to templates. Template renders navigation items with conditional CSS class for active state (e.g., `.nav-active`). CSS applies highlighting (background color, bold text, underline).

**Rationale**: Simple server-side approach. No JavaScript needed. CSS controls visual state.

**Alternatives Considered**:
- JavaScript-based active detection: Overcomplicated for server-rendered pages
- URL-based detection in template: Same effect, but context variable is clearer

### Q5: How should table pagination/sorting/filtering interact?

**Decision**: Sequential pipeline: filter → sort → paginate. User can set all three independently. State is ephemeral (resets on page reload/navigation away).

**Rationale**: Meets spec requirement that state resets on each visit to Browse page. Simple state management (client-side array manipulation).

**Alternatives Considered**:
- Persist state in URL/cookies: Spec explicitly says state resets
- Server-side state tracking: Breaks client-side performance goals

## Summary of Decisions

| Decision Area | Chosen Approach | Key Rationale |
|--------------|----------------|---------------|
| Navigation Integration | Jinja2 template inheritance with `base.html` | Maintains FastAPI-first, avoids duplication |
| Table Controls | DataTables library (CDN) client-side | Production-quality controls, minimal code, meets <1s performance goals |
| Scatter Plot Data | Query Sources via Astrodbkit, filter nulls, plot ra vs dec | Reuses existing patterns, follows principles |
| Active Page Indicator | Server-side context + CSS highlighting | Simple, no JavaScript needed |
| Table State Management | Ephemeral (reset on navigation) | Meets spec requirement for state reset |

## Implementation Readiness

✅ **Ready to proceed**: All technical decisions align with Constitution principles. DataTables library will be loaded via CDN (no framework or build dependency). Implementation approach is clear:

1. Create `base.html` template with navigation bar structure
2. Refactor `index.html` to extend base, fill home content
3. Create `browse.html` extending base, add Sources table + DataTables initialization
4. Create `plot.html` extending base, embed Bokeh plot
5. Update `src/routes/web.py` with `/browse` and `/plots` routes
6. Update `src/database/sources.py` with `get_all_sources()` function
7. Update `src/visualizations/scatter.py` to use actual ra/dec data
8. Add navigation CSS to `src/static/style.css`
9. Initialize DataTables on Sources table in `browse.html` with configuration for sorting, pagination, and global search


