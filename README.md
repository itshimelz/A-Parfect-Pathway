# Perfect Pathway

An AI-Assisted Decision-Making and Path Optimization System

## Overview

Intelligent simulation system that uses AI algorithms to find optimal paths in real-world environments, considering risk, danger zones, and role-specific strategies.

## Features

- **AI Pathfinding** - A\* Search with risk-weighted costs
- **Risk Prediction** - ML-based (Logistic Regression) danger assessment
- **Role-Based Logic** - Army (safe), Rescuer (balanced), Volunteer (efficient)
- **Danger Zones** - Configurable enemy camps that Army role avoids
- **Mission Briefings** - AI-generated (Gemini) tactical narratives
- **Real Map Data** - OpenStreetMap integration via OSMnx

## Quick Start

```bash
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Set Gemini API key for AI briefings
# Create .env file with: GEMINI_API_KEY=your_key_here

# 4. Run the app
streamlit run app.py
```

## Project Structure

```
A Perfect Pathway/
├── src/
│   ├── ai/           # Pathfinding, Risk Model, Mission Narrator
│   ├── roles/        # Army, Rescuer, Volunteer role classes
│   ├── environment/  # Map downloader, Graph enricher
│   └── utils/        # Visualizer
├── docs/             # Phase documentation
├── config.py         # Settings (map center, danger zones, API keys)
└── app.py            # Streamlit UI
```

## Usage

1. Select a **Role** (Army/Rescuer/Volunteer)
2. Choose **Source** and **Destination** streets
3. Click **Plan Mission** or **Random**
4. View the path on the map with role-specific colors
5. Read the auto-generated **Mission Briefing**

## Configuration

Edit `config.py` to:

- Change map center coordinates
- Add/remove danger zones
- Set Gemini API key

## Technologies

NetworkX | scikit-learn | OSMnx | Folium | Streamlit | Google Gemini

## License

Academic project for demonstration purposes.
