# Orbit Explorer — Revision Plan

## Context

Orbit Explorer is a browser-based applet for exploring the dynamics of generalized Collatz-style functions. Users set parameters (m, b, d) defining a function pair — `f(n) = n/d` on the divisibility class and `g(n) = m·n + b` otherwise — seed the iteration with a starting value, observe the trajectory, and save interesting cases to a Cases tool.

The applet was used in a middle-school session at Mariemont Junior High in May 2026. That session surfaced the UI issues this revision addresses.

## Repo Situation and Canonicalization Plan

Multiple copies of Orbit Explorer currently exist across GitHub repos:

- **`TEA-Collatz-Paper/applets/`** — older copy. Lives in the natural long-term home for the project (TEA = Technology Educator Alliance, the research collective).
- **`Ohio-Journal-Summer-2026/Apps/Orbit Explorer/orbit-explorer-main/`** — newer "v2" copy. Currently the deployed version (linked from the applet-library page).
- Possibly a standalone `orbit-explorer` dev repo (to be confirmed during reconnaissance).

**The canonicalization plan**: make `TEA-Collatz-Paper` the canonical home for all future development. Steps:

1. Diff the v2 copy in the journal repo against the older copy in TEA-Collatz-Paper.
2. Copy v2 into TEA-Collatz-Paper, replacing the older code.
3. Enable GitHub Pages on TEA-Collatz-Paper if not already enabled.
4. Apply the revisions in this document to the TEA-Collatz-Paper copy.
5. Update the applet-library page to link to the new TEA-Collatz-Paper deployment URL.
6. Decide what to do with the journal repo copy (archive in place, leave as a frozen snapshot, or delete).

**Consequence**: the deployed URL changes. Old: `ohiomathteacher.github.io/Ohio-Journal-Summer-2026/Apps/Orbit%20Explorer/...` (note the awful `%20` from the space in the folder name). New target: `ohiomathteacher.github.io/TEA-Collatz-Paper/applets/orbit-explorer/` — all lowercase, hyphens not spaces, minimal nesting depth, no redundant `-main` suffix. The clean URL is a hard requirement, not a nice-to-have.

## Revisions

### 1. Top Control Bar — Resize and Reorganize

The current top bar is too compact for its information density. Make it ~1.5–1.75× taller (target around 56–64px from the current ~36px), with proportionally larger fonts, slider thumbs, and input fields.

**Rationale**: The m/b/d sliders are the heart of the exploration and should be visually dominant. The seed input is the second most-used control. The action button is heavily used. All should be more prominent than they currently are.

### 2. Max-Steps Controller — Retire and Move to Top Bar

The standalone max-steps controller (currently a large panel that overlaps the cases table) should be retired. Replace it with a compact numeric input labeled "max steps" in the top bar, placed near the seed input.

**Rationale**: Max-steps is infrastructure, not a parameter. It does not deserve the visual real estate it currently consumes, and its current placement blocks the cases table.

### 3. Rename "Add" → "Show steps"

The button currently labeled "Add" (which iterates the function from the seed value) should be renamed to "Show steps".

**Rationale**: With auto-reset on new seed (see Revision 4), the additive semantic is gone. "Show steps" describes the actual action and fits the pedagogical framing.

### 4. Auto-Reset on New Seed

Typing a new value into the seed input and pressing Enter (or clicking "Show steps") should automatically clear the canvas of any previous trajectory before drawing the new one.

**Sub-behavior**: If the previous trajectory has not been saved to the Cases tool, briefly show a soft "Save first?" affordance near the canvas before clearing. Not a blocking modal — a visual nudge.

**Edge case**: Entering a blank value and pressing Enter clears the canvas entirely.

**Rationale**: Now that the Cases tool exists, overlaying multiple trajectories on one canvas creates clutter without benefit. Cases handles persistent comparison better.

### 5. View Menu (New)

Add a "View" menu/dropdown in the top bar containing:

**Scale modes** (radio buttons — pick one):
- Linear
- Log

**Cycle layout modes** (radio buttons — pick one):
- Polygon (points in trajectory order around a circle; default)
- Star (star-polygon connections {N/k} for cycle of length N; valid k values only)
- Sorted (points placed by magnitude around the circle)
- Parity-split (odd values on top half, even on bottom)

**Toggles** (checkboxes, independent):
- Show step numbers
- Parity coloring (odd vs even terms in distinct colors)

**Actions** (no indicator):
- Fit to canvas
- Reset view

**Rationale**: Different cycle visualizations help students see structure differently. Currently the cycle drawing is inconsistent — a 5-cycle is sometimes drawn as a pentagon, sometimes as a pentagram — depending on the order of trajectory hits. Making this an explicit user choice supports pattern discovery and connects to ideas in group theory.

The star-polygon options should be auto-restricted to valid {N/k} for the current cycle length (k must be coprime to N).

### 6. Canvas Zoom + Pan

Add zoom and pan controls to the trajectory canvas and to the cycle visualization.

**Control cluster** (corner of canvas):

```
[−]  100%  [+]  [Fit]  [Reset]
```

**Interactions**:
- Mouse scroll / trackpad pinch → zoom centered on cursor
- Click-and-drag on background → pan
- Double-click → fit-to-canvas

**Implementation note**: Wrap the canvas/SVG content in a transformable group (e.g., `<g transform="translate(x,y) scale(s)">` for SVG) so existing draw code remains in world coordinates and zoom/pan logic operates on a single transform.

**Rationale**: Trajectories can have peaks orders of magnitude larger than other terms, making fine detail invisible without zoom. Useful for both close inspection and big-picture fits.

### 7. Data Grid — Jump to Block

Add a numeric input above the data reference grids: type a number, press Enter, and the grid scrolls so that the block of 100 containing that number becomes the first one shown.

**Sub-behavior**: The target cell within the block is visually highlighted (a ring or background color) so the user can locate it.

**Rationale**: When hunting for a specific value, scrolling is slow. Direct addressing supports faster pattern-finding.

## Pedagogical Context

These revisions are motivated by classroom use with middle schoolers. The goal throughout is to surface mathematical structure without overwhelming the UI. Visual hierarchy should reflect cognitive priority: parameters and seed are the primary objects of attention; everything else is secondary infrastructure.

## Out of Scope for This Revision

- Multiple-trajectory overlay (the Cases tool replaces this)
- Adaptive max-steps with overflow nudges (a future option)
- Mobile-specific gestures beyond pinch-to-zoom

## Suggested Implementation Order

1. **Canonicalization** (see `claude-code-prompt.md`) — diff, copy v2 to TEA-Collatz-Paper, set up Pages, update applet-library link to a deployment that mirrors current functionality.
2. **Top bar work** — Revisions 1, 2, 3 (these touch the same component and are best done together).
3. **Auto-reset behavior** — Revision 4.
4. **View menu** — Revision 5.
5. **Zoom and pan** — Revision 6 (architecturally the heaviest; do after the layout is settled).
6. **Grid jump-to-block** — Revision 7 (independent of the rest; can be slotted in anywhere).
