import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# Ensure the Model folder exists
os.makedirs("C:/Users/saidh/Downloads/Furniture_Layout_Optimizer/AI_Furniture_Layout_Optimizer/Model", exist_ok=True)

# Load dataset using the same hardcoded path
dataset_path = "C:/Users/saidh/Downloads/Furniture_Layout_Optimizer/AI_Furniture_Layout_Optimizer/Dataset/furniture_layout_dataset_5000.csv"
df = pd.read_csv(dataset_path)

# Preprocess dataset
def extract_positions(furniture_str):
    """Extracts numerical positions from furniture placement strings."""
    positions = []
    for item in furniture_str.split(";"):
        if "(" in item and ")" in item:
            coords = item.split("(")[1].split(")")[0].split(",")
            positions.append([int(coords[0]), int(coords[1])])
    return np.mean(positions, axis=0) if positions else [0, 0]

df["Furniture_X"], df["Furniture_Y"] = zip(*df["Furniture_Placement"].map(extract_positions))

# Train model with better hyperparameters
X = df[["Room_Width", "Room_Height"]]
y = df[["Furniture_X", "Furniture_Y"]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=200, max_depth=15, random_state=42)  # Optimized model
model.fit(X_train, y_train)

# Function: Prevent Overlaps & Enforce Spacing
def adjust_furniture_positions(predicted_positions, room_width, room_height):
    """
    Adjusts furniture positions to prevent overlap and maintain spacing.
    Uses a simple logic-based approach.
    """
    adjusted_positions = []
    min_spacing = 2  # Minimum distance between furniture items

    for i, (x, y) in enumerate(predicted_positions):
        x = min(max(x, 1), room_width - 1)  # Ensure within room width
        y = min(max(y, 1), room_height - 1)  # Ensure within room height

        # Ensure spacing from other furniture
        retries = 0  # Prevent infinite shifting
        while any(np.linalg.norm([x - px, y - py]) < min_spacing for px, py in adjusted_positions):
            x += 1  # Shift right
            y += 1  # Shift down
            x = min(max(x, 1), room_width - 1)
            y = min(max(y, 1), room_height - 1)
            retries += 1
            if retries > 10:  # Avoid infinite loop
                break  

        adjusted_positions.append([round(x, 2), round(y, 2)])

    return adjusted_positions

# Save trained model using the same hardcoded path
model_path = "C:/Users/saidh/Downloads/Furniture_Layout_Optimizer/AI_Furniture_Layout_Optimizer/Model/furniture_placement_model_optimized.pkl"
joblib.dump(model, model_path)

print(f"Model trained and saved successfully to {model_path}!")
