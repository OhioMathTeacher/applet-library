# 🎱 Billiard Ball Physics — Momentum & Collisions

An interactive web applet for exploring **conservation of momentum** through elastic collisions between billiard balls.

**Physics Concept:** In elastic collisions, momentum is always conserved. The total momentum before collision equals the total momentum after collision.

---

## Features

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

- [ ] 2D collisions (balls can move vertically)
- [ ] Coefficient of restitution slider (elastic → inelastic continuum)
- [ ] Multiple balls (chain collisions)
- [ ] Energy conservation display alongside momentum
- [ ] Export collision data as CSV
- [ ] Slow-motion playback controls