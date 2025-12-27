import streamlit as st
from streamlit_folium import st_folium
import osmnx as ox
import folium
import random
from src.environment.map_downloader import download_graph, download_boundaries
from src.environment.graph_enricher import enrich_graph
from src.utils.visualizer import visualize_graph_static
from src.ai.pathfinding import find_path_astar
from config import MAP_CENTER_LAT, MAP_CENTER_LON, MAP_DEFAULT_RADIUS

st.set_page_config(page_title="A Perfect Pathway", layout="wide")

st.title("🛡️ A Perfect Pathway - Simulation Environment")
st.markdown("Real-world street network enriched with **AI-driven risk prediction**.")

# Sidebar for configuration
st.sidebar.header("Map Configuration")
lat = st.sidebar.number_input("Center Latitude", value=MAP_CENTER_LAT, format="%.6f")
lon = st.sidebar.number_input("Center Longitude", value=MAP_CENTER_LON, format="%.6f")
radius = st.sidebar.slider("Radius (meters)", 500, 5000, MAP_DEFAULT_RADIUS)
st.sidebar.markdown("---")

st.sidebar.header("Pathfinding AI")
path_mode = st.sidebar.selectbox(
    "AI Strategy", ["Safe (Army)", "Balanced (Volunteer)", "Fast (Civilian)"]
)
strategy_mode = "safe"
if "Volunteer" in path_mode:
    strategy_mode = "balanced"
if "Civilian" in path_mode:
    strategy_mode = "fast"


@st.cache_resource
def load_and_enrich_graph(lat, lon, radius):
    """Downloads and enriches the graph. Cached to avoid re-downloading."""
    location = (lat, lon)
    G = download_graph(location=location, dist=radius)
    if G:
        G = enrich_graph(G)
        return G
    return None


@st.cache_resource
def load_boundaries(lat, lon):
    return download_boundaries(location=(lat, lon))


def get_map(_G, _boundaries, lat, lon, radius, path_coords=None):
    """
    Generates the folium map object.
    Not cached to allow dynamic path updates.
    """
    m = visualize_graph_static(
        _G,
        filename="outputs/streamlit_map.html",
        edge_color="#5474D0",
        boundaries_gdf=_boundaries,
        center_coords=(lat, lon),
        radius=radius,
    )

    if path_coords:
        # Reverse geocode to get place names
        try:
            start_address = ox.geocode_to_gdf(
                f"{path_coords[0][0]}, {path_coords[0][1]}", which_result=1
            )
            start_name = (
                start_address.iloc[0].get("display_name", "Start").split(",")[0]
            )
        except:
            start_name = "Start Point"

        try:
            end_address = ox.geocode_to_gdf(
                f"{path_coords[-1][0]}, {path_coords[-1][1]}", which_result=1
            )
            end_name = (
                end_address.iloc[0].get("display_name", "Destination").split(",")[0]
            )
        except:
            end_name = "Destination"

        # Draw the calculated path
        folium.PolyLine(
            path_coords,
            color="#FF4B4B",
            weight=5,
            opacity=0.8,
            tooltip="AI Calculated Path",
        ).add_to(m)

        # Start Marker (Green) with place name
        folium.Marker(
            path_coords[0],
            popup=f"🚀 {start_name}",
            tooltip=start_name,
            icon=folium.Icon(color="green", icon="play"),
        ).add_to(m)

        # End Marker (Red) with place name
        folium.Marker(
            path_coords[-1],
            popup=f"{end_name}",
            tooltip=end_name,
            icon=folium.Icon(color="red", icon="flag"),
        ).add_to(m)

    return m


# Main logic
G = load_and_enrich_graph(lat, lon, radius)
boundaries = load_boundaries(lat, lon)

# Pathfinding State
if "path_coords" not in st.session_state:
    st.session_state["path_coords"] = None

if G:
    # Navigation Controls
    col1, col2 = st.columns([3, 1])

    with col2:
        st.subheader("Mission Control")
        if st.button("🎲 Generate Random Mission", type="primary"):
            nodes = list(G.nodes())
            if len(nodes) > 1:
                start_node = random.choice(nodes)
                end_node = random.choice(nodes)

                with st.spinner("AI calculating optimal path..."):
                    path_nodes, path_coords = find_path_astar(
                        G, start_node, end_node, weight_mode=strategy_mode
                    )
                    st.session_state["path_coords"] = path_coords
                    if path_coords:
                        st.success(f"Path Found! Steps: {len(path_nodes)}")
                    else:
                        st.error("No path found.")
            else:
                st.error("Graph has too few nodes.")

        st.metric("Nodes", G.number_of_nodes())
        st.metric("Edges", G.number_of_edges())

        st.markdown("### Risk Analysis")
        if st.session_state["path_coords"]:
            # Simple metric: number of segments
            st.info(f"Route Segments: {len(st.session_state['path_coords'])}")
            st.caption(f"Strategy: {path_mode}")

        # Display some edge data
        st.subheader("Intel Feed")
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
        if not gdf_edges.empty:
            sample_data = gdf_edges[
                ["risk_level", "enemy_probability", "resource_cost"]
            ].head(5)
            st.dataframe(sample_data, hide_index=True)

    with col1:
        st.subheader("Live Operational Map")
        m = get_map(G, boundaries, lat, lon, radius, st.session_state["path_coords"])

        if m:
            st_folium(m, width=900, height=600, key="main_map", returned_objects=[])
        else:
            st.error("Failed to generate map object.")

else:
    st.error("Could not load the graph. Please check your coordinates or try again.")
