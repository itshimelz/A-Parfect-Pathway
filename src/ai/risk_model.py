import random
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler


class RiskModel:
    """
    Predicts the risk level (0.0 to 1.0) of a road segment based on its features.

    Features used:
    - highway_type_rank: (1=cycleway/path to 5=motorway)
    - maxspeed: Speed limit
    - lanes: Number of lanes
    - length: Length of segment
    - bridge/tunnel: Boolean flags
    """

    def __init__(self):
        self.model = LogisticRegression()
        self.scaler = StandardScaler()
        self.is_trained = False

        # Mapping highway types to a numeric rank (Heuristic)
        # Higher rank = potentially faster/busier/more crucial
        self.highway_ranks = {
            "motorway": 5,
            "trunk": 5,
            "primary": 4,
            "secondary": 4,
            "tertiary": 3,
            "residential": 2,
            "living_street": 2,
            "service": 1,
            "track": 1,
            "footway": 0,
            "cycleway": 0,
            "path": 0,
        }

    def _extract_features(self, edge_data):
        """
        Extracts a feature vector from an edge's OSM data.
        """
        # Feature 1: Highway Rank
        highway = edge_data.get("highway", "residential")
        if isinstance(highway, list):
            highway = highway[0]
        rank = self.highway_ranks.get(highway, 2)

        # Feature 2: Maxspeed
        maxspeed = edge_data.get("maxspeed", 30)
        try:
            if isinstance(maxspeed, list):
                maxspeed = float(maxspeed[0])
            else:
                maxspeed = float(maxspeed)
        except (ValueError, TypeError):
            maxspeed = 30.0

        # Feature 3: Lanes
        lanes = edge_data.get("lanes", 1)
        try:
            if isinstance(lanes, list):
                lanes = float(lanes[0])
            else:
                lanes = float(lanes)
        except (ValueError, TypeError):
            lanes = 1.0

        # Feature 4: Length
        length = float(edge_data.get("length", 50.0))

        # Feature 5: Is Bridge/Tunnel
        is_bridge = 1.0 if "bridge" in edge_data else 0.0
        is_tunnel = 1.0 if "tunnel" in edge_data else 0.0

        return [rank, maxspeed, lanes, length, is_bridge, is_tunnel]

    def train_on_synthetic_data(self):
        """
        Trains the model on synthetic 'intel' to establish a baseline behavior.
        """
        if self.is_trained:
            return

        X = []
        y = []

        # Generate 1000 synthetic samples
        for _ in range(1000):
            # Simulated Features
            rank = random.randint(0, 5)
            maxspeed = random.choice([30, 40, 60, 80])
            lanes = random.randint(1, 4)
            length = random.uniform(20, 500)
            bridge = 0
            tunnel = 0

            # Logic for "Ground Truth": Main roads (high rank/speed) are "risky" (1) in this scenario (e.g., enemy checkpoints)
            # Small paths are "safe" (0)
            risk_prob = 0.1
            if rank >= 4:
                risk_prob += 0.6
            if maxspeed >= 60:
                risk_prob += 0.2

            label = 1 if random.random() < risk_prob else 0

            X.append([rank, maxspeed, lanes, length, bridge, tunnel])
            y.append(label)

        X = np.array(X)
        y = np.array(y)

        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
        print("Risk Model trained on synthetic data.")

    def predict_risk(self, edge_data):
        """
        Returns a risk probability (0.0 - 1.0) for a single edge.
        """
        if not self.is_trained:
            self.train_on_synthetic_data()

        features = np.array(self._extract_features(edge_data)).reshape(1, -1)
        features_scaled = self.scaler.transform(features)

        # Get probability of class 1 (High Risk)
        prob = self.model.predict_proba(features_scaled)[0][1]
        return round(prob, 2)
