Here’s your updated specification document with the **wall-search phase** integrated clearly and consistently across all relevant sections:

---

## Wall-Following Behavior Evolution – Specification Document

### 1. Behavior Objective

Develop and evolve a robot controller that enables **wall-following at a safe, fixed distance** from the wall in a simulated environment. The robot must **begin by actively searching for a wall** before engaging in wall-following behavior.

---

### 2. Performance Metrics

Define metrics to measure the effectiveness of the evolved behavior:

* **Average distance to wall:** Should remain close to a target threshold (e.g., 30 cm).
* **Time spent within safe distance range:** The longer the robot stays within acceptable bounds, the better.
* **Wall acquisition time:** Time taken from simulation start to first wall detection and transition to wall-following mode.

---

### 3. Robot Specification

Simulated robot should have the following characteristics:

* [x] **Drive system:** Differential drive (2 independently driven wheels).
* [ ]**Sensors:**

  * [x] At least **three proximity sensors**: left, front, and right.
  * [x] Approximate **180-degree forward-facing coverage**.
* **Motion constraints:**

  * [x] **Maximum linear speed:** e.g., 10 cm/s. (figure out if true)
  * [x] **Limited turning rate** to simulate realistic motion.

---

### 4. Simulation Environment

Set up the robot's environment in the simulator:

* **Walls:**

  * [x] At least one **long, straight wall**.
  * [x] Include **corners or turns** to test adaptability.
* **Starting positions:**

  * [x] Include positions where the robot starts **facing away from the wall**, requiring it to search for a wall first.
  * [x] Optionally use **multiple starting points** for robustness testing.

---

## Controller Design and Evolution Plan

### 5. Controller Representation

* [x] Implement hand-coded baseline controller.
* [x] Define parameters to evolve (e.g., distance thresholds, gain values).

**Controller Logic Structure:**

* Two-phase behavior:

  1. **Wall Search Phase**:

     * If no wall is detected within a predefined range (e.g., 50 cm), robot moves forward and slowly turns to search.
  2. **Wall-Following Phase**:

     * Once a wall is detected, robot switches to maintaining a target distance from the wall.

* Use a binary state flag (e.g., `searching_wall = True`) to manage phase transition.

---

### 6. Evolutionary Setup

* [x] Define genome structure (e.g., thresholds/gains as float values).

* [x] Set evolutionary algorithm parameters:

  * [x] Population size (e.g., 20–50).
  * [x] Number of generations (e.g., 30–100).
  * [x] Selection method (e.g., Genetic algorithm).
  * [x] Mutation operator (e.g., Gaussian noise).
  * [x] Crossover operator (optional).

* [x] Define fitness function:

  * [x] Reward staying near wall.
  * [x] Penalize collisions.
  * [x] Penalize distance variance.
  * [x] Penalize excessive time taken to detect and approach the wall (long wall acquisition time).

---

### 7. Experimental Setup

* [ ] Define trial duration (e.g., 1–2 minutes per evaluation).
* [ ] Use multiple environments or start positions for generality.
* [ ] Include trials where the robot **starts with no wall in view**.
* [ ] Run multiple trials per individual to reduce variance.
* [ ] Log and store data:

  * [ ] Distance to wall over time.
  * [ ] Number of collisions.
  * [ ] Wall acquisition time.
  * [ ] Final fitness score.
  * [ ] Robot path/trajectory plots (optional).

---

### 8. Results and Discussion

* [ ] Plot fitness over generations.
* [ ] Plot distance-to-wall for best individuals.
* [ ] Analyze **wall acquisition behavior** (e.g., exploration efficiency).
* [ ] Compare evolved vs. baseline controllers.
* [ ] Analyze behavior (e.g., corner following, oscillation).
* [ ] Discuss findings:

  * [ ] What worked.
  * [ ] What didn’t.
  * [ ] What to improve.
  * [ ] Potential extensions.

---

### 9. Final Report Checklist

* [ ] Task description and performance metrics.
* [ ] Robot and environment specification.
* [ ] Controller design and what is being evolved.
* [ ] Experimental and evolutionary setup.
* [ ] Results with statistics and visuals.
* [ ] Discussion and suggestions for future work.

---

Let me know if you'd like this exported to a formatted document (Markdown, PDF, etc.) or want to integrate some sample pseudocode.
