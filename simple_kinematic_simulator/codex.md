## Wall-Following Behavior Evolution – Specification Document

### 1. Behavior Objective

Develop and evolve a robot controller that enables **wall-following at a safe, fixed distance** from the wall in a simulated environment.

---

### 2. Performance Metrics

Define metrics to measure the effectiveness of the evolved behavior:

* **Average distance to wall:** Should remain close to a target threshold (e.g., 30 cm).
* **Time spent within safe distance range:** The longer the robot stays within acceptable bounds, the better.


### 3. Robot Specification

Simulated robot should have the following characteristics:

* **Drive system:** Differential drive (2 independently driven wheels).
* **Sensors:**

  * At least **three proximity sensors**: left, front, and right.
  * Approximate **180-degree forward-facing coverage**.
* **Motion constraints:**

  * **Maximum linear speed:** e.g., 0.3 m/s. (figure out if true)
  * **Limited turning rate** to simulate realistic motion.

---

### 4. Simulation Environment

Set up the robot's environment in the simulator:

* **Walls:**

  * At least one **long, straight wall**.
  * Include **corners or turns** to test adaptability.
* **Starting positions:**

  * Use **fixed positions** near the wall, not directly aligned.
  * Optionally use **multiple starting points** for robustness testing.

---

## Controller Design and Evolution Plan

### 5. Controller Representation

* [ ] Implement hand-coded baseline controller.
* [ ] Define parameters to evolve (e.g., distance thresholds, gain values).
* [ ] (Optional) Define an alternate controller (e.g., simple neural network).

---

### 6. Evolutionary Setup

* [ ] Define genome structure (e.g., thresholds/gains as float values).
* [ ] Set evolutionary algorithm parameters:

  * [ ] Population size (e.g., 20–50).
  * [ ] Number of generations (e.g., 30–100).
  * [ ] Selection method (e.g., Genetic algorithm).
  * [ ] Mutation operator (e.g., Gaussian noise).
  * [ ] Crossover operator (optional).
* [ ] Define fitness function:

  * [ ] Reward staying near wall.
  * [ ] Penalize collisions.
  * [ ] Penalize distance variance.

---

### 7. Experimental Setup

* [ ] Define trial duration (e.g., 1–2 minutes per evaluation).
* [ ] Use multiple environments or start positions for generality.
* [ ] Run multiple trials per individual to reduce variance.
* [ ] Log and store data:

  * [ ] Distance to wall over time.
  * [ ] Number of collisions.
  * [ ] Final fitness score.
  * [ ] Robot path/trajectory plots (optional).

---

### 8. Results and Discussion

* [ ] Plot fitness over generations.
* [ ] Plot distance-to-wall for best individuals.
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

