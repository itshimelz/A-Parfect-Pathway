# Phase 4: Learning & Simulation Engine

## **Objective**

Implement the Reinforcement Learning (Q-Learning) loop and the overall simulation manager that ties everything together.

## **Key Components**

### 1. **Q-Learning Agent (For Rescuer)**

- **Concept**: The agent doesn't know the map initially. It tries random paths (Exploration). As it succeeds or fails, it updates a Q-Table.
- **State**: The current node user is at.
- **Action**: Moving to a neighboring node.
- **Q-Table**: A matrix `[Nodes x Neighbors]` storing the value of taking an action.
- **Algorithm**:
  $Q(s, a) = Q(s, a) + \alpha [R + \gamma \max Q(s', a') - Q(s, a)]$
- **Training**: We need a "Training Phase" button in the UI that runs ~1000 fast episodes to "train" the Rescuer before the user sees the final result.

### 2. **Simulation Controller**

- **Purpose**: A central class to manage the "Game State".
- **Responsibilities**:
  - Load the map.
  - Instantiate the Roles.
  - Run the logic.
  - Collect stats (Total distance, total risk accumulated, success/fail).

## **Implementation Steps**

1.  **RL Agent**: Create `src/ai/q_learning.py`.
    - Class `QLearningAgent`.
    - Methods `train(episodes)`, `get_best_action(state)`.
2.  **Simulation Manager**: Create `src/simulation/engine.py`.
    - Function `run_single_episode(role, start, end)`.
    - Function `compare_algorithms(start, end)` -> Returns stats for all 3 roles.

## **Deliverables**

- A trained Q-Table (saved to file).
- A simulation script that outputs text logs: "Rescuer reached goal in 15 steps. Army reached in 25 steps (but 0 risk)."
