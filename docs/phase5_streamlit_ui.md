# Phase 5: User Interface (Streamlit)

## **Objective**

Create a web-based dashboard using `streamlit` to visualize the simulation, allowing users to interact with the map, select roles, and see the AI in action.

## **Key Features**

### 1. **Sidebar Controls**

- **Location Selector**: "Rajshahi", "Dhaka", or "Custom Coords".
- **Role Selector**: "Army", "Rescuer", "Volunteer", "Compare All".
- **Parameters**: Sliders for "Risk Tolerance", "Number of Training Episodes".

### 2. **Main Map Display**

- **Library**: `streamlit-folium`.
- **Visualization**:
  - Display the base map.
  - Color-code edges by Risk (Red = High Risk, Green = Safe).
  - Overlay the **calculated path** as a thick blue/orange line.
  - Markers for Start (Green Flag) and End (Red Flag).

### 3. **Data & Metrics**

- **Charts**: Bar charts comparing Time vs. Risk for the selected path.
- **Text**: Explanation of _why_ the AI chose this path (e.g., "Army chose this route to avoid High Conflict Zone at Node 542").

## **Implementation Steps**

1.  **Setup**: Create `app.py`.
2.  **Layout**: Use `st.sidebar` for inputs, `st.columns` for metrics.
3.  **Integration**:
    - Call methods from Phase 1 to load map.
    - Call methods from Phase 3/4 to get the path.
    - Pass the path coordinates to Folium to draw the `PolyLine`.
4.  **Refinement**: Add "Train Model" button to trigger the ML/RL training loops in real-time (with a progress bar).

## **Deliverables**

- A fully functional `app.py`.
- Users can click points on the map (if possible) or select from a list to define Start/End.
- Visual proof of different paths for different roles.
