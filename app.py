import streamlit as st
from streamlit_folium import st_folium
import osmnx as ox
import pandas as pd
from src.environment.map_downloader import download_graph, download_boundaries
from src.environment.graph_enricher import enrich_graph
from src.utils.visualizer import visualize_graph_static
from config import MAP_CENTER_LAT, MAP_CENTER_LON, MAP_DEFAULT_RADIUS

st.set_page_config(page_title="A Perfect Pathway", layout="wide")

st.title("A Perfect Pathway - Simulation Environment")
st.markdown("Real-world street network enriched with synthetic simulation attributes.")

# Sidebar for configuration
st.sidebar.header("Map Configuration")
lat = st.sidebar.number_input("Center Latitude", value=MAP_CENTER_LAT, format="%.6f")
lon = st.sidebar.number_input("Center Longitude", value=MAP_CENTER_LON, format="%.6f")
radius = st.sidebar.slider("Radius (meters)", 500, 5000, MAP_DEFAULT_RADIUS)


@st.cache_resource
def load_and_enrich_graph(lat, lon, radius):
    location = (lat, lon)
    G = download_graph(location=location, dist=radius)
    if G:
        G = enrich_graph(G)
        return G
    return None


@st.cache_resource
def load_boundaries(lat, lon):
    return download_boundaries(location=(lat, lon))


@st.cache_resource
def get_map(_G, _boundaries, lat, lon, radius):
    """Caches the folium map object to prevent continuous regeneration."""
    return visualize_graph_static(
        _G,
        filename="outputs/streamlit_map.html",
        edge_color="#5474D0",
        boundaries_gdf=_boundaries,
        center_coords=(lat, lon),
        radius=radius,
    )


# Main logic
G = load_and_enrich_graph(lat, lon, radius)
boundaries = load_boundaries(lat, lon)

if G:
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("Interactive Map")
        m = get_map(G, boundaries, lat, lon, radius)
        if m:
            # We use a static key to help Streamlit maintain state across reruns
            # returned_objects=[] prevents the map from triggering a rerun on every zoom/pan
            st_folium(m, width=900, height=600, key="main_map", returned_objects=[])
        else:
            st.error("Failed to generate map object.")

    with col2:
        st.subheader("Environment Stats")
        st.metric("Nodes", G.number_of_nodes())
        st.metric("Edges", G.number_of_edges())

        # Display some edge data
        st.subheader("Sample Edge Data")
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(G)
        if not gdf_edges.empty:
            sample_data = gdf_edges[
                ["risk_level", "enemy_probability", "resource_cost"]
            ].head(10)
            st.dataframe(sample_data)
else:
    st.error("Could not load the graph. Please check your coordinates or try again.")
