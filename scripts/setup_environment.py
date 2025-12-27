import sys
import os

# Add the project root to sys.path so we can import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.environment.map_downloader import download_graph, save_custom_graph
from src.environment.graph_enricher import enrich_graph
from src.utils.visualizer import visualize_graph_static

def main():
    LOCATION = "Dhaka, Bangladesh"
    RADIUS = 1000 # 1km radius for testing (keep it small for speed)
    OUTPUT_GRAPH_PATH = "data/processed_graph.pkl"
    OUTPUT_MAP_PATH = "outputs/initial_map.html"
    
    print("=== Phase 1: Environment Setup Started ===")
    
    # 1. Download
    G = download_graph(LOCATION, dist=RADIUS)
    
    if G is not None:
        # 2. Enrich
        G = enrich_graph(G)
        
        # 3. Save
        save_custom_graph(G, OUTPUT_GRAPH_PATH)
        
        # 4. Visualize
        visualize_graph_static(G, OUTPUT_MAP_PATH)
        
        print("=== Phase 1: Environment Setup Completed Successfully ===")
    else:
        print("=== Phase 1: Failed to download graph ===")

if __name__ == "__main__":
    main()
