# 🎱 Billiard Ball Physics — Momentum & Collisions

An interactive web applet for exploring **conservation of momentum** through elastic collisions between billiard balls.

**Physics Concept:** In elastic collisions, momentum is always conserved. The total momentum before collision equals the total momentum after collision.

---

## 🎯 Two Versions Available

This applet comes in two versions to demonstrate the evolution from basic simulation to comprehensive inquiry-based learning tool:

### **[Version 1: Basic Simulation](https://ohiomathteacher.github.io/applet-library/momentum-collisions/index-v1.html)**
Clean, focused physics demonstration with essential features

### **[Version 2: Inquiry-Based Learning Tool](https://ohiomathteacher.github.io/applet-library/momentum-collisions/index-v2.html)** ⭐ Enhanced
Complete educational experience with challenges, adaptive difficulty, multi-language support, and lab notebook

**[📊 Compare Versions](https://ohiomathteacher.github.io/applet-library/momentum-collisions/index-landing.html)** — Interactive comparison landing page

---

## Features (Version 1)

### 🎮 Interactive Controls
- **Adjustable Mass:** Change each ball's mass (0.5–5 kg) to see how it affects collision outcomes
- **Velocity Sliders:** Set initial velocities from -10 to +10 m/s for each ball
- **Real-time Momentum Display:** Watch momentum values update before and during collisions

### 🎯 Quick Scenarios
Three preset scenarios demonstrate key collision types:
1. **Equal Mass, Moving + Stationary** — Classic "cue ball" scenario where moving ball transfers momentum
2. **Head-On Collision** — Balls moving toward each other with equal speeds
3. **Heavy Hits Light** — Shows how mass differences affect post-collision velocities

### 📊 Visual Learning
- **Velocity Vectors:** White arrows show direction and magnitude of ball velocities
- **Mass-Based Sizing:** Heavier balls appear larger for visual intuition
- **Real-time Calculations:** Momentum values (p = mv) displayed continuously
- **Conservation Verification:** Compare "Total Before" vs "Total After" to verify the law

---

## Enhanced Features (Version 2) ⭐

### 🎯 Guided Challenge System
Five scaffolded challenges that guide student inquiry:
1. **Make Both Balls Stop** — Understanding equal and opposite momentum
2. **Make One Ball Stop** — Classic momentum transfer scenario
3. **Reverse Direction** — Exploring mass and velocity relationships
4. **Speed Transfer** — Heavy-to-light collision dynamics
5. **Create Your Own** — Open-ended investigation

Each challenge includes:
- Clear problem statement
- Contextual hints
- Gradual reveal of physics principles

### 📚 Adaptive Difficulty Levels
Three learning modes that adjust language and complexity:
- **Novice:** Simple terminology ("weight" instead of "mass", "push" instead of "momentum")
- **Intermediate:** Standard physics vocabulary with clear explanations
- **Experienced:** Advanced terminology with subscripts (p₁, p₂, Σp)

### 🌍 Multi-Language Support
Full interface translation in:
- **English** — Standard physics education language
- **Español** — Support for Spanish-speaking students
- **中文** — Chinese language support

All text, labels, challenges, and buttons adapt to selected language.

### 📝 Interactive Lab Notebook
Digital scratchpad for inquiry-based learning:
- **Capture Data Snapshots** — Save current state with one click (masses, velocities, momentum values)
- **Annotate Observations** — Add notes to each captured scenario
- **Timestamp Tracking** — Automatic time recording for each entry
- **Export Function** — Download entire notebook as formatted text file
- **Delete/Clear** — Manage entries individually or clear all

Perfect for:
- Documenting patterns and trends
- Comparing multiple collision scenarios
- Supporting claims with evidence
- Reflective learning practices

---

## The Physics

### Conservation of Momentum
**p₁ᵢ + p₂ᵢ = p₁f + p₂f**

Where:
- **p = mv** (momentum = mass × velocity)
- **i** = initial (before collision)
- **f** = final (after collision)

### Elastic Collision Equations
For 1D elastic collisions, the post-collision velocities are:

**v₁' = [(m₁ - m₂)v₁ + 2m₂v₂] / (m₁ + m₂)**  
**v₂' = [(m₂ - m₁)v₂ + 2m₁v₁] / (m₁ + m₂)**

---

## Pedagogical Use

### Discovery Questions
1. What happens when a heavy ball hits a light ball? Vice versa?
2. Can you create a scenario where ball 1 completely stops after collision?
3. Does the total momentum ever change during collisions?
4. How does mass affect the final velocity after collision?

### Common Student Misconceptions
- **"Heavier objects always move faster after collisions"** — Use the applet to show momentum distribution depends on initial conditions
- **"Momentum is created in collisions"** — The conservation display makes it clear momentum is constant
- **"Mass and velocity contribute equally"** — Experiment with different combinations to see momentum depends on both factors

### Extension Activities
- **Predict then Test:** Have students predict collision outcomes before running the simulation
- **Data Collection:** Record mass/velocity combinations and calculate expected outcomes by hand, then verify
- **Connection to Pool/Billiards:** Discuss real-world applications (why does the cue ball stop when hitting a stationary ball head-on?)

---

## Technical Details

- **Pure HTML/CSS/JavaScript** — No external dependencies
- **Canvas-based Animation** — Smooth 60fps rendering
- **Responsive Design** — Grid layout adapts to screen size
- **Physics Engine:** Implements:
  - 1D elastic collision equations
  - Wall boundary collisions with reflection
  - Velocity vector visualization
  - Mass-proportional visual scaling

---

## Inspiration

Created in response to McKenzie Sorce's PhET simulation recommendations, particularly inspired by PhET's interactive physics labs that make abstract concepts tangible through play and experimentation.

---

## Future Enhancements

### Version 1 & 2
- [ ] 2D collisions (balls can move vertically)
- [ ] Coefficient of restitution slider (elastic → inelastic continuum)
- [ ] Multiple balls (chain collisions)
- [ ] Energy conservation display alongside momentum
- [ ] Slow-motion playback controls

### Version 2 Specific
- [x] Guided challenge problems
- [x] Adaptive difficulty levels
- [x] Multi-language interface
- [x] Lab notebook / data capture
- [x] Export functionality
- [ ] Teacher dashboard for monitoring student progress
- [ ] Challenge completion tracking
- [ ] Pre/post assessment questions
- [ ] Collaboration features (share notebook entries)
- [ ] Additional languages (French, German, Arabic)

---

## Comparing Versions: Design Philosophy

**Version 1** focuses on clarity and simplicity. It's a solid, distraction-free tool for observing momentum conservation. Perfect for demonstrations, quick explorations, or students who want direct access to the simulation without scaffolding.

**Version 2** transforms the simulation into a complete learning environment. The challenge system guides inquiry, difficulty levels provide accessibility, language support opens doors for diverse learners, and the lab notebook encourages reflection and evidence-based reasoning.

**When to use which:**
- **V1:** Teacher-led demonstrations, advanced students, quick investigations
- **V2:** Independent student work, inquiry-based projects, diverse classrooms, formative assessment

Both versions maintain the same high-quality physics engine and visual design — the difference is in the pedagogical scaffolding.