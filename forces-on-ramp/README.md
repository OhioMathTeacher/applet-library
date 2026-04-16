# 📐 Forces on a Ramp

An interactive physics simulation for exploring forces on an inclined plane.

**Live Demo:** https://ohiomathteacher.github.io/applet-library/forces-on-ramp/  
**Pedagogical Notes:** https://ohiomathteacher.github.io/applet-library/forces-on-ramp/pedagogical-notes.html

> 📝 **For instructors:** The pedagogical notes page includes design rationale, lesson context from field testing, known limitations, and a space for students to contribute feedback.

---

## What is this?

This applet provides a hands-on way to explore the physics of objects on inclined planes — fundamental to understanding Newton's laws, force decomposition, and friction.

### The Physics

When an object sits on a ramp tilted at angle θ:
- **Gravity (mg)** pulls straight down
- **Normal force (FN)** pushes perpendicular to the ramp surface
- **Parallel component (mg sin θ)** pulls the object down the ramp
- **Perpendicular component (mg cos θ)** presses into the ramp
- **Friction (f = μk · FN)** opposes motion up the slope

---

## Features

### 🎛️ Interactive Controls
- **Ramp angle slider** — adjust from 0° to 45°
- **Mass slider** — change object mass from 10 to 100 kg
- **Friction toggle** — enable/disable kinetic friction with adjustable coefficient (μk)

### 📊 Force Vectors
- **Color-coded arrows** show all forces in real-time
- **Gravity (Fg)** — red, straight down
- **Normal force (FN)** — blue, perpendicular to ramp
- **Parallel/perpendicular components** — orange/gray (optional)
- **Friction (f)** — purple, opposing motion
- Vectors scale dynamically with force magnitude

### 🎯 Free Body Diagram
- Toggle on/off separate FBD view
- Isolates forces acting on the object
- Helps students connect diagram to real scenario

### 🧪 Physics Simulation
- **Drag the crate** to set its position on the ramp (adjusts potential energy)
- **Release button** — run physics simulation with realistic acceleration
- **Energy bar** — visualize PE ↔ KE conversion in real-time
- **Friction feedback** — alerts when friction is too strong to allow motion

### 📈 Live Calculations
- Gravity force (mg)
- Normal force (N)
- Parallel component (mg sin θ)
- Friction force (f)
- Net force
- Acceleration (a = F/m)
- Current velocity during simulation

---

## Pedagogical Use

### For Students
- **Predict before calculating** — what happens when you increase the angle? Mass? Friction?
- **Test edge cases** — what angle makes friction too strong? When does normal force equal weight?
- **Energy exploration** — drag crate to different heights, watch PE→KE conversion
- **Component practice** — decompose gravity into perpendicular and parallel components

### For Teachers
- Use as **pre-lab** before Hot Wheels F=ma experiments
- Perfect for **remote/hybrid** — students explore from home
- **Inquiry questions**: 
  - "What angle makes the object slide fastest?"
  - "Can you set friction so the crate barely moves?"
  - "How does doubling mass affect acceleration?"
- Complements hands-on ramps/dynamics carts

### Learning Objectives
- Understand force decomposition on inclined planes
- Connect free body diagrams to physical scenarios
- Explore relationship between angle, friction, and motion
- Apply F = ma to predict acceleration
- Visualize energy conservation (PE ↔ KE)

---

## Technical Notes

- Pure HTML/JavaScript/Canvas — no dependencies
- Works on desktop and mobile/tablet (touch-enabled dragging)
- Self-contained single file for easy embedding

---

## Credits

Created for TCE 432 (Science & Math Methods) at Miami University, Spring 2026.  
Designed to support McKenzie Sorce's revised Hot Wheels inquiry lesson on F=ma.
