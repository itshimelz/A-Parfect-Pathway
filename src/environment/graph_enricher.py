import random
from src.ai.risk_model import RiskModel


def enrich_graph(graph):
    """
    Adds synthetic simulation attributes to a real-world graph.

    Attributes added to edges:
        - risk_level (float): 0.0 (safe) to 1.0 (dangerous) predicted by ML model.
        - enemy_probability (float): Correlated with risk.
        - resource_cost (float): 1.0 to 10.0 (fuel/supplies needed).

    Args:
        graph (networkx.MultiDiGraph): The input graph (modified in-place).

    Returns:
        networkx.MultiDiGraph: The enriched graph.
    """
    print("Enriching graph with simulation attributes (using AI Risk Model)...")

    risk_model = RiskModel()

    for u, v, k, data in graph.edges(keys=True, data=True):
        # 1. Predict Risk using ML
        predicted_risk = risk_model.predict_risk(data)

        # 2. Enemy Prob is correlated with Risk
        # If risk is high, enemy prob is high
        enemy_prob = predicted_risk * random.uniform(0.7, 1.0)

        # 3. Resource Cost
        # Heuristic: Longer roads might have higher risk or resource cost
        length = float(data.get("length", 100))
        # Poor roads (rank 0 or 1) might cost more fuel per meter
        # We can loosely infer this from maxspeed or lack thereof
        maxspeed = data.get("maxspeed", 30)
        cost_factor = 1.5 if maxspeed == 30 else 1.0

        resource_cost = (length / 100) * cost_factor

        data["risk_level"] = predicted_risk
        data["enemy_probability"] = round(enemy_prob, 2)
        data["resource_cost"] = round(resource_cost, 2)

    print(f"Enriched {graph.number_of_edges()} edges.")
    return graph
