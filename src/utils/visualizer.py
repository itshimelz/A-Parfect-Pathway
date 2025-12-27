import osmnx as ox
import folium
import os

def visualize_graph_static(graph, filename="output/map.html"):
    """
    Generates a static HTML map visualization of the graph.
    
    Args:
        graph (networkx.MultiDiGraph): The graph to plot.
        filename (str): Output file path.
    """
    print(f"Generating map visualization to {filename}...")
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # In OSMnx 2.0, plot_graph_folium is removed.
        # We can implement a simple version by converting to GeoDataFrames
        gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph)
        
        # Center of the map
        center_y = gdf_nodes.geometry.y.mean()
        center_x = gdf_nodes.geometry.x.mean()
        
        m = folium.Map(location=[center_y, center_x], zoom_start=14, tiles="cartodbpositron")
        
        # Plot edges
        folium.GeoJson(
            gdf_edges,
            style_function=lambda feature: {
                'color': 'blue',
                'weight': 1,
                'opacity': 0.7
            }
        ).add_to(m)
        
        # Save map
        m.save(filename)
        print("Map visualization saved.")
    except Exception as e:
        print(f"Error visualizing graph: {e}")
