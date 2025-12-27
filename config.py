"""Project configuration settings for Perfect Pathway."""

# Environment Settings
ENVIRONMENT_WIDTH = 10
ENVIRONMENT_HEIGHT = 10
MAP_CENTER_LAT = 23.738113
MAP_CENTER_LON = 90.395857
MAP_DEFAULT_RADIUS = 2000

# AI Settings
A_STAR_WEIGHT = "combined"  # distance, time, risk, combined
RISK_PREDICTION_THRESHOLD = 0.5  # Classify as unsafe if > threshold

# Role Settings
ARMY_SAFETY_THRESHOLD = 0.7  # Min safety score for Army
RESCUER_SPEED_PRIORITY = 0.7  # Speed vs safety ratio
VOLUNTEER_EFFICIENCY_RATIO = 0.8  # Efficiency priority

# Training Settings
ML_TRAINING_SAMPLES = 500
ML_MODEL_TYPE = "logistic"  # logistic or decision_tree
Q_LEARNING_EPISODES = 100
Q_LEARNING_LEARNING_RATE = 0.1
Q_LEARNING_DISCOUNT_RATE = 0.95

# Visualization
MAP_ZOOM_LEVEL = 13
MAP_TILES = "OpenStreetMap"

# Logging
LOG_LEVEL = "INFO"
SAVE_PLOTS = True
PLOT_DPI = 300
