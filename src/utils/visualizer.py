import osmnx as ox
import folium
import os


# 1. Add color parameter with a default
def visualize_graph_static(
    graph,
    filename="output/map.html",
    edge_color="blue",
    boundaries_gdf=None,
    center_coords=None,
    radius=None,
):
    """
    Generates a static HTML map visualization.
    Args:
        graph (networkx.MultiDiGraph): The graph to visualize.
        filename (str): The output filename.
        edge_color (str): The color of the edges (e.g., 'red', '#ff0000').
        boundaries_gdf (geopandas.GeoDataFrame, optional): Geometries of administrative boundaries.
        center_coords (tuple, optional): (lat, lon) for the radius circle.
        radius (int, optional): Radius in meters for the circle.
    Returns:
        folium.Map: The generated map object.
    """
    print(f"Generating map visualization to {filename}...")
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph)

        center_y = gdf_nodes.geometry.y.mean()
        center_x = gdf_nodes.geometry.x.mean()

        m = folium.Map(
            location=[center_y, center_x],
            zoom_start=14,
            tiles="cartodbpositron",
            attribution_control=False,
        )

        # Inject CSS for rounded corners
        m.get_root().header.add_child(
            folium.Element("<style>.leaflet-container { border-radius: 12px; }</style>")
        )

        # Plot boundaries first (so they are in the background)
        if boundaries_gdf is not None and not boundaries_gdf.empty:
            print(f"Adding {len(boundaries_gdf)} administrative boundaries to map...")
            folium.GeoJson(
                boundaries_gdf,
                name="Administrative Boundaries",
                style_function=lambda feature: {
                    "fillColor": "#f2f2f2",
                    "color": "#666666",
                    "weight": 1,
                    "dashArray": "5, 5",
                    "fillOpacity": 0.2,
                },
                tooltip=folium.GeoJsonTooltip(
                    fields=["name"] if "name" in boundaries_gdf.columns else []
                ),
            ).add_to(m)

        # Plot radius circle
        if center_coords is not None and radius is not None:
            # OSMnx downloads a square box with side 2*radius.
            # A circle with original radius will cut off corners.
            # To cover the full street network, we can calculate the distance to the furthest node
            # or simply use radius * sqrt(2). Calculating actual furthest node is more precise.
            try:
                # OSMnx downloads a square box with side 2*radius.
                # A circle with original radius will cut off corners.
                # To cover the full street network, we use a 1.45 multiplier (approx sqrt(2) + buffer).
                visual_radius = radius * 1.45

                print(
                    f"Adding radius circle ({visual_radius:.0f}m) at {center_coords}..."
                )
                folium.Circle(
                    location=center_coords,
                    radius=visual_radius,
                    color="#666666",
                    weight=1,
                    fill=True,
                    fill_color="#666666",
                    fill_opacity=0.05,
                    dash_array="10, 10",
                    name="Operation Area",
                ).add_to(m)
            except Exception as circle_err:
                print(f"Error adding radius circle: {circle_err}")

        # Plot edges
        folium.GeoJson(
            gdf_edges,
            name="Street Network",
            style_function=lambda feature: {
                "color": edge_color,
                "weight": 2,
                "opacity": 0.7,
            },
        ).add_to(m)

        folium.LayerControl().add_to(m)

        m.save(filename)
        print("Map visualization saved.")
        return m
    except Exception as e:
        print(f"Error visualizing graph: {e}")
        return None
