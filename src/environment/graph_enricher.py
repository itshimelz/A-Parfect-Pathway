import random
import networkx as nx

def enrich_graph(graph):
    """
    Adds synthetic simulation attributes to a real-world graph.
    
    Attributes added to edges:
        - risk_level (float): 0.0 (safe) to 1.0 (dangerous)
        - enemy_probability (float): 0.0 (none) to 1.0 (certainty)
        - resource_cost (float): 1.0 to 10.0 (fuel/supplies needed)
        
    Args:
        graph (networkx.MultiDiGraph): The input graph (modified in-place).
        
    Returns:
        networkx.MultiDiGraph: The enriched graph.
    """
    print("Enriching graph with simulation attributes...")
    
    for u, v, k, data in graph.edges(keys=True, data=True):
        # Default randomness
        risk = random.random() # 0.0 to 1.0
        enemy_prob = random.random() * 0.5 # 0.0 to 0.5 (enemies are less common)
        
        # Heuristic: Longer roads might have higher risk or resource cost
        length = data.get("length", 100)
        resource_cost = (length / 100) * random.uniform(1.0, 2.0)
        
        # Create some "Zones" logic (simplified)
        # E.g. purely random for now, but in future could use node coordinates 
        # to define "Danger Zones"
        
        data["risk_level"] = round(risk, 2)
        data["enemy_probability"] = round(enemy_prob, 2)
        data["resource_cost"] = round(resource_cost, 2)
        
    print(f"Enriched {graph.number_of_edges()} edges.")
    return graph
