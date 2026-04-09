# 🍬 Sharing the Candy — Integer Partitions Explorer

An interactive web applet for exploring **integer partitions** — the fundamental question: "How many ways can you split a number into groups?"

**Live Demo:** https://ohiomathteacher.github.io/applet-library/integer-partitioning/

---

## What is this?

Based on **Problem 39: "Sharing the Candy"** from *Exploratory Problems in Mathematics*, this applet lets students hands-on explore one of the deepest concepts in combinatorics and number theory.

### The Question

If you have *n* jelly beans, how many ways can you distribute them into groups where order doesn't matter?

- For 4 beans: `[4]`, `[3,1]`, `[2,2]`, `[2,1,1]`, `[1,1,1,1]` → **5 ways**
- For 10 beans: **42 ways**
- For 100 beans: **190,569,292,356 ways** (!!)

---

## Features

### 🫘 Jelly Bean Lab
- **Drag-and-drop interface** — students physically build partitions by dragging colorful jelly beans into buckets
- **Discovery tracker** — records which partitions students have found
- **Hint system** — nudges students toward undiscovered partitions

### ⬤ Ferrers Diagrams
- Visual dot grid representation of each partition
- **Conjugate transformation** — flip rows↔columns to reveal deep connections
- Makes the **distinct parts = odd parts** theorem visible and intuitive

### 📊 Discovery Table
- Auto-generates the summary analysis from the textbook (page 115)
- Groups partitions by largest part
- Counts distinct-parts partitions

### 🔍 Constraint Filters
- Toggle between **All partitions**, **Distinct sizes only**, and **All odd parts**
- See the remarkable fact: # of distinct-parts partitions **always equals** # of odd-parts partitions

### 🎛️ Interactive Controls
- Slider from *n* = 1 to 30
- Start small (*n* = 4 or 5) to build intuition, then scale up to see explosive growth

---

## Pedagogical Use

### Suggested Sequence
1. **Start with n = 4 or 5** — challenge students to find ALL partitions using the Jelly Bean Lab before revealing the full list
2. **Notice patterns** — "How many partitions start with the number itself? With half the number?"
3. **Explore constraints** — Why do distinct-parts and odd-parts always match?
4. **Use Ferrers diagrams** — Can you see the bijection between distinct and odd partitions?
5. **Investigate growth** — How fast does the partition count grow? Can you predict *p*(11) from *p*(10)?

### Deep Question (from the textbook)
> **For *n* = 100, there are 190,569,292,356 partitions. Can you find a formula?**

Spoiler: There's no simple closed formula! This is an active area of research. The partition function *p*(*n*) connects to:
- Ramanujan's congruences
- Modular forms
- Quantum mechanics (bosonic Fock space)

---

## Technology

Pure HTML/CSS/JavaScript — no dependencies, no build step. Just open `index.html` in a browser.

---

## Credits

Inspired by **Problem 39** from *Exploratory Problems in Mathematics: Twenty Mathematical Expeditions* (pages 114-115).

Created for TCE 486 students exploring inquiry-based mathematics teaching.

---

## License

MIT — use freely in your classroom!
