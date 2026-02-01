# GIGA BIRD

**GIGA BIRD** is a high-population genetic algorithm simulation implemented in Python. It demonstrates the power of neuroevolution by training a population of 150 autonomous agents to navigate a procedurally generated obstacle course. Unlike traditional reinforcement learning that relies on backpropagation, GIGA BIRD uses a Darwinian selection process to evolve neural network weights over successive generations.

---

## Technical Overview

The project utilizes a custom-built neural network architecture and a genetic algorithm framework designed for high-concurrency simulation.

### Neural Architecture
Each agent is controlled by a feedforward neural network. To determine the optimal timing for a jump action, the network processes a vector of **5 real-time inputs**:

* **BIRD_Y**: Vertical position of the agent.
* **PIPE_DIST**: Horizontal distance to the next upcoming pipe.
* **PIPE_TOP**: Y-coordinate of the upper pipe boundary.
* **PIPE_BOTTOM**: Y-coordinate of the lower pipe boundary.
* **BIRD_VEL**: Current vertical velocity of the agent.



---

## Evolutionary Strategy

The simulation employs **Fitness-Proportionate Selection** (Roulette Wheel Selection) to drive the optimization process.

* **Fitness Scoring**: Agents earn fitness based on time survived, with a significant **+100 bonus** for every pipe successfully cleared.
* **Selection**: The top-performing genomes are prioritized to seed the next generation.
* **Crossover**: Genetic material is merged from parent genomes to produce offspring with potentially superior traits.

### Mutation Engine
To prevent local optima and maintain genetic diversity, the system utilizes a dual-mode weight mutation strategy:

1. **Perturbation (90% chance)**: Slightly adjusts existing weights by a small power factor to "fine-tune" behavior.
2. **Replacement (10% chance)**: Completely resets a weight to a random value between -2 and 2 to explore new strategies.

---

## Project Structure

| File | Responsibility |
| :--- | :--- |
| **main.py** | Entry point for the simulation and Pygame rendering loop. |
| **Genome.py** | Neural network logic, feedforward pass, and mutation functions. |
| **Population.py** | Manages genome collections, fitness evaluation, and evolution cycles. |
| **Bird.py** | Agent physics, collision state, and Genome-to-game interface. |
| **Pipe.py** | Procedural generation and movement logic for obstacles. |

---

## Requirements

* **Python 3.x**
* **Pygame 2.x**

```bash
pip install -r requirements.txt
<img width="393" height="596" alt="gen0" src="https://github.com/user-attachments/assets/d5b3282e-aba4-4f11-8f69-79abeb1741e8" />
<img width="387" height="590" alt="gen1" src="https://github.com/user-attachments/assets/881b93f5-17e6-46d8-b2a4-c1574b015acf" />
<img width="389" height="584" alt="gen5" src="https://github.com/user-attachments/assets/1e7a2202-b482-4934-ac68-103b1f3e32ce" />


