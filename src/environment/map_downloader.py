import osmnx as ox
import networkx as nx
import pickle
import os

def download_graph(location_name, dist=2000, network_type="drive"):
    """
    Downloads a graph from OpenStreetMap for a given location.
    
    Args:
        location_name (str): The name of the location (e.g., "Dhaka, Bangladesh").
        dist (int): The distance in meters from the center to download.
        network_type (str): The type of street network (e.g., "drive", "walk").
        
    Returns:
        networkx.MultiDiGraph: The downloaded graph.
    """
    print(f"Downloading graph for {location_name} with radius {dist}m...")
    try:
        # Check if location_name is a string or coordinates
        # For this project, we primarily assume string, but we can make it robust
        G = ox.graph_from_address(location_name, dist=dist, network_type=network_type)
        print("Graph downloaded successfully.")
        return G
    except Exception as e:
        print(f"Error downloading graph: {e}")
        return None

def save_custom_graph(graph, filepath):
    """
    Saves the NetworkX graph to a pickle file.
    
    Args:
        graph (networkx.MultiDiGraph): The graph to save.
        filepath (str): The path to the output file.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(graph, f)
        print(f"Graph saved to {filepath}")
    except Exception as e:
        print(f"Error saving graph: {e}")

def load_custom_graph(filepath):
    """
    Loads a NetworkX graph from a pickle file.
    
    Args:
        filepath (str): The path to the input file.
        
    Returns:
        networkx.MultiDiGraph: The loaded graph.
    """
    try:
        with open(filepath, "rb") as f:
            graph = pickle.load(f)
        print(f"Graph loaded from {filepath}")
        return graph
    except Exception as e:
        print(f"Error loading graph: {e}")
        return None
