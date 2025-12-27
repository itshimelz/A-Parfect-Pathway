# Perfect Pathway

## An AI-Assisted Decision-Making and Path Optimization System

### Overview

Perfect Pathway is an intelligent simulation system that models real-world environments as graphs and uses Artificial Intelligence algorithms to assist different roles in making optimal decisions under uncertainty, risk, and limited resources.

**Problem**: Decision-makers in disaster response, military operations, and humanitarian aid must choose optimal paths and actions, but traditional algorithms fail to consider dynamic factors like danger levels, time constraints, and changing environments.

**Solution**: Perfect Pathway integrates multiple AI techniques for realistic, intelligent decision-making:

- **A* Search Algorithm** - Intelligent pathfinding considering distance and risk
- **Machine Learning** - Risk prediction using Logistic Regression
- **Reinforcement Learning** - Q-Learning for adaptive decision-making
- **Role-Based Intelligence** - Specialized behavior for Army, Rescuer, and Volunteer

### Features

- ✅ Graph-based realistic environment with real-world attributes
- ✅ AI-assisted path recommendation
- ✅ Role-based intelligent behavior
- ✅ Risk prediction using Machine Learning
- ✅ Learning and adaptation using Reinforcement Learning
- ✅ Real map visualization (Folium + OSM)
- ✅ **Real Rajshahi street network integration**
- ✅ Complete simulation framework

### Project Structure

```
A Perfect Pathway/
├── src/
│   ├── environment/                # Graph and environment management
│   ├── ai/                         # AI algorithms (A*, ML, Q-Learning)
│   ├── roles/                      # Decision-making roles
│   ├── visualization/              # Map and graph visualization
│   ├── data_generation/            # Synthetic data generators
│   └── utils/                      # Utilities
├── examples/                       # Example scripts
├── simulations/                    # Pre-built scenarios
├── maps/                           # Generated map visualizations
├── cache/                          # API cache
├── data/                           # Training and model data
├── output/                         # Generated outputs
├── main.py                         # Map visualization demo
└── demo.py                         # Complete feature demo
```

### Setup

1. **Activate Virtual Environment**

```bash
# PowerShell
.\.venv\Scripts\Activate.ps1

# Command Prompt
.venv\Scripts\activate.bat
```

2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### AI Algorithms

#### 1. A* Search Algorithm

- **Purpose**: Intelligent pathfinding with heuristics
- **Optimization**: Distance, time, risk, or combined
- **Used by**: Army, Rescuer, Volunteer roles

#### 2. Machine Learning (Risk Prediction)

- **Model**: Logistic Regression
- **Input**: Edge features (distance, risk levels, enemy probability)
- **Output**: Safe/Unsafe classification
- **Used by**: Army (to avoid dangerous routes)

#### 3. Reinforcement Learning (Q-Learning)

- **Purpose**: Learn optimal decisions from experience
- **Used by**: Rescuer role for adaptive learning
- **Reward**: Successful rescues + speed + safety

### Roles & Strategies

#### Army
- **Priority**: Safety and strategic positioning
- **Strategy**: Finds safest paths using A*
- **Minimizes**: Risk and enemy probability

#### Rescuer
- **Priority**: Speed and rescue success
- **Strategy**: Fast paths with learned adaptations via Q-Learning
- **Maximizes**: People rescued per mission

#### Volunteer
- **Priority**: Resource efficiency
- **Strategy**: Balanced paths with optimal resource allocation
- **Maximizes**: Support efficiency per resource

### Requirements

- Python 3.8+
- See [requirements.txt](requirements.txt)

### Key Technologies

- **NetworkX** - Graph construction and analysis
- **scikit-learn** - Machine learning models
- **Folium** - Real map visualization
- **OSMnx** - Geographic data
- **Matplotlib** - Graph visualization

### Future Enhancements

- Deep learning for complex scenarios
- Multi-agent coordination
- Real-time dynamic environments
- More sophisticated reward functions

### License

Academic project for demonstration and coursework.

### Notes

- No deep neural networks (for clarity and explainability)
- Focus on correctness and real-world relevance
- Suitable for academic evaluation and demonstrations

