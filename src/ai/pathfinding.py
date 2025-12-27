import networkx as nx
import math


def haversine(u, v, G):
    """
    Heuristic function for A* Search.
    Calculates the great-circle distance between two nodes.
    """
    x1, y1 = G.nodes[u]["x"], G.nodes[u]["y"]
    x2, y2 = G.nodes[v]["x"], G.nodes[v]["y"]
    R = 6371000  # radius of Earth in meters

    phi1, phi2 = math.radians(y1), math.radians(y2)
    dphi = math.radians(y2 - y1)
    dlambda = math.radians(x2 - x1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def calculate_weight(u, v, d, mode="safe"):
    """
    Calculates the weight of an edge based on distance and risk.
    """
    # Handle MultiDiGraph structure where d might be {0: {path_data}, 1: {path_data}}
    # dependent on NetworkX version and graph type.
    edge_data = d
    if d and isinstance(d, dict):
        first_val = next(iter(d.values()))
        if isinstance(first_val, dict):
            # It's a MultiGraph dict of dicts
            edge_data = first_val

    length = edge_data.get("length", 1.0)
    risk = edge_data.get("risk_level", 0.0)

    if mode == "safe":
        # Army Logic: Avoid risk at all costs.
        # Cost = Length * (1 + 100 * Risk)
        # If risk is 0.1, multiplier is 11x
        return length * (1 + 100 * risk)

    elif mode == "balanced":
        # Volunteer Logic: Balance
        # Cost = Length * (1 + 5 * Risk)
        return length * (1 + 5 * risk)

    else:
        # Fast / Default
        return length


def find_path_astar(G, start_node, end_node, weight_mode="safe"):
    """
    Finds the optimal path using A* Search.

    Args:
        G (networkx.MultiDiGraph): The graph.
        start_node (int): Source node ID.
        end_node (int): Target node ID.
        weight_mode (str): 'safe', 'balanced', or 'fast'.

    Returns:
        tuple: (path_nodes, path_coords)
            path_nodes: List of node IDs.
            path_coords: List of (lat, lon) tuples following the street geometry.
    """
    try:
        # Define a lambda for the weight to pass context
        path_nodes = nx.astar_path(
            G,
            start_node,
            end_node,
            heuristic=lambda u, v: haversine(u, v, G),
            weight=lambda u, v, d: calculate_weight(u, v, d, weight_mode),
        )

        # Extract full geometry
        path_coords = []
        for i in range(len(path_nodes) - 1):
            u = path_nodes[i]
            v = path_nodes[i + 1]

            # Get edge data (taking the first key if multiple edges exist)
            edge_data = G.get_edge_data(u, v)[0]

            if "geometry" in edge_data:
                # Use the actual shape of the road
                # Geometry is usually a Shapely LineString -> list of (x, y)
                # We need (y, x) for Folium
                coords = [(lat, lon) for lon, lat in edge_data["geometry"].coords]
                path_coords.extend(coords)
            else:
                # Fallback to straight line
                u_node = G.nodes[u]
                v_node = G.nodes[v]
                path_coords.append((u_node["y"], u_node["x"]))
                path_coords.append((v_node["y"], v_node["x"]))

        return path_nodes, path_coords

    except nx.NetworkXNoPath:
        print(f"No path found between {start_node} and {end_node}")
        return None, None
    except Exception as e:
        print(f"Error in pathfinding: {e}")
        return None, None
